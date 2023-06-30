#coding:utf-8

"""
ID:          java.esp.functions.context.getinputmetadata
TITLE:       Testing of getInputMetadata method
DESCRIPTION: 
  Function gets metadata of input parameters
FBTEST:      functional.java.esp.functions.context.getinputmetadata
"""

import pytest
from firebird.qa import *

# version: 3.0

init_script_1 = """
 
create function test(i1 integer, i2 varchar(10), ts timestamp)
returns varchar(1000)
external name 'esp.TestContext.F_getInputMetadata()'
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
getIndex(TS): 3
InputMetadata:
getName: I1
getJavaClass: class java.lang.Object
getParameterClassName: java.lang.Object
getParameterCount: 3
getParameterMode: 0
getParameterType: 4
getParameterTypeName: null
getPrecision: 4
getScale: 0
isNullable: 1
isSigned: true
getName: I2
getJavaClass: class java.lang.Object
getParameterClassName: java.lang.Object
getParameterCount: 3
getParameterMode: 0
getParameterType: 12
getParameterTypeName: null
getPrecision: 10
getScale: 0
isNullable: 1
isSigned: true
getName: TS
getJavaClass: class java.lang.Object
getParameterClassName: java.lang.Object
getParameterCount: 3
getParameterMode: 0
getParameterType: 93
getParameterTypeName: null
getPrecision: 8
getScale: 0
isNullable: 0
isSigned: true
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
external name 'esp.TestContext.F_getInputMetadata()'
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
getIndex(TS): 3
InputMetadata:
getName: I1
getJavaClass: class java.lang.Object
getParameterClassName: java.lang.Object
getParameterCount: 3
getParameterMode: 0
getParameterType: 4
getParameterTypeName: null
getPrecision: 4
getScale: 0
isNullable: 1
isSigned: true
getName: I2
getJavaClass: class java.lang.Object
getParameterClassName: java.lang.Object
getParameterCount: 3
getParameterMode: 0
getParameterType: 12
getParameterTypeName: null
getPrecision: 10
getScale: 0
isNullable: 1
isSigned: true
getName: TS
getJavaClass: class java.lang.Object
getParameterClassName: java.lang.Object
getParameterCount: 3
getParameterMode: 0
getParameterType: 93
getParameterTypeName: null
getPrecision: 8
getScale: 0
isNullable: 0
isSigned: true
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
