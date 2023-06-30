#coding:utf-8

"""
ID:          java.esp.trigger.context.update-after-
TITLE:       Get context of AFTER UPDATE trigger
DESCRIPTION: 
FBTEST:      functional.java.esp.trigger.context.update_after_
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
external name 'esp.TestTrigger.getContext()'
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
Action: UPDATE
Table name: TEST_TABLE
Type: AFTER
Info stored at entry point metadata: null
Object name called trigger: TEST_TRIGGER
Field name: F_VARCHAR
Field class: class java.lang.Object
Old value: It is old value
New value: It is new value
New value after set: It is new value from Java
Field name: F_DATE
Field class: class java.lang.Object
Old value: 2012-12-09
New value: 2012-12-09
New value after set: 2008-04-09
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
external name 'esp.TestTrigger.getContext()'
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
Action: UPDATE
Table name: TEST_TABLE
Type: AFTER
Info stored at entry point metadata: null
Object name called trigger: TEST_TRIGGER
Field name: F_VARCHAR
Field class: class java.lang.Object
Old value: It is old value
New value: It is new value
New value after set: It is new value from Java
Field name: F_DATE
Field class: class java.lang.Object
Old value: 2012-12-09
New value: 2012-12-09
New value after set: 2008-04-09
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
