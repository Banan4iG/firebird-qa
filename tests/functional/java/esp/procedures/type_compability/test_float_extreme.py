#coding:utf-8

"""
ID:          java.esp.procedures.type-compability.float-extreme
TITLE:       External procedure call with extreme small and extreme big float input parameter
DESCRIPTION: 
FBTEST:      functional.java.esp.procedures.type_compability.float_extreme
"""

import pytest
from firebird.qa import *

init_script = """
CREATE TABLE TEST_TABLE (F_FLOAT FLOAT);
commit;


create procedure test(i FLOAT) 
external name 'esp.TestProcedure.floatIn(float)'
engine java;
commit;

"""

db = db_factory(init=init_script)

test_script = """
EXECUTE PROCEDURE TEST(1.175e-38);
EXECUTE PROCEDURE TEST(3.402e+38);
EXECUTE PROCEDURE TEST(-3.402e+38);
commit;


SELECT F_FLOAT FROM TEST_TABLE;
"""

act = isql_act('db', test_script)

expected_stdout = """
F_FLOAT
==============
1.1750000e-38
3.4020000e+38
-3.4020000e+38


"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
