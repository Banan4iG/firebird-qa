#coding:utf-8
#
# id:           bugs.core_0001
# title:        FBserver shutsdown when a user password is attempted to be modified to a empty string
# decription:   
# tracker_id:   CORE-0001
# min_versions: ['2.5.0']
# versions:     3.0
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 3.0
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """
    create or alter user tmp$c0001 password '123';
    commit;
    alter user tmp$c0001 password '';
    commit;
    drop user tmp$c0001;
    commit;
  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stderr_1 = """
    Statement failed, SQLSTATE = 42000
    unsuccessful metadata update
    -ALTER USER TMP$C0001 failed
    -Password should not be empty string
  """

@pytest.mark.version('>=3.0')
def test_1(act_1: Action):
    act_1.expected_stderr = expected_stderr_1
    act_1.execute()
    assert act_1.clean_expected_stderr == act_1.clean_stderr

