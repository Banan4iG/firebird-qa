#coding:utf-8

"""
ID:          job.drop-01
TITLE:       DROP job
DESCRIPTION: Drop existing job  
FBTEST:      /----none----/
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
CREATE JOB TEST_JOB 
'* * * * *'
COMMAND 'echo 1';
commit;
select cast(RDB$JOB_NAME as VARCHAR(20)) as JOB_NAME from RDB$JOBS;
drop JOB TEST_JOB;
commit;
select cast(RDB$JOB_NAME as VARCHAR(20)) as JOB_NAME from RDB$JOBS;
"""

act = isql_act('db', test_script)

expected_stdout = """
JOB_NAME             
==================== 
TEST_JOB
"""

@pytest.mark.version('>=5.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
