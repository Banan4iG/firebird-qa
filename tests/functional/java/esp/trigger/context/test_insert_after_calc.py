#coding:utf-8

"""
ID:          java.esp.trigger.context.insert-after-calc
TITLE:       Get context of AFTER INSERT trigger when using calculated fields
DESCRIPTION: 
FBTEST:      functional.java.esp.trigger.context.insert_after_calc
"""

import pytest
from firebird.qa import *

init_script = """
CREATE TABLE TEST_TABLE(A INTEGER COMPUTED BY (1), B varchar(100));
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

"""

db = db_factory(init=init_script)

test_script = """
INSERT INTO TEST_TABLE VALUES ('bbbb');
"""

act = isql_act('db', test_script)

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.execute()
