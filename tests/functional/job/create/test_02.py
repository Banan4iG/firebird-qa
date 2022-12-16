#coding:utf-8

"""
ID:          job.create-02
TITLE:       CREATE job
DESCRIPTION:
FBTEST:      /----none----/
"""

import pytest
from firebird.qa import *

init_script = """
CREATE TABLE tb(id INT);
commit;
"""

db = db_factory(init=init_script)

test_script = """
CREATE JOB TEST_JOB
'1 2 3 4 5'
INACTIVE
START DATE '02.02.2000 00:00'
END DATE '02.02.2002 00:00' 
COMMAND 'echo 1';
commit;
set list;
select * from RDB$JOBS;
drop JOB TEST_JOB;
commit;
"""

act = isql_act('db', test_script, substitutions=[('RDB\\$DATABASE[ ]+\\S+', 'RDB$DATABASE test.fdb'),('RDB\\$JOB_ID[ ]+\\d+', 'RDB$JOB_ID ID')])

expected_stdout = """
RDB$JOB_NAME                    TEST_JOB
RDB$JOB_ID ID
RDB$JOB_SOURCE                  0:1
echo 1
RDB$JOB_BLR                     <null>
RDB$DESCRIPTION                 <null>
RDB$OWNER_NAME                  SYSDBA
RDB$JOB_INACTIVE                1
RDB$JOB_TYPE                    1
RDB$JOB_SCHEDULE                1 2 3 4 5
RDB$START_DATE                  2000-02-02 00:00:00.0000
RDB$END_DATE                    2002-02-02 00:00:00.0000
RDB$DATABASE test.fdb
"""

@pytest.mark.version('>=5.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
