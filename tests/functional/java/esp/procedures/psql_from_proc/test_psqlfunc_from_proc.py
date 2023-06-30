#coding:utf-8

"""
ID:          java.esp.procedures.psql-from-proc.psqlfunc-from-proc
TITLE:       PSQL function call from external procedure
DESCRIPTION: 
FBTEST:      functional.java.esp.procedures.psql_from_proc.psqlfunc_from_proc
"""

import pytest
from firebird.qa import *

init_script = """
CREATE TABLE TEST_TABLE(F_VCHAR VARCHAR(50));
commit;

SET TERM ^ ;
CREATE FUNCTION GENERALFUNC
Returns varchar(50)
AS
BEGIN
    return 'string from generalfunc';
END^
SET TERM ; ^
commit;

CREATE OR ALTER PROCEDURE TEST
EXTERNAL NAME 'esp.TestProcedure.callPSQLfunction()' 
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
string from generalfunc
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
