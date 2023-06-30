#coding:utf-8

"""
ID:          java.esp.trigger.context.delete-after
TITLE:       Get context of AFTER DELETE trigger
DESCRIPTION: 
FBTEST:      functional.java.esp.trigger.context.delete_after
"""

import pytest
from firebird.qa import *

# version: 3.0

init_script_1 = """
CREATE TABLE TEST_TABLE(F_VARCHAR VARCHAR(30), F_TIME time);
commit;

CREATE TABLE CONTEXT_TABLE(context VARCHAR(2000));
commit;

CREATE OR ALTER TRIGGER TEST_TRIGGER 
FOR TEST_TABLE
ACTIVE
AFTER DELETE
external name 'esp.TestTrigger.getContext()'
engine JAVA;
commit;


"""

db_1 = db_factory(init=init_script_1)

test_script_1 = """
 
INSERT INTO TEST_TABLE VALUES ('It is old value', '12:35');
DELETE FROM TEST_TABLE;
 
SELECT context FROM CONTEXT_TABLE;
"""

act_1 = isql_act('db_1', test_script_1)

expected_stdout_1 = """
CONTEXT
===============================================================================
Action: DELETE
Table name: TEST_TABLE
Type: AFTER
Info stored at entry point metadata: null
Object name called trigger: TEST_TRIGGER
Field name: F_VARCHAR
Field class: class java.lang.Object
Old value: It is old value
New value: null
Field name: F_TIME
Field class: class java.lang.Object
Old value: 12:35:00
New value: null
"""

@pytest.mark.java
@pytest.mark.version('>=3.0,<4.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_stdout == act_1.clean_expected_stdout

# version: 4.0

init_script_2 = """
CREATE TABLE TEST_TABLE(F_VARCHAR VARCHAR(30), F_TIME time);
commit;

CREATE TABLE CONTEXT_TABLE(context VARCHAR(2000));
commit;

CREATE OR ALTER TRIGGER TEST_TRIGGER
FOR TEST_TABLE
ACTIVE
AFTER DELETE
external name 'esp.TestTrigger.getContext()'
engine JAVA;
commit;


"""

db_2 = db_factory(init=init_script_2)

test_script_2 = """

INSERT INTO TEST_TABLE VALUES ('It is old value', '12:35');
DELETE FROM TEST_TABLE;

SELECT context FROM CONTEXT_TABLE;
"""

act_2 = isql_act('db_2', test_script_2)

expected_stdout_2 = """
CONTEXT
================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
Action: DELETE
Table name: TEST_TABLE
Type: AFTER
Info stored at entry point metadata: null
Object name called trigger: TEST_TRIGGER
Field name: F_VARCHAR
Field class: class java.lang.Object
Old value: It is old value
New value: null
Field name: F_TIME
Field class: class java.lang.Object
Old value: 12:35:00
New value: null
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
