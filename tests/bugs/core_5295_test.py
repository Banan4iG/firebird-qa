#coding:utf-8
#
# id:           bugs.core_5295
# title:        Validation could read after the end-of-file when handle multifile database
# decription:
#                  Reproduced error on WI-V3.0.1.32542 (SS/SC/CS) and WI-T4.0.0.258, WI-T4.0.0.267 (SS).
#                  Could NOT reproduce on WI-V2.5.6.27017 (SuperClassic).
#
#                  07.08.2016: removed dependency on 'employee'-  there is some strange reports about missing it.
#                  Instead of using existing 'employee', its .fbk was created (on 2.5.7), added it to fpt-repo/fbk
#                  folder and is restored here.
#
# tracker_id:   CORE-5295
# min_versions: ['2.5.6']
# versions:     2.5.6
# qmid:         None

import pytest
from pathlib import Path
from firebird.qa import db_factory, python_act, Action, temp_file

# version: 2.5.6
# resources: None

substitutions_1 = [('\t+', ' '), ('^((?!checked_size|Error|error).)*$', '')]

init_script_1 = """"""

db_1 = db_factory(from_backup='core5295.fbk', init=init_script_1)

# test_script_1
#---
#
#  import os
#  import time
#  import subprocess
#
#  os.environ["ISC_USER"] = user_name
#  os.environ["ISC_PASSWORD"] = user_password
#
#  fbk_file='$(DATABASE_LOCATION)tmp.core_5295.fbk'
#  fdb_tmp1='$(DATABASE_LOCATION)tmp.core_5295.1.tmp'
#  fdb_tmp2='$(DATABASE_LOCATION)tmp.core_5295.2.tmp'
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
#  cleanup( (fbk_file, fdb_tmp1, fdb_tmp2) )
#
#  runProgram('gbak',['-b', dsn, fbk_file])
#  runProgram('gbak',['-rep',fbk_file, 'localhost:'+fdb_tmp1, '100000', fdb_tmp2 ])
#
#  f_val_log=open( os.path.join(context['temp_directory'],'tmp_gfix_v_5295.log'), 'w')
#
#  # Only 'gfix -v' raised error. Online validation works fine:
#  ################
#  subprocess.call([context['gfix_path'], "-v", 'localhost:'+fdb_tmp1], stdout=f_val_log, stderr=subprocess.STDOUT)
#
#  flush_and_close( f_val_log )
#
#  #I/O error during "ReadFile" operation for file "<path>	mp.core_5295.fd1"
#  #-Error while trying to read from file
#  #-<localized message: EOF encountered>
#
#  # NB: because of localized text inside f_val_log we have to SKIP scanning this file line-by-line
#  # and only check that its size is ZERO.
#  # If size of validation is non-zero than it must be considered as error:
#
#  print("checked_size of validation log: " + str(os.path.getsize(f_val_log.name)) )
#  with open( f_val_log.name,'r') as f:
#      for line in f:
#          print('VALIDATION LOG: '+line)
#
#
#  # cleanup:
#  ##########
#  time.sleep(1)
#  cleanup( (f_val_log.name, fbk_file, fdb_tmp1, fdb_tmp2) )
#
#---

act_1 = python_act('db_1', substitutions=substitutions_1)

fbk_file = temp_file('tmp_core_5295.fbk')
fdb_file_1 = temp_file('tmp_core_5295-1.fdb')
fdb_file_2 = temp_file('tmp_core_5295-2.db1')

@pytest.mark.version('>=2.5.6')
def test_1(act_1: Action, fbk_file: Path, fdb_file_1: Path, fdb_file_2: Path):
    with act_1.connect_server() as srv:
        srv.database.backup(database=act_1.db.db_path, backup=fbk_file)
        srv.wait()
        srv.database.restore(backup=fbk_file,
                             database=[fdb_file_1, fdb_file_2],
                             db_file_pages=[100000])
        srv.wait()
    # Only 'gfix -v' raised error. Online validation works fine:
    act_1.gfix(switches=['-v', act_1.get_dsn(fdb_file_1)])
    assert act_1.clean_stdout == act_1.clean_expected_stdout
