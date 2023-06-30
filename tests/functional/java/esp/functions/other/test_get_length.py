#coding:utf-8

"""
ID:          java.esp.functions.other.get-length
TITLE:       External function gets string length
DESCRIPTION: 
FBTEST:      functional.java.esp.functions.other.get_length
"""

import pytest
from firebird.qa import *

init_script = """
create function test_1(i varchar(10)) 
returns INTEGER
external name 'esp.TestFunction.getLength(byte[])' 
engine java;
commit;
"""

db = db_factory(init=init_script)

test_script = """

SELECT test_1('test') FROM RDB$DATABASE;
SELECT test_1(null) FROM RDB$DATABASE;
"""

act = isql_act('db', test_script)

expected_stdout = """        
TEST_1
============
4
TEST_1
============
<null>
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
