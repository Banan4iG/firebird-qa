#coding:utf-8

"""
ID:          java.esp.functions.argument-expression.external-function
TITLE:       External function call with input parameter as other external function
DESCRIPTION: 
FBTEST:      functional.java.esp.functions.argument_expression.external_function
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

create function test_21(i BOOLEAN) 
returns BOOLEAN
external name 'esp.TestFunction.boolInOut(boolean)' 
engine java;
commit;

create function test_22(i boolean) 
returns boolean
external name 'esp.TestFunction.BoolInOut(Boolean)' 
engine java;
commit;

"""

db = db_factory(init=init_script)

test_script = """

select test_1(test_2(34)) from rdb$database;
select test_2(test_1(34)) from rdb$database;
select test_3(test_1(34)) from rdb$database;
select test_4(test_2(34)) from rdb$database;
select test_5(test_4(34)) from rdb$database;
select test_6(test_3(34)) from rdb$database;
select test_7(test_5(34)) from rdb$database;
select test_8(test_6(34)) from rdb$database;
select test_9(test_8(34)) from rdb$database;
select test_10(test_7(34)) from rdb$database;
select test_11(test_10(34)) from rdb$database;

select test_12(test_1(34)) from rdb$database;
select cast(test_13(test_2(34)) as varchar(20)) as "TEST_13" from rdb$database;
select cast(test_14(test_3(34)) as varchar(20)) as "TEST_14" from rdb$database;
select test_15(test_4(34)) from rdb$database;
select test_16(test_12('test')) from rdb$database;

select test_17(test_13('05.03.2012')) from rdb$database;
select test_18(test_14('06:34')) from rdb$database;
select test_19(test_15('05.03.2012 06:34')) from rdb$database;
select test_20(test_16('05.03.2012')) from rdb$database;

select test_21(test_12('true')) from rdb$database;
select test_22(test_21(false)) from rdb$database;
"""

act = isql_act('db', test_script)

expected_stdout = """        
TEST_1
============
34
TEST_2
============
34
TEST_3
=======
34
TEST_4
=======
34
TEST_5
=====================
34
TEST_6
=====================
34
TEST_7
=====================
34.00
TEST_8
==============
34.000000
TEST_9
==============
34.000000
TEST_10
=======================
34.00000000000000
TEST_11
=======================
34.00000000000000
TEST_12
====================
34
TEST_13
====================
34
TEST_14
====================
34
TEST_15
====================
34
TEST_16
==========
test
TEST_17
===========
2012-03-05
TEST_18
=============
06:34:00.0000
TEST_19
=========================
2012-03-05 06:34:00.0000
TEST_20
===========
2012-03-05
TEST_21
=======
<true>
TEST_22
=======
<false>
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
