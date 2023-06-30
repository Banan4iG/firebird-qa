#coding:utf-8

"""
ID:          java.esp.functions.type-compatibility.udf-with-different-input-param-3
TITLE:       Call UDF with different  types of input params
DESCRIPTION: 
FBTEST:      functional.java.esp.functions.type_compatibility.udf_with_different_input_param_3
"""

import pytest
from firebird.qa import *

# version: 3.0

init_script_1 = """
create function test(a numeric(8,3), b smallint, c smallint, d char(5), e date, f timestamp, g time) 
returns varchar(100)
external name 'esp.TestFunction.multyInOut2(java.math.BigDecimal, Short, short, String, java.sql.Date, java.sql.Timestamp, java.sql.Time)' 
engine java;
commit;
"""

db_1 = db_factory(init=init_script_1)

test_script_1 = """SELECT TEST(12345.678,-1,1,'Hello','2007-08-11','2008-05-15 12:44:23','12:22:44') FROM RDB$DATABASE;
"""

act_1 = isql_act('db_1', test_script_1)

expected_stdout_1 = """
TEST
===============================================================================
12345.678_-1_1_Hello_2007-08-11_2008-05-15 12:44:23.0_12:22:44
"""

@pytest.mark.java
@pytest.mark.version('>=3.0,<4.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_stdout == act_1.clean_expected_stdout

# version: 4.0

init_script_2 = """
create function test(a numeric(8,3), b smallint, c smallint, d char(5), e date, f timestamp, g time)
returns varchar(100)
external name 'esp.TestFunction.multyInOut2(java.math.BigDecimal, Short, short, String, java.sql.Date, java.sql.Timestamp, java.sql.Time)'
engine java;
commit;
"""

db_2 = db_factory(init=init_script_2)

test_script_2 = """SELECT TEST(12345.678,-1,1,'Hello','2007-08-11','2008-05-15 12:44:23','12:22:44') FROM RDB$DATABASE;
"""

act_2 = isql_act('db_2', test_script_2)

expected_stdout_2 = """
TEST
====================================================================================================
12345.678_-1_1_Hello_2007-08-11_2008-05-15 12:44:23.0_12:22:44
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
