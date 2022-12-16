#coding:utf-8

"""
ID:          job.create-04
TITLE:       CREATE job
DESCRIPTION: Create job with incorrect number of schedule parameters
FBTEST:      /----none----/
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
CREATE JOB TEST_JOB
'*'
COMMAND 'echo 1';

CREATE JOB TEST_JOB
'* *'
COMMAND 'echo 1';

CREATE JOB TEST_JOB
'* * *'
COMMAND 'echo 1';

CREATE JOB TEST_JOB
'* * * *'
COMMAND 'echo 1';
"""

act = isql_act('db', test_script)

expected_stderror = """
Statement failed, SQLSTATE = 42000
unsuccessful metadata update
-CREATE JOB TEST_JOB failed
-badly formed hours in schedule string

Statement failed, SQLSTATE = 42000
unsuccessful metadata update
-CREATE JOB TEST_JOB failed
-badly formed days in schedule string

Statement failed, SQLSTATE = 42000
unsuccessful metadata update
-CREATE JOB TEST_JOB failed
-badly formed months in schedule string

Statement failed, SQLSTATE = 42000
unsuccessful metadata update
-CREATE JOB TEST_JOB failed
-badly formed week days in schedule string
"""

@pytest.mark.version('>=5.0')
def test_1(act: Action):
    act.expected_stderr = expected_stderror
    act.execute()
    assert act.clean_stderr == act.clean_expected_stderr
