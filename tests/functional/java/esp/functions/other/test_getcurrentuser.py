#coding:utf-8

"""
ID:          java.esp.functions.other.getcurrentuser
TITLE:       External function gets current user
DESCRIPTION: 
FBTEST:      functional.java.esp.functions.other.getcurrentuser
"""

import pytest
from firebird.qa import *

init_script = """
 
create function test(s varchar(100)) 
returns varchar(100)
external name 'esp.TestFunction.getCurrentUser(String)'
engine java;
commit;

"""

db = db_factory(init=init_script)

test_script = """
set list on;
SELECT TEST('jdbc:default:connection') FROM RDB$DATABASE;
"""

act = isql_act('db', test_script, substitutions=[('TEST.*', 'TEST user_name')])

expected_stdout = """    
	
	
TEST user_name

"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
