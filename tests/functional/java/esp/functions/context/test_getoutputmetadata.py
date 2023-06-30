#coding:utf-8

"""
ID:          java.esp.functions.context.getoutputmetadata
TITLE:       Testing of getOutputMetadata and getValuesInfo methods
DESCRIPTION: 
  Function gets metadata of output parameters through getValuesInfo method
FBTEST:      functional.java.esp.functions.context.getoutputmetadata
"""

import pytest
from firebird.qa import *

# version: 3.0

init_script_1 = """
 
create function test()
returns varchar(1000)
external name 'esp.TestContext.F_getOutputMetadata()'
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
OutputMetadata:
getName: null
getJavaClass: class java.lang.String
getParameterClassName: java.lang.String
getParameterCount: 1
getParameterMode: 0
getParameterType: 12
getParameterTypeName: null
getPrecision: 1000
getScale: 0
isNullable: 1
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

create function test()
returns varchar(1000)
external name 'esp.TestContext.F_getOutputMetadata()'
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
========================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
OutputMetadata:
getName: null
getJavaClass: class java.lang.String
getParameterClassName: java.lang.String
getParameterCount: 1
getParameterMode: 0
getParameterType: 12
getParameterTypeName: null
getPrecision: 1000
getScale: 0
isNullable: 1
isSigned: true
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
