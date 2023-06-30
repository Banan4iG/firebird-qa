#coding:utf-8

"""
ID:          java.esp.functions.type-compatibility.short-extreme
TITLE:       External function call with extreme small and extreme big smallint input parameter
DESCRIPTION: 
FBTEST:      functional.java.esp.functions.type_compatibility.short_extreme
"""

import pytest
from firebird.qa import *

init_script = """
create function test(i smallint) 
returns smallint
external name 'esp.TestFunction.shortInOut(short)'
engine java;
commit;
"""

db = db_factory(init=init_script)

test_script = """
SELECT TEST(32767) FROM RDB$DATABASE;
SELECT TEST(-32768) FROM RDB$DATABASE;
"""

act = isql_act('db', test_script)

expected_stdout = """   
TEST
=======
32767
TEST
=======
-32768
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
