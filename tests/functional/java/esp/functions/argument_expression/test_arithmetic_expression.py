#coding:utf-8

"""
ID:          java.esp.functions.argument-expression.arithmetic-expression
TITLE:       External function call with input parameter as an arithmetic expression
DESCRIPTION: 
FBTEST:      functional.java.esp.functions.argument_expression.arithmetic_expression
"""

import pytest
from firebird.qa import *

init_script = """
create function test_1(i INTEGER) 
returns INTEGER
external name 'esp.TestFunction.integerInOut(Integer)' 
engine java;
commit;

create function test_2(i INTEGER) 
returns INTEGER
external name 'esp.TestFunction.intInOut(int)' 
engine java;
commit;


create function test_3(i SMALLINT) 
returns SMALLINT
external name 'esp.TestFunction.ShortInOut(Short)'
engine java;
commit;

create function test_4(i SMALLINT) 
returns SMALLINT
external name 'esp.TestFunction.shortInOut(short)'
engine java;
commit;

create function test_5(i BIGINT) 
returns BIGINT
external name 'esp.TestFunction.LongInOut(Long)'
engine java;
commit;

create function test_6(i BIGINT) 
returns BIGINT
external name 'esp.TestFunction.longInOut(long)'
engine java;
commit;

create function test_7(i NUMERIC(10,2)) 
returns NUMERIC(10,2)
external name 'esp.TestFunction.bigDecimalInOut(java.math.BigDecimal)'
engine java;
commit;

create function test_8(i FLOAT) 
returns FLOAT
external name 'esp.TestFunction.floatInOut(float)'
engine java;
commit;

create function test_9(i FLOAT) 
returns FLOAT
external name 'esp.TestFunction.FloatInOut(Float)'
engine java;
commit;

create function test_10(i DOUBLE PRECISION) 
returns DOUBLE PRECISION
external name 'esp.TestFunction.doubleInOut(double)'
engine java;
commit;

create function test_11(i DOUBLE PRECISION) 
returns DOUBLE PRECISION
external name 'esp.TestFunction.DoubleInOut(Double)'
engine java;
commit;

create function test_12(i CHAR(10)) 
returns CHAR(10)
external name 'esp.TestFunction.stringInOut(String)'
engine java;
commit;

create function test_13(i BLOB) 
returns BLOB
external name 'esp.TestFunction.blobInOut2(java.sql.Blob)'
engine java;
commit;

create function test_14(i BLOB) 
returns BLOB
external name 'esp.TestFunction.blobInOut(org.firebirdsql.jdbc.FirebirdBlob)'
engine java;
commit;

create function test_15(i INTEGER) 
returns INTEGER
external name 'esp.TestFunction.ObjectInOut(Object)'
engine java;
commit;

create function test_16(i VARCHAR(10)) 
returns VARCHAR(10)
external name 'esp.TestFunction.byteInOut(byte[])'
engine java;
commit;

create function test_17(i DATE) 
returns DATE
external name 'esp.TestFunction.dateInOut(java.sql.Date)'
engine java;
commit;

create function test_18(i DATE) 
returns DATE
external name 'esp.TestFunction.utilDateInOut(java.util.Date)'
engine java;
commit;

create function test_19(i TIME) 
returns TIME
external name 'esp.TestFunction.timeInOut(java.sql.Time)'
engine java;
commit;
"""

db = db_factory(init=init_script)

test_script = """
SELECT TEST_1(1+1) FROM RDB$DATABASE;
SELECT TEST_1(-3.2*2+5) FROM RDB$DATABASE;

SELECT TEST_2(1+1) FROM RDB$DATABASE;
SELECT TEST_2(-3.2*2+5) FROM RDB$DATABASE;

SELECT TEST_3(1+1) FROM RDB$DATABASE;
SELECT TEST_3(-3.2*2+5) FROM RDB$DATABASE;

SELECT TEST_4(1+1) FROM RDB$DATABASE;
SELECT TEST_4(-3.2*2+5) FROM RDB$DATABASE;

SELECT TEST_5(1+1) FROM RDB$DATABASE;
SELECT TEST_5(-3.2*2+5) FROM RDB$DATABASE;

SELECT TEST_6(1+1) FROM RDB$DATABASE;
SELECT TEST_6(-3.2*2+5) FROM RDB$DATABASE;

SELECT TEST_7(1+1) FROM RDB$DATABASE;
SELECT TEST_7(-3.2*2+5) FROM RDB$DATABASE;

SELECT TEST_8(1+1) FROM RDB$DATABASE;
SELECT TEST_8(-3.2*2+5) FROM RDB$DATABASE;

SELECT TEST_9(1+1) FROM RDB$DATABASE;
SELECT TEST_9(-3.2*2+5) FROM RDB$DATABASE;

SELECT cast(TEST_10(1+1) as varchar(10)) as "TEST_10" FROM RDB$DATABASE;
SELECT cast(TEST_10(-3.2*2+5) as varchar(10)) as "TEST_10" FROM RDB$DATABASE;

SELECT TEST_11(1+1) FROM RDB$DATABASE;
SELECT TEST_11(-3.2*2+5) FROM RDB$DATABASE;

SELECT TEST_12(1+1) FROM RDB$DATABASE;
SELECT TEST_12(-3.2*2+5) FROM RDB$DATABASE;

SELECT cast(TEST_13(1+1) as varchar(10)) as "TEST_13" FROM RDB$DATABASE;
SELECT cast(TEST_13(-3.2*2+5) as varchar(10)) as "TEST_13" FROM RDB$DATABASE;

SELECT cast(TEST_14(1+1) as varchar(10)) as "TEST_14" FROM RDB$DATABASE;
SELECT cast(TEST_14(-3.2*2+5) as varchar(10)) as "TEST_14" FROM RDB$DATABASE;

SELECT TEST_15(1+1) FROM RDB$DATABASE;
SELECT TEST_15(-3.2*2+5) FROM RDB$DATABASE;

SELECT TEST_16(1+1) FROM RDB$DATABASE;
SELECT TEST_16(-3.2*2+5) FROM RDB$DATABASE;

SELECT TEST_17(cast('30.09.2012' as date) +1) FROM RDB$DATABASE;
SELECT TEST_17(cast('01.10.2012' as date) -1) FROM RDB$DATABASE;

SELECT TEST_18(cast('30.09.2012' as date) +1) FROM RDB$DATABASE;
SELECT TEST_18(cast('01.10.2012' as date) - 1 ) FROM RDB$DATABASE;

SELECT TEST_19(cast('04:09' as time) +1) FROM RDB$DATABASE;
SELECT TEST_19(cast('04:09' as time) -1) FROM RDB$DATABASE;
"""

act = isql_act('db', test_script)

expected_stdout = """        
TEST_1
============
2
TEST_1
============
-1
TEST_2
============
2
TEST_2
============
-1
TEST_3
=======
2
TEST_3
=======
-1
TEST_4
=======
2
TEST_4
=======
-1
TEST_5
=====================
2
TEST_5
=====================
-1
TEST_6
=====================
2
TEST_6
=====================
-1
TEST_7
=====================
2.00
TEST_7
=====================
-1.40
TEST_8
==============
2.0000000
TEST_8
==============
-1.4000000
TEST_9
==============
2.0000000
TEST_9
==============
-1.4000000
TEST_10
==========
2.0000000
TEST_10
==========
-1.4000000
TEST_11
=======================
2.000000000000000
TEST_11
=======================
-1.400000000000000
TEST_12
==========
2
TEST_12
==========
-1.4
TEST_13
==========
2
TEST_13
==========
-1.4
TEST_14
==========
2
TEST_14
==========
-1.4
TEST_15
============
2
TEST_15
============
-1
TEST_16
==========
2
TEST_16
==========
-1.4

TEST_17
===========
2012-10-01

TEST_17
===========
2012-09-30

TEST_18
===========
2012-10-01

TEST_18
===========
2012-09-30

TEST_19
=============
04:09:01.0000

TEST_19
=============
04:08:59.0000
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
