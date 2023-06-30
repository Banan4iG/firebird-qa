#coding:utf-8

"""
ID:          java.esp.trigger.other.set-new-value-of-nonexistent-field
TITLE:       Set new value of nonexistent field from BEFORE UPDATE trigger
DESCRIPTION: 
FBTEST:      functional.java.esp.trigger.other.set_new_value_of_nonexistent_field
"""

import pytest
from firebird.qa import *

substitutions = [('esp.TestTrigger.*', ''), ('org.firebirdsql.fbjava.*', '')]

init_script = """
CREATE TABLE TEST_TABLE(NEW_VALUE VARCHAR(30));
commit;

CREATE OR ALTER TRIGGER TEST_TRIGGER 
FOR TEST_TABLE
ACTIVE
BEFORE UPDATE
external name 'esp.TestTrigger.setNewValue2()'
engine JAVA;
commit;


"""

db = db_factory(init=init_script)

test_script = """
INSERT INTO TEST_TABLE VALUES ('It is old value');
UPDATE TEST_TABLE SET NEW_VALUE='It is new value'; 
"""

act = isql_act('db', test_script, substitutions=substitutions)

expected_stderr = """

Statement failed, SQLSTATE = HY000
java.lang.IndexOutOfBoundsException: Values index out of bounds: Index: 2, Size: 1
at org.firebirdsql.fbjava.impl.ValuesImpl.checkIndex
at org.firebirdsql.fbjava.impl.ValuesImpl.getObject
at org.firebirdsql.fbjava.impl.ValuesImpl.setObject
at esp.TestTrigger.setNewValue2
-At trigger 'TEST_TRIGGER'
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stderr = expected_stderr
    act.execute()
    assert act.clean_stderr == act.clean_expected_stderr
