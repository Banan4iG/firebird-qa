#coding:utf-8

"""
ID:          java.esp.trigger.context.javaudf.update-after
TITLE:       Get context of AFTER UPDATE trigger
DESCRIPTION: 
FBTEST:      functional.java.esp.trigger.context.javaudf.update_after
"""

import pytest
from firebird.qa import *

# version: 3.0

init_script_1 = """
CREATE TABLE TEST_TABLE(F_VARCHAR VARCHAR(30), F_DATE date);
commit;

CREATE TABLE CONTEXT_TABLE(context VARCHAR(2000));
commit;

CREATE OR ALTER TRIGGER TEST_TRIGGER 
FOR TEST_TABLE
ACTIVE
AFTER UPDATE
external name 'esp.TestTrigger.getContextJavaudf()'
engine JAVA;
commit;

"""

db_1 = db_factory(init=init_script_1)

test_script_1 = """
INSERT INTO TEST_TABLE VALUES ('It is old value', '09.12.2012');
UPDATE TEST_TABLE SET F_VARCHAR='It is new value'; 	
 
SELECT context FROM CONTEXT_TABLE;
"""

act_1 = isql_act('db_1', test_script_1)

expected_stdout_1 = """
CONTEXT
===============================================================================
Action: 2
Table name: TEST_TABLE
Old value: It is old value
New value: It is new value
New value after set: New value from Java
"""

@pytest.mark.java
@pytest.mark.version('>=3.0,<4.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_stdout == act_1.clean_expected_stdout

# version: 4.0

init_script_2 = """
CREATE TABLE TEST_TABLE(F_VARCHAR VARCHAR(30), F_DATE date);
commit;

CREATE TABLE CONTEXT_TABLE(context VARCHAR(2000));
commit;

CREATE OR ALTER TRIGGER TEST_TRIGGER
FOR TEST_TABLE
ACTIVE
AFTER UPDATE
external name 'esp.TestTrigger.getContextJavaudf()'
engine JAVA;
commit;

"""

db_2 = db_factory(init=init_script_2)

test_script_2 = """
INSERT INTO TEST_TABLE VALUES ('It is old value', '09.12.2012');
UPDATE TEST_TABLE SET F_VARCHAR='It is new value';

SELECT context FROM CONTEXT_TABLE;
"""

act_2 = isql_act('db_2', test_script_2)

expected_stdout_2 = """
CONTEXT
================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
Action: 2
Table name: TEST_TABLE
Old value: It is old value
New value: It is new value
New value after set: New value from Java
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
