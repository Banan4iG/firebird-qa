#coding:utf-8

"""
ID:          java.esp.procedures.resultset-out
TITLE:       Call of ESP which returns ResultSet
DESCRIPTION: 
FBTEST:      functional.java.esp.procedures.resultset_out
"""

import pytest
from firebird.qa import *

# version: 3.0

init_script_1 = """
 
CREATE TABLE TEST_TABLE(F_INTEGER INTEGER, F_VARCHAR VARCHAR(10));
commit;

CREATE OR ALTER PROCEDURE TEST
RETURNS(F_INTEGER INTEGER, F_VARCHAR VARCHAR(10))
EXTERNAL NAME 'esp.TestProcedure.testRS()' 
ENGINE JAVA;
commit;

"""

db_1 = db_factory(init=init_script_1)

test_script_1 = """
SELECT * FROM TEST;
"""

act_1 = isql_act('db_1', test_script_1)

expected_stdout_1 = """         
F_INTEGER F_VARCHAR
============ ==========
1 test1
2 test2
3 test3
4 test4
5 test5
6 test6
7 test7
8 test8
9 test9
10 test10
"""

@pytest.mark.java
@pytest.mark.version('>=3.0,<4.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_stdout == act_1.clean_expected_stdout

# version: 4.0

init_script_2 = """

CREATE TABLE TEST_TABLE(F_INTEGER INTEGER, F_VARCHAR VARCHAR(10));
commit;

CREATE OR ALTER PROCEDURE TEST
RETURNS(F_INTEGER INTEGER, F_VARCHAR VARCHAR(10))
EXTERNAL NAME 'esp.TestProcedure.testERS()'
ENGINE JAVA;
commit;

"""

db_2 = db_factory(init=init_script_2)

test_script_2 = """
SELECT * FROM TEST;
"""

act_2 = isql_act('db_2', test_script_2)

expected_stdout_2 = """
F_INTEGER F_VARCHAR
============ ==========
1 test1
2 test2
3 test3
4 test4
5 test5
6 test6
7 test7
8 test8
9 test9
10 test10
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
