#coding:utf-8
#
# id:           bugs.core_2268
# title:        GFIX causes BUGCHECK errors with non valid transaction numbers
# decription:
# tracker_id:   CORE-2268
# min_versions: []
# versions:     2.5
# qmid:         None

import pytest
from firebird.qa import db_factory, python_act, Action

# version: 2.5
# resources: None

substitutions_1 = [('^failed to reconnect to a transaction in database.*', '')]

init_script_1 = """"""

db_1 = db_factory(page_size=4096, sql_dialect=3, init=init_script_1)

# test_script_1
#---
# runProgram('gfix',['-user',user_name,'-pas',user_password,'-commit','1000000',dsn])
#
#---

act_1 = python_act('db_1', substitutions=substitutions_1)

expected_stderr_1 = """transaction is not in limbo
-transaction 1000000 is in an ill-defined state

"""

@pytest.mark.version('>=2.5')
def test_1(act_1: Action):
    act_1.expected_stderr = expected_stderr_1
    act_1.gfix(switches=['-commit', '1000000', act_1.db.dsn])
    assert act_1.clean_stderr == act_1.clean_expected_stderr


