#coding:utf-8

"""
ID:          replication.blob_not_found_in_rw_replica_if_target_row_exists
ISSUE:       7070
TITLE:       Error "BLOB is not found" while replication converts INSERT into UPDATE for a conflicting record
DESCRIPTION:
    Test temporary changes mode of replica using external call: gfix -replica read_write ...
    Then we create table TEST(ID int, b blob) on master, without adding records in it, and WAIT
    until this table will appear on replica DB.
    Maximal waiting time is limited by variable MAX_TIME_FOR_WAIT_SEGMENT_IN_LOG).
    Message starting with phrase 'POINT-1A ...' is printed when this table appears in replica DB.

    NB. Despite that we can create such table at the same time on replica, this ticket issue can be
    reproduced only when we make table on master and wait until it will be replicated on replica.

    After this we:
    * add record with binary blob (using stream API) into REPLICA database; commit;
    * add record with another binary blob into MASTER database; commit;

    Message "WARNING: Record being inserted into table TEST already exists, updating instead" must appear
    in the replication log at this point but after that message about successfully replicated segment must also be.
    Message 'ERROR: Blob ... is not found for table TEST' must NOT appear.
    If these conditions are met then script issues message starting with 'Point-1B ...'

    Further,  we invoke ISQL with executing auxiliary script for drop all DB objects on master (with '-nod' command switch).
    After all objects will be dropped, we have to wait again until  replica becomes actual with master (see 'POINT-2').

    Finally, we extract metadata for master and replica and compare them (see 'f_meta_diff').
    The only difference in metadata must be 'CREATE DATABASE' statement with different DB names - we suppress it,
    thus metadata difference must not be issued.

    Confirmed bug on 4.0.1.2682 and 5.0.0.338, got in the replication.log:
        ERROR: Blob 128.0 is not found for table TEST
FBTEST:      tests.functional.replication.blob_not_found_in_rw_replica_if_target_row_exists
NOTES:
    [26.08.2022] pzotov
    1. In case of any errors (somewhat_failed <> 0) test will re-create db_main and db_repl, and then perform all needed
       actions to resume replication (set 'replica' flag on db_repl, enabling publishing in db_main, remove all files
       from subdirectories <repl_journal> and <repl_archive> which must present in the same folder as <db_main>).
    2. Warning raises on Windows and Linux:
       ../../../usr/local/lib/python3.9/site-packages/_pytest/config/__init__.py:1126
          /usr/local/lib/python3.9/site-packages/_pytest/config/__init__.py:1126: 
          PytestAssertRewriteWarning: Module already imported so cannot be rewritten: __editable___firebird_qa_0_17_0_finder
            self._mark_plugins_for_rewrite(hook)
       The reason currently is unknown.

    Checked on 5.0.0.623, 4.0.1.2692 - both CS and SS. Both on Windows and Linux.
"""
import os
import shutil
import re
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

substitutions = [('Start removing objects in:.*', 'Start removing objects'),
                 ('Finish. Total objects removed:  [1-9]\\d*', 'Finish. Total objects removed'),
                 ('.* CREATE DATABASE .*', ''),
                 ('[\t ]+', ' '),
                 ('FOUND message about replicated segment N .*', 'FOUND message about replicated segment')]

act_db_main = python_act('db_main', substitutions=substitutions)
act_db_repl = python_act('db_repl', substitutions=substitutions)
tmp_data = temp_file(filename = 'tmp_blob_for_replication.dat')

# Length of generated blob:
###########################
DATA_LEN = 65 * 1024 * 1024
###########################

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
def test_1(act_db_main: Action,  act_db_repl: Action, tmp_data: Path, capsys):

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
            db_info[a,  'db_fw_initial'] = con.info.write_mode


    with act_db_repl.connect_server() as srv:
        srv.database.set_replica_mode(database = act_db_repl.db.db_path, mode = ReplicaMode.READ_WRITE)

    # ONLY FOR THIS test: forcedly change FW to OFF, without any condition.
    # Otherwise changes may not be delivered to replica for <MAX_TIME_FOR_WAIT_DATA_IN_REPLICA> seconds.
    #####################
    act_db_main.db.set_async_write()
    act_db_repl.db.set_async_write()

    # Must be EMPTY:
    out_prep = capsys.readouterr().out
    if out_prep:
        # Some problem raised during change DB header(s)
        pass
    else:
        sql_init = '''
            set bail on;
            recreate table test(id int primary key using index test_pk, b blob);
            commit;
        '''
        act_db_main.isql(switches=['-q'], input = sql_init, combine_output = True)
        out_prep = act_db_main.clean_stdout
        act_db_main.reset()

    if out_prep:
        # Some problem raised during init_sql execution
        pass
    else:
        # Query to be used for check that all DB objects present in replica (after last DML statement completed on master DB):
        ddl_ready_query = "select 1 from rdb$relations where rdb$relation_name = upper('test')"
        ##############################################################################
        ###  W A I T   U N T I L    R E P L I C A    B E C O M E S   A C T U A L   ###
        ##############################################################################
        watch_replica( act_db_repl, MAX_TIME_FOR_WAIT_DATA_IN_REPLICA, ddl_ready_query)
        # Must be EMPTY:
        out_prep = capsys.readouterr().out

    if out_prep:
        # Some problem raised with delivering DDL changes to replica
        pass
    else:
        blob_inserted_hashes = {}

        # NB: first we put blob into REPLICA database!
        ##############################################
        for a in (act_db_repl, act_db_main):
            with a.db.connect(no_db_triggers = True) as con:
                with con.cursor() as cur:
                    # Generate random binary data and writing to file which will be loaded as stream blob into DB:
                    tmp_data.write_bytes( bytearray(os.urandom(DATA_LEN)) )
                    with open(tmp_data, 'rb') as blob_file:
                        # [doc]: crypt_hash() returns VARCHAR strings with OCTETS charset with length depended on algorithm.
                        # ### ACHTUNG ### ISQL will convert this octets to HEX-form, e.g.:
                        # select cast('AF' as varchar(2) charset octets) ... --> '4146' // i.e. bytes order = BIG-endian.
                        # firebird-driver does NOT perform such transformation, and output for this example will be: b'AF'. 
                        # We have to:
                        # 1. Convert this string to integer using 'big' for bytesOrder (despite that default value most likely = 'little'!)
                        # 2. Convert this (decimal!) integer to hex and remove "0x" prefix from it. This can be done using format() function.
                        # 3. Apply upper() to this string and pad it with zeroes to len=128 (because such padding is always done by ISQL).
                        cur.execute("insert into test(id, b) values(1, ?) returning crypt_hash(b using sha512)", (blob_file,) )
                        ins_blob_hash_raw = cur.fetchone()[0]                                       # b'\xfa\x80\x8a...'
                        ins_blob_hash_raw = format(int.from_bytes(ins_blob_hash_raw,  'big'), 'x')  # 'fa808a...'
                        blob_inserted_hashes[ a.db.db_path ] = ins_blob_hash_raw.upper().rjust(128, '0')
                con.commit()

        # Must be EMPTY:
        out_main = capsys.readouterr().out

    if out_main:
        # Some problem raised with writing blob into replica or master DB:
        pass
    else:
        # No errors must be now. We have to wait now until blob from MASTER be delivered
        # to REPLICA and replace there "old" blob (in the record with ID = 1).

        isql_check_script = f"""
            set bail on;
            set blob all;
            set list on;
            set count on;
            select
                rdb$get_context('SYSTEM','REPLICA_MODE') replica_mode
                ,crypt_hash(b using sha512) as blob_hash
            from test;
        """

        isql_expected_out = f"""
            REPLICA_MODE READ-WRITE
            BLOB_HASH {blob_inserted_hashes[ act_db_main.db.db_path ]}
            Records affected: 1
        """
        
        ##############################################################################
        ###  W A I T   U N T I L    R E P L I C A    B E C O M E S   A C T U A L   ###
        ##############################################################################
        watch_replica( act_db_repl, MAX_TIME_FOR_WAIT_DATA_IN_REPLICA, '', isql_check_script, isql_expected_out)
        # Must be EMPTY:
        out_main = capsys.readouterr().out


    drop_db_objects(act_db_main, act_db_repl, capsys)

    # Return FW to initial values (if needed):
    for a in (act_db_main, act_db_repl):
        if db_info[a,'db_fw_initial'] == DbWriteMode.SYNC:
            a.db.set_sync_write()


    # Return replica mode to its 'normal' value: READ-ONLY:
    with act_db_repl.connect_server() as srv:
        srv.database.set_replica_mode(database = act_db_repl.db.db_path, mode = ReplicaMode.READ_ONLY)

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
