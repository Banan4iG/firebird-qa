#coding:utf-8

"""
ID:          java.esp.trigger.other.evaluate-fields-update
TITLE:       Skip evaluating of some fields on update
DESCRIPTION: 
FBTEST:      functional.java.esp.trigger.other.evaluate_fields_update
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
	NEWTEST1 VARCHAR(10),
	NEWTEST2 VARCHAR(10),
	NEWTEST3 VARCHAR(30), 
	NEWTEST4 VARCHAR(10),
	OLDTEST1 VARCHAR(10),
	OLDTEST2 VARCHAR(10),
	OLDTEST3 VARCHAR(30), 
	OLDTEST4 VARCHAR(10));

INSERT INTO TEST_TABLE1 VALUES ('val0', 1000, CAST('01.01.2000 12:00' as TIMESTAMP));
commit;

"""

db = db_factory(init=init_script)

test_script = """
CREATE OR ALTER TRIGGER TEST_TRIGGER
FOR TEST_TABLE1
ACTIVE
AFTER UPDATE
external name 'esp.TestTrigger.evaluate_all_fields_update()'
engine JAVA;
commit;

UPDATE TEST_TABLE1 SET TEST1 = 'val1', TEST2 = 1001, TEST3 = CAST('01.01.2001 12:00' as TIMESTAMP);
commit;

CREATE OR ALTER TRIGGER TEST_TRIGGER
FOR TEST_TABLE1
ACTIVE
BEFORE UPDATE
external name 'esp.TestTrigger.do_not_evaluate_field_test1_update()'
engine JAVA;
commit;

UPDATE TEST_TABLE1 SET TEST1 = 'val2', TEST2 = 1002, TEST3 = CAST('01.01.2002 12:00' as TIMESTAMP);
commit;

CREATE OR ALTER TRIGGER TEST_TRIGGER
FOR TEST_TABLE1
ACTIVE
AFTER UPDATE
external name 'esp.TestTrigger.do_not_evaluate_field_test2_test4_update()'
engine JAVA;
commit;

UPDATE TEST_TABLE1 SET TEST1 = 'val3', TEST2 = 1003, TEST3 = CAST('01.01.2003 12:00' as TIMESTAMP);
commit;

CREATE OR ALTER TRIGGER TEST_TRIGGER
FOR TEST_TABLE1
ACTIVE
BEFORE UPDATE
external name 'esp.TestTrigger.evaluate_field_test1_update()'
engine JAVA;
commit;

UPDATE TEST_TABLE1 SET TEST1 = 'val4', TEST2 = 1004, TEST3 = CAST('01.01.2004 12:00' as TIMESTAMP);
commit;

CREATE OR ALTER TRIGGER TEST_TRIGGER
FOR TEST_TABLE1
ACTIVE
AFTER UPDATE
external name 'esp.TestTrigger.evaluate_field_test2_test4_update()'
engine JAVA;
commit;

UPDATE TEST_TABLE1 SET TEST1 = 'val5', TEST2 = 1005, TEST3 = CAST('01.01.2005 12:00' as TIMESTAMP);
commit;

CREATE OR ALTER TRIGGER TEST_TRIGGER
FOR TEST_TABLE1
ACTIVE
BEFORE UPDATE
external name 'esp.TestTrigger.do_not_evaluate_computed_fields_update()'
engine JAVA;
commit;

UPDATE TEST_TABLE1 SET TEST1 = 'val6', TEST2 = 1006, TEST3 = CAST('01.01.2006 12:00' as TIMESTAMP);
commit;

CREATE OR ALTER TRIGGER TEST_TRIGGER
FOR TEST_TABLE1
ACTIVE
AFTER UPDATE
external name 'esp.TestTrigger.do_not_evaluate_field_test2_do_not_evaluate_computed_fields_update()'
engine JAVA;
commit;

UPDATE TEST_TABLE1 SET TEST1 = 'val7', TEST2 = 1007, TEST3 = CAST('01.01.2007 12:00' as TIMESTAMP);
commit;
 
select * from TEST_TABLE2;
"""

act = isql_act('db', test_script)

expected_stdout = """
NEWTEST1   NEWTEST2   NEWTEST3                       NEWTEST4   OLDTEST1   OLDTEST2   OLDTEST3                       OLDTEST4
========== ========== ============================== ========== ========== ========== ============================== ==========
val1       1001       2001-01-01 12:00:00.0          COMPUTED   val0       1000       2000-01-01 12:00:00.0          COMPUTED
<null>     1002       2002-01-01 12:00:00.0          COMPUTED   <null>     1001       2001-01-01 12:00:00.0          COMPUTED
val3       <null>     2003-01-01 12:00:00.0          <null>     <null>     <null>     2002-01-01 12:00:00.0          <null>
val4       <null>     <null>                         <null>     val3       <null>     <null>                         <null>
<null>     1005       <null>                         COMPUTED   <null>     <null>     <null>                         COMPUTED
val6       1006       2006-01-01 12:00:00.0          <null>     val5       1005       2005-01-01 12:00:00.0          <null>
val7       <null>     2007-01-01 12:00:00.0          <null>     val6       <null>     2006-01-01 12:00:00.0          <null>
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
