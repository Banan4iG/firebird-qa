#coding:utf-8

"""
ID:          java.esp.procedures.proc-from.func
TITLE:       External procedure call from external function
DESCRIPTION: 
FBTEST:      functional.java.esp.procedures.proc_from.func
"""

import pytest
from firebird.qa import *

# version: 3.0

init_script_1 = """
CREATE TABLE TEST_TABLE(F_BIGINT BIGINT);
commit;
 
CREATE PROCEDURE TEST(s bigint)
returns (b bigint)
EXTERNAL NAME 'esp.TestProcedure.insertValue(Long, Long[])' 
ENGINE JAVA;
commit;

CREATE FUNCTION MAINTEST(B BIGINT)
RETURNS BIGINT
EXTERNAL NAME 'esp.TestFunction.callProcFromFunc(Long)' 
ENGINE JAVA;
commit;
"""

db_1 = db_factory(init=init_script_1)

test_script_1 = """
 
select MAINTEST(1000) from rdb$database;
commit;
"""

act_1 = isql_act('db_1', test_script_1)

expected_stdout_1 = """             
	
MAINTEST
=====================
1001
"""

@pytest.mark.java
@pytest.mark.version('>=3.0,<4.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_stdout == act_1.clean_expected_stdout

# version: 4.0

init_script_2 = """
CREATE TABLE TEST_TABLE(F_BIGINT BIGINT);
commit;

CREATE PROCEDURE TEST(s bigint)
returns (b bigint)
EXTERNAL NAME 'esp.TestProcedure.insertValueReturnERS(Long, Long[])'
ENGINE JAVA;
commit;

CREATE FUNCTION MAINTEST(B BIGINT)
RETURNS BIGINT
EXTERNAL NAME 'esp.TestFunction.callProcFromFunc(Long)'
ENGINE JAVA;
commit;
"""

db_2 = db_factory(init=init_script_2)

test_script_2 = """

select MAINTEST(1000) from rdb$database;
commit;
"""

act_2 = isql_act('db_2', test_script_2)

expected_stdout_2 = """

MAINTEST
=====================
1001
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
