#coding:utf-8

"""
ID:          java.esp.functions.argument-expression.context-variable
TITLE:       External function call with input parameter as a context variable
DESCRIPTION: 
FBTEST:      functional.java.esp.functions.argument_expression.context_variable
"""

import pytest
from firebird.qa import *

substitutions = [('\\d{4}\\-\\d{2}\\-\\d{2}', 'date'), ('\\d{2}:\\d{2}:\\d{2}\\.\\d{4}', 'time')]

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


create table test_table(id integer);
commit;
"""

db = db_factory(init=init_script)

test_script = """
set list;
set term !;
execute block 
returns(result1 integer, result2 integer, result3 smallint, result4 smallint, result5 bigint, result6 bigint, result7 NUMERIC(10,2), result8 FLOAT, result9 FLOAT, result10 DOUBLE PRECISION, result11 DOUBLE PRECISION, result12 VARCHAR(10), result13 VARCHAR(10), result14 VARCHAR(10), result15 VARCHAR(10), result16 VARCHAR(10), result17 date, result18 time, result19 timestamp, result20 date)
as
begin
	insert into test_table values(2);
	result1 = TEST_1(ROW_COUNT);
	result2 = TEST_2(ROW_COUNT);
	result3 = TEST_3(ROW_COUNT);
	result4 = TEST_4(ROW_COUNT);
	result5 = TEST_5(ROW_COUNT);
	result6 = TEST_6(ROW_COUNT);
	result7 = TEST_7(ROW_COUNT);
	result8 = TEST_8(ROW_COUNT);
	result9 = TEST_9(ROW_COUNT);
	result10 = TEST_10(ROW_COUNT);
	result11 = TEST_11(ROW_COUNT);
	
	result12 = TEST_12(ROW_COUNT);
	result13 = TEST_13(ROW_COUNT);
	result14 = TEST_14(ROW_COUNT);
	result15 = TEST_15(ROW_COUNT);
	result16 = TEST_16(ROW_COUNT);
	result17 = TEST_17(CURRENT_DATE);
	result18 = TEST_18(CURRENT_TIME);
	result19 = TEST_19(CURRENT_TIMESTAMP);
	result20 = TEST_20(CURRENT_DATE);
	suspend;
end!
set term ;!

"""

act = isql_act('db', test_script, substitutions=substitutions)

expected_stdout = """        

RESULT1                         1
RESULT2                         1
RESULT3                         1
RESULT4                         1
RESULT5                         1
RESULT6                         1
RESULT7                         1.00
RESULT8                         1
RESULT9                         1
RESULT10                        1.000000000000000
RESULT11                        1.000000000000000
RESULT12                        1
RESULT13                        1
RESULT14                        1
RESULT15                        1
RESULT16                        1
RESULT17                        date
RESULT18                        time
RESULT19                        date time
RESULT20                        date
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
