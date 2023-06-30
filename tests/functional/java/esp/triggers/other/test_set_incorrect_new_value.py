#coding:utf-8

"""
ID:          java.esp.triggers.other.set-incorrect-new-value
TITLE:       Set incorrect new value from BEFORE UPDATE trigger
DESCRIPTION: 
FBTEST:      functional.java.esp.triggers.other.set_incorrect_new_value
"""

import pytest
from firebird.qa import *

init_script = """
CREATE TABLE TEST_TABLE(F_INTEGER INTEGER);
commit;

CREATE OR ALTER TRIGGER TEST_TRIGGER 
FOR TEST_TABLE
ACTIVE
BEFORE UPDATE
external name 'esp.TestTrigger.setNewValue()'
engine JAVA;
commit;


"""

db = db_factory(init=init_script)

test_script = """
INSERT INTO TEST_TABLE VALUES (5);
UPDATE TEST_TABLE SET F_INTEGER = 10;
"""

act = isql_act('db', test_script, substitutions=[('$\\s+a.*', ''), ('class ', ''), ('\\(.*\\)', '')])

expected_stderr = """Statement failed, SQLSTATE = HY000
java.lang.ClassCastException: java.lang.String cannot be cast to java.math.BigDecimal
-At trigger 'TEST_TRIGGER'
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stderr = expected_stderr
    act.execute()
    assert act.clean_stderr == act.clean_expected_stderr
