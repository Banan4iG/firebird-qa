#coding:utf-8

"""
ID:          java.esp.trigger.context.update-before-calc
TITLE:       Get context of BEFORE UPDATE trigger when using calculated fields
DESCRIPTION: 
FBTEST:      functional.java.esp.trigger.context.update_before_calc
"""

import pytest
from firebird.qa import *

init_script = """
CREATE TABLE TEST_TABLE(A INTEGER COMPUTED BY (1), B bigint);
commit;

CREATE TABLE CONTEXT_TABLE(context VARCHAR(2000));
commit;

CREATE OR ALTER TRIGGER TEST_TRIGGER 
FOR TEST_TABLE
ACTIVE
BEFORE UPDATE
external name 'esp.TestTrigger.getContext()'
engine JAVA;
commit;

"""

db = db_factory(init=init_script)

test_script = """
INSERT INTO TEST_TABLE VALUES (9);
UPDATE TEST_TABLE SET B=21342434; 
"""

act = isql_act('db', test_script)

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.execute()
