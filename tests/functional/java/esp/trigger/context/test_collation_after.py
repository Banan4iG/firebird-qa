#coding:utf-8

"""
ID:          java.esp.trigger.context.collation-after
TITLE:       Get context of ddl trigger on AFTER CREATE, DROP COLLATION
DESCRIPTION: 
FBTEST:      functional.java.esp.trigger.context.collation_after
"""

import pytest
from firebird.qa import *

# version: 3.0

init_script_1 = """

CREATE TABLE CONTEXT_TABLE(context VARCHAR(2000));
commit;

CREATE TRIGGER TEST_TRIGGER 
ACTIVE
AFTER CREATE COLLATION or DROP COLLATION
external name 'esp.TestTrigger.getContext()'
engine JAVA;
commit;

"""

db_1 = db_factory(init=init_script_1)

test_script_1 = """

create collation test_collat FOR ISO8859_1 from external ('ISO8859_1_UNICODE');
commit;

drop collation test_collat;
commit;
 
SELECT context FROM CONTEXT_TABLE;
"""

act_1 = isql_act('db_1', test_script_1)

expected_stdout_1 = """
CONTEXT
===============================================================================
Action: DDL
Table name:
Type: DATABASE
Info stored at entry point metadata: null
Object name called trigger: TEST_TRIGGER
Action: DDL
Table name:
Type: DATABASE
Info stored at entry point metadata: null
Object name called trigger: TEST_TRIGGER
"""

@pytest.mark.java
@pytest.mark.version('>=3.0,<4.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_stdout == act_1.clean_expected_stdout

# version: 4.0

init_script_2 = """

CREATE TABLE CONTEXT_TABLE(context VARCHAR(2000));
commit;

CREATE TRIGGER TEST_TRIGGER
ACTIVE
AFTER CREATE COLLATION or DROP COLLATION
external name 'esp.TestTrigger.getContext()'
engine JAVA;
commit;

"""

db_2 = db_factory(init=init_script_2)

test_script_2 = """

create collation test_collat FOR ISO8859_1 from external ('ISO8859_1_UNICODE');
commit;

drop collation test_collat;
commit;

SELECT context FROM CONTEXT_TABLE;
"""

act_2 = isql_act('db_2', test_script_2)

expected_stdout_2 = """
CONTEXT
================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
Action: DDL
Table name:
Type: DATABASE
Info stored at entry point metadata: null
Object name called trigger: TEST_TRIGGER
Action: DDL
Table name:
Type: DATABASE
Info stored at entry point metadata: null
Object name called trigger: TEST_TRIGGER
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
