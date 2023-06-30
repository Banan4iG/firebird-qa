#coding:utf-8

"""
ID:          java.esp.functions.type-compatibility.sql-time
TITLE:       External function call with java.sql.Time type of result and input parameter
DESCRIPTION: 
  External function is declared with SQL types compatible with java.sql.Time Java type. Parameter as a constant.
FBTEST:      functional.java.esp.functions.type_compatibility.sql_time
"""

import pytest
from firebird.qa import *

# version: 3.0

substitutions_1 = [('\\d{4}-\\d{2}-\\d{2}\\s\\d{2}:\\d{2}:\\d{2}\\.\\d{4}', '23:49:00.0000')]

init_script_1 = """
create function test_1(i CHAR(15)) 
returns CHAR(15)
external name 'esp.TestFunction.timeInOut(java.sql.Time)'
engine java;
commit;

create function test_2(i VARCHAR(15)) 
returns VARCHAR(15)
external name 'esp.TestFunction.timeInOut(java.sql.Time)'
engine java;
commit;

create function test_3(i BLOB) 
returns BLOB
external name 'esp.TestFunction.timeInOut(java.sql.Time)'
engine java;
commit;

create function test_4(i TIME) 
returns TIME
external name 'esp.TestFunction.timeInOut(java.sql.Time)'
engine java;
commit;

create function test_5(i TIMESTAMP) 
returns TIMESTAMP
external name 'esp.TestFunction.timeInOut(java.sql.Time)'
engine java;
commit;
"""

db_1 = db_factory(init=init_script_1)

test_script_1 = """
 
SELECT TEST_1('11:58:59') FROM RDB$DATABASE;
SELECT TEST_1('11.58.59.4043') FROM RDB$DATABASE;

SELECT TEST_2('09:00:34.345') FROM RDB$DATABASE;
SELECT TEST_2('09.00.34.345') FROM RDB$DATABASE;

SELECT cast(TEST_3('17:34') as varchar(15)) as "TEST_3" FROM RDB$DATABASE;
SELECT cast(TEST_3('17.34') as varchar(15)) as "TEST_3" FROM RDB$DATABASE;

SELECT TEST_4('07:27:47') FROM RDB$DATABASE;
SELECT TEST_4('07.27.47') FROM RDB$DATABASE;

SELECT TEST_5('23.09.1935 23:49') FROM RDB$DATABASE;
SELECT TEST_5('23.09.1935 23.49') FROM RDB$DATABASE;
"""

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """         
TEST_1
===============
11:58:59.0000
TEST_1
===============
11:58:59.4040
TEST_2
===============
09:00:34.3450
TEST_2
===============
09:00:34.3450
TEST_3
===============
17:34:00.0000
TEST_3
===============
17:34:00.0000
TEST_4
=============
07:27:47.0000
TEST_4
=============
07:27:47.0000
TEST_5
=========================
23:49:00.0000
TEST_5
=========================
23:49:00.0000
"""

@pytest.mark.java
@pytest.mark.version('>=3.0,<4.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_stdout == act_1.clean_expected_stdout

# version: 4.0

substitutions_2 = [('\\d{4}-\\d{2}-\\d{2}\\s\\d{2}:\\d{2}:\\d{2}\\.\\d{4}', '23:49:00.0000')]

init_script_2 = """
create function test_1(i CHAR(15))
returns CHAR(15)
external name 'esp.TestFunction.timeInOut(java.sql.Time)'
engine java;
commit;

create function test_2(i VARCHAR(15))
returns VARCHAR(15)
external name 'esp.TestFunction.timeInOut(java.sql.Time)'
engine java;
commit;

create function test_3(i BLOB)
returns BLOB
external name 'esp.TestFunction.timeInOut(java.sql.Time)'
engine java;
commit;

create function test_4(i TIME)
returns TIME
external name 'esp.TestFunction.timeInOut(java.sql.Time)'
engine java;
commit;

create function test_5(i TIMESTAMP)
returns TIMESTAMP
external name 'esp.TestFunction.timeInOut(java.sql.Time)'
engine java;
commit;
"""

db_2 = db_factory(init=init_script_2)

test_script_2 = """

SELECT TEST_1('11:58:59') FROM RDB$DATABASE;

SELECT TEST_2('09:00:34.345') FROM RDB$DATABASE;

SELECT cast(TEST_3('17:34') as varchar(15)) as "TEST_3" FROM RDB$DATABASE;

SELECT TEST_4('07:27:47') FROM RDB$DATABASE;

SELECT TEST_5('23.09.1935 23:49') FROM RDB$DATABASE;
"""

act_2 = isql_act('db_2', test_script_2, substitutions=substitutions_2)

expected_stdout_2 = """
TEST_1
===============
11:58:59.0000
TEST_2
===============
09:00:34.3450
TEST_3
===============
17:34:00.0000
TEST_4
=============
07:27:47.0000
TEST_5
=========================
23:49:00.0000
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
