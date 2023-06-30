#coding:utf-8

"""
ID:          java.esp.procedures.psql-from-proc.psqltrigger-from-proc
TITLE:       PSQL trigger call from external procedure
DESCRIPTION: 
FBTEST:      functional.java.esp.procedures.psql_from_proc.psqltrigger_from_proc
"""

import pytest
from firebird.qa import *

init_script = """
CREATE TABLE TEST_TABLE(ID INTEGER, NAME VARCHAR(50));
commit;

SET TERM ^ ;
CREATE OR ALTER TRIGGER TEST_TRIGER 
FOR TEST_TABLE 
ACTIVE
BEFORE INSERT
AS
BEGIN
  IF (NEW.NAME IS NULL OR NEW.NAME = '') THEN
    NEW.NAME = 'name_from_trigger';
END^
SET TERM ; ^
commit;

CREATE OR ALTER PROCEDURE TEST
EXTERNAL NAME 'esp.TestProcedure.callPSQLtrigger()' 
ENGINE JAVA;
commit;
"""

db = db_factory(init=init_script)

test_script = """
EXECUTE PROCEDURE TEST;
commit;

SELECT * FROM TEST_TABLE;
"""

act = isql_act('db', test_script)

expected_stdout = """	
ID NAME
============ ==================================================
12 name_from_trigger
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
