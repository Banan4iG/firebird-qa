#coding:utf-8

"""
ID:          replication.dblevel_triggers_must_not_fire_on_replica
ISSUE:       6850
TITLE:       Replica DB must not fire DB-level triggers but their activity on master must be eventually seen in replica
DESCRIPTION:
    Test creates five DB-level triggers in the master DB (on connect/disconnect; on tx start/commit/rollback).
    Each of them registers apropriate event in the table with name 'log_db_triggers_activity'.
    This table must eventually have five records in BOTH databases (i.e. not only in master, but in replica also).
    After creating metadata we make test connect to master DB to fire these triggers.

    Then we wait until replica becomes actual to master, and this delay will last no more then threshold
    that is defined by MAX_TIME_FOR_WAIT_SEGMENT_IN_LOG variable (measured in seconds).
    During this delay, we check every second for replication log and search there line with number of last generated
    segment (which was replicated and deleting finally).
    We can assume that replication finished OK only when such line is found see ('POINT-1').

    After this, we do query master and replica databases and obtain data from 'log_db_triggers_activity' table: it must
    have records about every fired trigger. Content of this table must be identical on master and replica, see queries
    to v_log_db_triggers_activity (both on master and replica DB).

    Then we invoke ISQL with executing auxiliary script for drop all DB objects on master (with '-nod' command switch).
    After all objects will be dropped, we have to wait again until  replica becomes actual with master (see 'POINT-2').

    Finally, we extract metadata for master and replica and compare them (see 'f_meta_diff').
    The only difference in metadata must be 'CREATE DATABASE' statement with different DB names - we suppress it,
    thus metadata difference must not be issued.

    ################
    ### N O T E  ###
    ################
    Test assumes that master and replica DB have been created beforehand.
    Also, it assumes that %FB_HOME%/replication.conf has been prepared with apropriate parameters for replication.
    Particularly, name of directories and databases must have info about checked FB major version and ServerMode.
        * verbose = true // in order to find out line with message that required segment was replicated
        * section for master database with specified parameters:
            journal_directory = "!fbt_repo!/tmp/fb-replication.!fb_major!.!server_mode!.journal"
            journal_archive_directory = "!fbt_repo!/tmp/fb-replication.!fb_major!.!server_mode!.archive"
            journal_archive_command = "copy $(pathname) $(archivepathname)"
            journal_archive_timeout = 10
        * section for replica database with specified parameter:
             journal_source_directory =  "!fbt_repo!/tmp/fb-replication.!fb_major!.!server_mode!.archive"

    Master and replica databases must be created in "!fbt_repo!	mp" directory and have names like these:
        'fbt-main.fb40.SS.fdb'; 'fbt-repl.fb40.SS.fdb'; - for FB 4.x ('SS' = Super; 'CS' = Classic)
        'fbt-main.fb50.SS.fdb'; 'fbt-repl.fb50.SS.fdb'; - for FB 5.x ('SS' = Super; 'CS' = Classic)
        NB: fixed numeric value ('40' or '50') must be used for any minor FB version (4.0; 4.0.1; 4.1; 5.0; 5.1 etc)

    These two databases must NOT be dropped in any of tests related to replication!
    They are created and dropped in the batch scenario which prepares FB instance to be checked for each ServerMode
    and make cleanup after it, i.e. when all tests will be completed.

    NB. Currently this task was implemented only in Windows batch, thus test has attribute platform = 'Windows'.

    Temporary comment. For debug purpoces:
        1) find out SUFFIX of the name of FB service which is to be tested (e.g. 'DefaultInstance', '40SS' etc);
        2) copy file %fbt-repo%/tests/functional/tabloid/batches/setup-fb-for-replication.bat.txt
           to some place and rename it "*.bat";
        3) open this .bat in editor and asjust value of 'fbt_repo' variable;
        4) run: setup-fb-for-replication.bat [SUFFIX_OF_FB_SERVICE]
           where SUFFIX_OF_FB_SERVICE is ending part of FB service which you want to check:
           DefaultInstance ; 40ss ; 40cs ; 50ss ; 50cs etc
        5) batch 'setup-fb-for-replication.bat' will:
           * stop selected FB instance
           * create test databases (in !fbt_repo!/tmp);
           * prepare journal/archive sub-folders for replication (also in !fbt_repo!/tmp);
           * replace %fb_home%/replication.conf with apropriate
           * start selected FB instance
        6) run this test (FB instance will be already launched by setup-fb-for-replication.bat):
            %fpt_repo%/fbt-run2.bat dblevel-triggers-must-not-fire-on-replica.fbt 50ss, etc

    Checked on:
        4.0.1.2519 SS: 56.48s, CS: 99.31s
        5.0.0.82   SS: 20.63s, CS: 21.39s
FBTEST:      tests.functional.replication.dblevel_triggers_must_not_fire_on_replica
"""

import pytest
from firebird.qa import *

substitutions = [('Start removing objects in:.*', 'Start removing objects'),
                 ('Finish. Total objects removed:  [1-9]\\d*', 'Finish. Total objects removed'),
                 ('.* CREATE DATABASE .*', '')]

db = db_factory()

act = python_act('db', substitutions=substitutions)

expected_stdout = """
    POINT-1 FOUND message about replicated segment.

    MAIN_DB_TRIGGER_FIRED           DB_ATTACH
    MAIN_DB_TRIGGER_FIRED           TX_START
    MAIN_DB_TRIGGER_FIRED           TX_ROLLBACK
    MAIN_DB_TRIGGER_FIRED           TX_COMMIT
    MAIN_DB_TRIGGER_FIRED           DB_DETACH
    Records affected: 5

    REPL_DB_TRIGGER_FIRED           DB_ATTACH
    REPL_DB_TRIGGER_FIRED           TX_START
    REPL_DB_TRIGGER_FIRED           TX_ROLLBACK
    REPL_DB_TRIGGER_FIRED           TX_COMMIT
    REPL_DB_TRIGGER_FIRED           DB_DETACH
    Records affected: 5

    Start removing objects in:      C:\\FBTESTING\\QA\\FBT-REPO\\TMP\\FBT-MAIN.FB50.FDB
    Finish. Total objects removed:  9

    POINT-2 FOUND message about replicated segment.
"""

@pytest.mark.skip('FIXME: Not IMPLEMENTED')
@pytest.mark.version('>=4.0')
@pytest.mark.platform('Windows')
def test_1(act: Action):
    pytest.fail("Not IMPLEMENTED")

# test_script_1
#---
#
#  import os
#  import subprocess
#  import re
#  import difflib
#  import shutil
#  import time
#
#  os.environ["ISC_USER"] = user_name
#  os.environ["ISC_PASSWORD"] = user_password
#
#  #####################################
#  MAX_TIME_FOR_WAIT_SEGMENT_IN_LOG = 65
#  #####################################
#
#  svc = fdb.services.connect(host='localhost', user=user_name, password=user_password)
#  FB_HOME = svc.get_home_directory()
#  svc.close()
#
#  engine = db_conn.engine_version         # 4.0; 4.1; 5.0 etc -- type float
#  fb_major = 'fb' + str(engine)[:1] + '0' # 'fb40'; 'fb50'
#
#  cur = db_conn.cursor()
#  cur.execute("select rdb$config_value from rdb$config where upper(rdb$config_name) = upper('ServerMode')")
#  server_mode = 'XX'
#  for r in cur:
#      if r[0] == 'Super':
#          server_mode = 'SS'
#      elif r[0] == 'SuperClassic':
#          server_mode = 'SC'
#      elif r[0] == 'Classic':
#          server_mode = 'CS'
#  cur.close()
#
#  # 'fbt-main.fb50.ss.fdb' etc:
#  db_main = os.path.join( context['temp_directory'], 'fbt-main.' + fb_major + '.' + server_mode + '.fdb' )
#  db_repl = db_main.replace( 'fbt-main.', 'fbt-repl.')
#
#  # Folders for journalling and archieving segments.
#  repl_journal_dir = os.path.join( context['temp_directory'], 'fb-replication.' + fb_major + '.' + server_mode + '.journal' )
#  repl_archive_dir = os.path.join( context['temp_directory'], 'fb-replication.' + fb_major + '.' + server_mode +  '.archive' )
#
#  db_conn.close()
#
#  #--------------------------------------------
#
#  def flush_and_close( file_handle ):
#      # https://docs.python.org/2/library/os.html#os.fsync
#      # If you're starting with a Python file object f,
#      # first do f.flush(), and
#      # then do os.fsync(f.fileno()), to ensure that all internal buffers associated with f are written to disk.
#      global os
#
#      file_handle.flush()
#      if file_handle.mode not in ('r', 'rb') and file_handle.name != os.devnull:
#          # otherwise: "OSError: [Errno 9] Bad file descriptor"!
#          os.fsync(file_handle.fileno())
#      file_handle.close()
#
#  #--------------------------------------------
#
#  def cleanup( f_names_list ):
#      global os
#      for i in range(len( f_names_list )):
#         if type(f_names_list[i]) == file:
#            del_name = f_names_list[i].name
#         elif type(f_names_list[i]) == str:
#            del_name = f_names_list[i]
#         else:
#            print('Unrecognized type of element:', f_names_list[i], ' - can not be treated as file.')
#            del_name = None
#
#         if del_name and os.path.isfile( del_name ):
#             os.remove( del_name )
#
#  #--------------------------------------------
#
#  def wait_for_data_in_replica( fb_home, max_allowed_time_for_wait, db_main, prefix_msg = '' ):
#
#      global re
#      global difflib
#      global time
#
#      replold_lines = []
#      with open( os.path.join(fb_home,'replication.log'), 'r') as f:
#          replold_lines = f.readlines()
#
#      con = fdb.connect( dsn = 'localhost:' + db_main, no_db_triggers = 1)
#      cur = con.cursor()
#      cur.execute("select rdb$get_context('SYSTEM','REPLICATION_SEQUENCE') from rdb$database")
#      for r in cur:
#          last_generated_repl_segment = r[0]
#      cur.close()
#      con.close()
#
#      #print('last_generated_repl_segment:', last_generated_repl_segment)
#
#
#      # +IMAGE-PC1 (replica) Fri Jun 11 17:57:01 2021
#      # +       Database: C:\\FBTESTING\\QA\\FBT-REPO\\TMP\\FBT-REPL.FB50.FDB
#      # +       VERBOSE: Added 1 segment(s) to the processing queue
#      # +
#      # +IMAGE-PC1 (replica) Fri Jun 11 17:57:04 2021
#      # +       Database: C:\\FBTESTING\\QA\\FBT-REPO\\TMP\\FBT-REPL.FB50.FDB
#      # +       VERBOSE: Segment 1 (2582 bytes) is replicated in 1 second(s), deleting the file
#
#      p=re.compile( '\\+\\s+verbose:\\s+segment\\s+%(last_generated_repl_segment)s\\s+\\(\\d+\\s+bytes\\)\\s+is\\s+replicated.*deleting' % locals(), re.IGNORECASE)
#
#      found_required_message = False
#      for i in range(0,max_allowed_time_for_wait):
#          time.sleep(1)
#
#          # Get content of fb_home replication.log _after_ isql finish:
#          f_repllog_new = open( os.path.join(fb_home,'replication.log'), 'r')
#          diff_data = difflib.unified_diff(
#              replold_lines,
#              f_repllog_new.readlines()
#            )
#          f_repllog_new.close()
#
#          for k,d in enumerate(diff_data):
#              if p.search(d):
#                  print( (prefix_msg + ' ' if prefix_msg else '') + 'FOUND message about replicated segment.' )
#                  found_required_message = True
#                  break
#
#          if found_required_message:
#              break
#
#      if not found_required_message:
#          print('UNEXPECTED RESULT: no message about replicated segment for %d seconds.' % max_allowed_time_for_wait)
#
#  #--------------------------------------------
#
#  sql_ddl = '''    set bail on;
#      set list on;
#
#      select mon$database_name from mon$database;
#
#      set term ^;
#      execute block as
#      begin
#          -- Define context variable in order to prevent
#          -- DB-level triggers from firing during this execution:
#          rdb$set_context('USER_SESSION', 'SKIP_DBLEVEL_TRG','1');
#      end
#      ^
#      set term ;^
#
#      -- ::: NB :::
#      -- We can not start this script from 'zero-point', i.e. 'create table ...; create view ... ;' etc,
#      -- because it will fail if master or replica DB contain some objects which could remain there
#      -- due to fail of some previous test which also had deal with replication and used these databases.
#      -- Here we must remove all dependencies and only after this table can be recreated:
#      create or alter trigger trg_tx_start on transaction start as begin end;
#      create or alter trigger trg_tx_commit on transaction commit as begin end;
#      create or alter trigger trg_tx_rollback on transaction rollback as begin end;
#      create or alter trigger trg_connect active on connect as begin end;
#      create or alter trigger trg_disconnect active on disconnect as begin end;
#      create or alter procedure sp_log_dblevel_trg_event as begin end;
#      create or alter view v_log_db_triggers_activity as select 1 x from rdb$database;
#
#      -- result: no more objects that depend on table 'log_db_triggers_activity', now we can recreate it.
#
#      recreate table log_db_triggers_activity (
#          id int generated by default as identity constraint pk_log_db_triggers_activity primary key
#          ,dts timestamp default 'now'
#          ,att integer default current_connection
#          ,trn integer default current_transaction
#          ,app varchar(80)
#          ,evt varchar(80)
#      );
#
#      create or alter view v_log_db_triggers_activity as select * from log_db_triggers_activity;
#
#      set term ^;
#      create or alter procedure sp_log_dblevel_trg_event (
#          a_event_type varchar(80) -- type of column log_db_triggers_activity.evt
#         ,a_working_tx int default null
#      )
#      as
#          declare v_app varchar(255);
#          declare p smallint;
#          declare back_slash char(1);
#      begin
#          v_app = reverse( right(rdb$get_context('SYSTEM','CLIENT_PROCESS'), 80) );
#          back_slash = ascii_char(92); -- backward slash; do NOT specify it literally otherwise Python will handle it as empty string!
#          p = maxvalue(position(back_slash in v_app ), position('/' in v_app ));
#          v_app = reverse(substring(v_app from 1 for p-1));
#          execute statement( 'insert into v_log_db_triggers_activity( trn, app, evt) values( ?, ?, ? )' ) ( coalesce(:a_working_tx, current_transaction), :v_app, :a_event_type) ;
#
#      end
#      ^
#
#      create or alter trigger trg_tx_start on transaction start as
#      begin
#          if (rdb$get_context('USER_SESSION', 'SKIP_DBLEVEL_TRG') is null ) then
#              -- execute procedure sp_log_dblevel_trg_event( 'TX_START, TIL=' || coalesce( rdb$get_context('SYSTEM', 'ISOLATION_LEVEL'), '[null]' ) );
#              execute procedure sp_log_dblevel_trg_event( 'TX_START' );
#      end
#      ^
#
#      create or alter trigger trg_tx_commit on transaction commit as
#      begin
#          if (rdb$get_context('USER_SESSION', 'SKIP_DBLEVEL_TRG') is null ) then
#              -- execute procedure sp_log_dblevel_trg_event( 'TX_COMMIT, TIL=' || coalesce( rdb$get_context('SYSTEM', 'ISOLATION_LEVEL'), '[null]' ) );
#              execute procedure sp_log_dblevel_trg_event( 'TX_COMMIT' );
#      end
#      ^
#
#      create or alter trigger trg_tx_rollback on transaction rollback as
#          declare v_current_tx int;
#      begin
#          v_current_tx = current_transaction;
#          if (rdb$get_context('USER_SESSION', 'SKIP_DBLEVEL_TRG') is null ) then
#              in autonomous transaction do
#              -- execute procedure sp_log_dblevel_trg_event( 'TX_ROLLBACK, TIL=' || coalesce( rdb$get_context('SYSTEM', 'ISOLATION_LEVEL'), '[null]' ), v_current_tx );
#              execute procedure sp_log_dblevel_trg_event( 'TX_ROLLBACK' );
#      end
#      ^
#
#      create or alter trigger trg_connect active on connect position 0 as
#      begin
#          if (rdb$get_context('USER_SESSION', 'SKIP_DBLEVEL_TRG') is null ) then
#              execute procedure sp_log_dblevel_trg_event( 'DB_ATTACH' );
#      end
#      ^
#
#      create or alter trigger trg_disconnect active on disconnect position 0 as
#          declare v_current_tx int;
#      begin
#          if (rdb$get_context('USER_SESSION', 'SKIP_DBLEVEL_TRG') is null ) then
#              execute procedure sp_log_dblevel_trg_event( 'DB_DETACH');
#      end
#      ^
#      set term ;^
#      commit;
#
#      select rdb$get_context('SYSTEM','REPLICATION_SEQUENCE') as last_generated_repl_segment from rdb$database;
#      quit;
#  ''' % locals()
#
#
#  f_sql_chk = open( os.path.join(context['temp_directory'],'tmp_repltest_skip_db_trg.sql'), 'w')
#  f_sql_chk.write(sql_ddl)
#  flush_and_close( f_sql_chk )
#
#  # Get content of FB_HOME replication.log _before_ launching ISQL:
#  #############
#
#  replold_lines = []
#  with open( os.path.join(FB_HOME,'replication.log'), 'r') as f:
#      replold_lines = f.readlines()
#
#  f_sql_log = open( ''.join( (os.path.splitext(f_sql_chk.name)[0], '.log' ) ), 'w')
#  f_sql_err = open( ''.join( (os.path.splitext(f_sql_chk.name)[0], '.err' ) ), 'w')
#  subprocess.call( [ context['isql_path'], 'localhost:' + db_main, '-i', f_sql_chk.name ], stdout = f_sql_log, stderr = f_sql_err)
#  flush_and_close( f_sql_log )
#  flush_and_close( f_sql_err )
#
#  last_generated_repl_segment = 0
#
#  with open(f_sql_err.name,'r') as f:
#      for line in f:
#          print('UNEXPECTED STDERR in initial SQL: ' + line)
#          MAX_TIME_FOR_WAIT_SEGMENT_IN_LOG = 0
#
#  if MAX_TIME_FOR_WAIT_SEGMENT_IN_LOG: # ==> initial SQL script finished w/o errors
#
#      # Test connect to master DB, just to fire DB-level triggers:
#      ###########################
#      con1 = fdb.connect( dsn = 'localhost:' + db_main)
#      con1.execute_immediate('recreate table test(id int)')
#      con1.close()
#
#      ##############################################################################
#      ###  W A I T   U N T I L    R E P L I C A    B E C O M E S   A C T U A L   ###
#      ##############################################################################
#      wait_for_data_in_replica( FB_HOME, MAX_TIME_FOR_WAIT_SEGMENT_IN_LOG, db_main, 'POINT-1' )
#
#      runProgram('isql', ['localhost:' + db_main, '-nod'], 'set count on; set list on; select evt as main_db_trigger_fired from v_log_db_triggers_activity order by id;')
#      runProgram('isql', ['localhost:' + db_repl, '-nod'], 'set count on; set list on; select evt as repl_db_trigger_fired from v_log_db_triggers_activity order by id;')
#
#
#  # return initial state of master DB:
#  # remove all DB objects (tables, views, ...):
#  # --------------------------------------------
#  sql_clean_ddl = os.path.join(context['files_location'],'drop-all-db-objects.sql')
#
#  f_clean_log=open( os.path.join(context['temp_directory'],'drop-all-db-objects.log'), 'w')
#  f_clean_err=open( ''.join( ( os.path.splitext(f_clean_log.name)[0], '.err') ), 'w')
#  subprocess.call( [context['isql_path'], 'localhost:' + db_main, '-q', '-nod', '-i', sql_clean_ddl], stdout=f_clean_log, stderr=f_clean_err )
#  flush_and_close(f_clean_log)
#  flush_and_close(f_clean_err)
#
#  with open(f_clean_err.name,'r') as f:
#      for line in f:
#          print('UNEXPECTED STDERR in cleanup SQL: ' + line)
#          MAX_TIME_FOR_WAIT_SEGMENT_IN_LOG = 0
#
#  with open(f_clean_log.name,'r') as f:
#      for line in f:
#          # show number of dropped objects
#          print(line)
#
#  if MAX_TIME_FOR_WAIT_SEGMENT_IN_LOG: # ==> initial SQL script finished w/o errors
#
#      ##############################################################################
#      ###  W A I T   U N T I L    R E P L I C A    B E C O M E S   A C T U A L   ###
#      ##############################################################################
#      wait_for_data_in_replica( FB_HOME, MAX_TIME_FOR_WAIT_SEGMENT_IN_LOG, db_main, 'POINT-2' )
#
#      f_main_meta_sql=open( os.path.join(context['temp_directory'],'db_main_meta.sql'), 'w')
#      subprocess.call( [context['isql_path'], 'localhost:' + db_main, '-q', '-nod', '-ch', 'utf8', '-x'], stdout=f_main_meta_sql, stderr=subprocess.STDOUT )
#      flush_and_close( f_main_meta_sql )
#
#      f_repl_meta_sql=open( os.path.join(context['temp_directory'],'db_repl_meta.sql'), 'w')
#      subprocess.call( [context['isql_path'], 'localhost:' + db_repl, '-q', '-nod', '-ch', 'utf8', '-x'], stdout=f_repl_meta_sql, stderr=subprocess.STDOUT )
#      flush_and_close( f_repl_meta_sql )
#
#      db_main_meta=open(f_main_meta_sql.name, 'r')
#      db_repl_meta=open(f_repl_meta_sql.name, 'r')
#
#      diffmeta = ''.join(difflib.unified_diff(
#          db_main_meta.readlines(),
#          db_repl_meta.readlines()
#        ))
#      db_main_meta.close()
#      db_repl_meta.close()
#
#      f_meta_diff=open( os.path.join(context['temp_directory'],'db_meta_diff.txt'), 'w', buffering = 0)
#      f_meta_diff.write(diffmeta)
#      flush_and_close( f_meta_diff )
#
#      # Following must issue only TWO rows:
#      #     UNEXPECTED METADATA DIFF.: -/* CREATE DATABASE 'localhost:[db_main]' ... */
#      #     UNEXPECTED METADATA DIFF.: -/* CREATE DATABASE 'localhost:[db_repl]' ... */
#      # Only thes lines will be suppressed further (see subst. section):
#      with open(f_meta_diff.name, 'r') as f:
#          for line in f:
#             if line[:1] in ('-', '+') and line[:3] not in ('---','+++'):
#                 print('UNEXPECTED METADATA DIFF.: ' + line)
#
#
#  # cleanup:
#  ##########
#  cleanup( (f_sql_chk, f_sql_log, f_sql_err,f_clean_log,f_clean_err,f_main_meta_sql,f_repl_meta_sql,f_meta_diff) )
#
#---
