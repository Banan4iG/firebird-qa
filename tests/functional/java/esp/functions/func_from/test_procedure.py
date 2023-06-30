#coding:utf-8

"""
ID:          java.esp.functions.func-from.procedure
TITLE:       External function call from external procedure
DESCRIPTION: 
FBTEST:      functional.java.esp.functions.func_from.procedure
"""

import pytest
from firebird.qa import *

init_script = """

CREATE FUNCTION TEST(B FLOAT)
RETURNS FLOAT
EXTERNAL NAME 'esp.TestFunction.floatInOut(float)' 
ENGINE JAVA;
commit;

CREATE PROCEDURE MAINTEST(B FLOAT)
EXTERNAL NAME 'esp.TestProcedure.callFuncFromProcedure(float)' 
ENGINE JAVA;
commit;

create table test_table (num float);
commit;
"""

db = db_factory(init=init_script)

test_script = """
 
EXECUTE PROCEDURE MAINTEST(124.68);
commit;

select num from test_table;
"""

act = isql_act('db', test_script)

expected_stdout = """             
NUM
==============
124.68000
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
