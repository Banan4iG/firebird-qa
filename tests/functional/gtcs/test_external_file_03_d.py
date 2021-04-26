#coding:utf-8
#
# id:           functional.gtcs.external_file_03_d
# title:        GTCS/tests/external-file-03-d. Test for external table with field of SMALLINT datatype
# decription:   
#               	Original test see in:
#                       https://github.com/FirebirdSQL/fbtcs/blob/master/GTCS/tests/EXT_REL_0_3_D.script
#                   Checked on: 4.0.0.2240; 3.0.7.33380
#                
# tracker_id:   
# min_versions: ['3.0']
# versions:     3.0
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 3.0
# resources: None

substitutions_1 = [('[ \t]+', ' ')]

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
#  tmp_file = os.path.join(context['temp_directory'],'tmp_ext_03_d.tmp')
#  if os.path.isfile( tmp_file):
#       os.remove( tmp_file )
#  
#  this_fdb = db_conn.database_name
#  
#  sql_cmd='''
#      connect 'localhost:%(this_fdb)s' user '%(user_name)s' password '%(user_password)s';
#      create table ext_table external file '%(tmp_file)s' (f01 smallint);
#      commit;
#      insert into ext_table (f01) values ( 32767);
#      insert into ext_table (f01) values (-32768);
#      insert into ext_table (f01) values (1);
#      insert into ext_table (f01) values (-1);
#      insert into ext_table (f01) values (0);
#      insert into ext_table (f01) values ( 32768);
#      insert into ext_table (f01) values ( -32769);
#      commit;
#      set list on;
#      set count on;
#      select * from ext_table order by f01;
#  ''' % dict(globals(), **locals())
#  
#  runProgram('isql', [ '-q' ], sql_cmd)
#  
#  f_sql_chk = open( os.path.join(context['temp_directory'],'tmp_ext_03_d.sql'), 'w')
#  f_sql_chk.write(sql_cmd)
#  f_sql_chk.close()
#  
#  time.sleep(1)
#  
#  os.remove(f_sql_chk.name)
#  os.remove( tmp_file )
#  
#    
#---
#act_1 = python_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    F01 -32768
    F01 -1
    F01 0
    F01 1
    F01 32767
    Records affected: 5
  """
expected_stderr_1 = """
    Statement failed, SQLSTATE = 22003
    arithmetic exception, numeric overflow, or string truncation
    -numeric value is out of range

    Statement failed, SQLSTATE = 22003
    arithmetic exception, numeric overflow, or string truncation
    -numeric value is out of range
  """

@pytest.mark.version('>=3.0')
@pytest.mark.xfail
def test_external_file_03_d_1(db_1):
    pytest.fail("Test not IMPLEMENTED")


