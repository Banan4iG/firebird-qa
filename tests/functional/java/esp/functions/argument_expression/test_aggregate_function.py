#coding:utf-8

"""
ID:          java.esp.functions.argument-expression.aggregate-function
TITLE:       External function call with input parameter as a aggregate function
DESCRIPTION: 
FBTEST:      functional.java.esp.functions.argument_expression.aggregate_function
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

create table test_table(id integer unique, number integer, name varchar(20), d date, t time, ts timestamp, flag boolean);
insert into test_table values(1, 23, 'Ann', '04.12.1839', '23:45', '04.12.1839 23:45', true);
insert into test_table values(2, 46, 'Peter', '23.05.2000', '09:36', '23.05.2000 09:36', false);
commit;
"""

db = db_factory(init=init_script)

test_script = """

select test_1((select max(number) from test_table)) from rdb$database;
select test_2((select min(number) from test_table)) from rdb$database;
select test_3((select max(number) from test_table)) from rdb$database;
select test_4((select min(number) from test_table)) from rdb$database;
select test_5((select max(number) from test_table)) from rdb$database;
select test_6((select min(number) from test_table)) from rdb$database;
select test_7((select max(number) from test_table)) from rdb$database;
select test_8((select min(number) from test_table)) from rdb$database;
select test_9((select max(number) from test_table)) from rdb$database;
select test_10((select min(number) from test_table)) from rdb$database;
select test_11((select max(number) from test_table)) from rdb$database;
select test_12((select list(name) from test_table)) from rdb$database;
select cast(test_13((select list(name) from test_table)) as varchar(20)) as "TEST_13" from rdb$database;
select cast(test_14((select list(name) from test_table)) as varchar(20)) as "TEST_14" from rdb$database;
select test_15((select list(name) from test_table)) from rdb$database;
select test_16((select list(name) from test_table)) from rdb$database;
select test_17((select max(d) from test_table)) from rdb$database;
select test_18((select max(t) from test_table)) from rdb$database;
select test_19((select max(ts) from test_table)) from rdb$database;
select test_20((select max(d) from test_table)) from rdb$database;
select test_21((select max(flag) from test_table)) from rdb$database;
select test_22((select min(flag) from test_table)) from rdb$database;
"""

act = isql_act('db', test_script)

expected_stdout = """        
TEST_1
============
46
TEST_2
============
23
TEST_3
=======
46
TEST_4
=======
23
TEST_5
=====================
46
TEST_6
=====================
23
TEST_7
=====================
46.00
TEST_8
==============
23.000000
TEST_9
==============
46.000000
TEST_10
=======================
23.00000000000000
TEST_11
=======================
46.00000000000000
TEST_12
====================
Ann,Peter
TEST_13
====================
Ann,Peter
TEST_14
====================
Ann,Peter
TEST_15
====================
Ann,Peter
TEST_16
==========
Ann,Peter
TEST_17
===========
2000-05-23
TEST_18
=============
23:45:00.0000
TEST_19
=========================
2000-05-23 09:36:00.0000
TEST_20
===========
2000-05-23
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
