#coding:utf-8

"""
ID:          java.esp.trigger.context.delete-before-calc
TITLE:       Get context of BEFORE DELETE trigger when using calculated fields
DESCRIPTION: 
FBTEST:      functional.java.esp.trigger.context.delete_before_calc
"""

import pytest
from firebird.qa import *

init_script = """
CREATE TABLE TEST_TABLE(A INTEGER COMPUTED BY (1), B timestamp);
commit;

CREATE TABLE CONTEXT_TABLE(context VARCHAR(2000));
commit;

CREATE OR ALTER TRIGGER TEST_TRIGGER 
FOR TEST_TABLE
ACTIVE
BEFORE DELETE
external name 'esp.TestTrigger.getContext()'
engine JAVA;
commit;

"""

db = db_factory(init=init_script)

test_script = """
 
INSERT INTO TEST_TABLE VALUES ('13.04.1903 12:35');
DELETE FROM TEST_TABLE;
"""

act = isql_act('db', test_script)

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.execute()
