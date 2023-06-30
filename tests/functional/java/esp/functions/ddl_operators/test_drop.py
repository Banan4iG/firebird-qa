#coding:utf-8

"""
ID:          java.esp.functions.ddl-operators.drop
TITLE:       Testing DROP operator for external function
DESCRIPTION: 
FBTEST:      functional.java.esp.functions.ddl_operators.drop
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

drop function test;
commit;

select test(2.7432) from rdb$database;
"""

act = isql_act('db', test_script)

expected_stdout = """                   
TEST
=======================
2.743200000000000
"""

expected_stderr = """
Statement failed, SQLSTATE = 39000
Dynamic SQL Error
-SQL error code = -804
-Function unknown
-TEST
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.expected_stderr = expected_stderr
    act.execute()
    assert (act.clean_stdout == act.clean_expected_stdout and
            act.clean_stderr == act.clean_expected_stderr)
