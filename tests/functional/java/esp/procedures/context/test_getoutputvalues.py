#coding:utf-8

"""
ID:          java.esp.procedures.context.getoutputvalues
TITLE:       Testing of getObject method
DESCRIPTION: 
  Procedure gets values of output parameters through getObject method
FBTEST:      functional.java.esp.procedures.context.getoutputvalues
"""

import pytest
from firebird.qa import *

# version: 3.0

init_script_1 = """
 
create procedure test
returns (output_value1 varchar(100), output_value2 integer, output_value3 timestamp)
external name 'esp.TestContext.P_getOutputValues()'
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
OUTPUT_VALUE1                                                                                        OUTPUT_VALUE2             OUTPUT_VALUE3
=============================================================================== ============= =========================
null
null
null                                                                                             <null>                    <null>
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
returns (output_value1 varchar(100), output_value2 integer, output_value3 timestamp)
external name 'esp.TestContext.P_getOutputValues()'
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
OUTPUT_VALUE1                                                                                        OUTPUT_VALUE2             OUTPUT_VALUE3
==================================================================================================== ============= =========================
null
null
null                                                                                             <null>                    <null>
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
