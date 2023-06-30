#coding:utf-8

"""
ID:          java.esp.functions.context.getinputvalues
TITLE:       Testing of getObject method
DESCRIPTION: 
  Function gets values of input parameters through getObject method
FBTEST:      functional.java.esp.functions.context.getinputvalues
"""

import pytest
from firebird.qa import *

# version: 3.0

init_script_1 = """
 
create function test(i1 integer, i2 varchar(10), ts timestamp)
returns varchar(1000)
external name 'esp.TestContext.F_getInputValues()'
engine java;
commit;
"""

db_1 = db_factory(init=init_script_1)

test_script_1 = """
select test(324, 'hello', '10.12.1989 10:30') from rdb$database;
commit;
"""

act_1 = isql_act('db_1', test_script_1)

expected_stdout_1 = """  
TEST
===============================================================================
324
hello
1989-12-10 10:30:00.0
"""

@pytest.mark.java
@pytest.mark.version('>=3.0,<4.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_stdout == act_1.clean_expected_stdout

# version: 4.0

init_script_2 = """

create function test(i1 integer, i2 varchar(10), ts timestamp)
returns varchar(1000)
external name 'esp.TestContext.F_getInputValues()'
engine java;
commit;
"""

db_2 = db_factory(init=init_script_2)

test_script_2 = """
select test(324, 'hello', '10.12.1989 10:30') from rdb$database;
commit;
"""

act_2 = isql_act('db_2', test_script_2)

expected_stdout_2 = """
TEST
========================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
324
hello
1989-12-10 10:30:00.0
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
