#coding:utf-8

"""
ID:          job.create-07
TITLE:       CREATE job
DESCRIPTION: Create job with incorrect SQL command
FBTEST:      /----none----/
"""

import pytest
from firebird.qa import *

db = db_factory()

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
"""

act = isql_act('db', test_script)

expected_stderr = """
Statement failed, SQLSTATE = 42S02
unsuccessful metadata update
-CREATE JOB TEST_JOB failed
-Dynamic SQL Error
-SQL error code = -204
-Table unknown
-TB
-At line 5, column 13
"""

@pytest.mark.version('>=5.0')
def test_1(act: Action):
    act.expected_stderr  = expected_stderr 
    act.execute()
    assert act.clean_stderr  == act.clean_expected_stderr 
