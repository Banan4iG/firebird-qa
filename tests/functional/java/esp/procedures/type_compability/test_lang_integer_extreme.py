#coding:utf-8

"""
ID:          java.esp.procedures.type-compability.lang-integer-extreme
TITLE:       External procedure call with extreme small and extreme big integer input parameter
DESCRIPTION: 
FBTEST:      functional.java.esp.procedures.type_compability.lang_integer_extreme
"""

import pytest
from firebird.qa import *

init_script = """
CREATE TABLE TEST_TABLE (F_INTEGER INTEGER);
commit;

create procedure test(i INTEGER) 
external name 'esp.TestProcedure.integerIn(Integer)'
engine java;
commit;

"""

db = db_factory(init=init_script)

test_script = """
 
EXECUTE PROCEDURE TEST(-2147483648);
EXECUTE PROCEDURE TEST(2147483647);
commit;

SELECT F_INTEGER FROM TEST_TABLE;
"""

act = isql_act('db', test_script)

expected_stdout = """
F_INTEGER
============
-2147483648
2147483647
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
