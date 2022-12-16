#coding:utf-8

"""
ID:          job.drop-02
TITLE:       DROP job
DESCRIPTION: Drop not existing job  
FBTEST:      /----none----/
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
drop JOB TEST_JOB;
"""

act = isql_act('db', test_script)

expected_stderr = """
Statement failed, SQLSTATE = 42000
Job TEST_JOB not found
"""

@pytest.mark.version('>=5.0')
def test_1(act: Action):
    act.expected_stderr = expected_stderr
    act.execute()
    assert act.clean_stderr == act.clean_expected_stderr
