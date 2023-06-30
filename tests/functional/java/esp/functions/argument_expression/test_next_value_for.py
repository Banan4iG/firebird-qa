#coding:utf-8

"""
ID:          java.esp.functions.argument-expression.next-value-for
TITLE:       External function call with input parameter as NEXT VALUE FOR operator
DESCRIPTION: 
FBTEST:      functional.java.esp.functions.argument_expression.next_value_for
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


CREATE GENERATOR test_gen
START WITH 2 INCREMENT 2;
"""

db_1 = db_factory(init=init_script_1)

test_script_1 = """
SELECT TEST_1(NEXT VALUE FOR test_gen) FROM RDB$DATABASE;

SELECT TEST_2(NEXT VALUE FOR test_gen) FROM RDB$DATABASE;

SELECT TEST_3(NEXT VALUE FOR test_gen) FROM RDB$DATABASE;

SELECT TEST_4(NEXT VALUE FOR test_gen) FROM RDB$DATABASE;

SELECT TEST_5(NEXT VALUE FOR test_gen) FROM RDB$DATABASE;

SELECT TEST_6(NEXT VALUE FOR test_gen) FROM RDB$DATABASE;

SELECT TEST_7(NEXT VALUE FOR test_gen) FROM RDB$DATABASE;

SELECT TEST_8(NEXT VALUE FOR test_gen) FROM RDB$DATABASE;

SELECT TEST_9(NEXT VALUE FOR test_gen) FROM RDB$DATABASE;

SELECT TEST_10(NEXT VALUE FOR test_gen) FROM RDB$DATABASE;

SELECT TEST_11(NEXT VALUE FOR test_gen) FROM RDB$DATABASE;

SELECT TEST_12(NEXT VALUE FOR test_gen) FROM RDB$DATABASE;

SELECT cast(TEST_13(NEXT VALUE FOR test_gen) as varchar(10)) as "TEST_10" FROM RDB$DATABASE;

SELECT cast(TEST_14(NEXT VALUE FOR test_gen) as varchar(10)) as "TEST_10" FROM RDB$DATABASE;

SELECT TEST_15(NEXT VALUE FOR test_gen) FROM RDB$DATABASE;

SELECT TEST_16(NEXT VALUE FOR test_gen) FROM RDB$DATABASE;
"""

act_1 = isql_act('db_1', test_script_1)

expected_stdout_1 = """        
TEST_1
============
4
TEST_2
============
6
TEST_3
=======
8
TEST_4
=======
10
TEST_5
=====================
12
TEST_6
=====================
14
TEST_7
=====================
16.00
TEST_8
==============
18.000000
TEST_9
==============
20.000000
TEST_10
=======================
22.00000000000000
TEST_11
=======================
24.00000000000000
TEST_12
==========
26
TEST_10
==========
28
TEST_10
==========
30
TEST_15
============
32
TEST_16
==========
34
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


CREATE GENERATOR test_gen
START WITH 2 INCREMENT 2;
"""

db_2 = db_factory(init=init_script_2)

test_script_2 = """
SELECT TEST_1(NEXT VALUE FOR test_gen) FROM RDB$DATABASE;

SELECT TEST_2(NEXT VALUE FOR test_gen) FROM RDB$DATABASE;

SELECT TEST_3(NEXT VALUE FOR test_gen) FROM RDB$DATABASE;

SELECT TEST_4(NEXT VALUE FOR test_gen) FROM RDB$DATABASE;

SELECT TEST_5(NEXT VALUE FOR test_gen) FROM RDB$DATABASE;

SELECT TEST_6(NEXT VALUE FOR test_gen) FROM RDB$DATABASE;

SELECT TEST_7(NEXT VALUE FOR test_gen) FROM RDB$DATABASE;

SELECT TEST_8(NEXT VALUE FOR test_gen) FROM RDB$DATABASE;

SELECT TEST_9(NEXT VALUE FOR test_gen) FROM RDB$DATABASE;

SELECT TEST_10(NEXT VALUE FOR test_gen) FROM RDB$DATABASE;

SELECT TEST_11(NEXT VALUE FOR test_gen) FROM RDB$DATABASE;

SELECT TEST_12(NEXT VALUE FOR test_gen) FROM RDB$DATABASE;

SELECT cast(TEST_13(NEXT VALUE FOR test_gen) as varchar(10)) as "TEST_10" FROM RDB$DATABASE;

SELECT cast(TEST_14(NEXT VALUE FOR test_gen) as varchar(10)) as "TEST_10" FROM RDB$DATABASE;

SELECT TEST_15(NEXT VALUE FOR test_gen) FROM RDB$DATABASE;

SELECT TEST_16(NEXT VALUE FOR test_gen) FROM RDB$DATABASE;
"""

act_2 = isql_act('db_2', test_script_2)

expected_stdout_2 = """
TEST_1
============
2
TEST_2
============
4
TEST_3
=======
6
TEST_4
=======
8
TEST_5
=====================
10
TEST_6
=====================
12
TEST_7
=====================
14.00
TEST_8
==============
16.000000
TEST_9
==============
18.000000
TEST_10
=======================
20.00000000000000
TEST_11
=======================
22.00000000000000
TEST_12
==========
24
TEST_10
==========
26
TEST_10
==========
28
TEST_15
============
30
TEST_16
==========
32
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
