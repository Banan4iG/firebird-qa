#coding:utf-8

"""
ID:          java.esp.functions.argument-expression.imbedded-function
TITLE:       External function call with input parameter as a common imbedded function
DESCRIPTION: 
FBTEST:      functional.java.esp.functions.argument_expression.imbedded_function
"""

import pytest
from firebird.qa import *

# version: 3.0

init_script_1 = """
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

create function test_12(i VARCHAR(20)) 
returns VARCHAR(20)
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

create function test_15(i VARCHAR(20)) 
returns VARCHAR(20)
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

create function test_18(i TIME) 
returns TIME
external name 'esp.TestFunction.timeInOut(java.sql.Time)'
engine java;
commit;

create function test_19(i TIMESTAMP) 
returns TIMESTAMP
external name 'esp.TestFunction.timeStampInOut(java.sql.Timestamp)'
engine java;
commit;

create function test_20(i DATE) 
returns DATE
external name 'esp.TestFunction.utilDateInOut(java.util.Date)'
engine java;
commit;
"""

db_1 = db_factory(init=init_script_1)

test_script_1 = """
SELECT TEST_1(SQRT(4.5)) FROM RDB$DATABASE;

SELECT TEST_2(exp(2)) FROM RDB$DATABASE;

SELECT TEST_3(pi()) FROM RDB$DATABASE;

SELECT TEST_4(mod(7.5,2.5)) FROM RDB$DATABASE;

SELECT TEST_5(log(2,4)) FROM RDB$DATABASE;

SELECT TEST_6(floor(4.5)) FROM RDB$DATABASE;

SELECT TEST_7(sin(0.5)) FROM RDB$DATABASE;

SELECT TEST_8(abs(4.5)) FROM RDB$DATABASE;

SELECT TEST_9(cos(1.5)) FROM RDB$DATABASE;

SELECT TEST_10(atan(1)) FROM RDB$DATABASE;

SELECT TEST_11(power(3,2)) FROM RDB$DATABASE;

SELECT TEST_12(left('abcdef',2)) FROM RDB$DATABASE;

SELECT cast(TEST_13(RIGHT('abcdef',2)) as varchar(10)) as "TEST_13" FROM RDB$DATABASE;

SELECT cast(TEST_14(TRIM('a' from 'aaabcdsaefa')) as varchar(10)) as "TEST_14" FROM RDB$DATABASE;

SELECT TEST_15(UPPER('abc')) FROM RDB$DATABASE;

SELECT TEST_16(LOWER('ABc')) FROM RDB$DATABASE;

SELECT TEST_17(DATEADD(5 year to cast('10.03.2014' as date))) FROM RDB$DATABASE;

SELECT TEST_18(DATEADD(2 hour to cast('10:35' as time))) FROM RDB$DATABASE;

SELECT TEST_19(DATEADD(2 hour to cast('10.03.2014 10:35' as timestamp))) FROM RDB$DATABASE;

SELECT TEST_20(DATEADD(5 year to cast('10.03.2014' as date))) FROM RDB$DATABASE;
"""

act_1 = isql_act('db_1', test_script_1)

expected_stdout_1 = """        
TEST_1
============
2
TEST_2
============
7
TEST_3
=======
3
TEST_4
=======
2
TEST_5
=====================
2
TEST_6
=====================
4
TEST_7
=====================
0.48
TEST_8
==============
4.5000000
TEST_9
==============
0.070737198
TEST_10
=======================
0.7853981633974483
TEST_11
=======================
9.000000000000000
TEST_12
====================
ab
TEST_13
==========
ef
TEST_14
==========
bcdsaef
TEST_15
====================
ABC
TEST_16
==========
abc
TEST_17
===========
2019-03-10
TEST_18
=============
12:35:00.0000
TEST_19
=========================
2014-03-10 12:35:00.0000
TEST_20
===========
2019-03-10
"""

@pytest.mark.java
@pytest.mark.version('>=3.0,<4.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_stdout == act_1.clean_expected_stdout

# version: 4.0

init_script_2 = """
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

create function test_12(i VARCHAR(20))
returns VARCHAR(20)
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

create function test_15(i VARCHAR(20))
returns VARCHAR(20)
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

create function test_18(i TIME)
returns TIME
external name 'esp.TestFunction.timeInOut(java.sql.Time)'
engine java;
commit;

create function test_19(i TIMESTAMP)
returns TIMESTAMP
external name 'esp.TestFunction.timeStampInOut(java.sql.Timestamp)'
engine java;
commit;

create function test_20(i DATE)
returns DATE
external name 'esp.TestFunction.utilDateInOut(java.util.Date)'
engine java;
commit;
"""

db_2 = db_factory(init=init_script_2)

test_script_2 = """
SELECT TEST_1(SQRT(4.5)) FROM RDB$DATABASE;

SELECT TEST_2(exp(2)) FROM RDB$DATABASE;

SELECT TEST_3(pi()) FROM RDB$DATABASE;

SELECT TEST_4(mod(7.5,2.5)) FROM RDB$DATABASE;

SELECT TEST_5(log(2,4)) FROM RDB$DATABASE;

SELECT TEST_6(floor(4.5)) FROM RDB$DATABASE;

SELECT TEST_7(sin(0.5)) FROM RDB$DATABASE;

SELECT TEST_8(abs(4.5)) FROM RDB$DATABASE;

SELECT TEST_9(cos(1.5)) FROM RDB$DATABASE;

SELECT TEST_10(atan(1)) FROM RDB$DATABASE;

SELECT TEST_11(power(3,2)) FROM RDB$DATABASE;

SELECT TEST_12(left('abcdef',2)) FROM RDB$DATABASE;

SELECT cast(TEST_13(RIGHT('abcdef',2)) as varchar(10)) as "TEST_13" FROM RDB$DATABASE;

SELECT cast(TEST_14(TRIM('a' from 'aaabcdsaefa')) as varchar(10)) as "TEST_14" FROM RDB$DATABASE;

SELECT TEST_15(UPPER('abc')) FROM RDB$DATABASE;

SELECT TEST_16(LOWER('ABc')) FROM RDB$DATABASE;

SELECT TEST_17(DATEADD(5 year to cast('10.03.2014' as date))) FROM RDB$DATABASE;

SELECT TEST_18(DATEADD(2 hour to cast('10:35' as time))) FROM RDB$DATABASE;

SELECT TEST_19(DATEADD(2 hour to cast('10.03.2014 10:35' as timestamp))) FROM RDB$DATABASE;

SELECT TEST_20(DATEADD(5 year to cast('10.03.2014' as date))) FROM RDB$DATABASE;
"""

act_2 = isql_act('db_2', test_script_2)

expected_stdout_2 = """
TEST_1
============
2
TEST_2
============
7
TEST_3
=======
3
TEST_4
=======
2
TEST_5
=====================
2
TEST_6
=====================
4
TEST_7
=====================
0.48
TEST_8
==============
4.5000000
TEST_9
==============
0.070737198
TEST_10
=======================
0.7853981633974483
TEST_11
=======================
9.000000000000000
TEST_12
====================
ab
TEST_13
==========
ef
TEST_14
==========
bcdsaef
TEST_15
====================
ABC
TEST_16
==========
abc
TEST_17
===========
2019-03-10
TEST_18
=============
12:35:00.0000
TEST_19
=========================
2014-03-10 12:35:00.0000
TEST_20
===========
2019-03-10
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
