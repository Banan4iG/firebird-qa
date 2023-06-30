#coding:utf-8

"""
ID:          java.esp.procedures.context.setinputvalues
TITLE:       Testing of setObject method
DESCRIPTION: 
  Procedure sets values for input parameters through setObject method
FBTEST:      functional.java.esp.procedures.context.setinputvalues
"""

import pytest
from firebird.qa import *

# version: 3.0

init_script_1 = """
create table test_table(num integer, name varchar(100), ts timestamp); 
 
create procedure test(i1 integer, i2 varchar(10), ts timestamp)
external name 'esp.TestContext.P_setInputValues()'
engine java;
commit; 

"""

db_1 = db_factory(init=init_script_1)

test_script_1 = """

 
execute procedure test(324, 'hello', '10.12.1989 10:30');
commit;

select * from test_table;
"""

act_1 = isql_act('db_1', test_script_1)

expected_stdout_1 = """  
NUM NAME                                                                                                                        TS
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
create table test_table(num integer, name varchar(100), ts timestamp);

create procedure test(i1 integer, i2 varchar(10), ts timestamp)
external name 'esp.TestContext.P_setInputValues()'
engine java;
commit;

"""

db_2 = db_factory(init=init_script_2)

test_script_2 = """


execute procedure test(324, 'hello', '10.12.1989 10:30');
commit;

select * from test_table;
"""

act_2 = isql_act('db_2', test_script_2)

expected_stdout_2 = """
NUM NAME                                                                                                                        TS
============ ==================================================================================================== =========================
423 hello world!                                                                                         2008-04-10 10:11:12.0000
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
