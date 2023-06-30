#coding:utf-8

"""
ID:          java.esp.functions.other.getinternalcontext
TITLE:       External function invokes get method in org.firebirdsql.fbjava.impl.InternalContext class
DESCRIPTION: 
FBTEST:      functional.java.esp.functions.other.getinternalcontext
"""

import pytest
from firebird.qa import *

init_script = """
 
create function test() 
returns integer
external name 'esp.TestFunction.getInternalContext()'
engine java;
commit;

"""

db = db_factory(init=init_script)

test_script = """
SELECT TEST() FROM RDB$DATABASE;
"""

act = isql_act('db', test_script)

expected_stdout = """    
	
TEST
============
0
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
