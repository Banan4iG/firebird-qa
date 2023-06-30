#coding:utf-8

"""
ID:          java.esp.functions.other.recursive-factorial
TITLE:       Recursive call external function
DESCRIPTION: 
FBTEST:      functional.java.esp.functions.other.recursive_factorial
"""

import pytest
from firebird.qa import *

init_script = """
create function factor(x integer)
returns bigint
external name 'esp.TestFunction.factorial(int)'
engine java;
commit;
"""

db = db_factory(init=init_script)

act = isql_act('db', """SELECT FACTOR(5) FROM RDB$DATABASE;""")

expected_stdout = """               
FACTOR
=====================
120
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
