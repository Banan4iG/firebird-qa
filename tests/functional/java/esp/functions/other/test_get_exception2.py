#coding:utf-8

"""
ID:          java.esp.functions.other.get-exception2
TITLE:       External function calls exception
DESCRIPTION: 
FBTEST:      functional.java.esp.functions.other.get_exception2
"""

import pytest
from firebird.qa import *

init_script = """
 
create function test() 
returns integer
external name 'esp.TestFunction.getException2()'
engine java;
commit;

"""

db = db_factory(init=init_script)

test_script = """
SELECT TEST() FROM RDB$DATABASE;
"""

act = isql_act('db', test_script, substitutions=[('esp.TestFunction.getException.*', '')])

expected_stdout = """    
TEST
============
"""

expected_stderr = """
Statement failed, SQLSTATE = HY000
java.lang.Exception: test_exc2
at esp.TestFunction.getException2(TestFunction.java:231)
Caused by: java.lang.Exception: test_exc
at esp.TestFunction.getException(TestFunction.java:219)
at esp.TestFunction.getException2(TestFunction.java:226)
-At function 'TEST'
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.expected_stderr = expected_stderr
    act.execute()
    assert (act.clean_stdout == act.clean_expected_stdout and
            act.clean_stderr == act.clean_expected_stderr)
