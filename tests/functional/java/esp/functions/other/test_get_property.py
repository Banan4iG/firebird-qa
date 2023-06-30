#coding:utf-8

"""
ID:          java.esp.functions.other.get-property
TITLE:       External function gets system property
DESCRIPTION: 
FBTEST:      functional.java.esp.functions.other.get_property
"""

import pytest
from firebird.qa import *

init_script = """
 
create function test(i VARCHAR(100)) 
returns VARCHAR(100)
external name 'esp.TestFunction.getProperty(String)'
engine java;
commit;
"""

db = db_factory(init=init_script)

test_script = """
set list on;
SELECT TEST('os.name') FROM RDB$DATABASE;
"""

act = isql_act('db', test_script, substitutions=[('TEST.*', 'TEST os_name')])

expected_stdout = """        
TEST os_name
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
