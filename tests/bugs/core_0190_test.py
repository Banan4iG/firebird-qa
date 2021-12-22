#coding:utf-8
#
# id:           bugs.core_0190
# title:        SYSDBA can grant non existent roles
# decription:
# tracker_id:   CORE-0190
# min_versions: ['2.5.0']
# versions:     3.0
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action, user_factory, User

# version: 3.0
# resources: None

substitutions_1 = [('Statement failed, SQLSTATE = HY000', ''), ('record not found for user:.*', '')]

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """
    grant no_such_role to tmp$c0196;
    commit;
    set count on;
    set list on;
    select * from rdb$user_privileges where rdb$user = upper('tmp$c0196') rows 1;
    commit;
"""

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    Records affected: 0
"""

expected_stderr_1 = """
    Statement failed, SQLSTATE = 28000
    unsuccessful metadata update
    -GRANT failed
    -SQL role NO_SUCH_ROLE does not exist
"""

user_1 = user_factory('db_1', name='tmp$c0196', password='123')

@pytest.mark.version('>=3.0')
def test_1(act_1: Action, user_1: User):
    act_1.expected_stdout = expected_stdout_1
    act_1.expected_stderr = expected_stderr_1
    act_1.execute()
    assert act_1.clean_stderr == act_1.clean_expected_stderr
    assert act_1.clean_stdout == act_1.clean_expected_stdout

