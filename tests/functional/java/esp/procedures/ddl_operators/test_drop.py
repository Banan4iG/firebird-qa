#coding:utf-8

"""
ID:          java.esp.procedures.ddl-operators.drop
TITLE:       Testing DROP operator for external procedure
DESCRIPTION: 
FBTEST:      functional.java.esp.procedures.ddl_operators.drop
"""

import pytest
from firebird.qa import *

init_script = """
 
CREATE TABLE TEST_TABLE (F_DOUBLE DOUBLE PRECISION);
commit;
 
create procedure test(i double precision) 
external name 'esp.TestProcedure.doubleIn(double)'
engine java;
commit;
"""

db = db_factory(init=init_script)

test_script = """
execute procedure test(23.09);
commit;

SELECT F_DOUBLE FROM TEST_TABLE;
commit;

drop procedure test;
commit;

execute procedure test(34);
commit;

SELECT F_DOUBLE FROM TEST_TABLE;
"""

act = isql_act('db', test_script)

expected_stdout = """                   
F_DOUBLE
=======================
23.09000000000000
F_DOUBLE
=======================
23.09000000000000
"""

expected_stderr = """
Statement failed, SQLSTATE = 42000
Dynamic SQL Error
-SQL error code = -204
-Procedure unknown
-TEST
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.expected_stderr = expected_stderr
    act.execute()
    assert (act.clean_stdout == act.clean_expected_stdout and
            act.clean_stderr == act.clean_expected_stderr)
