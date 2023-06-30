#coding:utf-8

"""
ID:          java.esp.functions.argument-expression.internal-variable
TITLE:       External function call with input parameter as a internal variable
DESCRIPTION: 
FBTEST:      functional.java.esp.functions.argument_expression.internal_variable
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
set list;
set term !;
execute block 
returns(result1 integer, result2 integer, result3 smallint, result4 smallint, result5 bigint, result6 bigint, result7 NUMERIC(10,2), result8 FLOAT, result9 FLOAT, result10 DOUBLE PRECISION, result11 DOUBLE PRECISION, result12 VARCHAR(10), result13 VARCHAR(10), result14 VARCHAR(10), result15 VARCHAR(10), result16 VARCHAR(10), result17 date, result18 time, result19 timestamp, result20 date, result21 boolean, result22 boolean)
as
declare INTVAR_1 integer;
declare INTVAR_2 varchar(10);
declare INTVAR_3 date;
declare INTVAR_4 time;
declare INTVAR_5 timestamp;
declare INTVAR_6 boolean;
begin
	INTVAR_1 = 56;
	INTVAR_2 = 'test';
	INTVAR_3 = '10.04.1945';
	INTVAR_4 = '05:53';
	INTVAR_5 = '10.04.1945 05:53';
	INTVAR_6 = true;
	
	result1 = TEST_1(INTVAR_1);
	result2 = TEST_2(INTVAR_1);
	result3 = TEST_3(INTVAR_1);
	result4 = TEST_4(INTVAR_1);
	result5 = TEST_5(INTVAR_1);
	result6 = TEST_6(INTVAR_1);
	result7 = TEST_7(INTVAR_1);
	result8 = TEST_8(INTVAR_1);
	result9 = TEST_9(INTVAR_1);
	result10 = TEST_10(INTVAR_1);
	result11 = TEST_11(INTVAR_1);
	
	result12 = TEST_12(INTVAR_2);
	result13 = TEST_13(INTVAR_2);
	result14 = TEST_14(INTVAR_2);
	result15 = TEST_15(INTVAR_2);
	result16 = TEST_16(INTVAR_2);
	result17 = TEST_17(INTVAR_3);
	result18 = TEST_18(INTVAR_4);
	result19 = TEST_19(INTVAR_5);
	result20 = TEST_20(INTVAR_3);
	result21 = TEST_21(INTVAR_6);
	result22 = TEST_22(INTVAR_6);
	suspend;
end!
set term ;!

"""

act = isql_act('db', test_script)

expected_stdout = """        

RESULT1                         56
RESULT2                         56
RESULT3                         56
RESULT4                         56
RESULT5                         56
RESULT6                         56
RESULT7                         56.00
RESULT8                         56
RESULT9                         56
RESULT10                        56.00000000000000
RESULT11                        56.00000000000000
RESULT12                        test
RESULT13                        test
RESULT14                        test
RESULT15                        test
RESULT16                        test
RESULT17                        1945-04-10
RESULT18                        05:53:00.0000
RESULT19                        1945-04-10 05:53:00.0000
RESULT20                        1945-04-10
RESULT21                        <true>
RESULT22                        <true>
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
