#coding:utf-8
#
# id:           bugs.gh_6709
# title:        gbak discards replica mode [CORE6478]
# decription:
#                   https://github.com/FirebirdSQL/firebird/issues/6709
#
#                   Confirmed bug on 4.0.0.2353: 'replica' flag was not preserved after restoring DB.
#                   Checked on: 4.0.1.2624, 5.0.0.244 -- all OK.
#
# tracker_id:
# min_versions: ['4.0']
# versions:     4.0
# qmid:         None

import pytest
from firebird.qa import db_factory, python_act, Action

# version: 4.0
# resources: None

substitutions_1 = [('[ \t]+', ' ')]

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

# test_script_1
#---
#
#  import os
#  import shutil
#  import subprocess
#
#  os.environ["ISC_USER"] = user_name
#  os.environ["ISC_PASSWORD"] = user_password
#
#  this_fdb=db_conn.database_name
#  db_conn.close()
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
#  test_fdb=os.path.join(context['temp_directory'],'tmp_gh_6709.source.fdb')
#  test_fbk=os.path.join(context['temp_directory'],'tmp_gh_6709.fbk')
#  test_res=os.path.join(context['temp_directory'],'tmp_gh_6709.restored')
#
#  for r_mode in ('read_only', 'read_write'):
#      cleanup( (test_fdb, test_res) )
#      shutil.copy2( this_fdb, test_fdb )
#      runProgram('gfix', [ 'localhost:' + test_fdb, '-replica', r_mode ] )
#      runProgram('isql', [ 'localhost:' + test_fdb ], '''set list on; select rdb$get_context('SYSTEM', 'REPLICA_MODE') as "Result of gfix -replica %(r_mode)s:" from rdb$database;''' % locals() )
#      runProgram('gbak', [ '-b', 'localhost:' + test_fdb, test_fbk ] )
#      runProgram('gbak', [ '-c', '-m', test_fbk, 'localhost:' + test_res ] )
#      runProgram('isql', [ 'localhost:' + test_res ], '''set list on; select rdb$get_context('SYSTEM', 'REPLICA_MODE') as "Result of backup/restore for %(r_mode)s:" from rdb$database;''' % locals() )
#
#  cleanup( (test_fdb, test_fbk, test_res) )
#
#---
act_1 = python_act('db_1', substitutions=substitutions_1)

expected_stdout_1 = """
    Result of gfix -replica read_only:       READ-ONLY
    Result of backup/restore for read_only:  READ-ONLY
    Result of gfix -replica read_write:      READ-WRITE
    Result of backup/restore for read_write: READ-WRITE
"""

@pytest.mark.skip('FIXME: Not IMPLEMENTED')
@pytest.mark.version('>=4.0')
def test_1(act_1: Action):
    pytest.fail("Not IMPLEMENTED")
