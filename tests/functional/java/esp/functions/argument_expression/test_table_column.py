#coding:utf-8

"""
ID:          java.esp.functions.argument-expression.table-column
TITLE:       External function call with input parameter as a table column
DESCRIPTION: 
FBTEST:      functional.java.esp.functions.argument_expression.table_column
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
commit;
"""

db = db_factory(init=init_script)

test_script = """

select test_1(number) from test_table;
select test_2(number) from test_table;
select test_3(number) from test_table;
select test_4(number) from test_table;
select test_5(number) from test_table;
select test_6(number) from test_table;
select test_7(number) from test_table;
select test_8(number) from test_table;
select test_9(number) from test_table;
select test_10(number) from test_table;
select test_11(number) from test_table;
select test_12(name) from test_table;
select cast(test_13(name) as varchar(20)) as "TEST_13" from test_table;
select cast(test_14(name) as varchar(20)) as "TEST_14" from test_table;
select test_15(name) from test_table;
select test_16(name) from test_table;
select test_17(d) from test_table;
select test_18(t) from test_table;
select test_19(ts) from test_table;
select test_20(d) from test_table;
select test_21(flag) from test_table;
select test_22(flag) from test_table;
"""

act = isql_act('db', test_script)

expected_stdout = """        
TEST_1
============
23
TEST_2
============
23
TEST_3
=======
23
TEST_4
=======
23
TEST_5
=====================
23
TEST_6
=====================
23
TEST_7
=====================
23.00
TEST_8
==============
23.000000
TEST_9
==============
23.000000
TEST_10
=======================
23.00000000000000
TEST_11
=======================
23.00000000000000
TEST_12
====================
Ann
TEST_13
====================
Ann
TEST_14
====================
Ann
TEST_15
====================
Ann
TEST_16
==========
Ann
TEST_17
===========
1839-12-04
TEST_18
=============
23:45:00.0000
TEST_19
=========================
1839-12-04 23:45:00.0000
TEST_20
===========
1839-12-04
TEST_21
=======
<true>
TEST_22
=======
<true>
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
