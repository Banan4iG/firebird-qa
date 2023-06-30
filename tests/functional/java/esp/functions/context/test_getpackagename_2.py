#coding:utf-8

"""
ID:          java.esp.functions.context.getpackagename-2
TITLE:       Testing of getPackageName method
DESCRIPTION: 
  Function gets the metadata package name that called it
FBTEST:      functional.java.esp.functions.context.getpackagename_2
"""

import pytest
from firebird.qa import *

# version: 3.0

init_script_1 = """
 
 set term !;
 create package test_pack
 as 
 begin
 function test returns varchar(255);
 end!
 
 create package body test_pack
 as 
 begin
 function test returns varchar(255)
 external name 'esp.TestContext.F_getPackageName()'
 engine java;
 end!
 
 set term ;!
 
"""

db_1 = db_factory(init=init_script_1)

test_script_1 = """
 
select test_pack.test() from rdb$database;
"""

act_1 = isql_act('db_1', test_script_1)

expected_stdout_1 = """                   
TEST
===============================================================================
TEST_PACK
"""

@pytest.mark.java
@pytest.mark.version('>=3.0,<4.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_stdout == act_1.clean_expected_stdout

# version: 4.0

init_script_2 = """

 set term !;
 create package test_pack
 as
 begin
 function test returns varchar(255);
 end!

 create package body test_pack
 as
 begin
 function test returns varchar(255)
 external name 'esp.TestContext.F_getPackageName()'
 engine java;
 end!

 set term ;!

"""

db_2 = db_factory(init=init_script_2)

test_script_2 = """

select test_pack.test() from rdb$database;
"""

act_2 = isql_act('db_2', test_script_2)

expected_stdout_2 = """
TEST
===============================================================================================================================================================================================================================================================
TEST_PACK
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
