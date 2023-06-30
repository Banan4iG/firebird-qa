#coding:utf-8

"""
ID:          java.esp.trigger.context.javaudf.any-ddl-statement-after
TITLE:       Get context of ddl trigger on AFTER ANY DDl STATEMENT
DESCRIPTION: 
FBTEST:      functional.java.esp.trigger.context.javaudf.any_ddl_statement_after
"""

import pytest
from firebird.qa import *

# version: 3.0

init_script_1 = """

CREATE TABLE CONTEXT_TABLE(context VARCHAR(2000));
commit;

CREATE TRIGGER TEST_TRIGGER 
ACTIVE
AFTER ANY DDl STATEMENT
external name 'esp.TestTrigger.getContextJavaudf()'
engine JAVA;
commit;
"""

db_1 = db_factory(init=init_script_1)

test_script_1 = """

CREATE MAPPING TEST_MAP
USING *
FROM ANY USER
TO USER;
commit;

set term !;
recreate function test_func
returns boolean
as 
begin 
	return true;
end!
commit!
set term ;!

recreate table test_table(id integer);
commit;


DROP MAPPING TEST_MAP;
commit;
 
SELECT context FROM CONTEXT_TABLE;
"""

act_1 = isql_act('db_1', test_script_1)

expected_stdout_1 = """
CONTEXT
===============================================================================
Action: 9
Action: 9
Action: 9
Action: 9

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
AFTER ANY DDl STATEMENT
external name 'esp.TestTrigger.getContextJavaudf()'
engine JAVA;
commit;
"""

db_2 = db_factory(init=init_script_2)

test_script_2 = """

CREATE MAPPING TEST_MAP
USING *
FROM ANY USER
TO USER;
commit;

set term !;
recreate function test_func
returns boolean
as
begin
	return true;
end!
commit!
set term ;!

recreate table test_table(id integer);
commit;


DROP MAPPING TEST_MAP;
commit;

SELECT context FROM CONTEXT_TABLE;
"""

act_2 = isql_act('db_2', test_script_2)

expected_stdout_2 = """
CONTEXT
================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
Action: 9
Action: 9
Action: 9
Action: 9

"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
