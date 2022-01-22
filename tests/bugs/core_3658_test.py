#coding:utf-8

"""
ID:          issue-4008
ISSUE:       4008
TITLE:       FBSVCMGR connects to server as OS user name rather than value of ISC_USER environment variable
DESCRIPTION:
NOTES:
[17.11.2021] pcisar
  Implementation is complicated, and IMHO not worth of realization
JIRA:        CORE-3658
"""

import pytest
from firebird.qa import *

db = db_factory()

act = python_act('db')

expected_stdout = """
Expected line found.
Expected line found.
Expected line found.
Expected line found.
"""

@pytest.mark.skip("Test fate to be determined")
@pytest.mark.version('>=3')
def test_1(act: Action):
    pytest.skip("Test not IMPLEMENTED")

# test_script_1
#---
# import os
#  import subprocess
#  from subprocess import Popen
#  import time
#  import re
#
#  os.environ["ISC_USER"] = user_name
#  os.environ["ISC_PASSWORD"] = user_password
#
#  # Obtain engine version:
#  engine = str(db_conn.engine_version) # convert to text because 'float' object has no attribute 'startswith'
#  db_file = db_conn.database_name
#  db_conn.close()
#
#  #---------------------------------------------
#
#  def flush_and_close(file_handle):
#      # https://docs.python.org/2/library/os.html#os.fsync
#      # If you're starting with a Python file object f,
#      # first do f.flush(), and
#      # then do os.fsync(f.fileno()), to ensure that all internal buffers associated with f are written to disk.
#      global os
#
#      file_handle.flush()
#      if file_handle.mode not in ('r', 'rb'):
#          # otherwise: "OSError: [Errno 9] Bad file descriptor"!
#          os.fsync(file_handle.fileno())
#      file_handle.close()
#
#  #--------------------------------------------
#
#  def cleanup( f_names_list ):
#      global os
#      for i in range(len( f_names_list )):
#         if os.path.isfile( f_names_list[i]):
#              os.remove( f_names_list[i] )
#              if os.path.isfile( f_names_list[i]):
#                  print('ERROR: can not remove file ' + f_names_list[i])
#
#  #--------------------------------------------
#
#  txt25 = '''# Trace config, format for 2.5. Generated auto, do not edit!
#  <services>
#     enabled true
#     log_services true
#    log_errors true
#  </services>
#  '''
#
#  # NOTES ABOUT TRACE CONFIG FOR 3.0:
#  # 1) Header contain clauses in different format vs FB 2.5: its header's data must be enclosed with '{' '}';
#  # 2) Name and value must be separated by EQUALITY sign ('=') in FB-3 trace.conf, otherwise we get runtime error:
#  #    element "<. . .>" have no attribute value set
#  txt30 = '''# Trace config, format for 2.5. Generated auto, do not edit!
#  services
#  {
#    enabled = true
#    log_services = true
#    log_errors = true
#  }
#  '''
#
#  f_trccfg=open( os.path.join(context['temp_directory'],'tmp_trace_3658.cfg'), 'w')
#  if engine.startswith('2.5'):
#      f_trccfg.write(txt25)
#  else:
#      f_trccfg.write(txt30)
#  flush_and_close( f_trccfg )
#
#
#  # ##############################################################
#  # S T A R T   T R A C E   i n   S E P A R A T E    P R O C E S S
#  # ##############################################################
#
#  f_trclog=open( os.path.join(context['temp_directory'],'tmp_trace_3658.log'), 'w')
#  p = Popen([ context['fbsvcmgr_path'], "localhost:service_mgr" , "action_trace_start" , "trc_cfg" , f_trccfg.name], stdout=f_trclog, stderr=subprocess.STDOUT)
#  time.sleep(2)
#
#  # ####################################################
#  # G E T  A C T I V E   T R A C E   S E S S I O N   I D
#  # ####################################################
#  # Save active trace session info into file for further parsing it and obtain session_id back (for stop):
#
#  f_trclst=open( os.path.join(context['temp_directory'],'tmp_trace_3658.lst'), 'w')
#  subprocess.call([context['fbsvcmgr_path'], "localhost:service_mgr", "action_trace_list"], stdout=f_trclst, stderr=subprocess.STDOUT)
#  flush_and_close( f_trclst )
#
#  # !!! DO NOT REMOVE THIS LINE !!!
#  time.sleep(1)
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
#
#  # ####################################################
#  # S E N D   R E Q U E S T    T R A C E   T O   S T O P
#  # ####################################################
#  fn_nul = open(os.devnull, 'w')
#  subprocess.call([context['fbsvcmgr_path'], "localhost:service_mgr", "action_trace_stop","trc_id", trcssn], stdout=fn_nul)
#  fn_nul.close()
#
#  # 23.02.2021. DELAY FOR AT LEAST 1 SECOND REQUIRED HERE!
#  # Otherwise trace log can remain empty.
#  time.sleep(1)
#
#  # Doc about Popen.terminate():
#  # https://docs.python.org/2/library/subprocess.html
#  # Stop the child. On Posix OSs the method sends SIGTERM to the child.
#  # On Windows the Win32 API function TerminateProcess() is called to stop the child.
#
#  # Doc about Win API TerminateProcess() function:
#  # https://msdn.microsoft.com/en-us/library/windows/desktop/ms686714%28v=vs.85%29.aspx
#  # The terminated process cannot exit until all pending I/O has been completed or canceled.
#  # TerminateProcess is ____asynchronous____; it initiates termination and returns immediately.
#  #                         ^^^^^^^^^^^^
#  p.terminate()
#  flush_and_close( f_trclog )
#
#  # Output log of trace for comparing it with expected.
#  # ::: NB ::: Content if trace log is converted to UPPER case in order to reduce change of mismatching with
#  # updated trace output in some future versions:
#
#  # Windows:
#  #     2.5.x: service_mgr, (Service 00000000007C9B88, SYSDBA, TCPv4:127.0.0.1/59583, C:\\FBsCin
#  bsvcmgr.exe:6888)
#  #     3.0.x: service_mgr, (Service 000000000818B140, SYSDBA, TCPv6:::1/59557, C:\\FBSS
#  bsvcmgr.exe:7044)
#  #     4.0.x: service_mgr, (Service 0000000010B51DC0, SYSDBA, TCPv6:::1/59569, C:\\FB SS
#  bsvcmgr.exe:5616)
#  # Linux:
#  #     service_mgr, (Service 0x7f46c4027c40, SYSDBA, TCPv4:127.0.0.1/51226, /var/tmp/fb40tmp/bin/fbsvcmgr:20947)
#
#  p=re.compile('service_mgr,[	 ]+\\(\\s*Service[	 ]+\\S+[,]?[	 ]+sysdba[,]?', re.IGNORECASE)
#  with open( f_trclog.name,'r') as f:
#      for line in f:
#          if p.search(line):
#              print('Expected line found.')
#
#  cleanup( [i.name for i in (f_trccfg, f_trclog, f_trclst) ] )
#
#
#---
