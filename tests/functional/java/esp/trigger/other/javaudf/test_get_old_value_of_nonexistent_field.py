#coding:utf-8

"""
ID:          java.esp.trigger.other.javaudf.get-old-value-of-nonexistent-field
TITLE:       Get old value of nonexistent field from AFTER UPDATE trigger
DESCRIPTION: 
FBTEST:      functional.java.esp.trigger.other.javaudf.get_old_value_of_nonexistent_field
"""

import pytest
from firebird.qa import *

substitutions = [('esp.TestTrigger.*', ''), ('org.firebirdsql.javaudf.*', ''), ('sun.*', ''), ('java.lang.reflect.*', ''), ('ct.*', ''), ('org.firebirdsql.fbjava.*', '')]

init_script = """
CREATE TABLE TEST_TABLE1(F_VARCHAR VARCHAR(20));
commit;

CREATE TABLE TEST_TABLE(OLD_VALUE VARCHAR(20));
commit;

CREATE OR ALTER TRIGGER TEST_TRIGGER 
FOR TEST_TABLE1 
ACTIVE
AFTER UPDATE
EXTERNAL NAME 'esp.TestTrigger.getObject_Old_jespudfcompat_not_exist_field()'
engine JAVA;
commit;

INSERT INTO TEST_TABLE1 VALUES ('It is old value');

"""

db = db_factory(init=init_script)

test_script = """
UPDATE TEST_TABLE1 SET F_VARCHAR='It is new value'; 
"""

act = isql_act('db', test_script, substitutions=substitutions)

expected_stderr = """	
Statement failed, SQLSTATE = HY000
java.lang.IndexOutOfBoundsException: Values index out of bounds: Index: -1, Size: 1
at
at
at
at
at
-At trigger 'TEST_TRIGGER'
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stderr = expected_stderr
    act.execute()
    assert act.clean_stderr == act.clean_expected_stderr
