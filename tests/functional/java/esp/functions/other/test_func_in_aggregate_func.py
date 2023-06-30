#coding:utf-8

"""
ID:          java.esp.functions.other.func-in-aggregate-func
TITLE:       External functions as an expression of the aggregate function
DESCRIPTION: 
FBTEST:      functional.java.esp.functions.other.func_in_aggregate_func
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

db_1 = db_factory(init=init_script_1)

test_script_1 = """
SELECT MAX(TEST_1(12)) FROM RDB$DATABASE;

SELECT MIN(TEST_2(12)) FROM RDB$DATABASE;

SELECT AVG(TEST_3(12)) FROM RDB$DATABASE;

SELECT MAX(TEST_4(12)) FROM RDB$DATABASE;

SELECT MIN(TEST_5(12)) FROM RDB$DATABASE;

SELECT AVG(TEST_6(12)) FROM RDB$DATABASE;

SELECT MAX(TEST_7(12)) FROM RDB$DATABASE;

SELECT MIN(TEST_8(12)) FROM RDB$DATABASE;

SELECT AVG(TEST_9(12)) FROM RDB$DATABASE;

SELECT MAX(TEST_10(12)) FROM RDB$DATABASE;

SELECT MIN(TEST_11(12)) FROM RDB$DATABASE;

SELECT cast(LIST(TEST_12('test')) as varchar(30))  as "LIST" FROM RDB$DATABASE;

SELECT cast(MAX(TEST_13('test')) as varchar(10)) as "TEST_10" FROM RDB$DATABASE;

SELECT cast(MIN(TEST_14('test')) as varchar(10)) as "TEST_10" FROM RDB$DATABASE;

SELECT cast(LIST(TEST_15('test')) as varchar(30)) as "LIST" FROM RDB$DATABASE;

SELECT MAX(TEST_16('test')) FROM RDB$DATABASE;

SELECT MAX(TEST_17('10.11.1982')) FROM RDB$DATABASE;

SELECT MAX(TEST_18('23:45')) FROM RDB$DATABASE;

SELECT cast(LIST(TEST_19('10.11.1982 23:45')) as varchar(30))  as "LIST" FROM RDB$DATABASE;

SELECT MAX(TEST_20('10.11.1982')) FROM RDB$DATABASE;

SELECT MAX(TEST_21(true)) FROM RDB$DATABASE;

SELECT MAX(TEST_22(false)) FROM RDB$DATABASE;
"""

act_1 = isql_act('db_1', test_script_1)

expected_stdout_1 = """        
MAX
============
12
MIN
============
12
AVG
=====================
12
MAX
=======
12
MIN
=====================
12
AVG
=====================
12
MAX
=====================
12.00
MIN
==============
12.000000
AVG
=======================
12.00000000000000
MAX
=======================
12.00000000000000
MIN
=======================
12.00000000000000
LIST
==============================
test
TEST_10
==========
test
TEST_10
==========
test
LIST
==============================
test
MAX
==========
test
MAX
===========
1982-11-10
MAX
=============
23:45:00.0000
LIST
==============================
1982-11-10 23:45:00.0000
MAX
===========
1982-11-10
MAX
=======
<true>
MAX
=======
<false>
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

db_2 = db_factory(init=init_script_2)

test_script_2 = """
SELECT MAX(TEST_1(12)) FROM RDB$DATABASE;

SELECT MIN(TEST_2(12)) FROM RDB$DATABASE;

SELECT AVG(TEST_3(12)) FROM RDB$DATABASE;

SELECT MAX(TEST_4(12)) FROM RDB$DATABASE;

SELECT MIN(TEST_5(12)) FROM RDB$DATABASE;

SELECT AVG(TEST_6(12)) FROM RDB$DATABASE;

SELECT MAX(TEST_7(12)) FROM RDB$DATABASE;

SELECT MIN(TEST_8(12)) FROM RDB$DATABASE;

SELECT AVG(TEST_9(12)) FROM RDB$DATABASE;

SELECT MAX(TEST_10(12)) FROM RDB$DATABASE;

SELECT MIN(TEST_11(12)) FROM RDB$DATABASE;

SELECT cast(LIST(TEST_12('test')) as varchar(30))  as "LIST" FROM RDB$DATABASE;

SELECT cast(MAX(TEST_13('test')) as varchar(10)) as "TEST_10" FROM RDB$DATABASE;

SELECT cast(MIN(TEST_14('test')) as varchar(10)) as "TEST_10" FROM RDB$DATABASE;

SELECT cast(LIST(TEST_15('test')) as varchar(30)) as "LIST" FROM RDB$DATABASE;

SELECT MAX(TEST_16('test')) FROM RDB$DATABASE;

SELECT MAX(TEST_17('10.11.1982')) FROM RDB$DATABASE;

SELECT MAX(TEST_18('23:45')) FROM RDB$DATABASE;

SELECT cast(LIST(TEST_19('10.11.1982 23:45')) as varchar(30))  as "LIST" FROM RDB$DATABASE;

SELECT MAX(TEST_20('10.11.1982')) FROM RDB$DATABASE;

SELECT MAX(TEST_21(true)) FROM RDB$DATABASE;

SELECT MAX(TEST_22(false)) FROM RDB$DATABASE;
"""

act_2 = isql_act('db_2', test_script_2)

expected_stdout_2 = """
MAX
============
12
MIN
============
12
AVG
=====================
12
MAX
=======
12
MIN
=====================
12
AVG
=====================
12
MAX
=====================
12.00
MIN
==============
12.000000
AVG
=======================
12.00000000000000
MAX
=======================
12.00000000000000
MIN
=======================
12.00000000000000
LIST
==============================
test
TEST_10
==========
test
TEST_10
==========
test
LIST
==============================
test
MAX
==========
test
MAX
===========
1982-11-10
MAX
=============
23:45:00.0000
LIST
==============================
1982-11-10 23:45:00.0000
MAX
===========
1982-11-10
MAX
=======
<true>
MAX
=======
<false>
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
