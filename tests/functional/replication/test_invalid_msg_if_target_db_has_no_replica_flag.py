#coding:utf-8

"""
ID:          replication.invalid_msg_if_target_db_has_no_replica_flag
ISSUE:       6989
TITLE:       Invalid message in replication.log (and possibly crash in the case of synchronous
  replication) when the target DB has no its "replica" flag set
DESCRIPTION:
    Test changes replica DB attribute (removes 'replica' flag). Then we do some trivial DDL on master (create and drop table).
    Log of replication must soon contain "ERROR: Database is not in the replica mode"
    If this phrase does not appear during <MAX_TIME_FOR_WAIT_SEGMENT_IN_LOG> seconds then we have a bug.

    Otherwise we continue and return attribute 'replica' to the target DB.
    After this replication log must contain phrase:
        VERBOSE: Segment <N> (<M> bytes) is replicated in <K> ms, deleting the file.
    We can assume that replication finished OK only when such line is found see ('POINT-1').

    Further,  we invoke ISQL with executing auxiliary script for drop all DB objects on master (with '-nod' command switch).
    After all objects will be dropped, we have to wait again until  replica becomes actual with master (see 'POINT-2').

    Finally, we extract metadata for master and replica and compare them (see 'f_meta_diff').
    The only difference in metadata must be 'CREATE DATABASE' statement with different DB names - we suppress it,
    thus metadata difference must not be issued.

FBTEST:      tests.functional.replication.invalid_msg_if_target_db_has_no_replica_flag
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
from firebird.driver import connect, create_database, DbWriteMode, ReplicaMode

# QA_GLOBALS -- dict, is defined in qa/plugin.py, obtain settings
# from act.files_dir/'test_config.ini':
repl_settings = QA_GLOBALS['replication']

MAX_TIME_FOR_WAIT_SEGMENT_IN_LOG = int(repl_settings['max_time_for_wait_segment_in_log'])
MAIN_DB_ALIAS = repl_settings['main_db_alias']
REPL_DB_ALIAS = repl_settings['repl_db_alias']

db_main = db_factory( filename = '#' + MAIN_DB_ALIAS, do_not_create = True, do_not_drop = True)
db_repl = db_factory( filename = '#' + REPL_DB_ALIAS, do_not_create = True, do_not_drop = True)

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

def wait_for_data_in_replica( act_db_main: Action, max_allowed_time_for_wait, prefix_msg = '' ):

    replication_log = act_db_main.home_dir / 'replication.log'

    replold_lines = []
    with open(replication_log, 'r') as f:
        replold_lines = f.readlines()

    with act_db_main.db.connect(no_db_triggers = True) as con:
        with con.cursor() as cur:
            cur.execute("select rdb$get_context('SYSTEM','REPLICATION_SEQUENCE') from rdb$database")
            last_generated_repl_segment = cur.fetchone()[0]

    # VERBOSE: Segment 1 (2582 bytes) is replicated in 1 second(s), deleting the file
    # VERBOSE: Segment 2 (200 bytes) is replicated in 82 ms, deleting the file
    p_successfully_replicated = re.compile( f'\\+\\s+verbose:\\s+segment\\s+{last_generated_repl_segment}\\s+\\(\\d+\\s+bytes\\)\\s+is\\s+replicated.*deleting', re.IGNORECASE)

    # VERBOSE: Segment 16 replication failure at offset 33628
    p_replication_failure = re.compile('segment\\s+\\d+\\s+replication\\s+failure', re.IGNORECASE)

    # ERROR: Database is not in the replica mode
    p_database_not_replica = re.compile('ERROR:\\s+Database.* not.* replica', re.IGNORECASE)

    found_required_message = False
    found_replfail_message = False
    found_common_error_msg = False

    for i in range(0,max_allowed_time_for_wait):

        time.sleep(1)

        # Get content of fb_home replication.log _after_ isql finish:
        with open(replication_log, 'r') as f:
            diff_data = unified_diff(
                replold_lines,
                f.readlines()
              )

        for k,d in enumerate(diff_data):
            if p_successfully_replicated.search(d):
                # We FOUND phrase "VERBOSE: Segment <last_generated_repl_segment> ... is replicated ..." in the replication log.
                # This is expected success, break!
                print( (prefix_msg + ' ' if prefix_msg else '') + f'FOUND message about replicated segment N {last_generated_repl_segment}.' )
                found_required_message = True
                break

            if p_replication_failure.search(d):
                print( (prefix_msg + ' ' if prefix_msg else '') + 'SEGMENT_FAILURE: ' + d )
                found_replfail_message = True
                break

            if p_database_not_replica.search(d):
                print( (prefix_msg + ' ' if prefix_msg else '') + 'EXPECTED_NOT_REPL')
                found_required_message = True
                break

            if 'ERROR:' in d:
                print( (prefix_msg + ' ' if prefix_msg else '') + 'COMMON_FAILURE: ' + d )
                found_common_error_msg = True
                break

        if found_required_message or found_replfail_message or found_common_error_msg:
            break

    if not found_required_message:
        print('UNEXPECTED RESULT: no message about replicating segment N {last_generated_repl_segment} for {max_allowed_time_for_wait} seconds.')

#--------------------------------------------

@pytest.mark.version('>=4.0.1')
def test_1(act_db_main: Action,  act_db_repl: Action, capsys):

    #assert '' == capsys.readouterr().out

    ###################
    somewhat_failed = 1
    ###################
    try:

        with act_db_repl.connect_server() as srv:
            srv.database.set_replica_mode(database = act_db_repl.db.db_path, mode = ReplicaMode.NONE)

        sql_init = '''
            set bail on;
            set list on;
            recreate table test(id int primary key using index test_pk, x int);
            commit;
            insert into test(id, x) values(1, 100);
            commit;
        '''

        act_db_main.expected_stderr = ''
        act_db_main.isql(switches=['-q'], input = sql_init)
        assert act_db_main.clean_stderr == act_db_main.clean_expected_stderr
        act_db_main.reset()

        # During next <MAX_TIME_FOR_WAIT_SEGMENT_IN_LOG> seconds message
        # "ERROR: Database is not in the replica mode" must appear in replication log:

        act_db_main.expected_stdout = 'EXPECTED_NOT_REPL'
        ##################################################################
        ###  W A I T   F O R   M E S S A G E   I N   R E P L . L O G   ###
        ##################################################################
        wait_for_data_in_replica( act_db_main, MAX_TIME_FOR_WAIT_SEGMENT_IN_LOG, '' )

        act_db_main.stdout = capsys.readouterr().out
        assert act_db_main.clean_stdout == act_db_main.clean_expected_stdout
        act_db_main.reset()

        #---------------------------------------------------

        # Return db_repl mode to 'read-only' (as it was before this test)
        # and wait after it for <MAX_TIME_FOR_WAIT_SEGMENT_IN_LOG> seconds
        # for previoously created segment be replicated:
        with act_db_repl.connect_server() as srv:
            srv.database.set_replica_mode(database = act_db_repl.db.db_path, mode = ReplicaMode.READ_ONLY)


        act_db_main.expected_stdout = 'POINT-1 FOUND message about replicated segment'
        ##############################################################################
        ###  W A I T   U N T I L    R E P L I C A    B E C O M E S   A C T U A L   ###
        ##############################################################################
        wait_for_data_in_replica( act_db_main, MAX_TIME_FOR_WAIT_SEGMENT_IN_LOG, 'POINT-1' )

        act_db_main.stdout = capsys.readouterr().out
        assert act_db_main.clean_stdout == act_db_main.clean_expected_stdout
        act_db_main.reset()

        #-----------------------------------------------------------------------
            
        # Check that both databases has the same data:
        for a in (act_db_main,act_db_repl):
            db_name = a.db.db_path.upper()

            sql_chk = f'''
                set list on;
                set blob all;
                set count on;
                select
                    '{db_name}' as db_name
                    ,t.*
                from test t;
            '''
        
            for a in (act_db_main,act_db_repl):
                a.expected_stdout = f"""
                    DB_NAME {db_name}
                    ID                1
                    X               100
                    Records affected: 1
                """
                a.isql(switches=['-q', '-nod'], input = sql_chk)
                assert a.clean_stdout == a.clean_expected_stdout
                a.reset()

        #---------------------------------------------------

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
                assert a.clean_stdout == a.clean_expected_stdout
                a.reset()

                
                a.expected_stdout = 'POINT-2 FOUND message about replicated segment'
                ##############################################################################
                ###  W A I T   U N T I L    R E P L I C A    B E C O M E S   A C T U A L   ###
                ##############################################################################
                wait_for_data_in_replica( a, MAX_TIME_FOR_WAIT_SEGMENT_IN_LOG, 'POINT-2' )

                a.stdout = capsys.readouterr().out
                assert a.clean_stdout == a.clean_expected_stdout
                a.reset()

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
        assert diff_meta == ''

        ###################
        somewhat_failed = 0
        ###################

    except Exception as e:
        pass


    if somewhat_failed:
        # If any previous assert failed, we have to RECREATE both master and slave databases.
        # Otherwise further execution of this test or other replication-related tests most likely will fail.
        for a in (act_db_main,act_db_repl):
            d = a.db.db_path
            a.db.drop()
            dbx = create_database(str(d), user = a.db.user)
            dbx.close()
            with a.connect_server() as srv:
                srv.database.set_write_mode(database = d, mode=DbWriteMode.ASYNC)
                srv.database.set_sweep_interval(database = d, interval = 0)
                if a == act_db_repl:
                    srv.database.set_replica_mode(database = d, mode = ReplicaMode.READ_ONLY)
                else:
                    with a.db.connect() as con:
                        # !! IT IS ASSUMED THAT REPLICATION FOLDERS ARE IN THE SAME DIR AS <DB_MAIN> !!
                        # DO NOT use 'a.db.db_path' for ALIASED database!
                        # Its '.parent' property will be '.' rather than full path.
                        # Use only con.info.name for that:
                        repl_root_path = Path(con.info.name).parent
                        repl_jrn_sub_dir = repl_settings['journal_sub_dir']
                        repl_arc_sub_dir = repl_settings['archive_sub_dir']

                        # Clean folders repl_journal and repl_archive (remove all files from there):
                        for p in (repl_jrn_sub_dir,repl_arc_sub_dir):
                            assert cleanup_folder(repl_root_path / p) == 0, f"Directory {str(p)} remains non-empty."

                        con.execute_immediate('alter database enable publication')
                        con.execute_immediate('alter database include all to publication')
                        con.commit()

    assert somewhat_failed == 0
