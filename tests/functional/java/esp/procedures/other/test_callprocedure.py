#coding:utf-8

"""
ID:          java.esp.procedures.other.callprocedure
TITLE:       PSQL procedure call from external procedure
DESCRIPTION: 
FBTEST:      functional.java.esp.procedures.other.callprocedure
"""

import pytest
from firebird.qa import *

# version: 3.0

init_script_1 = """
CREATE TABLE TEST_TABLE(F_VCHAR VARCHAR(50));
commit;


CREATE OR ALTER PROCEDURE GENERALSP
EXTERNAL NAME 'esp.TestProcedure.procWithoutParam()' 
ENGINE JAVA;
commit;


CREATE OR ALTER PROCEDURE TEST
EXTERNAL NAME 'esp.TestProcedure.callPSQLprocedure()' 
ENGINE JAVA;
commit;
"""

db_1 = db_factory(init=init_script_1)

test_script_1 = """
EXECUTE PROCEDURE TEST;
commit;

SELECT F_VCHAR FROM TEST_TABLE;
"""

act_1 = isql_act('db_1', test_script_1)

expected_stdout_1 = """
F_VCHAR
==================================================
test
"""

@pytest.mark.java
@pytest.mark.version('>=3.0,<4.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_stdout == act_1.clean_expected_stdout

# version: 4.0

init_script_2 = """
CREATE TABLE TEST_TABLE(F_VCHAR VARCHAR(50));
commit;


CREATE OR ALTER PROCEDURE GENERALSP
EXTERNAL NAME 'esp.TestProcedure.procWithoutParam()'
ENGINE JAVA;
commit;


CREATE OR ALTER PROCEDURE TEST
EXTERNAL NAME 'esp.TestProcedure.callPSQLprocedureERS()'
ENGINE JAVA;
commit;
"""

db_2 = db_factory(init=init_script_2)

test_script_2 = """
EXECUTE PROCEDURE TEST;
commit;

SELECT F_VCHAR FROM TEST_TABLE;
"""

act_2 = isql_act('db_2', test_script_2)

expected_stdout_2 = """
F_VCHAR
==================================================
test
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
