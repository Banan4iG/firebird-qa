#coding:utf-8

"""
ID:          java.esp.functions.type-compatibility.lang-float-extreme
TITLE:       External function call with extreme small and extreme big float input parameter
DESCRIPTION: 
FBTEST:      functional.java.esp.functions.type_compatibility.lang_float_extreme
"""

import pytest
from firebird.qa import *

init_script = """
create function test(i float) 
returns float
external name 'esp.TestFunction.FloatInOut(Float)' 
engine java;
commit;
"""

db = db_factory(init=init_script)

test_script = """
SELECT TEST(1.175e-38) FROM RDB$DATABASE;
SELECT TEST(3.402e+38) FROM RDB$DATABASE;
SELECT TEST(-3.402e+38) FROM RDB$DATABASE;
"""

act = isql_act('db', test_script)

expected_stdout = """          
TEST
==============
1.1750000e-38

TEST
==============
3.4020000e+38

TEST
==============
-3.4020000e+38
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
