#coding:utf-8

"""
ID:          java.esp.trigger.context.insert-before
TITLE:       Get context of BEFORE INSERT trigger
DESCRIPTION: 
FBTEST:      functional.java.esp.trigger.context.insert_before
"""

import pytest
from firebird.qa import *

# version: 3.0

substitutions_1 = [('org.firebirdsql.jdbc.FBBlob@.*', 'org.firebirdsql.jdbc.FBBlob@'), ('javax.sql.rowset.serial.SerialBlob@.*', 'javax.sql.rowset.serial.SerialBlob@')]

init_script_1 = """
CREATE TABLE TEST_TABLE(F_VARCHAR VARCHAR(30), F_BLOB BLOB);
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

db_1 = db_factory(init=init_script_1)

test_script_1 = """
 
INSERT INTO TEST_TABLE VALUES ('It is new value', 'blob value');
 
SELECT cast(F_BLOB as varchar(100)) FROM TEST_TABLE;
 
SELECT context FROM CONTEXT_TABLE;
"""

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
CAST
===============================================================================
It is new value from Java
CONTEXT
===============================================================================
Action: INSERT
Table name: TEST_TABLE
Type: BEFORE
Info stored at entry point metadata: null
Object name called trigger: TEST_TRIGGER
Field name: F_VARCHAR
Field class: class java.lang.Object
Old value: null
New value: It is new value
New value after set: It is new value from Java
Field name: F_BLOB
Field class: class java.lang.Object
Old value: null
New value: org.firebirdsql.jdbc.FBBlob@
New value after set: javax.sql.rowset.serial.SerialBlob@
"""

@pytest.mark.java
@pytest.mark.version('>=3.0,<4.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_stdout == act_1.clean_expected_stdout

# version: 4.0

substitutions_2 = [('org.firebirdsql.jdbc.FBBlob@.*', 'org.firebirdsql.jdbc.FBBlob@'), ('javax.sql.rowset.serial.SerialBlob@.*', 'javax.sql.rowset.serial.SerialBlob@')]

init_script_2 = """
CREATE TABLE TEST_TABLE(F_VARCHAR VARCHAR(30), F_BLOB BLOB);
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

db_2 = db_factory(init=init_script_2)

test_script_2 = """

INSERT INTO TEST_TABLE VALUES ('It is new value', 'blob value');

SELECT cast(F_BLOB as varchar(100)) FROM TEST_TABLE;

SELECT context FROM CONTEXT_TABLE;
"""

act_2 = isql_act('db_2', test_script_2, substitutions=substitutions_2)

expected_stdout_2 = """
CAST
====================================================================================================
It is new value from Java
CONTEXT
================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
Action: INSERT
Table name: TEST_TABLE
Type: BEFORE
Info stored at entry point metadata: null
Object name called trigger: TEST_TRIGGER
Field name: F_VARCHAR
Field class: class java.lang.Object
Old value: null
New value: It is new value
New value after set: It is new value from Java
Field name: F_BLOB
Field class: class java.lang.Object
Old value: null
New value: org.firebirdsql.jdbc.FBBlob@
New value after set: javax.sql.rowset.serial.SerialBlob@
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
