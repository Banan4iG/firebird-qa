#coding:utf-8

"""
ID:          java.esp.functions.type-compatibility.lang-object
TITLE:       External function call with java.lang.Object type of result and input parameter
DESCRIPTION: 
  External function is declared with SQL types compatible with java.lang.Object Java type. Parameter as a constant.
FBTEST:      functional.java.esp.functions.type_compatibility.lang_object
"""

import pytest
from firebird.qa import *

init_script = """

create function test_1(i INTEGER) 
returns INTEGER
external name 'esp.TestFunction.ObjectInOut(Object)' 
engine java;
commit;

create function test_2(i SMALLINT) 
returns SMALLINT
external name 'esp.TestFunction.ObjectInOut(Object)'
engine java;
commit;


create function test_3(i BIGINT) 
returns BIGINT
external name 'esp.TestFunction.ObjectInOut(Object)'
engine java;
commit;

create function test_4(i NUMERIC(10,2)) 
returns NUMERIC(10,2)
external name 'esp.TestFunction.ObjectInOut(Object)'
engine java;
commit;

create function test_5(i DECIMAL(10,2)) 
returns DECIMAL(10,2)
external name 'esp.TestFunction.ObjectInOut(Object)'
engine java;
commit;

create function test_6(i FLOAT) 
returns FLOAT
external name 'esp.TestFunction.ObjectInOut(Object)'
engine java;
commit;

create function test_7(i DOUBLE PRECISION) 
returns DOUBLE PRECISION
external name 'esp.TestFunction.ObjectInOut(Object)'
engine java;
commit;

create function test_8(i CHAR(10)) 
returns CHAR(10)
external name 'esp.TestFunction.ObjectInOut(Object)'
engine java;
commit;

create function test_9(i VARCHAR(10)) 
returns VARCHAR(10)
external name 'esp.TestFunction.ObjectInOut(Object)'
engine java;
commit;

create function test_10(i BLOB) 
returns BLOB
external name 'esp.TestFunction.ObjectInOut(Object)'
engine java;
commit;

create function test_11(i DATE) 
returns DATE
external name 'esp.TestFunction.ObjectInOut(Object)'
engine java;
commit;

create function test_12(i TIME) 
returns TIME
external name 'esp.TestFunction.ObjectInOut(Object)'
engine java;
commit;

create function test_13(i TIMESTAMP) 
returns TIMESTAMP
external name 'esp.TestFunction.ObjectInOut(Object)'
engine java;
commit;

create function test_14(i BOOLEAN) 
returns BOOLEAN
external name 'esp.TestFunction.ObjectInOut(Object)'
engine java;
commit;
"""

db = db_factory(init=init_script)

test_script = """
SELECT TEST_1(5) FROM RDB$DATABASE;
SELECT TEST_1(-5.55) FROM RDB$DATABASE;
SELECT TEST_1(14.35) FROM RDB$DATABASE;
SELECT TEST_1(null) FROM RDB$DATABASE;

SELECT TEST_2(5) FROM RDB$DATABASE;
SELECT TEST_2(-5.55) FROM RDB$DATABASE;
SELECT TEST_2(14.35) FROM RDB$DATABASE;
SELECT TEST_2(null) FROM RDB$DATABASE;

SELECT TEST_3(5) FROM RDB$DATABASE;
SELECT TEST_3(-5.55) FROM RDB$DATABASE;
SELECT TEST_3(14.35) FROM RDB$DATABASE;
SELECT TEST_3(null) FROM RDB$DATABASE;

SELECT TEST_4(5) FROM RDB$DATABASE;
SELECT TEST_4(-5.55) FROM RDB$DATABASE;
SELECT TEST_4(14.35) FROM RDB$DATABASE;
SELECT TEST_4(null) FROM RDB$DATABASE;

SELECT TEST_5(5) FROM RDB$DATABASE;
SELECT TEST_5(-5.55) FROM RDB$DATABASE;
SELECT TEST_5(14.35) FROM RDB$DATABASE;
SELECT TEST_5(null) FROM RDB$DATABASE;

SELECT TEST_6(5) FROM RDB$DATABASE;
SELECT TEST_6(-5.55) FROM RDB$DATABASE;
SELECT TEST_6(14.35) FROM RDB$DATABASE;
SELECT TEST_6(null) FROM RDB$DATABASE;

SELECT TEST_7(5) FROM RDB$DATABASE;
SELECT TEST_7(-5.55) FROM RDB$DATABASE;
SELECT TEST_7(14.35) FROM RDB$DATABASE;
SELECT TEST_7(null) FROM RDB$DATABASE;

SELECT TEST_8('CHAR') FROM RDB$DATABASE;
SELECT TEST_8(null) FROM RDB$DATABASE;

SELECT TEST_9('VARCHAR') FROM RDB$DATABASE;
SELECT TEST_9(null) FROM RDB$DATABASE;

SELECT cast(TEST_10('BLOB') as varchar(10)) as "TEST_10" FROM RDB$DATABASE;
SELECT TEST_10(null) FROM RDB$DATABASE;

SELECT TEST_11('05.04.1902') FROM RDB$DATABASE;
SELECT TEST_11(null) FROM RDB$DATABASE;

SELECT TEST_12('12:45') FROM RDB$DATABASE;
SELECT TEST_12(null) FROM RDB$DATABASE;

SELECT TEST_13('05.04.1902 12:45') FROM RDB$DATABASE;
SELECT TEST_13(null) FROM RDB$DATABASE;

SELECT TEST_14(false) FROM RDB$DATABASE;
SELECT TEST_14(null) FROM RDB$DATABASE;
"""

act = isql_act('db', test_script)

expected_stdout = """          
TEST_1
============
5
TEST_1
============
-6
TEST_1
============
14
TEST_1
============
<null>
TEST_2
=======
5
TEST_2
=======
-6
TEST_2
=======
14
TEST_2
=======
<null>
TEST_3
=====================
5
TEST_3
=====================
-6
TEST_3
=====================
14
TEST_3
=====================
<null>
TEST_4
=====================
5.00
TEST_4
=====================
-5.55
TEST_4
=====================
14.35
TEST_4
=====================
<null>
TEST_5
=====================
5.00
TEST_5
=====================
-5.55
TEST_5
=====================
14.35
TEST_5
=====================
<null>
TEST_6
==============
5.0000000
TEST_6
==============
-5.5500002
TEST_6
==============
14.350000
TEST_6
==============
<null>
TEST_7
=======================
5.000000000000000
TEST_7
=======================
-5.550000000000000
TEST_7
=======================
14.35000000000000
TEST_7
=======================
<null>
TEST_8
==========
CHAR
TEST_8
==========
<null>
TEST_9
==========
VARCHAR
TEST_9
==========
<null>
TEST_10
==========
BLOB
TEST_10
=================
<null>
TEST_11
===========
1902-04-05
TEST_11
===========
<null>
TEST_12
=============
12:45:00.0000
TEST_12
=============
<null>
TEST_13
=========================
1902-04-05 12:45:00.0000
TEST_13
=========================
<null>
TEST_14
=======
<false>
TEST_14
=======
<null>
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
