#coding:utf-8

"""
ID:          java.esp.procedures.ddl-operators.alter
TITLE:       Testing ALTER operator for external procedure
DESCRIPTION: 
FBTEST:      functional.java.esp.procedures.ddl_operators.alter
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

alter procedure test(i double precision) 
external name 'esp.TestProcedure.doubleInAlter(double)'
engine java;
commit;

execute procedure test(0);
commit;

SELECT F_DOUBLE FROM TEST_TABLE;

"""

act = isql_act('db', test_script, substitutions=[('0.0000000000000000', '0.000000000000000')])

expected_stdout = """                   
F_DOUBLE
=======================
23.09000000000000
F_DOUBLE
=======================
0.000000000000000
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
