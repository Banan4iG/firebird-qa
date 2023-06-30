#coding:utf-8

"""
ID:          java.esp.functions.type-compatibility.lang-integer-extreme
TITLE:       External function call with extreme small and extreme big integer input parameter
DESCRIPTION: 
FBTEST:      functional.java.esp.functions.type_compatibility.lang_integer_extreme
"""

import pytest
from firebird.qa import *

init_script = """
create function test(i integer)
returns integer
external name 'esp.TestFunction.integerInOut(Integer)' 
engine java;
commit;
"""

db = db_factory(init=init_script)

test_script = """
SELECT TEST(-2147483648) FROM RDB$DATABASE;
SELECT TEST(2147483647) FROM RDB$DATABASE;
"""

act = isql_act('db', test_script)

expected_stdout = """        
TEST
============
-2147483648
TEST
============
2147483647
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
