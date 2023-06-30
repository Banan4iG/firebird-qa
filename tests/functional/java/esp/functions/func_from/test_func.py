#coding:utf-8

"""
ID:          java.esp.functions.func-from.func
TITLE:       External function call from other external function
DESCRIPTION: 
FBTEST:      functional.java.esp.functions.func_from.func
"""

import pytest
from firebird.qa import *

init_script = """

CREATE FUNCTION TEST(B BIGINT)
RETURNS BIGINT
EXTERNAL NAME 'esp.TestFunction.LongInOut(Long)' 
ENGINE JAVA;
commit;

CREATE FUNCTION MAINTEST(B BIGINT)
RETURNS BIGINT
EXTERNAL NAME 'esp.TestFunction.callFuncFromFunc(Long)' 
ENGINE JAVA;
commit;
"""

db = db_factory(init=init_script)

test_script = """
 
SELECT MAINTEST(10000000) FROM rdb$database;
commit;
"""

act = isql_act('db', test_script)

expected_stdout = """             
MAINTEST
=====================
10000000
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
