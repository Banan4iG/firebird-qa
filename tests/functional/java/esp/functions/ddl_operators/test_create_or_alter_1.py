#coding:utf-8

"""
ID:          java.esp.functions.ddl-operators.create-or-alter-1
TITLE:       Testing CREATE OR ALTER operator for external function when function is created
DESCRIPTION: 
FBTEST:      functional.java.esp.functions.ddl_operators.create_or_alter_1
"""

import pytest
from firebird.qa import *

init_script = """
 
create function test(i double precision) 
returns double precision
external name 'esp.TestFunction.doubleInOut(double)'
engine java;
commit;
"""

db = db_factory(init=init_script)

test_script = """
select test(2.7432) from rdb$database;
commit;

create or alter function test(i double precision) 
returns double precision
external name 'esp.TestFunction.IncDouble(Double)'
engine java;
commit;

select test(2.7432) from rdb$database;
"""

act = isql_act('db', test_script)

expected_stdout = """                   
TEST
=======================
2.743200000000000
	  
TEST
=======================
3.743200000000000
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
