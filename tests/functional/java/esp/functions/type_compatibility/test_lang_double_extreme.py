#coding:utf-8

"""
ID:          java.esp.functions.type-compatibility.lang-double-extreme
TITLE:       External function call with extreme small and extreme big double precision input parameter
DESCRIPTION: 
FBTEST:      functional.java.esp.functions.type_compatibility.lang_double_extreme
"""

import pytest
from firebird.qa import *

init_script = """
create function test(i double precision) 
returns double precision
external name 'esp.TestFunction.DoubleInOut(Double)'
engine java;
commit;
"""

db = db_factory(init=init_script)

test_script = """
SELECT TEST(2e-308) FROM RDB$DATABASE;
SELECT TEST(1.797e+308) FROM RDB$DATABASE;
SELECT TEST(-1.797e+308) FROM RDB$DATABASE;
"""

act = isql_act('db', test_script)

expected_stdout = """                    
TEST
=======================
2.000000000000000e-308
TEST
=======================
 1.797000000000000e+308
 TEST
=======================
-1.797000000000000e+308
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
