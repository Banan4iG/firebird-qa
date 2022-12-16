#coding:utf-8

"""
ID:          job.create-01
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
set term ^;
CREATE JOB TEST_JOB
'* * * * *' 
AS 
BEGIN
INSERT INTO tb VALUES(1);
END^
set term ;^
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
BEGIN
INSERT INTO tb VALUES(1);
END
RDB$JOB_BLR                     0:2
BLOB display set to subtype 1. This BLOB: subtype = 0
RDB$DESCRIPTION                 <null>
RDB$OWNER_NAME                  SYSDBA
RDB$JOB_INACTIVE                0
RDB$JOB_TYPE                    0
RDB$JOB_SCHEDULE                * * * * *
RDB$START_DATE                  <null>
RDB$END_DATE                    <null>
RDB$DATABASE test.fdb
"""

@pytest.mark.version('>=5.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
