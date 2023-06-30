#coding:utf-8

"""
ID:          java.esp.functions.other.get-int
TITLE:       External function gets number from request
DESCRIPTION: 
FBTEST:      functional.java.esp.functions.other.get_int
"""

import pytest
from firebird.qa import *

init_script = """
create function test_1() 
returns INTEGER
external name 'esp.TestFunction.getInt()' 
engine java;
commit;
"""

db = db_factory(init=init_script)

test_script = """

SELECT test_1() FROM RDB$DATABASE;
"""

act = isql_act('db', test_script)

expected_stdout = """        
TEST_1
============
22
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
