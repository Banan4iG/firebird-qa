#coding:utf-8

"""
ID:          java.esp.procedures.proc-from.psqlproc
TITLE:       External procedure call from PSQL procedure
DESCRIPTION: 
FBTEST:      functional.java.esp.procedures.proc_from.psqlproc
"""

import pytest
from firebird.qa import *

init_script = """
CREATE TABLE TEST_TABLE(F_BIGINT BIGINT);
commit;

CREATE OR ALTER PROCEDURE TEST(B BIGINT)
EXTERNAL NAME 'esp.TestProcedure.longIn(long)' 
ENGINE JAVA;
commit;

SET TERM ^ ;
CREATE OR ALTER PROCEDURE TEST_PSQL_PROC(B BIGINT)
AS
BEGIN
  EXECUTE PROCEDURE TEST(B);
END^
SET TERM ; ^
commit;
"""

db = db_factory(init=init_script)

test_script = """
EXECUTE PROCEDURE TEST_PSQL_PROC(-1000000000);
commit;

SELECT F_BIGINT FROM TEST_TABLE;
"""

act = isql_act('db', test_script)

expected_stdout = """             
F_BIGINT
=====================
-1000000000
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
