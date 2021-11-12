#coding:utf-8
#
# id:           functional.transactions.read_consist_sttm_restart_on_update_02
# title:        READ CONSISTENCY. Check creation of new statement-level snapshot and restarting changed caused by UPDATE. Test-02.
# decription:   
#                   Initial article for reading:
#                   https://asktom.oracle.com/pls/asktom/f?p=100:11:::::P11_QUESTION_ID:11504247549852
#                   Note on terms which are used there: "BLOCKER", "LONG" and "FIRSTLAST" - their names are slightly changed here
#                   to: LOCKER-1, WORKER and LOCKER-2 respectively.
#               
#                   **********************************************
#               
#                   This test verifies that statement-level snapshot and restart will be performed when "main" session ("worker") 
#                   performs UPDATE statement and is involved in update conflicts.
#                   ("When update conflict is detected <...> then engine <...> creates new statement-level snapshot and restart execution...")
#               
#                   ::: NB :::
#                   This test uses script %FBT_REPO%
#               iles
#               ead-consist-sttm-restart-DDL.sql which contains common DDL for all other such tests.
#                   Particularly, it contains two TRIGGERS (TLOG_WANT and TLOG_DONE) which are used for logging of planned actions and actual
#                   results against table TEST. These triggers use AUTONOMOUS transactions in order to have ability to see results in any
#                   outcome of test.
#               
#                   ###############
#                   Following scenario if executed here (see also: "doc\\README.read_consistency.md"; hereafer is marked as "DOC"):
#               
#                   * five rows are inserted into the table TEST, with IDs: 1,2,3,4,5
#                   * session 'locker-1' ("BLOCKER" in Tom Kyte's article ):
#                           delete from test where id = 5;
#               
#                   * session 'worker' ("LONG" in TK article) has mission:
#                           update test set id = -id where exists(select * from test where id < 0 or id = 5) order by id; // using TIL = read committed read consistency
#               
#                       // Execution will have PLAN ORDER <ASCENDING_INDEX>.
#                       // Worker starts with updating rows with ID = 1...4 but can not change row with ID = 5 because of locker-1.
#                       // Because of detecting update conflist, worker changes here its TIL to RC NO RECORD_VERSION.
#               
#                   * session 'locker-2' ("FIRSTLAST" in TK article):
#                           (1) insert into test(id) values(-11);
#                           (2) commit;
#                           (3) delete from test where id = -11;
#               
#                       // session-'worker' remains waiting at this point because row with ID = 5 is still occupied by by locker-1.
#                       // Record with (new) id = -11 will be seen further because worker's TIL was changed to RC NO RECORD_VERSION.
#               
#                   * session 'locker-1':
#                           (1) commit;
#                           (2) insert into test(id) values(-12);
#                           (3) commit;
#                           (4) delete from test where id = -12;
#               
#                       // This: '(1) commit' - removes record with id = 5.
#                       // Because of TIL = RC NRV session-'worker' must see all committed records regardless on its own snapshot.
#                       // Thus worker sees record with id = -11 (which is locked now by locker-2) and puts write-lock on it.
#                       // [DOC]: "b) engine put write lock on conflicted record"
#                       // BECAUSE OF FACT THAT AT LEAST ONE ROW *WAS FOUND* - STATEMENT-LEVEL RESTART *NOT* YET OCCURS HERE.
#                       // [DOC]: "d) when there is *no more* records to fetch, engine start to undo all actions performed since
#                       //            top-level statement execution starts and preserve already taken write locks
#                       //         e) then engine restores transaction isolation mode as READ COMMITTED *READ CONSISTENCY*, 
#                       //            creates new statement-level snapshot and restart execution of top-level statement."
#               
#                   * session 'locker-2':
#                           (1) commit;
#                           (2) insert into test(id) values(-13);
#                           (3) commit;
#                           (4) update test set id=id where id = -13;
#                       
#                       // This: '(1) commit' - removes record with id = -11.
#                       // Because of TIL = RC NRV session-'worker' must see all committed records regardless on its own snapshot.
#                       // Thus worker sees record with id = -12 (which is locked now by locker-1) and puts write-lock on it.
#                       // BECAUSE OF FACT THAT AT LEAST ONE ROW *WAS FOUND* - STATEMENT-LEVEL RESTART *NOT* YET OCCURS HERE.
#               
#                   * session 'locker-1':
#                           (1) commit;
#                           (2) insert into test(id) values(-14);
#                           (3) commit;
#                           (4) update test set id=id where id = -14;
#               
#                       // This: '(1) commit' - removes record with id = -12.
#                       // Because of TIL = RC NRV session-'worker' must see all committed records regardless on its own snapshot.
#                       // Thus worker sees record with id = -13 (which is locked now by locker-2) and puts write-lock on it.
#                       // BECAUSE OF FACT THAT AT LEAST ONE ROW *WAS FOUND* - STATEMENT-LEVEL RESTART *NOT* YET OCCURS HERE.
#               
#                   * session 'locker-2':
#                           (1) commit;
#               
#                       // This removes record with id = -13.
#                       // Worker still waits for record with id = -14 which is occupied by locker-1.
#               
#                   * session 'locker-1':
#                           (1) commit;
#               
#                       // This removes record with id = -14.
#                       // At this point there are no more records to be locked (by worker) that meet cursor condition: worker did put
#                       // write locks on all rows that meet its cursor conditions.
#                       // BECAUSE OF FACT THAT NO MORE RECORDS FOUND TO BE LOCKED, WORKER DOES UNDO BUT KEEP LOCKS AND THEN
#                       // MAKES FIRST STATEMENT-LEVEL RESTART. This restart is also the last in this test.
#               
#               
#                   Expected result:
#                   * session-'worker' must update of only rows with ID = 1...4 (reverting sign of IDs value).
#               
#                   * Two unique values must be in the column TLOG_DONE.SNAP_NO for session-'worker' when it performed UPDATE statement: first of them
#                     was created by initial statement start and second reflects SINGLE restart (this column has values which are evaluated using
#                     rdb$get_context('SYSTEM', 'SNAPSHOT_NUMBER') -- see trigger TEST_AIUD).
#                     It is enough to count these values using COUNT(*) or enumarate them by DENSE_RANK() function.
#               
#                   NOTE: concrete values of fields TRN, GLOBAL_CN and SNAP_NO in the TLOG_DONE can differ from one to another run!
#                   This is because of concurrent nature of connections that work against database. We must not assume that these values will be constant.
#                           
#                   ################
#               
#                   Checked on 4.0.0.2195
#                   26.09.2020: added for-loop in order to check different target objects: TABLE ('test') and VIEW ('v_test'), see 'checked_mode'.
#                
# tracker_id:   
# min_versions: ['4.0']
# versions:     4.0
# qmid:         

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 4.0
# resources: None

substitutions_1 = [('=', ''), ('[ \t]+', ' ')]

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

# test_script_1
#---
# 
#  import os
#  import sys
#  import subprocess
#  from subprocess import Popen
#  from fdb import services
#  import time
#  
#  os.environ["ISC_USER"] = user_name
#  os.environ["ISC_PASSWORD"] = user_password
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
#      for f in f_names_list:
#         if type(f) == file:
#            del_name = f.name
#         elif type(f) == str:
#            del_name = f
#         else:
#            print('Unrecognized type of element:', f, ' - can not be treated as file.')
#            del_name = None
#  
#         if del_name and os.path.isfile( del_name ):
#             os.remove( del_name )
#      
#  #--------------------------------------------
#  
#  sql_init_ddl = os.path.join(context['files_location'],'read-consist-sttm-restart-DDL.sql')
#  
#  for checked_mode in('table', 'view'):
#  
#      target_obj = 'test' if checked_mode == 'table' else 'v_test'
#  
#      f_init_log=open( os.path.join(context['temp_directory'],'read-consist-sttm-restart-DDL.log'), 'w')
#      f_init_err=open( ''.join( ( os.path.splitext(f_init_log.name)[0], '.err') ), 'w')
#  
#      subprocess.call( [context['isql_path'], dsn, '-q', '-i', sql_init_ddl], stdout=f_init_log, stderr=f_init_err )
#      flush_and_close(f_init_log)
#      flush_and_close(f_init_err)
#  
#      # add rows with ID = 1, 2, ..., 5:
#      sql_addi='''
#          set term ^;
#          execute block as
#          begin
#              rdb$set_context('USER_SESSION', 'WHO', 'INIT_DATA');
#          end
#          ^
#          set term ;^
#          insert into %(target_obj)s(id, x) select row_number()over(),row_number()over() from rdb$types rows 5;
#          commit;
#      '''  % locals()
#      runProgram('isql', [ dsn, '-q' ], sql_addi)
#  
#      con_lock_1 = fdb.connect( dsn = dsn )
#      con_lock_2 = fdb.connect( dsn = dsn )
#      con_lock_1.execute_immediate( "execute block as begin rdb$set_context('USER_SESSION', 'WHO', 'LOCKER #1'); end" )
#      con_lock_2.execute_immediate( "execute block as begin rdb$set_context('USER_SESSION', 'WHO', 'LOCKER #2'); end" )
#  
#  
#      #########################
#      ###  L O C K E R - 1  ###
#      #########################
#  
#      con_lock_1.execute_immediate( 'delete from %(target_obj)s where id = 5'  % locals())
#  
#      sql_text='''
#          connect '%(dsn)s';
#          set list on;
#          set autoddl off;
#          set term ^;
#          execute block returns (whoami varchar(30)) as
#          begin
#              whoami = 'WORKER'; -- , ATT#' || current_connection;
#              rdb$set_context('USER_SESSION','WHO', whoami);
#              -- suspend;
#          end
#          ^
#          set term ;^
#          commit;
#          --set echo on;
#          SET KEEP_TRAN_PARAMS ON;
#          set transaction read committed read consistency;
#          --select current_connection, current_transaction from rdb$database;
#          set list off;
#          set wng off;
#          --set plan on;
#          set count on;
#  
#          update %(target_obj)s set id = -id order by id; -- THIS MUST BE LOCKED
#  
#          -- check results:
#          -- ###############
#  
#          select id from %(target_obj)s order by id; -- this will produce output only after all lockers do their commit/rollback
#  
#          select v.old_id, v.op, v.snap_no_rank from v_worker_log v where v.op = 'upd';
#  
#          set width who 10;
#          -- DO NOT check this! Values can differ here from one run to another!
#          -- select id, trn, who, old_id, new_id, op, rec_vers, global_cn, snap_no from tlog_done order by id;
#  
#          rollback;
#  
#      '''  % dict(globals(), **locals())
#  
#      f_worker_sql=open( os.path.join(context['temp_directory'],'tmp_sttm_restart_on_update_02.sql'), 'w')
#      f_worker_sql.write(sql_text)
#      flush_and_close(f_worker_sql)
#  
#  
#      f_worker_log=open( ''.join( ( os.path.splitext(f_worker_sql.name)[0], '.log') ), 'w')
#      f_worker_err=open( ''.join( ( os.path.splitext(f_worker_log.name)[0], '.err') ), 'w')
#  
#      ############################################################################
#      ###  L A U N C H     W O R K E R    U S I N G     I S Q L,   A S Y N C.  ###
#      ############################################################################
#  
#      p_worker = Popen( [ context['isql_path'], '-pag', '999999', '-q', '-i', f_worker_sql.name ],stdout=f_worker_log, stderr=f_worker_err)
#      time.sleep(1)
#  
#      #########################
#      ###  L O C K E R - 2  ###
#      #########################
#      con_lock_2.execute_immediate( 'insert into %(target_obj)s(id) values(-11)'  % locals())
#      con_lock_2.commit()
#      con_lock_2.execute_immediate( 'delete from %(target_obj)s where id = -11'  % locals())
#  
#      #########################
#      ###  L O C K E R - 1  ###
#      #########################
#      con_lock_1.commit()
#      con_lock_1.execute_immediate( 'insert into %(target_obj)s(id) values(-12)'  % locals())
#      con_lock_1.commit()
#      con_lock_1.execute_immediate( 'delete from %(target_obj)s where id = -12'  % locals())
#  
#  
#      #########################
#      ###  L O C K E R - 2  ###
#      #########################
#      con_lock_2.commit()
#      con_lock_2.execute_immediate( 'insert into %(target_obj)s(id) values(-13)'  % locals())
#      con_lock_2.commit()
#      con_lock_2.execute_immediate( 'delete from %(target_obj)s where id = -13'  % locals())
#  
#      #########################
#      ###  L O C K E R - 1  ###
#      #########################
#      con_lock_1.commit()
#      con_lock_1.execute_immediate( 'insert into %(target_obj)s(id) values(-14)'  % locals())
#      con_lock_1.commit()
#      con_lock_1.execute_immediate( 'delete from %(target_obj)s where id = -14'  % locals())
#  
#      #########################
#      ###  L O C K E R - 2  ###
#      #########################
#      con_lock_1.commit()
#  
#      #########################
#      ###  L O C K E R - 1  ###
#      #########################
#      con_lock_2.commit() # WORKER will complete his job after this
#  
#  
#      # Here we wait for ISQL complete its mission:
#      p_worker.wait()
#  
#      flush_and_close(f_worker_log)
#      flush_and_close(f_worker_err)
#  
#      # Close lockers:
#      ################
#      for c in (con_lock_1, con_lock_2):
#          c.close()
#  
#      # CHECK RESULTS
#      ###############
#      with open(f_worker_log.name,'r') as f:
#          for line in f:
#              if line.strip():
#                  print('checked_mode: %(checked_mode)s, STDLOG: %(line)s' % locals())
#  
#      for f in (f_init_err, f_worker_err):
#          with open(f.name,'r') as g:
#              for line in g:
#                  if line.strip():
#                      print( 'checked_mode: ', checked_mode, ' UNEXPECTED STDERR IN ' + g.name + ':', line)
#  
#  #<for checked mode in(...)
#  
#  # Cleanup.
#  ##########
#  time.sleep(1)
#  cleanup( (f_init_log, f_init_err, f_worker_sql, f_worker_log, f_worker_err) )
#    
#---
#act_1 = python_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    checked_mode: table, STDLOG: Records affected: 4

    checked_mode: table, STDLOG:      ID
    checked_mode: table, STDLOG: =======
    checked_mode: table, STDLOG:      -4
    checked_mode: table, STDLOG:      -3
    checked_mode: table, STDLOG:      -2
    checked_mode: table, STDLOG:      -1
    checked_mode: table, STDLOG: Records affected: 4

    checked_mode: table, STDLOG:  OLD_ID OP              SNAP_NO_RANK
    checked_mode: table, STDLOG: ======= ====== =====================
    checked_mode: table, STDLOG:       1 UPD                        1
    checked_mode: table, STDLOG:       2 UPD                        1
    checked_mode: table, STDLOG:       3 UPD                        1
    checked_mode: table, STDLOG:       4 UPD                        1
    checked_mode: table, STDLOG:       1 UPD                        2
    checked_mode: table, STDLOG:       2 UPD                        2
    checked_mode: table, STDLOG:       3 UPD                        2
    checked_mode: table, STDLOG:       4 UPD                        2
    checked_mode: table, STDLOG: Records affected: 8


    
    checked_mode: view, STDLOG: Records affected: 4

    checked_mode: view, STDLOG:      ID
    checked_mode: view, STDLOG: =======
    checked_mode: view, STDLOG:      -4
    checked_mode: view, STDLOG:      -3
    checked_mode: view, STDLOG:      -2
    checked_mode: view, STDLOG:      -1
    checked_mode: view, STDLOG: Records affected: 4

    checked_mode: view, STDLOG:  OLD_ID OP              SNAP_NO_RANK
    checked_mode: view, STDLOG: ======= ====== =====================
    checked_mode: view, STDLOG:       1 UPD                        1
    checked_mode: view, STDLOG:       2 UPD                        1
    checked_mode: view, STDLOG:       3 UPD                        1
    checked_mode: view, STDLOG:       4 UPD                        1
    checked_mode: view, STDLOG:       1 UPD                        2
    checked_mode: view, STDLOG:       2 UPD                        2
    checked_mode: view, STDLOG:       3 UPD                        2
    checked_mode: view, STDLOG:       4 UPD                        2
    checked_mode: view, STDLOG: Records affected: 8
  """

@pytest.mark.version('>=4.0')
@pytest.mark.xfail
def test_1(db_1):
    pytest.fail("Test not IMPLEMENTED")

