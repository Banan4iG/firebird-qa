#coding:utf-8

"""
ID:          java.esp.trigger.context.insert-after
TITLE:       Get context of AFTER INSERT trigger
DESCRIPTION: 
FBTEST:      functional.java.esp.trigger.context.insert_after
"""

import pytest
from firebird.qa import *

# version: 3.0

init_script_1 = """
CREATE TABLE TEST_TABLE(F_VARCHAR VARCHAR(30), F_FLOAT float);
commit;

CREATE TABLE CONTEXT_TABLE(context VARCHAR(2000));
commit;

CREATE OR ALTER TRIGGER TEST_TRIGGER 
FOR TEST_TABLE
ACTIVE
AFTER INSERT
external name 'esp.TestTrigger.getContext()'
engine JAVA;
commit;

INSERT INTO TEST_TABLE VALUES ('It is new value', 456.678);

"""

db_1 = db_factory(init=init_script_1)

test_script_1 = """
SELECT context FROM CONTEXT_TABLE;
"""

act_1 = isql_act('db_1', test_script_1)

expected_stdout_1 = """
CONTEXT
===============================================================================
Action: INSERT
Table name: TEST_TABLE
Type: AFTER
Info stored at entry point metadata: null
Object name called trigger: TEST_TRIGGER
Field name: F_VARCHAR
Field class: class java.lang.Object
Old value: null
New value: It is new value
New value after set: It is new value from Java
Field name: F_FLOAT
Field class: class java.lang.Object
Old value: null
New value: 456.678
New value after set: 46.45
"""

@pytest.mark.java
@pytest.mark.version('>=3.0,<4.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_stdout == act_1.clean_expected_stdout

# version: 4.0

init_script_2 = """
CREATE TABLE TEST_TABLE(F_VARCHAR VARCHAR(30), F_FLOAT float);
commit;

CREATE TABLE CONTEXT_TABLE(context VARCHAR(2000));
commit;

CREATE OR ALTER TRIGGER TEST_TRIGGER
FOR TEST_TABLE
ACTIVE
AFTER INSERT
external name 'esp.TestTrigger.getContext()'
engine JAVA;
commit;

INSERT INTO TEST_TABLE VALUES ('It is new value', 456.678);

"""

db_2 = db_factory(init=init_script_2)

test_script_2 = """
SELECT context FROM CONTEXT_TABLE;
"""

act_2 = isql_act('db_2', test_script_2)

expected_stdout_2 = """
CONTEXT
================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
Action: INSERT
Table name: TEST_TABLE
Type: AFTER
Info stored at entry point metadata: null
Object name called trigger: TEST_TRIGGER
Field name: F_VARCHAR
Field class: class java.lang.Object
Old value: null
New value: It is new value
New value after set: It is new value from Java
Field name: F_FLOAT
Field class: class java.lang.Object
Old value: null
New value: 456.678
New value after set: 46.45
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
