#coding:utf-8

"""
ID:          java.esp.functions.type-compatibility.float
TITLE:       External function call with float type of result and input parameter
DESCRIPTION: 
  External function is declared with SQL types compatible with float Java type. Parameter as a constant.
FBTEST:      functional.java.esp.functions.type_compatibility.float
"""

import pytest
from firebird.qa import *

init_script = """
create function test_1(i smallint) 
returns smallint
external name 'esp.TestFunction.floatInOut(float)'
engine java;
commit;

create function test_2(i integer) 
returns integer
external name 'esp.TestFunction.floatInOut(float)'
engine java;
commit;

create function test_3(i BIGINT) 
returns BIGINT
external name 'esp.TestFunction.floatInOut(float)'
engine java;
commit;

create function test_4(i NUMERIC(10,2)) 
returns NUMERIC(10,2)
external name 'esp.TestFunction.floatInOut(float)'
engine java;
commit;

create function test_5(i DECIMAL(10,2)) 
returns DECIMAL(10,2)
external name 'esp.TestFunction.floatInOut(float)'
engine java;
commit;

create function test_6(i FLOAT) 
returns FLOAT
external name 'esp.TestFunction.floatInOut(float)'
engine java;
commit;

create function test_7(i DOUBLE PRECISION) 
returns DOUBLE PRECISION
external name 'esp.TestFunction.floatInOut(float)'
engine java;
commit;

create function test_8(i CHAR(10)) 
returns CHAR(10)
external name 'esp.TestFunction.floatInOut(float)'
engine java;
commit;

create function test_9(i VARCHAR(10)) 
returns VARCHAR(10)
external name 'esp.TestFunction.floatInOut(float)'
engine java;
commit;

create function test_10(i BLOB) 
returns BLOB
external name 'esp.TestFunction.floatInOut(float)'
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

SELECT TEST_8('5') FROM RDB$DATABASE;
SELECT TEST_8('-5.55') FROM RDB$DATABASE;
SELECT TEST_8('14.35') FROM RDB$DATABASE;
SELECT TEST_8(null) FROM RDB$DATABASE;

SELECT TEST_9('5') FROM RDB$DATABASE;
SELECT TEST_9('-5.55') FROM RDB$DATABASE;
SELECT TEST_9('14.35') FROM RDB$DATABASE;
SELECT TEST_9(null) FROM RDB$DATABASE;

SELECT cast(TEST_10('5') as varchar(10)) as "TEST_10" FROM RDB$DATABASE;
SELECT cast(TEST_10('-5.55') as varchar(10)) as "TEST_10" FROM RDB$DATABASE;
SELECT cast(TEST_10('14.35') as varchar(10)) as "TEST_10" FROM RDB$DATABASE;
SELECT cast(TEST_10(null) as varchar(10)) as "TEST_10" FROM RDB$DATABASE;
"""

act = isql_act('db', test_script, substitutions=[('\\.00000(0)*', '.000000000000000')])

expected_stdout = """          
TEST_1
=======
5
TEST_1
=======
-6
TEST_1
=======
14
TEST_1
=======
0
TEST_2
============
5
TEST_2
============
-6
TEST_2
============
14
TEST_2
============
0
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
0
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
0.00
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
0.00
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
0.0000000
TEST_7
=======================
5.000000000000000
TEST_7
=======================
-5.550000190734863
TEST_7
=======================
14.35000038146973
TEST_7
=======================
0.000000000000000
TEST_8
==========
5.0000000
TEST_8
==========
-5.5500002
TEST_8
==========
14.350000
TEST_8
==========
0.0000000
TEST_9
==========
5.0000000
TEST_9
==========
-5.5500002
TEST_9
==========
14.350000
TEST_9
==========
0.0000000
TEST_10
==========
5.0000000
TEST_10
==========
-5.5500002
TEST_10
==========
14.350000
TEST_10
==========
0.0000000
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
