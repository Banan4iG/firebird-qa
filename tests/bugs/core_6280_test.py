#coding:utf-8
#
# id:           bugs.core_6280
# title:        MERGE statement loses parameters in WHEN (NOT) MATCHED clause that will never be matched, crashes server in some situations
# decription:   
#                   Confirmed crash on WI-V3.0.5.33220, WI-T4.0.0.1871 - but only when run MERGE statements with parameters from Python. NO crash when run it from ISQL.
#                   No crash on 4.0.0.1881, but message "No SQLDA for input values provided" will raise for any number of input parameters: 2 or 3.
#                   18.04.2020: checked on 3.0.6.33288. Reduced minimal allowed version to 3.0.6.
#                
# tracker_id:   CORE-6280
# min_versions: ['3.0.6']
# versions:     3.0.6
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 3.0.6
# resources: None

substitutions_1 = []

init_script_1 = """
    recreate table t(i int not null primary key, j int);
  """

db_1 = db_factory(sql_dialect=3, init=init_script_1)

# test_script_1
#---
# 
#  cur=db_conn.cursor()
#  stm='''
#      merge into t
#      using (select 1 x from rdb$database) on 1 = 1
#      when matched then
#          update set j = ?
#      when matched and i = ? then
#          delete
#      when not matched then
#          insert (i, j) values (1, ?)
#  '''
#  
#  try:
#      cur.execute( stm ) (1,2,)
#      # cur.execute( stm ) (1,2,3,) -- also leads to "No SQLDA for input values provided"
#  except Exception as e:
#      print(e[0])
#  finally:
#      cur.close()
#      db_conn.close()
#  
#    
#---
#act_1 = python_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    Error while executing SQL statement:
    - SQLCODE: -902
    - Dynamic SQL Error
    - SQLDA error
    - No SQLDA for input values provided
  """

@pytest.mark.version('>=3.0.6')
@pytest.mark.xfail
def test_1(db_1):
    pytest.fail("Test not IMPLEMENTED")


