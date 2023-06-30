#coding:utf-8

"""
ID:          java.esp.functions.type-compatibility.udf-with-different-input-param-2
TITLE:       Call UDF with different  types of input params
DESCRIPTION: 
FBTEST:      functional.java.esp.functions.type_compatibility.udf_with_different_input_param_2
"""

import pytest
from firebird.qa import *

init_script = """
create function test(a integer, b integer,c bigint,d bigint, e double precision, f double precision, g float, h float, i numeric(15,2), j smallint) 
returns double precision
external name 'esp.TestFunction.multyInOut1(Integer, int, Long, long, Double, double, Float, float, java.math.BigDecimal, Short)'
engine java;
commit;
"""

db = db_factory(init=init_script)

test_script = """SELECT TEST(1,1,1,1,1.0,1.0,1.0,1.0,1.0,1) FROM RDB$DATABASE;
"""

act = isql_act('db', test_script)

expected_stdout = """                
TEST
=======================
10.00000000000000
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
