#coding:utf-8

"""
ID:          java.esp.functions.context.getpackagename-1
TITLE:       Testing of getPackageName method
DESCRIPTION: 
  For unpackaged function return null
FBTEST:      functional.java.esp.functions.context.getpackagename_1
"""

import pytest
from firebird.qa import *

# version: 3.0

init_script_1 = """
 
create function test
returns varchar(255)
external name 'esp.TestContext.F_getPackageName()'
engine java;
commit;
"""

db_1 = db_factory(init=init_script_1)

test_script_1 = """
select test() from rdb$database;
commit;
"""

act_1 = isql_act('db_1', test_script_1)

expected_stdout_1 = """                   
TEST
===============================================================================
<null>
"""

@pytest.mark.java
@pytest.mark.version('>=3.0,<4.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_stdout == act_1.clean_expected_stdout

# version: 4.0

init_script_2 = """

create function test
returns varchar(255)
external name 'esp.TestContext.F_getPackageName()'
engine java;
commit;
"""

db_2 = db_factory(init=init_script_2)

test_script_2 = """
select test() from rdb$database;
commit;
"""

act_2 = isql_act('db_2', test_script_2)

expected_stdout_2 = """
TEST
===============================================================================================================================================================================================================================================================
<null>
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
