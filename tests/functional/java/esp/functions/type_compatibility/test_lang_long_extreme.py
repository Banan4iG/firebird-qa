#coding:utf-8

"""
ID:          java.esp.functions.type-compatibility.lang-long-extreme
TITLE:       External function call with extreme small and extreme big bigint input parameter
DESCRIPTION: 
FBTEST:      functional.java.esp.functions.type_compatibility.lang_long_extreme
"""

import pytest
from firebird.qa import *

init_script = """
create function test (i bigint) 
returns bigint
external name 'esp.TestFunction.LongInOut(Long)'
engine java;
commit;
"""

db = db_factory(init=init_script)

test_script = """
SELECT TEST(-9223372036854775808) FROM RDB$DATABASE;
SELECT TEST(9223372036854775807) FROM RDB$DATABASE;
"""

act = isql_act('db', test_script)

expected_stdout = """                 
TEST
=====================
-9223372036854775808
TEST
=====================
9223372036854775807
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
