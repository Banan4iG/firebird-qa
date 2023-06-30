#coding:utf-8

"""
ID:          java.esp.trigger.other.evaluate-fields-delete
TITLE:       Skip evaluating of some fields on delete
DESCRIPTION: 
FBTEST:      functional.java.esp.trigger.other.evaluate_fields_delete
"""

import pytest
from firebird.qa import *

init_script = """

CREATE TABLE TEST_TABLE1(
	TEST1 VARCHAR(10),
	TEST2 INTEGER,
	TEST3 TIMESTAMP,
	TEST4 VARCHAR(10) COMPUTED BY ('COMPUTED'));
CREATE TABLE TEST_TABLE2(
	TEST1 VARCHAR(10),
	TEST2 VARCHAR(10),
	TEST3 VARCHAR(30), 
	TEST4 VARCHAR(10));
	
INSERT INTO TEST_TABLE1 VALUES ('val0', 1000, CAST('01.01.2000 12:00' as TIMESTAMP));
INSERT INTO TEST_TABLE1 VALUES ('val1', 1001, CAST('01.01.2001 12:00' as TIMESTAMP));
INSERT INTO TEST_TABLE1 VALUES ('val2', 1002, CAST('01.01.2002 12:00' as TIMESTAMP));
INSERT INTO TEST_TABLE1 VALUES ('val3', 1003, CAST('01.01.2003 12:00' as TIMESTAMP));
INSERT INTO TEST_TABLE1 VALUES ('val4', 1004, CAST('01.01.2004 12:00' as TIMESTAMP));
INSERT INTO TEST_TABLE1 VALUES ('val5', 1005, CAST('01.01.2005 12:00' as TIMESTAMP));
INSERT INTO TEST_TABLE1 VALUES ('val6', 1006, CAST('01.01.2006 12:00' as TIMESTAMP));
commit;	

"""

db = db_factory(init=init_script)

test_script = """

CREATE OR ALTER TRIGGER TEST_TRIGGER
FOR TEST_TABLE1
ACTIVE
AFTER DELETE
external name 'esp.TestTrigger.evaluate_all_fields_delete()'
engine JAVA;
commit;

DELETE FROM TEST_TABLE1 WHERE TEST1 = 'val0';
commit; 

CREATE OR ALTER TRIGGER TEST_TRIGGER
FOR TEST_TABLE1
ACTIVE
BEFORE DELETE
external name 'esp.TestTrigger.do_not_evaluate_field_test1_delete()'
engine JAVA;
commit;

DELETE FROM TEST_TABLE1 WHERE TEST1 = 'val1';
commit; 

CREATE OR ALTER TRIGGER TEST_TRIGGER
FOR TEST_TABLE1
ACTIVE
AFTER DELETE
external name 'esp.TestTrigger.do_not_evaluate_field_test2_test4_delete()'
engine JAVA;
commit;

DELETE FROM TEST_TABLE1 WHERE TEST1 = 'val2';
commit; 

CREATE OR ALTER TRIGGER TEST_TRIGGER
FOR TEST_TABLE1
ACTIVE
BEFORE DELETE
external name 'esp.TestTrigger.evaluate_field_test1_delete()'
engine JAVA;
commit;

DELETE FROM TEST_TABLE1 WHERE TEST1 = 'val3';
commit;

CREATE OR ALTER TRIGGER TEST_TRIGGER
FOR TEST_TABLE1
ACTIVE
AFTER DELETE
external name 'esp.TestTrigger.evaluate_field_test2_test4_delete()'
engine JAVA;
commit;

DELETE FROM TEST_TABLE1 WHERE TEST1 = 'val4';
commit;  

CREATE OR ALTER TRIGGER TEST_TRIGGER
FOR TEST_TABLE1
ACTIVE
BEFORE DELETE
external name 'esp.TestTrigger.do_not_evaluate_computed_fields_delete()'
engine JAVA;
commit;

DELETE FROM TEST_TABLE1 WHERE TEST1 = 'val5';
commit;  

CREATE OR ALTER TRIGGER TEST_TRIGGER
FOR TEST_TABLE1
ACTIVE
AFTER DELETE
external name 'esp.TestTrigger.do_not_evaluate_field_test2_do_not_evaluate_computed_fields_delete()'
engine JAVA;
commit;

DELETE FROM TEST_TABLE1 WHERE TEST1 = 'val6';
commit; 
 
select * from TEST_TABLE2;
"""

act = isql_act('db', test_script)

expected_stdout = """
TEST1      TEST2      TEST3                          TEST4
========== ========== ============================== ==========
val0       1000       2000-01-01 12:00:00.0          COMPUTED
<null>     1001       2001-01-01 12:00:00.0          COMPUTED
val2       <null>     2002-01-01 12:00:00.0          <null>
val3       <null>     <null>                         <null>
<null>     1004       <null>                         COMPUTED
val5       1005       2005-01-01 12:00:00.0          <null>
val6       <null>     2006-01-01 12:00:00.0          <null>
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
