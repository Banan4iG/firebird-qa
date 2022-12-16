#coding:utf-8

"""
ID:          job.create-03
TITLE:       CREATE job
DESCRIPTION: Create job with incorrect position for schedule parameters
FBTEST:      /----none----/
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
CREATE JOB TEST_JOB
ACTIVE
'* * * * *'
COMMAND 'echo 1';
"""

act = isql_act('db', test_script)

expected_stderror = """
Statement failed, SQLSTATE = 42000
Dynamic SQL Error
-SQL error code = -104
-Token unknown - line 2, column 1
-ACTIVE
"""

@pytest.mark.version('>=5.0')
def test_1(act: Action):
    act.expected_stderr = expected_stderror
    act.execute()
    assert act.clean_stderr == act.clean_expected_stderr
