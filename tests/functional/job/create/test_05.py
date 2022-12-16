#coding:utf-8

"""
ID:          job.create-05
TITLE:       CREATE job
DESCRIPTION: Create job with different posible values of schedule parameters
FBTEST:      /----none----/
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
CREATE JOB TEST_JOB
'2,5 */1 3-5/1 * *'
COMMAND 'echo 1';
select cast(RDB$JOB_SCHEDULE as VARCHAR(20)) as JOB_SCHEDULE from RDB$JOBS;
drop job TEST_JOB;
"""

act = isql_act('db', test_script)

expected_stdout = """
JOB_SCHEDULE
====================
2,5 */1 3-5/1 * *
"""

@pytest.mark.version('>=5.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
