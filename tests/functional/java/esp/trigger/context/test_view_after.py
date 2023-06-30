#coding:utf-8

"""
ID:          java.esp.trigger.context.view-after
TITLE:       Get context of ddl trigger on AFTER CREATE, ALTER, DROP VIEW
DESCRIPTION: 
FBTEST:      functional.java.esp.trigger.context.view_after
"""

import pytest
from firebird.qa import *

# version: 3.0

init_script_1 = """

CREATE TABLE CONTEXT_TABLE(context VARCHAR(2000));
commit;

CREATE TRIGGER TEST_TRIGGER 
ACTIVE
AFTER CREATE VIEW or ALTER VIEW or DROP VIEW
external name 'esp.TestTrigger.getContext()'
engine JAVA;
commit;

create table test_table(id integer, name varchar(100));
"""

db_1 = db_factory(init=init_script_1)

test_script_1 = """

create view test_view as select name from test_table;
commit;

alter view test_view as select name from test_table;
commit;

recreate view test_view as select name from test_table;
commit;

create or alter view test_view as select name from test_table;
commit;

drop view test_view;
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
AFTER CREATE VIEW or ALTER VIEW or DROP VIEW
external name 'esp.TestTrigger.getContext()'
engine JAVA;
commit;

create table test_table(id integer, name varchar(100));
"""

db_2 = db_factory(init=init_script_2)

test_script_2 = """

create view test_view as select name from test_table;
commit;

alter view test_view as select name from test_table;
commit;

recreate view test_view as select name from test_table;
commit;

create or alter view test_view as select name from test_table;
commit;

drop view test_view;
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
