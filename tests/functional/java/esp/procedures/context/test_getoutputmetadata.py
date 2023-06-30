#coding:utf-8

"""
ID:          java.esp.procedures.context.getoutputmetadata
TITLE:       Testing of getOutputMetadata method
DESCRIPTION: 
  Procedure gets metadata of output parameters
FBTEST:      functional.java.esp.procedures.context.getoutputmetadata
"""

import pytest
from firebird.qa import *

# version: 3.0

init_script_1 = """
 
create procedure test
returns (str varchar(1000), num integer)
external name 'esp.TestContext.P_getOutputMetadata()'
engine java;
commit;
"""

db_1 = db_factory(init=init_script_1)

test_script_1 = """
select * from test;
commit;
"""

act_1 = isql_act('db_1', test_script_1)

expected_stdout_1 = """                   
STR                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               NUM
=============================================================================== ============
getName: STR
getJavaClass: class java.lang.Object
getParameterClassName: java.lang.Object
getParameterCount: 2
getParameterMode: 0
getParameterType: 12
getParameterTypeName: null
getPrecision: 1000
getScale: 0
isNullable: 1
isSigned: true
getName: NUM
getJavaClass: class java.lang.Object
getParameterClassName: java.lang.Object
getParameterCount: 2
getParameterMode: 0
getParameterType: 4
getParameterTypeName: null
getPrecision: 4
getScale: 0
isNullable: 1
isSigned: true
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

create procedure test
returns (str varchar(1000), num integer)
external name 'esp.TestContext.P_getOutputMetadata()'
engine java;
commit;
"""

db_2 = db_factory(init=init_script_2)

test_script_2 = """
select * from test;
commit;
"""

act_2 = isql_act('db_2', test_script_2)

expected_stdout_2 = """
STR                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               NUM
======================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================== ============
getName: STR
getJavaClass: class java.lang.String
getParameterClassName: java.lang.String
getParameterCount: 2
getParameterMode: 0
getParameterType: 12
getParameterTypeName: null
getPrecision: 1000
getScale: 0
isNullable: 1
isSigned: true
getName: NUM
getJavaClass: class java.lang.Integer
getParameterClassName: java.lang.Integer
getParameterCount: 2
getParameterMode: 0
getParameterType: 4
getParameterTypeName: null
getPrecision: 4
getScale: 0
isNullable: 0
isSigned: true
<null>
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
