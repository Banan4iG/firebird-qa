#coding:utf-8

"""
ID:          java.esp.procedures.psql-from-proc.psqlproc-from-proc
TITLE:       PSQL procedure call from external procedure
DESCRIPTION: 
FBTEST:      functional.java.esp.procedures.psql_from_proc.psqlproc_from_proc
"""

import pytest
from firebird.qa import *

init_script = """
CREATE TABLE TEST_TABLE(F_VCHAR VARCHAR(50));
commit;

SET TERM ^ ;
CREATE OR ALTER PROCEDURE GENERALSP 
AS
BEGIN
  INSERT INTO TEST_TABLE VALUES('ok');
END^
SET TERM ; ^
commit;

CREATE OR ALTER PROCEDURE TEST
EXTERNAL NAME 'esp.TestProcedure.callPSQLprocedure()' 
ENGINE JAVA;
commit;
"""

db = db_factory(init=init_script)

test_script = """
EXECUTE PROCEDURE TEST;
commit;

SELECT F_VCHAR FROM TEST_TABLE;
"""

act = isql_act('db', test_script)

expected_stdout = """
F_VCHAR
==================================================
ok
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
