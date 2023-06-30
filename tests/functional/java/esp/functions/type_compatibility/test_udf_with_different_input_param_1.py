#coding:utf-8

"""
ID:          java.esp.functions.type-compatibility.udf-with-different-input-param-1
TITLE:       Call UDF with different  input param and with varchar output param
DESCRIPTION: 
FBTEST:      functional.java.esp.functions.type_compatibility.udf_with_different_input_param_1
"""

import pytest
from firebird.qa import *

# version: 3.0

init_script_1 = """
create function test(i integer, j bigint, k integer, l bigint) 
returns varchar(100)
external name 'esp.TestFunction.multyInOut(Integer, Long, int, long)' 
engine java;
commit;
"""

db_1 = db_factory(init=init_script_1)

act_1 = isql_act('db_1', """SELECT TEST(1,2,3,4) FROM RDB$DATABASE;""")

expected_stdout_1 = """
TEST
===============================================================================
24
"""

@pytest.mark.java
@pytest.mark.version('>=3.0,<4.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_stdout == act_1.clean_expected_stdout

# version: 4.0

init_script_2 = """
create function test(i integer, j bigint, k integer, l bigint)
returns varchar(100)
external name 'esp.TestFunction.multyInOut(Integer, Long, int, long)'
engine java;
commit;
"""

db_2 = db_factory(init=init_script_2)

act_2 = isql_act('db_2', """SELECT TEST(1,2,3,4) FROM RDB$DATABASE;""")

expected_stdout_2 = """
TEST
====================================================================================================
24
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
