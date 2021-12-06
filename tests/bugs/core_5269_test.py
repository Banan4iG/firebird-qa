#coding:utf-8
#
# id:           bugs.core_5269
# title:        FBTRACEMGR should understand 'role <name>' command switch (needed to explicitly connect with role with 'TRACE_ANY_ATTACHMENT' privilege)
# decription:
#                  We create two users and one of them is granted with role that allows him to watch other users activity.
#                  Than we start FBSVCMGR utility with specifying this user and his ROLE so that he can start wathing.
#                  After this we make trivial query to database from another user.
#                  Finally, we check trace log that was recived by watching user: this log must contain phrases about
#                  preprating, starting and executing statements.
#
#                  Checked on 4.0.0.321 - works fine.
#
# tracker_id:   CORE-5269
# min_versions: ['4.0']
# versions:     4.0
# qmid:         None

import pytest
import time
from threading import Thread, Barrier
from firebird.qa import db_factory, python_act, Action, user_factory, User

# version: 4.0
# resources: None

substitutions_1 = [('\t+', ' '),
                   ('^((?!ROLE_|PREPARE_STATEMENT|EXECUTE_STATEMENT_START|EXECUTE_STATEMENT_FINISH).)*$', ''),
                   ('.*PREPARE_STATEMENT', 'TRACE_LOG: PREPARE_STATEMENT'),
                   ('.*EXECUTE_STATEMENT_START', 'TRACE_LOG: EXECUTE_STATEMENT_START'),
                   ('.*EXECUTE_STATEMENT_FINISH', 'TRACE_LOG: EXECUTE_STATEMENT_FINISH')]

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

# test_script_1
#---
#
#  import os
#  import sys
#  import subprocess
#  import time
#
#  os.environ["ISC_USER"] = user_name
#  os.environ["ISC_PASSWORD"] = user_password
#  db_file = db_conn.database_name
#  db_conn.close()
#
#  #--------------------------------------------
#
#  def flush_and_close(file_handle):
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
#  sql_ddl='''     set wng off;
#       set bail on;
#       set list on;
#
#       create or alter user TMP$C5269_1 password '123' revoke admin role;
#       create or alter user TMP$C5269_2 password '456' revoke admin role;
#       revoke all on all from TMP$C5269_1;
#       revoke all on all from TMP$C5269_2;
#       commit;
#
#       -- Trace other users' attachments
#       create role role_for_trace_any_attachment
#           set system privileges to TRACE_ANY_ATTACHMENT;
#       commit;
#
#       grant role_for_trace_any_attachment to user TMP$C5269_2;
#       commit;
#
#       set list on;
#       select p.rdb$user as role_grantee, p.rdb$grantor as role_grantor, r.rdb$role_name as role_name, r.rdb$owner_name as role_owner
#       from rdb$user_privileges p
#       join rdb$roles r on p.rdb$relation_name = r.rdb$role_name
#       where p.rdb$user = upper('TMP$C5269_2');
#  '''
#  runProgram('isql',[dsn],sql_ddl)
#
#  att1 = fdb.connect(dsn=dsn,user='TMP$C5269_1',password='123')
#  cur1 = att1.cursor()
#
#  txt30 = '''# Trace config, format for 3.0. Generated auto, do not edit!
#  database=#%[\\\\\\\\/]bugs.core_5269.fdb
#  {
#    enabled = true
#    log_statement_prepare = true
#    log_statement_start = true
#    log_statement_finish = true
#    time_threshold = 0
#    max_sql_length = 5000
#  }
#  '''
#
#  f_trccfg=open( os.path.join(context['temp_directory'],'tmp_trace_5269.cfg'), 'w')
#  f_trccfg.write(txt30)
#  flush_and_close( f_trccfg )
#
#
#  # Now we run TRACE in child process (asynchronous)
#  ##################
#
#  f_trclog=open( os.path.join(context['temp_directory'],'tmp_trace_5269.log'), 'w')
#  f_trcerr=open( os.path.join(context['temp_directory'],'tmp_trace_5269.err'), 'w')
#  #'''
#  p_trace=subprocess.Popen( [context['fbsvcmgr_path'],"localhost:service_mgr",
#                             "user", "TMP$C5269_2",
#                             "password", "456",
#                             "role", "role_for_trace_any_attachment",
#                             "action_trace_start", "trc_cfg", f_trccfg.name
#                            ],
#                            stdout=f_trclog, stderr=f_trcerr
#                          )
#
#  time.sleep(1)
#
#  cur1.execute("select current_user from rdb$database")
#  cur1.close()
#  att1.close()
#
#  time.sleep(1)
#
#  # Getting ID of launched trace session and STOP it:
#  ###################################################
#
#  # Save active trace session info into file for further parsing it and obtain session_id back (for stop):
#  f_trclst=open( os.path.join(context['temp_directory'],'tmp_trace_5269.lst'), 'w')
#  subprocess.call([context['fbsvcmgr_path'], "localhost:service_mgr",
#                   "action_trace_list"],
#                   stdout=f_trclst, stderr=subprocess.STDOUT
#                 )
#  flush_and_close( f_trclst )
#
#  trcssn=0
#  with open( f_trclst.name,'r') as f:
#      for line in f:
#          i=1
#          if 'Session ID' in line:
#              for word in line.split():
#                  if i==3:
#                      trcssn=word
#                  i=i+1
#              break
#
#  # Result: `trcssn` is ID of active trace session. Now we have to terminate it:
#  f_trclst=open(f_trclst.name,'a')
#  f_trclst.seek(0,2)
#  subprocess.call([context['fbsvcmgr_path'], "localhost:service_mgr",
#                   "action_trace_stop",
#                   "trc_id",trcssn],
#                   stdout=f_trclst, stderr=subprocess.STDOUT
#                 )
#  flush_and_close( f_trclst )
#
#  p_trace.terminate()
#  flush_and_close( f_trclog )
#  flush_and_close( f_trcerr )
#
#  runProgram('isql',[dsn],'drop user TMP$C5269_1; drop user TMP$C5269_2; commit;')
#
#  with open( f_trclog.name,'r') as f:
#      for line in f:
#          print('TRACE LOG: '+line)
#
#  with open( f_trcerr.name,'r') as f:
#      for line in f:
#          print('UNEXPECTED TRACE ERR: '+line)
#
#
#  # Cleanup.
#  ##########
#  # Wait! Otherwise get WindowsError 32 on attempt to remove trace log and err files:
#  time.sleep(1)
#  cleanup( (f_trclog, f_trcerr, f_trccfg,f_trclst) )
#
#---

act_1 = python_act('db_1', substitutions=substitutions_1)

expected_stdout_1_a = """
    ROLE_GRANTEE                    TMP$C5269_2
    ROLE_GRANTOR                    SYSDBA
    ROLE_NAME                       ROLE_FOR_TRACE_ANY_ATTACHMENT
    ROLE_OWNER                      SYSDBA
"""

expected_stdout_1_b = """
    TRACE LOG: 2016-08-06T11:51:38.9360 (2536:01FD0CC8) PREPARE_STATEMENT
    TRACE LOG: 2016-08-06T11:51:38.9360 (2536:01FD0CC8) EXECUTE_STATEMENT_START
    TRACE LOG: 2016-08-06T11:51:38.9360 (2536:01FD0CC8) EXECUTE_STATEMENT_FINISH
"""

def trace_session(act: Action, b: Barrier):
    cfg30 = ['# Trace config, format for 3.0. Generated auto, do not edit!',
             f'database=%[\\\\/]{act.db.db_path.name}',
             '{',
             '  enabled = true',
             '  time_threshold = 0',
             '  log_initfini = false',
             '  log_statement_start = true',
             '  log_statement_finish = true',
             '  max_sql_length = 5000',
             '  log_statement_prepare = true',
             '}']
    with act.connect_server(user='TMP$C5269_2', password='456',
                            role='role_for_trace_any_attachment') as srv:
        srv.trace.start(config='\n'.join(cfg30))
        b.wait()
        for line in srv:
            print(line)

user_1_a = user_factory(name='TMP$C5269_1', password='123')
user_1_b = user_factory(name='TMP$C5269_2', password='456')

test_script_1_a = """
set list on;
select p.rdb$user as role_grantee, p.rdb$grantor as role_grantor, r.rdb$role_name as role_name, r.rdb$owner_name as role_owner
from rdb$user_privileges p
join rdb$roles r on p.rdb$relation_name = r.rdb$role_name
where p.rdb$user = upper('TMP$C5269_2');
"""

@pytest.mark.version('>=4.0')
def test_1(act_1: Action, user_1_a: User, user_1_b: User, capsys):
    with act_1.test_role('role_for_trace_any_attachment'):
        with act_1.db.connect() as con:
            con.execute_immediate('alter role role_for_trace_any_attachment set system privileges to TRACE_ANY_ATTACHMENT')
            con.commit()
            con.execute_immediate('grant role_for_trace_any_attachment to user TMP$C5269_2')
            con.commit()
        act_1.expected_stdout = expected_stdout_1_a
        act_1.isql(switches=[], input=test_script_1_a)
        assert act_1.clean_stdout == act_1.clean_expected_stdout
        # Run trace
        b = Barrier(2)
        trace_thread = Thread(target=trace_session, args=[act_1, b])
        trace_thread.start()
        b.wait()
        # Test
        with act_1.db.connect(user='TMP$C5269_1', password='123') as con:
            c = con.cursor()
            c.execute('select current_user from rdb$database')
        time.sleep(2)
        # End trace
        with act_1.connect_server() as srv:
            for session in list(srv.trace.sessions.keys()):
                srv.trace.stop(session_id=session)
            trace_thread.join(1.0)
            if trace_thread.is_alive():
                pytest.fail('Trace thread still alive')
        # Check
        act_1.reset()
        act_1.expected_stdout = expected_stdout_1_b
        act_1.stdout = capsys.readouterr().out
        assert act_1.clean_stdout == act_1.clean_expected_stdout

