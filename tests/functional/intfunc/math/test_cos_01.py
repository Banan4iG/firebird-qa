#coding:utf-8
#
# id:           functional.intfunc.math.cos_01
# title:        New Built-in Functions, Firebird 2.1 : COS( <number>)
# decription:   test of COS
#               Returns the cosine of a number. The angle is specified in radians and returns a value in the range -1 to 1.
# tracker_id:   
# min_versions: []
# versions:     2.1
# qmid:         functional.intfunc.math.cos_01

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 2.1
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """select COS( 14) from rdb$database;
select COS( 0) from rdb$database;

"""

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """      COS
      =======================
      0.1367372182078336
      COS
      =======================
      1.000000000000000




"""

@pytest.mark.version('>=2.1')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout

