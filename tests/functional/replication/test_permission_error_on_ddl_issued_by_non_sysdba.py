#coding:utf-8

"""
ID:          replication.permission_error_on_ddl_issued_by_non_sysdba
ISSUE:       https://github.com/FirebirdSQL/firebird/issues/6856
TITLE:       Permission error with replication
DESCRIPTION:
    Test perform actions which are specified in the ticket: create user, grant him admin role and create VIEW
    with specifying this user as its OWNER.

    After this we wait until replica becomes actual to master, and this delay will last no more then threshold that
    is defined by MAX_TIME_FOR_WAIT_DATA_IN_REPLICA variable (measured in seconds), see QA_ROOT/files/test_config.ini

    We query RDB$ tables on replica with check presense of just created view and who is the OWNER of it
    (see calls of watch_replica() function).

    Further, we invoke ISQL with executing auxiliary script for drop all DB objects on master (with '-nod' command switch).
    After all objects will be dropped, we have to wait again until replica becomes actual with master.
    Check that both DB have no custom objects is performed (see UNION-ed query to rdb$ tables + filtering on rdb$system_flag).

    Finally, we extract metadata for master and replica and make comparison.
    The only difference in metadata must be 'CREATE DATABASE' statement with different DB names - we suppress it,
    thus metadata difference must not be issued.

    Confirmed bug on 4.0.1.2578 and 5.0.0.169: messages "ERROR: unsuccessful metadata update / CREATE OR ALTER VIEW v_test failed"
    will be added into replication log and after this replication gets stuck.

FBTEST:      tests.functional.replication.permission_error_on_ddl_issued_by_non_sysdba
NOTES:
    [25.08.2022] pzotov
    Warning raises on Windows and Linux:
        ../../../usr/local/lib/python3.9/site-packages/_pytest/config/__init__.py:1126
        /usr/local/lib/python3.9/site-packages/_pytest/config/__init__.py:1126: 
        PytestAssertRewriteWarning: Module already imported so cannot be rewritten: __editable___firebird_qa_0_17_0_finder
        self._mark_plugins_for_rewrite(hook)
    The reason currently is unknown.

    [18.04.2023] pzotov
    Test was fully re-implemented. We have to query replica DATABASE for presense of data that we know there must appear.
    We have to avoid query of replication log - not only verbose can be disabled, but also because code is too complex.

    NOTE-1.
        We use 'assert' only at the final point of test, with printing detalization about encountered problem(s).
        During all previous steps, we only store unexpected output to variables, e.g.: out_main = capsys.readouterr().out etc.
    NOTE-2.
        Temporary DISABLED execution on Linux when ServerMode = Classic. Replication can unexpectedly stop with message
        'Engine is shutdown' appears in replication.log. Sent report to dimitr, waiting for fix.
    NOTE-3.
        This test changes FW to OFF in order to reduce time of DDL operations. FW is restored to initial state at final point.
        Otherwise changes may not be delivered to replica for <MAX_TIME_FOR_WAIT_DATA_IN_REPLICA> seconds.
    
    Checked on 5.0.0.1017, 4.0.1.2930 - both CS and SS.

"""
import os
import shutil
from difflib import unified_diff
from pathlib import Path
import time

import pytest
from firebird.qa import *
from firebird.driver import connect, create_database, DbWriteMode, ReplicaMode, ShutdownMode, ShutdownMethod, DatabaseError

# QA_GLOBALS -- dict, is defined in qa/plugin.py, obtain settings
# from act.files_dir/'test_config.ini':
repl_settings = QA_GLOBALS['replication']

MAX_TIME_FOR_WAIT_DATA_IN_REPLICA = int(repl_settings['max_time_for_wait_data_in_replica'])
MAIN_DB_ALIAS = repl_settings['main_db_alias']
REPL_DB_ALIAS = repl_settings['repl_db_alias']

db_main = db_factory( filename = '#' + MAIN_DB_ALIAS, do_not_create = True, do_not_drop = True)
db_repl = db_factory( filename = '#' + REPL_DB_ALIAS, do_not_create = True, do_not_drop = True)

tmp_dba = user_factory('db_main', name='tmp_user_gh_6856', password='123', plugin = 'Srp', admin = True)

substitutions = [('Start removing objects in:.*', 'Start removing objects'),
                 ('Finish. Total objects removed:  [1-9]\\d*', 'Finish. Total objects removed'),
                 ('.* CREATE DATABASE .*', ''),
                 ('REP_BLOB_ID.*', ''),
                 ('[\t ]+', ' '),
                 ('FOUND message about replicated segment N .*', 'FOUND message about replicated segment')]

act_db_main = python_act('db_main', substitutions=substitutions)
act_db_repl = python_act('db_repl', substitutions=substitutions)

#--------------------------------------------

def cleanup_folder(p):
    # Removed all files and subdirs in the folder <p>
    # Used for cleanup <repl_journal> and <repl_archive> when replication must be reset
    # in case when any error occurred during test execution.
    assert os.path.dirname(p) != p, f"@@@ ABEND @@@ CAN NOT operate in the file system root directory. Check your code!"
    for root, dirs, files in os.walk(p):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))
    return len(os.listdir(p))

#--------------------------------------------

def reset_replication(act_db_main, act_db_repl, db_main_file, db_repl_file):
    out_reset = ''

    with act_db_main.connect_server() as srv:

        # !! IT IS ASSUMED THAT REPLICATION FOLDERS ARE IN THE SAME DIR AS <DB_MAIN> !!
        # DO NOT use 'a.db.db_path' for ALIASED database!
        # It will return '.' rather than full path+filename.

        repl_root_path = Path(db_main_file).parent
        repl_jrn_sub_dir = repl_settings['journal_sub_dir']
        repl_arc_sub_dir = repl_settings['archive_sub_dir']

        for f in (db_main_file, db_repl_file):
            # Method db.drop() changes LINGER to 0, issues 'delete from mon$att' with suppressing exceptions
            # and calls 'db.drop_database()' (also with suppressing exceptions).
            # We change DB state to FULL SHUTDOWN instead of call action.db.drop() because
            # this is more reliable (it kills all attachments in all known cases and does not use mon$ table)
            #
            try:
                srv.database.shutdown(database = f, mode = ShutdownMode.FULL, method = ShutdownMethod.FORCED, timeout = 0)
            except DatabaseError as e:
                out_reset += e.__str__()

            # REMOVE db file from disk:
            ###########################
            os.unlink(f)

        # Clean folders repl_journal and repl_archive: remove all files from there.
        for p in (repl_jrn_sub_dir,repl_arc_sub_dir):
            if cleanup_folder(repl_root_path / p) > 0:
                out_reset += f"Directory {str(p)} remains non-empty.\n"

    if out_reset == '':
        for a in (act_db_main,act_db_repl):
            d = a.db.db_path

            try:
                dbx = create_database(str(d), user = a.db.user)
                dbx.close()
                with a.connect_server() as srv:
                    srv.database.set_write_mode(database = d, mode = DbWriteMode.ASYNC)
                    srv.database.set_sweep_interval(database = d, interval = 0)
                    if a == act_db_repl:
                        srv.database.set_replica_mode(database = d, mode = ReplicaMode.READ_ONLY)
                    else:
                        with a.db.connect() as con:
                            con.execute_immediate('alter database enable publication')
                            con.execute_immediate('alter database include all to publication')
                            con.commit()
            except DatabaseError as e:
                out_reset += e.__str__()
            
    # Must remain EMPTY:
    return out_reset

#--------------------------------------------

def watch_replica( a: Action, max_allowed_time_for_wait, ddl_ready_query = '', isql_check_script = '', replica_expected_out = ''):

    retcode = 1;
    ready_to_check = False
    if ddl_ready_query:
        with a.db.connect(no_db_triggers = True) as con:
            with con.cursor() as cur:
                for i in range(0,max_allowed_time_for_wait):
                    cur.execute(ddl_ready_query)
                    count_actual = cur.fetchone()
                    if count_actual:
                        ready_to_check = True
                        break
                    else:
                        con.rollback()
                        time.sleep(1)
    else:
        ready_to_check = True

    if not ready_to_check:
        print( f'UNEXPECTED. Initial check query did not return any rows for {max_allowed_time_for_wait} seconds.' )
        print('Initial check query:')
        print(ddl_ready_query)
        return
    
    final_check_pass = False
    if isql_check_script:
        retcode = 0
        for i in range(max_allowed_time_for_wait):
            a.reset()
            a.expected_stdout = replica_expected_out
            a.isql(switches=['-q', '-nod'], input = isql_check_script, combine_output = True)

            if a.return_code:
                # "Token unknown", "Name longer than database column size" etc: we have to
                # immediately break from this loop because isql_check_script is incorrect!
                break
            
            if a.clean_stdout == a.clean_expected_stdout:
                final_check_pass = True
                break
            if i < max_allowed_time_for_wait-1:
                time.sleep(1)

        if not final_check_pass:
            print(f'UNEXPECTED. Final check query did not return expected dataset for {max_allowed_time_for_wait} seconds.')
            print('Final check query:')
            print(isql_check_script)
            print('Expected output:')
            print(a.clean_expected_stdout)
            print('Actual output:')
            print(a.clean_stdout)
            print(f'ISQL return_code={a.return_code}')
            print(f'Waited for {i} seconds')

        a.reset()

    else:
        final_check_pass = True

    return

#--------------------------------------------

def drop_db_objects(act_db_main: Action,  act_db_repl: Action, capsys):

    # return initial state of master DB:
    # remove all DB objects (tables, views, ...):
    #
    db_main_meta, db_repl_meta = '', ''
    for a in (act_db_main,act_db_repl):
        if a == act_db_main:
            sql_clean = (a.files_dir / 'drop-all-db-objects.sql').read_text()
            a.expected_stdout = """
                Start removing objects
                Finish. Total objects removed
            """
            a.isql(switches=['-q', '-nod'], input = sql_clean, combine_output = True)
            if a.clean_stdout == a.clean_expected_stdout:
                a.reset()
            else:
                print(a.clean_expected_stdout)
                a.reset()
                break

            # NB: one need to remember that rdb$system_flag can be NOT ONLY 1 for system used objects!
            # For example, it has value =3 for triggers that are created to provide CHECK-constraints,
            # Custom DB objects always have rdb$system_flag = 0 (or null for some very old databases).
            # We can be sure that there are no custom DB objects if following query result is NON empty:
            #
            ddl_ready_query = """
                select 1
                from rdb$database
                where NOT exists (
                    select custom_db_object_flag
                    from (
                        select rt.rdb$system_flag as custom_db_object_flag from rdb$triggers rt
                        UNION ALL
                        select rt.rdb$system_flag from rdb$relations rt
                        UNION ALL
                        select rt.rdb$system_flag from rdb$functions rt
                        UNION ALL
                        select rt.rdb$system_flag from rdb$procedures rt
                        UNION ALL
                        select rt.rdb$system_flag from rdb$exceptions rt
                        UNION ALL
                        select rt.rdb$system_flag from rdb$fields rt
                        UNION ALL
                        select rt.rdb$system_flag from rdb$collations rt
                        UNION ALL
                        select rt.rdb$system_flag from rdb$generators rt
                        UNION ALL
                        select rt.rdb$system_flag from rdb$roles rt
                        UNION ALL
                        select rt.rdb$system_flag from rdb$auth_mapping rt
                        UNION ALL
                        select 1 from sec$users s
                        where upper(s.sec$user_name) <> 'SYSDBA'
                    ) t
                    where coalesce(t.custom_db_object_flag,0) = 0
                )
            """


            ##############################################################################
            ###  W A I T   U N T I L    R E P L I C A    B E C O M E S   A C T U A L   ###
            ##############################################################################
            watch_replica( act_db_repl, MAX_TIME_FOR_WAIT_DATA_IN_REPLICA, ddl_ready_query)

            # Must be EMPTY:
            print(capsys.readouterr().out)

            db_main_meta = a.extract_meta(charset = 'utf8', io_enc = 'utf8')
        else:
            db_repl_meta = a.extract_meta(charset = 'utf8', io_enc = 'utf8')

        ######################
        ### A C H T U N G  ###
        ######################
        # MANDATORY, OTHERWISE REPLICATION GETS STUCK ON SECOND RUN OF THIS TEST
        # WITH 'ERROR: Record format with length NN is not found for table TEST':
        a.gfix(switches=['-sweep', a.db.dsn])


    # Final point: metadata must become equal:
    #
    diff_meta = ''.join(unified_diff( \
                         [x for x in db_main_meta.splitlines() if 'CREATE DATABASE' not in x],
                         [x for x in db_repl_meta.splitlines() if 'CREATE DATABASE' not in x])
                       )
    # Must be EMPTY:
    print(diff_meta)

#--------------------------------------------

@pytest.mark.version('>=4.0.1')
def test_1(act_db_main: Action,  act_db_repl: Action, tmp_dba: User, capsys):


    out_prep, out_main, out_drop = '', '', ''

    # Obtain full path + filename for DB_MAIN and DB_REPL aliases.
    # NOTE: we must NOT use 'a.db.db_path' for ALIASED databases!
    # It will return '.' rather than full path+filename.
    # Use only con.info.name for that!
    #    
    db_info = {}
    for a in (act_db_main, act_db_repl):
        with a.db.connect(no_db_triggers = True) as con:
            if a == act_db_main and a.vars['server-arch'] == 'Classic' and os.name != 'nt':
                pytest.skip("Waiting for FIX: 'Engine is shutdown' in replication log for CS. Linux only.")
            db_info[a,  'db_full_path'] = con.info.name

    sql_init = f"""
        execute block as
        begin
            execute statement 'create or alter view v_test as select 1 x from rdb$database'
            with autonomous transaction
            as user '{tmp_dba.name}' password '{tmp_dba.password}' role 'rdb$admin';
        end
    """

    with act_db_main.db.connect(no_db_triggers = True) as con:
        con.execute_immediate(f'grant rdb$admin to user {tmp_dba.name}')
        con.commit()
        con.execute_immediate(sql_init)
        con.commit()


    # Must be EMPTY:
    out_prep = capsys.readouterr().out
   
    if out_prep:
        # Some problem raised during initial DDL and/or blob writing
        pass
    else:
        # Query to be used for check that all DB objects present in replica (after last DML statement completed on master DB):
        ddl_ready_query = "select 1 from rdb$relations where rdb$relation_name = upper('v_test')"

        # Query to be used that replica DB contains all expected data (after last DML statement completed on master DB):
        isql_check_script = """
            set list on;
            set count on;
            select
                rdb$get_context('SYSTEM','REPLICA_MODE') replica_mode
                ,v.x
                ,r.rdb$owner_name
            from v_test v
            cross join rdb$relations r
            where coalesce(r.rdb$system_flag,0) = 0 and r.rdb$relation_name = upper('v_test')
            ;
        """

        isql_expected_out = f"""
            REPLICA_MODE READ-ONLY
            X 1
            RDB$OWNER_NAME {tmp_dba.name.upper()}
            Records affected: 1
        """
        ##############################################################################
        ###  W A I T   U N T I L    R E P L I C A    B E C O M E S   A C T U A L   ###
        ##############################################################################
        watch_replica( act_db_repl, MAX_TIME_FOR_WAIT_DATA_IN_REPLICA, ddl_ready_query, isql_check_script, isql_expected_out)
        # Must be EMPTY:
        out_main = capsys.readouterr().out

    drop_db_objects(act_db_main, act_db_repl, capsys)

    # Must be EMPTY:
    out_drop = capsys.readouterr().out

    if [ x for x in (out_prep, out_main, out_drop) if x.strip() ]:
        # We have a problem either with DDL/DML or with dropping DB objects.
        # First, we have to RECREATE both master and slave databases
        # (otherwise further execution of this test or other replication-related tests most likely will fail):
        out_reset = reset_replication(act_db_main, act_db_repl, db_info[act_db_main,'db_full_path'], db_info[act_db_repl,'db_full_path'])

        # Next, we display out_main, out_drop and out_reset:
        #
        print('Problem(s) detected:')
        if out_prep.strip():
            print('out_prep:\n', out_prep)
        if out_main.strip():
            print('out_main:\n', out_main)
        if out_drop.strip():
            print('out_drop:\n', out_drop)
        if out_reset.strip():
            print('out_reset:\n', out_reset)

        assert '' == capsys.readouterr().out
