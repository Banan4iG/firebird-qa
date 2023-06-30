#coding:utf-8

"""
ID:          java.esp.procedures.context.getinputmetadata
TITLE:       Testing of getInputMetadata method
DESCRIPTION: 
  Procedure gets metadata of input parameters
FBTEST:      functional.java.esp.procedures.context.getinputmetadata
"""

import pytest
from firebird.qa import *

# version: 3.0

db_1 = db_factory()

test_script_1 = """
create procedure test(i integer, s varchar(100), ts timestamp)
returns (INPUT_METADATA varchar(5000))
external name 'esp.TestContext.P_getInputMetadata()'
engine java;
commit; 
 
select * from test(324, 'hello', '19.08.2034 12:24');
commit;
"""

act_1 = isql_act('db_1', test_script_1)

expected_stdout_1 = """  
INPUT_METADATA
===============================================================================
getIndex(TS): 3
InputMetadata:
getName: I
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
getName: S
getJavaClass: class java.lang.Object
getParameterClassName: java.lang.Object
getParameterCount: 3
getParameterMode: 0
getParameterType: 12
getParameterTypeName: null
getPrecision: 100
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

db_2 = db_factory()

test_script_2 = """
create procedure test(i integer, s varchar(100), ts timestamp)
returns (INPUT_METADATA varchar(5000))
external name 'esp.TestContext.P_getInputMetadata()'
engine java;
commit;

select * from test(324, 'hello', '19.08.2034 12:24');
commit;
"""

act_2 = isql_act('db_2', test_script_2)

expected_stdout_2 = """
INPUT_METADATA
========================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
getIndex(TS): 3
InputMetadata:
getName: I
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
getName: S
getJavaClass: class java.lang.Object
getParameterClassName: java.lang.Object
getParameterCount: 3
getParameterMode: 0
getParameterType: 12
getParameterTypeName: null
getPrecision: 100
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
