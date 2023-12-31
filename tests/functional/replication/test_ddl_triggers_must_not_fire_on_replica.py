#coding:utf-8
"""
ID:          replication.ddl_triggers_must_not_fire_on_replica
TITLE:       DDL-triggers must fire only on master DB
DESCRIPTION:
    Test creates all kinds of DDL triggers in the master DB.
    Each of them registers apropriate event in the table with name 'log_ddl_triggers_activity'.
    After this we create all kinds of DB objects (tables, procedure, function, etc) in master DB to fire these triggers.

    After this we wait until replica becomes actual to master, and this delay will last no more then threshold that
    is defined by MAX_TIME_FOR_WAIT_DATA_IN_REPLICA variable (measured in seconds), see QA_ROOT/files/test_config.ini
    Check is performed by querying DB replica, see call of watch_replica() function.

    ### ACHTUNG ###
    Currently DDL changes performed by trigger do not apply to replica DB, see #7547.
    Test will be further re-implemented after this issue will be fixed.
    We can only check that final DDL statement has been applied to replica, see query
    "select 1 from rdb$relations r where r.rdb$relation_name = upper('t_ddl_completed')"
    ###############

    Further, we invoke ISQL with executing auxiliary script for drop all DB objects on master (with '-nod' command switch).
    After all objects will be dropped, we have to wait again until replica becomes actual with master.
    Check that both DB have no custom objects is performed (see UNION-ed query to rdb$ tables + filtering on rdb$system_flag).

    Finally, we extract metadata for master and replica and make comparison.
    The only difference in metadata must be 'CREATE DATABASE' statement with different DB names - we suppress it,
    thus metadata difference must not be issued.

FBTEST:      tests.functional.replication.ddl_triggers_must_not_fire_on_replica
NOTES:
    [25.08.2022] pzotov
    Warning raises on Windows and Linux:
       ../../../usr/local/lib/python3.9/site-packages/_pytest/config/__init__.py:1126
          /usr/local/lib/python3.9/site-packages/_pytest/config/__init__.py:1126: 
          PytestAssertRewriteWarning: Module already imported so cannot be rewritten: __editable___firebird_qa_0_17_0_finder
            self._mark_plugins_for_rewrite(hook)
       The reason currently is unknown.

    [15.04.2023] pzotov
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

    Checked on 5.0.0.1014, 4.0.3.2929 - both SS and CS.
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
        for i in range(max_allowed_time_for_wait):
            a.reset()
            a.expected_stdout = replica_expected_out
            a.isql(switches=['-q', '-nod'], input = isql_check_script, combine_output = False)
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
            print(f'Waited for {i} seconds')
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
def test_1(act_db_main: Action,  act_db_repl: Action, capsys):

    out_prep, out_main, out_drop = '', '', ''

    # Obtain full path + filename for DB_MAIN and DB_REPL aliases.
    # NOTE: we must NOT use 'a.db.db_path' for ALIASED databases!
    # It will return '.' rather than full path+filename.
    # Use only con.info.name for that!
    #    
    db_main_file, db_repl_file = '', ''
    db_main_fw, db_repl_fw = DbWriteMode.ASYNC, DbWriteMode.ASYNC

    with act_db_main.db.connect(no_db_triggers = True) as con:
        if act_db_main.vars['server-arch'] == 'Classic' and os.name != 'nt':
            pytest.skip("Waiting for FIX: 'Engine is shutdown' in replication log for CS. Linux only.")

        db_main_file = con.info.name
        db_main_fw = con.info.write_mode

    with act_db_repl.db.connect(no_db_triggers = True) as con:
        db_repl_file = con.info.name
        db_repl_fw = con.info.write_mode

    # ONLY FOR THIS test: forcedly change FW to OFF, without any condition.
    # Otherwise changes may not be delivered to replica for <MAX_TIME_FOR_WAIT_DATA_IN_REPLICA> seconds.
    #####################
    act_db_main.db.set_async_write()
    act_db_repl.db.set_async_write()


    # Must be EMPTY:
    out_prep = capsys.readouterr().out

    sql_init = """   
        set bail on;

        recreate table log_ddl_triggers_activity (
            id int generated by default as identity constraint pk_log_ddl_triggers_activity primary key
            ,ddl_trigger_name varchar(64)
            ,event_type varchar(25) not null
            ,object_type varchar(25) not null
            ,ddl_event varchar(25) not null
            ,object_name varchar(64) not null
            ,dts timestamp default 'now'
        );


        set term ^;
        execute block as
            declare v_lf char(1) = x'0A';
        begin
            rdb$set_context('USER_SESSION', 'SKIP_DDL_TRIGGER', '1');

            for
                with
                a as (
                    select 'ANY DDL STATEMENT' x from rdb$database union all
                    select 'CREATE TABLE' from rdb$database union all
                    select 'ALTER TABLE' from rdb$database union all
                    select 'DROP TABLE' from rdb$database union all
                    select 'CREATE PROCEDURE' from rdb$database union all
                    select 'ALTER PROCEDURE' from rdb$database union all
                    select 'DROP PROCEDURE' from rdb$database union all
                    select 'CREATE FUNCTION' from rdb$database union all
                    select 'ALTER FUNCTION' from rdb$database union all
                    select 'DROP FUNCTION' from rdb$database union all
                    select 'CREATE TRIGGER' from rdb$database union all
                    select 'ALTER TRIGGER' from rdb$database union all
                    select 'DROP TRIGGER' from rdb$database union all
                    select 'CREATE EXCEPTION' from rdb$database union all
                    select 'ALTER EXCEPTION' from rdb$database union all
                    select 'DROP EXCEPTION' from rdb$database union all
                    select 'CREATE VIEW' from rdb$database union all
                    select 'ALTER VIEW' from rdb$database union all
                    select 'DROP VIEW' from rdb$database union all
                    select 'CREATE DOMAIN' from rdb$database union all
                    select 'ALTER DOMAIN' from rdb$database union all
                    select 'DROP DOMAIN' from rdb$database union all
                    select 'CREATE ROLE' from rdb$database union all
                    select 'ALTER ROLE' from rdb$database union all
                    select 'DROP ROLE' from rdb$database union all
                    select 'CREATE SEQUENCE' from rdb$database union all
                    select 'ALTER SEQUENCE' from rdb$database union all
                    select 'DROP SEQUENCE' from rdb$database union all
                    select 'CREATE USER' from rdb$database union all
                    select 'ALTER USER' from rdb$database union all
                    select 'DROP USER' from rdb$database union all
                    select 'CREATE INDEX' from rdb$database union all
                    select 'ALTER INDEX' from rdb$database union all
                    select 'DROP INDEX' from rdb$database union all
                    select 'CREATE COLLATION' from rdb$database union all
                    select 'DROP COLLATION' from rdb$database union all
                    select 'ALTER CHARACTER SET' from rdb$database union all
                    select 'CREATE PACKAGE' from rdb$database union all
                    select 'ALTER PACKAGE' from rdb$database union all
                    select 'DROP PACKAGE' from rdb$database union all
                    select 'CREATE PACKAGE BODY' from rdb$database union all
                    select 'DROP PACKAGE BODY' from rdb$database
                )
                ,e as (
                    select 'before' w from rdb$database union all select 'after' from rdb$database
                )
                ,t as (
                    select upper(trim(replace(trim(a.x),' ','_')) || iif(e.w='before', '_before', '_after')) as trg_name, a.x, e.w
                    from e, a
                )

                select
                       'create or alter trigger trg_' || t.trg_name
                    || ' active ' || t.w || ' ' || trim(t.x) || ' as '
                    || :v_lf
                    || 'begin'
                    || :v_lf
                    || q'{    if (rdb$get_context('USER_SESSION', 'SKIP_DDL_TRIGGER') is null) then}'
                    || :v_lf
                    || '        insert into log_ddl_triggers_activity(ddl_trigger_name, event_type, object_type, ddl_event, object_name) values('
                    || :v_lf
                    || q'{'}' || trim(t.trg_name) || q'{'}'
                    || :v_lf
                    || q'{, rdb$get_context('DDL_TRIGGER', 'EVENT_TYPE')}'
                    || :v_lf
                    || q'{, rdb$get_context('DDL_TRIGGER', 'OBJECT_TYPE')}'
                    || :v_lf
                    || q'{, rdb$get_context('DDL_TRIGGER', 'DDL_EVENT')}'
                    || :v_lf
                    || q'{, rdb$get_context('DDL_TRIGGER', 'OBJECT_NAME')}'
                    || :v_lf
                    || ');'
                    || :v_lf
                    || ' end'
                    as sttm
                from t
                as cursor c
            do begin
                 execute statement(c.sttm) with autonomous transaction;
            end

            rdb$set_context('USER_SESSION', 'SKIP_DDL_TRIGGER', null);
        end
        ^
        commit
        ^

        create table test(id int not null, name varchar(10))
        ^
        alter table test add constraint test_pk primary key(id)
        ^
        ----------
        create procedure sp_test as begin end
        ^
        alter procedure sp_test as declare x int; begin x=1; end
        ^
        ----------
        create function fn_test(a_id int) returns bigint as
        begin
            return a_id * a_id;
        end
        ^
        alter function fn_test(a_id int) returns int128 as
        begin
            return a_id * a_id * a_id;
        end
        ^
        ----------
        create trigger trg_connect_test on connect as
        begin
        end
        ^
        alter trigger trg_connect_test as
            declare x int;
        begin
            x = 1;
        end
        ^
        ----------
        create exception exc_test 'Invalud value: @1'
        ^
        alter exception exc_test 'Bad values: @1 and @2'
        ^
        ----------
        create view v_test as select 1 x from rdb$database
        ^
        alter view v_test as select 1 x, 2 y from rdb$database
        ^
        ----------
        create domain dm_test int
        ^
        alter domain dm_test set not null
        ^
        ----------
        create role r_test
        ^
        alter role r_test set system privileges to use_gstat_utility, ignore_db_triggers
        ^
        ----------
        create sequence g_test
        ^
        alter sequence g_test restart with 123
        ^
        ----------
        /*
        create or alter user u_test password '123' using plugin Srp
        ^
        alter user u_test password '456'
        ^
        */
        ----------
        create index test_name on test(name)
        ^
        alter index test_name inactive
        ^
        ----------
        create collation name_coll for utf8 from unicode case insensitive
        ^
        ----------
        alter character set iso8859_1 set default collation pt_br
        ^
        ----------
        create or alter package pg_test as
        begin
           function pg_fn1 returns int;
        end
        ^
        alter package pg_test as
        begin
           function pg_fn1(a_x int) returns int128;
        end
        ^

        create package body pg_test as
        begin
           function pg_fn1(a_x int) returns int128 as
           begin
               return a_x * a_x * a_x;
           end
        end
        ^
        recreate table t_ddl_completed(id int primary key)
        ^
        commit
        ^
    """

    act_db_main.isql(switches=['-q'], input = sql_init, combine_output = True)
    out_prep = act_db_main.clean_stdout
    act_db_main.reset()

    if out_prep:
        # Init SQL raised error.
        pass
    else:

        # Query to be used for check that all DB objects present in replica (after last DDL statement completed on master DB):
        ddl_ready_query = "select 1 from rdb$relations r where r.rdb$relation_name = upper('t_ddl_completed')"
        isql_check_script = ''

        # DO NOT DELETE! To be used after #7547 will be fixed
        # (currently this query returns NOTHING on replica db)
        ######################################
        #isql_check_script = """
        #    set list on;
        #    set count on;
        #    select
        #         a.id
        #        ,a.ddl_trigger_name
        #        ,a.event_type
        #        ,a.object_type
        #        ,a.ddl_event
        #        ,a.object_name
        #    from log_ddl_triggers_activity a
        #    order by a.id;
        #"""

        isql_expected_out = """
        """

        ##############################################################################
        ###  W A I T   U N T I L    R E P L I C A    B E C O M E S   A C T U A L   ###
        ##############################################################################
        watch_replica( act_db_repl, MAX_TIME_FOR_WAIT_DATA_IN_REPLICA, ddl_ready_query, isql_check_script, isql_expected_out)
        # Must be EMPTY:
        out_main = capsys.readouterr().out

    
    drop_db_objects(act_db_main, act_db_repl, capsys)

    # Return FW to initial values (if needed):
    if db_main_fw == DbWriteMode.SYNC:
        act_db_main.db.set_sync_write()
    if db_repl_fw == DbWriteMode.SYNC:
        act_db_repl.db.set_sync_write()

    # Must be EMPTY:
    out_drop = capsys.readouterr().out

    if [ x for x in (out_prep, out_main, out_drop) if x.strip() ]:
        # We have a problem either with DDL/DML or with dropping DB objects.
        # First, we have to RECREATE both master and slave databases
        # (otherwise further execution of this test or other replication-related tests most likely will fail):
        out_reset = reset_replication(act_db_main, act_db_repl, db_main_file, db_repl_file)

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

