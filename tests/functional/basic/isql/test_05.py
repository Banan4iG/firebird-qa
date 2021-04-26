#coding:utf-8
#
# id:           functional.basic.isql.isql_05
# title:        ISQL should be able to process single statement with length up to 10*1024*1024 chars
# decription:   
#                  Source sample see in CORE-5382 ("Incorrect processing (truncation) of SQL statement with length 10MB+1").
#                  Test prepares script with two SELECT statements: 
#                  One of them has length EXACTLY equal to 10*1024*1024 chars (excluding final ';'), another length = 10Mb + 1.
#                  First statement should be executed OK, second should fail.
#                  Checked on WI-V3.0.2.32625, WI-T4.0.0.440
#               
#                  PS. Best place of this test in functional/basic/isql/ folder rather than in 'bugs' one.
#                
# tracker_id:   
# min_versions: ['3.0']
# versions:     3.0
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 3.0
# resources: None

substitutions_1 = [('After line .*', ''), ('-At line.*', ''), ('At line.*', '')]

init_script_1 = """
    recreate table dua(i int);
    insert into dua(i) values(1);
    commit;
  """

db_1 = db_factory(sql_dialect=3, init=init_script_1)

# test_script_1
#---
# import os
#  import subprocess
#  import fdb
#  
#  db_conn.close()
#  
#  dml_pref='select /*'
#  dml_suff='*/ %s i from rdb$database;'
#  
#  # prepare DB for testing: create lot of tables:
#  ###############################################
#  f_work_sql=open( os.path.join(context['temp_directory'],'tmp_work_5382.sql'), 'w')
#  f_work_sql.write('set list on;' + os.linesep)
#  f_work_sql.write( (dml_pref.ljust(10485729,'-') + dml_suff) % (10485760) )
#  f_work_sql.write( (dml_pref.ljust(10485730,'-') + dml_suff) % (10485761) )
#  f_work_sql.close()
#  
#  runProgram('isql',[dsn,'-user',user_name,'-pas',user_password,'-i',f_work_sql.name])
#  os.remove(f_work_sql.name)
#    
#---
#act_1 = python_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
      I                               10485760
  """
expected_stderr_1 = """
    Statement failed, SQLSTATE = 54000
    Dynamic SQL Error
    -SQL error code = -902
    -Implementation limit exceeded
    -SQL statement is too long. Maximum size is 10485760 bytes.
  """

@pytest.mark.version('>=3.0')
@pytest.mark.xfail
def test_isql_05_1(db_1):
    pytest.fail("Test not IMPLEMENTED")


