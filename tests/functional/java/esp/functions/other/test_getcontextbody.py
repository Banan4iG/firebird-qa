#coding:utf-8

"""
ID:          java.esp.functions.other.getcontextbody
TITLE:       External function invokes method getBody
DESCRIPTION: 
FBTEST:      functional.java.esp.functions.other.getcontextbody
"""

import pytest
from firebird.qa import *

# version: 3.0

init_script_1 = """
 
create function test() 
returns varchar(100)
external name 'esp.TestFunction.getContextBody()'
engine java;
commit;

"""

db_1 = db_factory(init=init_script_1)

test_script_1 = """
SELECT TEST() FROM RDB$DATABASE;
"""

act_1 = isql_act('db_1', test_script_1)

expected_stdout_1 = """    
	
	
TEST
===============================================================================
"""

@pytest.mark.java
@pytest.mark.version('>=3.0,<4.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_stdout == act_1.clean_expected_stdout

# version: 4.0

init_script_2 = """

create function test()
returns varchar(100)
external name 'esp.TestFunction.getContextBody()'
engine java;
commit;

"""

db_2 = db_factory(init=init_script_2)

test_script_2 = """
SELECT TEST() FROM RDB$DATABASE;
"""

act_2 = isql_act('db_2', test_script_2)

expected_stdout_2 = """


TEST
====================================================================================================
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
