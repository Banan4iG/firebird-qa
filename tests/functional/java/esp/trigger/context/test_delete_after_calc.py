#coding:utf-8

"""
ID:          java.esp.trigger.context.delete-after-calc
TITLE:       Get context of AFTER DELETE trigger when using calculated fields
DESCRIPTION: 
FBTEST:      functional.java.esp.trigger.context.delete_after_calc
"""

import pytest
from firebird.qa import *

init_script = """
CREATE TABLE TEST_TABLE(A INTEGER COMPUTED BY (1), B time);
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

db = db_factory(init=init_script)

test_script = """
 
INSERT INTO TEST_TABLE VALUES ('12:35');
DELETE FROM TEST_TABLE;
"""

act = isql_act('db', test_script)

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.execute()
