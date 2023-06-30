#coding:utf-8

"""
ID:          java.esp.trigger.context.insert-before-calc
TITLE:       Get context of BEFORE INSERT trigger when using calculated fields
DESCRIPTION: 
FBTEST:      functional.java.esp.trigger.context.insert_before_calc
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
BEFORE INSERT
external name 'esp.TestTrigger.getContext()'
engine JAVA;
commit;

"""

db = db_factory(init=init_script)

test_script = """
INSERT INTO TEST_TABLE(B) VALUES ('aaaa');  
"""

act = isql_act('db', test_script)

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.execute()
