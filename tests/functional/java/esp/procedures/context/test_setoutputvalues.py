#coding:utf-8

"""
ID:          java.esp.procedures.context.setoutputvalues
TITLE:       Testing of setObject method
DESCRIPTION: 
  Procedure sets values for output parameters through setObject method
FBTEST:      functional.java.esp.procedures.context.setoutputvalues
"""

import pytest
from firebird.qa import *

# version: 3.0

init_script_1 = """
 
create procedure test
returns(i1 integer, i2 varchar(100), ts timestamp)
external name 'esp.TestContext.P_setOutputValues()'
engine java;
commit; 

"""

db_1 = db_factory(init=init_script_1)

test_script_1 = """

 
execute procedure test;
commit;


"""

act_1 = isql_act('db_1', test_script_1)

expected_stdout_1 = """  	
I1 I2                                                                                                                          TS
============ =============================================================================== =========================
423 hello world!                                                                                         2008-04-10 10:11:12.0000
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
returns(i1 integer, i2 varchar(100), ts timestamp)
external name 'esp.TestContext.P_setOutputValuesERS()'
engine java;
commit;

"""

db_2 = db_factory(init=init_script_2)

test_script_2 = """


execute procedure test;
commit;


"""

act_2 = isql_act('db_2', test_script_2)

expected_stdout_2 = """
I1 I2                                                                                                                          TS
============ ==================================================================================================== =========================
423 hello world!                                                                                         2008-04-10 10:11:12.0000
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
