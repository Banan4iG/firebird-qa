#coding:utf-8

"""
ID:          java.esp.procedures.context.getnameinfo-2
TITLE:       Testing of getNameInfo method
DESCRIPTION: 
  Procedure gets info stored at entry point metadata.
FBTEST:      functional.java.esp.procedures.context.getnameinfo_2
"""

import pytest
from firebird.qa import *

# version: 3.0

init_script_1 = """
 
create table test_table(str varchar(100));
 
create procedure test
external name 'esp.TestContext.P_getNameInfo()!hello world!!!'
engine java;
commit;
"""

db_1 = db_factory(init=init_script_1)

test_script_1 = """
execute procedure test;
commit;

select * from test_table;
"""

act_1 = isql_act('db_1', test_script_1)

expected_stdout_1 = """                   
	
STR
===============================================================================
hello world!!!
"""

@pytest.mark.java
@pytest.mark.version('>=3.0,<4.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_stdout == act_1.clean_expected_stdout

# version: 4.0

init_script_2 = """

create table test_table(str varchar(100));

create procedure test
external name 'esp.TestContext.P_getNameInfo()!hello world!!!'
engine java;
commit;
"""

db_2 = db_factory(init=init_script_2)

test_script_2 = """
execute procedure test;
commit;

select * from test_table;
"""

act_2 = isql_act('db_2', test_script_2)

expected_stdout_2 = """

STR
====================================================================================================
hello world!!!
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
