#coding:utf-8
#
# id:           bugs.core_4889
# title:        FBSVCMGR with `action_trace_start` prevents in 3.0 SuperServer from connecting using local protocol
# decription:
#                   Confirmed failing to create embedded attach on build 31948.
#                   Confirmed successful work on build 32268, architectures: SS, SC and CS.
#                   10.12.2019. Additional check:
#                       4.0.0.1685 SS: 11.439s.
#                       4.0.0.1685 CS: 12.078s.
#                       3.0.5.33206 SS: 10.827s.
#                       3.0.5.33206 CS: 11.793s.
#
#                   13.04.2021. Adapted for run both on Windows and Linux. Checked on:
#                     Windows: 3.0.8.33445, 4.0.0.2416
#                     Linux:   3.0.8.33426, 4.0.0.2416
#
# tracker_id:   CORE-4889
# min_versions: ['3.0']
# versions:     3.0
# qmid:         None

import pytest
import time
from threading import Thread, Barrier
from firebird.qa import db_factory, python_act, Action

# version: 3.0
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

# test_script_1
#---
#
#  import os
#  import subprocess
#  from subprocess import Popen
#  import time
#
#  fdb_file='$(DATABASE_LOCATION)bugs.core_4889.fdb'
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
#      for i in range(len( f_names_list )):
#         if type(f_names_list[i]) == file:
#            del_name = f_names_list[i].name
#         elif type(f_names_list[i]) == str:
#            del_name = f_names_list[i]
#         else:
#            print('Unrecognized type of element:', f_names_list[i], ' - can not be treated as file.')
#            print('type(f_names_list[i])=',type(f_names_list[i]))
#            del_name = None
#
#         if del_name and os.path.isfile( del_name ):
#             os.remove( del_name )
#
#  #--------------------------------------------
#
#
#  # Prepare config for trace session that will be launched by call of FBSVCMGR:
#  ################
#  txt = '''database= %[\\\\\\\\/]bugs.core_4889.fdb
#  {
#    enabled = true
#    time_threshold = 0
#    log_errors = true
#    log_statement_finish = true
#  }
#  '''
#  trc_cfg=open( os.path.join(context['temp_directory'],'tmp_trace_4889.cfg'), 'w')
#  trc_cfg.write(txt)
#  flush_and_close( trc_cfg )
#
#  #####################################################################
#  # Async. launch of trace session using FBSVCMGR action_trace_start:
#
#  trc_log = open( os.path.join(context['temp_directory'],'tmp_trace_4889.log'), 'w')
#
#  # Execute a child program in a new process, redirecting STDERR to the same target as of STDOUT:
#  p_svcmgr = Popen( [context['fbsvcmgr_path'], "localhost:service_mgr",
#                     "action_trace_start","trc_cfg", trc_cfg.name],
#                    stdout=trc_log, stderr=subprocess.STDOUT)
#
#  # Wait! Trace session is initialized not instantly!
#  time.sleep(2)
#
#  #####################################################################
#
#  # Determine active trace session ID (for further stop):
#
#  trc_lst = open( os.path.join(context['temp_directory'],'tmp_trace_4889.lst'), 'w')
#  subprocess.call([context['fbsvcmgr_path'], "localhost:service_mgr",
#                   "action_trace_list"],
#                   stdout=trc_lst, stderr=subprocess.STDOUT
#                 )
#  flush_and_close( trc_lst )
#
#  # Session ID: 5
#  #   user:
#  #   date:  2015-08-27 15:24:14
#  #   flags: active, trace
#
#  trcssn=0
#  with open( trc_lst.name,'r') as f:
#      for line in f:
#          i=1
#          if 'Session ID' in line:
#              for word in line.split():
#                  if i==3:
#                      trcssn=word
#                  i=i+1
#              break
#
#  # Result: `trcssn` is ID of active trace session.
#  # We have to terminate trace session that is running on server BEFORE we termitane process `p_svcmgr`
#  if trcssn==0:
#      print("Error parsing trace session ID.")
#      flush_and_close( trc_log )
#
#  else:
#      #####################################################################
#
#      # Preparing script for ISQL:
#
#      sql_cmd='''
#      set list on;
#      set count on;
#      select
#          iif(a.mon$remote_protocol is null, 'internal', 'remote') as connection_protocol,
#          iif(a.mon$remote_process is null,  'internal', 'remote') as connection_process,
#          iif(a.mon$remote_pid     is null,  'internal', 'remote') as connection_remote_pid,
#          a.mon$auth_method as auth_method -- should be: 'User name in DPB'
#      from rdb$database r
#      left join mon$attachments a on a.mon$attachment_id = current_connection and a.mon$system_flag = 0;
#      commit;
#      '''
#
#      isql_cmd=open( os.path.join(context['temp_directory'],'tmp_isql_4889.sql'), 'w')
#      isql_cmd.write(sql_cmd)
#      flush_and_close( isql_cmd )
#
#      #######################################################################
#
#      # Async. launch ISQL process with EMBEDDED connect.
#      # ::::: NB :::::
#      # Confirmed that this action:
#      # works fine on WI-V3.0.0.31940, build 14-jul-2015
#      # **HANGS**  on WI-V3.0.0.31948, build 16-jul-2015
#
#      isql_log=open( os.path.join(context['temp_directory'],'tmp_isql_4889.log'), 'w')
#      p_isql = Popen( [ context['isql_path'] , fdb_file,
#                        "-user", "tmp$no$such$user$4889",
#                        "-n", "-i", isql_cmd.name ],
#                      stdout=isql_log,
#                      stderr=subprocess.STDOUT
#                    )
#
#      # do NOT remove this delay:
#      time.sleep(5)
#
#      p_isql.terminate()
#      flush_and_close( isql_log )
#
#      #####################################################################
#
#      # Stop trace session:
#
#      trc_lst=open(trc_lst.name, "a")
#      trc_lst.seek(0,2)
#      subprocess.call([ context['fbsvcmgr_path'], "localhost:service_mgr",
#                        "action_trace_stop","trc_id",trcssn],
#                        stdout=trc_lst, stderr=subprocess.STDOUT
#                     )
#      flush_and_close( trc_lst )
#
#      p_svcmgr.terminate()
#      flush_and_close( trc_log )
#
#      # do NOT remove this delay:
#      time.sleep(2)
#
#      #####################################################################
#
#      # Output logs:
#
#      i=0
#      with open( trc_log.name,'r') as f:
#          for line in f:
#              if ') EXECUTE_STATEMENT_FINISH' in line:
#                 i=1
#              if i==1 and '1 records fetched' in line:
#                 i=2
#                 print("OK: found text in trace related to EMBEDDED connect.")
#                 break
#
#      if not i==2:
#          print("FAILED to found text in trace related to EMBEDDED connect.")
#
#      if os.path.getsize(isql_log.name) == 0:
#          print("FAILED to print log from EMBEDDED connect: log is EMPTY.")
#      else:
#          with open( isql_log.name,'r') as f:
#              print(f.read())
#          f.close()
#
#
#  # do NOT remove this pause otherwise log of trace will not be enable for deletion and test will finish with
#  # Exception raised while executing Python test script. exception: WindowsError: 32
#
#  # On WI-V3.0.0.31948 final output was:
#  # FAILED to found text in trace related to EMBEDDED connect.
#  # FAILED to print log from EMBEDDED connect: log is EMPTY.
#
#  #####################################################################
#
#  # Cleanup:
#  time.sleep(1)
#  cleanup( (trc_lst, trc_cfg, trc_log,isql_cmd, isql_log) )
#
#
#---

act_1 = python_act('db_1', substitutions=substitutions_1)

expected_stdout_1 = """
     OK: found text in trace related to EMBEDDED connect.
     CONNECTION_PROTOCOL             internal
     CONNECTION_PROCESS              internal
     CONNECTION_REMOTE_PID           internal
     AUTH_METHOD                     User name in DPB
     Records affected: 1
"""

def trace_session(act: Action, b: Barrier):
    cfg30 = ['# Trace config, format for 3.0. Generated auto, do not edit!',
             f'database=%[\\\\/]{act.db.db_path.name}',
             '{',
             '  enabled = true',
             '  time_threshold = 0',
             '  log_initfini = false',
             '  log_errors = true',
             '  log_statement_finish = true',
             '}']
    with act.connect_server() as srv:
        srv.trace.start(config='\n'.join(cfg30))
        b.wait()
        for line in srv:
            print(line)

@pytest.mark.version('>=3.0')
def test_1(act_1: Action, capsys):
    b = Barrier(2)
    trace_thread = Thread(target=trace_session, args=[act_1, b])
    trace_thread.start()
    b.wait()
    isq_script = """
    set list on;
    set count on;
    select
        iif(a.mon$remote_protocol is null, 'internal', 'remote') as connection_protocol,
        iif(a.mon$remote_process is null,  'internal', 'remote') as connection_process,
        iif(a.mon$remote_pid     is null,  'internal', 'remote') as connection_remote_pid,
        a.mon$auth_method as auth_method -- should be: 'User name in DPB'
    from rdb$database r
    left join mon$attachments a on a.mon$attachment_id = current_connection and a.mon$system_flag = 0;
    commit;
    """
    act_1.isql(switches=['-n', '-user', 'tmp$no$such$user$4889', str(act_1.db.db_path)],
               connect_db=False, input=isq_script)
    output = act_1.stdout
    with act_1.connect_server() as srv:
        for session in list(srv.trace.sessions.keys()):
            srv.trace.stop(session_id=session)
        trace_thread.join(1.0)
        if trace_thread.is_alive():
            pytest.fail('Trace thread still alive')
    trace_log = capsys.readouterr().out
    #
    # Process logs
    i = 0
    for line in trace_log.splitlines():
        if ') EXECUTE_STATEMENT_FINISH' in line:
            i = 1
        if i == 1 and '1 records fetched' in line:
            i = 2
            print("OK: found text in trace related to EMBEDDED connect.")
            break
    if not i == 2:
        print("FAILED to found text in trace related to EMBEDDED connect.")
    print(output if output else "FAILED to print log from EMBEDDED connect: log is EMPTY.")
    # Check
    act_1.expected_stdout = expected_stdout_1
    act_1.stdout = capsys.readouterr().out
    assert act_1.clean_stdout == act_1.clean_expected_stdout
