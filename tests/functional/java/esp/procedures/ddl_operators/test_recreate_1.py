#coding:utf-8

"""
ID:          java.esp.procedures.ddl-operators.recreate-1
TITLE:       Testing RECREATE operator for external procedure when procedure is not created
DESCRIPTION: 
FBTEST:      functional.java.esp.procedures.ddl_operators.recreate_1
"""

import pytest
from firebird.qa import *

init_script = """
 
CREATE TABLE TEST_TABLE (F_DOUBLE DOUBLE PRECISION);
commit; 

insert into test_table values(10000);
 
recreate procedure test(i double precision) 
external name 'esp.TestProcedure.doubleInAlter(double)'
engine java;
commit;

"""

db = db_factory(init=init_script)

test_script = """

execute procedure test(-9999);
commit;

SELECT F_DOUBLE FROM TEST_TABLE;
commit;
"""

act = isql_act('db', test_script)

expected_stdout = """  
F_DOUBLE
=======================
-9999.000000000000
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
