#coding:utf-8

"""
ID:          java.esp.procedures.proc-from.trigger
TITLE:       External procedure call from external trigger
DESCRIPTION: 
FBTEST:      functional.java.esp.procedures.proc_from.trigger
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

CREATE TRIGGER TEST_TRIGGER 
FOR TEST_TABLE ACTIVE
BEFORE UPDATE
EXTERNAL NAME 'esp.TestTrigger.callProcFromTrigger()'
engine JAVA;
commit;

"""

db_1 = db_factory(init=init_script_1)

test_script_1 = """
 
INSERT INTO TEST_TABLE VALUES (20);
UPDATE TEST_TABLE SET F_BIGINT=30;

select F_BIGINT from test_table;
"""

act_1 = isql_act('db_1', test_script_1)

expected_stdout_1 = """             
	
F_BIGINT
=====================
201
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

CREATE TRIGGER TEST_TRIGGER
FOR TEST_TABLE ACTIVE
BEFORE UPDATE
EXTERNAL NAME 'esp.TestTrigger.callProcFromTrigger()'
engine JAVA;
commit;

"""

db_2 = db_factory(init=init_script_2)

test_script_2 = """

INSERT INTO TEST_TABLE VALUES (20);
UPDATE TEST_TABLE SET F_BIGINT=30;

select F_BIGINT from test_table;
"""

act_2 = isql_act('db_2', test_script_2)

expected_stdout_2 = """

F_BIGINT
=====================
201
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
