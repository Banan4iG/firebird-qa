#coding:utf-8

"""
ID:          java.esp.procedures.ddl-operators.create-or-alter-2
TITLE:       Testing CREATE OR ALTER operator for external procedure when procedure is not created
DESCRIPTION: 
FBTEST:      functional.java.esp.procedures.ddl_operators.create_or_alter_2
"""

import pytest
from firebird.qa import *

init_script = """
 
CREATE TABLE TEST_TABLE (F_DOUBLE DOUBLE PRECISION);
commit; 

insert into test_table values (234);
 
create or alter procedure test(i double precision) 
external name 'esp.TestProcedure.doubleInAlter(double)'
engine java;
commit;

"""

db = db_factory(init=init_script)

test_script = """

execute procedure test(0);
commit;

SELECT F_DOUBLE FROM TEST_TABLE;
commit;
"""

act = isql_act('db', test_script, substitutions=[('\\.00000(0)*', '.000000000000000')])

expected_stdout = """  
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
