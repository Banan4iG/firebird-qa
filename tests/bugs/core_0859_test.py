#coding:utf-8
#
# id:           bugs.core_0859
# title:        Sorting is allowed for blobs and arrays
# decription:   This one is supposed to fail for now, as we restored the legacy behavior until we're able to implement DISTINCT for blobs properly
# tracker_id:   CORE-859
# min_versions: []
# versions:     9.1
# qmid:         bugs.core_859

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 9.1
# resources: None

substitutions_1 = []

init_script_1 = """create table t (i integer, b blob sub_type text, a integer [5]);
"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

# test_script_1
#---
# c = db_conn.cursor()
#  try:
#    c.prep('select * from t order by b')
#  except:
#    pass
#  else:
#    print ('Test Failed in case 1')
#  
#  try:
#    c.prep('select * from t order by a')
#  except:
#    pass
#  else:
#    print ('Test Failed in case 2')
#  
#  try:
#    c.prep('select b, count(*) from t group by b')
#  except:
#    pass
#  else:
#    print ('Test Failed in case 3')
#  
#  try:
#    c.prep('select a, count(*) from t group by a')
#  except:
#    pass
#  else:
#    print ('Test Failed in case 4')
#  
#  
#---
#act_1 = python_act('db_1', test_script_1, substitutions=substitutions_1)


@pytest.mark.version('>=9.1')
@pytest.mark.xfail
def test_1(db_1):
    pytest.fail("Test not IMPLEMENTED")


