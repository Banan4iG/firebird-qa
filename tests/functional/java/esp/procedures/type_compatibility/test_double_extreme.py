#coding:utf-8

"""
ID:          java.esp.procedures.type-compatibility.double-extreme
TITLE:       External procedure call with extreme small and extreme big double precision input parameter
DESCRIPTION: 
FBTEST:      functional.java.esp.procedures.type_compatibility.double_extreme
"""

import pytest
from firebird.qa import *

init_script = """
CREATE TABLE TEST_TABLE (F_DOUBLE DOUBLE PRECISION);
commit; 
 
create procedure test(i DOUBLE PRECISION) 
external name 'esp.TestProcedure.doubleIn(double)'
engine java;
commit;

"""

db = db_factory(init=init_script)

test_script = """
EXECUTE PROCEDURE TEST(2e-308);
EXECUTE PROCEDURE TEST(1.797e+308);
EXECUTE PROCEDURE TEST(-1.797e+308);
commit;

SELECT F_DOUBLE FROM TEST_TABLE;
"""

act = isql_act('db', test_script)

expected_stdout = """                    
F_DOUBLE
=======================
2.000000000000000e-308
1.797000000000000e+308
-1.797000000000000e+308
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
