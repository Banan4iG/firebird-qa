#coding:utf-8

"""
ID:          java.esp.procedures.argument-expression.imbedded-function
TITLE:       External procedure call with input parameter as a common imbedded function
DESCRIPTION: 
FBTEST:      functional.java.esp.procedures.argument_expression.imbedded_function
"""

import pytest
from firebird.qa import *

# version: 3.0

init_script_1 = """
CREATE TABLE TEST_TABLE(col varchar(150));
commit;  
 
create procedure test_1(i INTEGER) 
external name 'esp.TestProcedure.integerIn(Integer)' 
engine java;
commit;

create procedure test_2(i INTEGER) 
external name 'esp.TestProcedure.intIn(int)' 
engine java;
commit;


create procedure test_3(i SMALLINT) 
external name 'esp.TestProcedure.ShortIn(Short)'
engine java;
commit;

create procedure test_4(i SMALLINT) 
external name 'esp.TestProcedure.shortIn(short)'
engine java;
commit;

create procedure test_5(i BIGINT) 
external name 'esp.TestProcedure.LongIn(Long)'
engine java;
commit;

create procedure test_6(i BIGINT) 
external name 'esp.TestProcedure.longIn(long)'
engine java;
commit;

create procedure test_7(i NUMERIC(10,2)) 
external name 'esp.TestProcedure.bigDecimalIn(java.math.BigDecimal)'
engine java;
commit;

create procedure test_8(i FLOAT) 
external name 'esp.TestProcedure.floatIn(float)'
engine java;
commit;

create procedure test_9(i FLOAT) 
external name 'esp.TestProcedure.FloatIn(Float)'
engine java;
commit;

create procedure test_10(i DOUBLE PRECISION) 
external name 'esp.TestProcedure.doubleIn(double)'
engine java;
commit;

create procedure test_11(i DOUBLE PRECISION) 
external name 'esp.TestProcedure.DoubleIn(Double)'
engine java;
commit;

create procedure test_12(i VARCHAR(20)) 
external name 'esp.TestProcedure.stringIn(String)'
engine java;
commit;

create procedure test_13(i BLOB) 
external name 'esp.TestProcedure.sqlblobIn(java.sql.Blob)'
engine java;
commit;

create procedure test_14(i BLOB) 
external name 'esp.TestProcedure.blobIn(org.firebirdsql.jdbc.FirebirdBlob)'
engine java;
commit;

create procedure test_15(i VARCHAR(20)) 
external name 'esp.TestProcedure.ObjectIn(Object)'
engine java;
commit;

create procedure test_16(i VARCHAR(10)) 
external name 'esp.TestProcedure.byteIn(byte[])'
engine java;
commit;

create procedure test_17(i DATE) 
external name 'esp.TestProcedure.dateIn(java.sql.Date)'
engine java;
commit;

create procedure test_18(i TIME) 
external name 'esp.TestProcedure.timeIn(java.sql.Time)'
engine java;
commit;

create procedure test_19(i TIMESTAMP) 
external name 'esp.TestProcedure.timeStampIn(java.sql.Timestamp)'
engine java;
commit;

create procedure test_20(i DATE) 
external name 'esp.TestProcedure.util_dateIn(java.util.Date)'
engine java;
commit;
"""

db_1 = db_factory(init=init_script_1)

test_script_1 = """
 
EXECUTE PROCEDURE TEST_1(SQRT(4.5));
EXECUTE PROCEDURE TEST_2(exp(2));
EXECUTE PROCEDURE TEST_3(pi());
EXECUTE PROCEDURE TEST_4(mod(7.5,2.5));
EXECUTE PROCEDURE TEST_5(log(2,4));
EXECUTE PROCEDURE TEST_6(floor(4.5));
EXECUTE PROCEDURE TEST_7(sin(0.5));
EXECUTE PROCEDURE TEST_8(abs(4.5));
EXECUTE PROCEDURE TEST_9(cos(1.5));
EXECUTE PROCEDURE TEST_10(atan(1));
EXECUTE PROCEDURE TEST_11(power(3,2));
EXECUTE PROCEDURE TEST_12(left('abcdef',2));
EXECUTE PROCEDURE TEST_13(RIGHT('abcdef',2)) ;
EXECUTE PROCEDURE TEST_14(TRIM('a' from 'aaabcdsaefa'));
EXECUTE PROCEDURE TEST_15(UPPER('abc'));
EXECUTE PROCEDURE TEST_16(LOWER('ABc'));
EXECUTE PROCEDURE TEST_17(DATEADD(5 year to cast('10.03.2014' as date)));
EXECUTE PROCEDURE TEST_18(DATEADD(2 hour to cast('10:35' as time)));
EXECUTE PROCEDURE TEST_19(DATEADD(2 hour to cast('10.03.2014 10:35' as timestamp)));
EXECUTE PROCEDURE TEST_20(DATEADD(5 year to cast('10.03.2014' as date)));
commit;

select * from test_table;
"""

act_1 = isql_act('db_1', test_script_1)

expected_stdout_1 = """
COL
===============================================================================
2
7
3
2
2
4
0.48
4.5
0.0707372
0.7853981633974483
9.0
ab
ef
bcdsaef
ABC
abc
2019-03-10
12:35:00
2014-03-10 12:35:00.0
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
CREATE TABLE TEST_TABLE(col varchar(150));
commit;

create procedure test_1(i INTEGER)
external name 'esp.TestProcedure.integerIn(Integer)'
engine java;
commit;

create procedure test_2(i INTEGER)
external name 'esp.TestProcedure.intIn(int)'
engine java;
commit;


create procedure test_3(i SMALLINT)
external name 'esp.TestProcedure.ShortIn(Short)'
engine java;
commit;

create procedure test_4(i SMALLINT)
external name 'esp.TestProcedure.shortIn(short)'
engine java;
commit;

create procedure test_5(i BIGINT)
external name 'esp.TestProcedure.LongIn(Long)'
engine java;
commit;

create procedure test_6(i BIGINT)
external name 'esp.TestProcedure.longIn(long)'
engine java;
commit;

create procedure test_7(i NUMERIC(10,2))
external name 'esp.TestProcedure.bigDecimalIn(java.math.BigDecimal)'
engine java;
commit;

create procedure test_8(i FLOAT)
external name 'esp.TestProcedure.floatIn(float)'
engine java;
commit;

create procedure test_9(i FLOAT)
external name 'esp.TestProcedure.FloatIn(Float)'
engine java;
commit;

create procedure test_10(i DOUBLE PRECISION)
external name 'esp.TestProcedure.doubleIn(double)'
engine java;
commit;

create procedure test_11(i DOUBLE PRECISION)
external name 'esp.TestProcedure.DoubleIn(Double)'
engine java;
commit;

create procedure test_12(i VARCHAR(20))
external name 'esp.TestProcedure.stringIn(String)'
engine java;
commit;

create procedure test_13(i BLOB)
external name 'esp.TestProcedure.sqlblobIn(java.sql.Blob)'
engine java;
commit;

create procedure test_14(i BLOB)
external name 'esp.TestProcedure.blobIn(org.firebirdsql.jdbc.FirebirdBlob)'
engine java;
commit;

create procedure test_15(i VARCHAR(20))
external name 'esp.TestProcedure.ObjectIn(Object)'
engine java;
commit;

create procedure test_16(i VARCHAR(10))
external name 'esp.TestProcedure.byteIn(byte[])'
engine java;
commit;

create procedure test_17(i DATE)
external name 'esp.TestProcedure.dateIn(java.sql.Date)'
engine java;
commit;

create procedure test_18(i TIME)
external name 'esp.TestProcedure.timeIn(java.sql.Time)'
engine java;
commit;

create procedure test_19(i TIMESTAMP)
external name 'esp.TestProcedure.timeStampIn(java.sql.Timestamp)'
engine java;
commit;

create procedure test_20(i DATE)
external name 'esp.TestProcedure.util_dateIn(java.util.Date)'
engine java;
commit;
"""

db_2 = db_factory(init=init_script_2)

test_script_2 = """

EXECUTE PROCEDURE TEST_1(SQRT(4.5));
EXECUTE PROCEDURE TEST_2(exp(2));
EXECUTE PROCEDURE TEST_3(pi());
EXECUTE PROCEDURE TEST_4(mod(7.5,2.5));
EXECUTE PROCEDURE TEST_5(log(2,4));
EXECUTE PROCEDURE TEST_6(floor(4.5));
EXECUTE PROCEDURE TEST_7(sin(0.5));
EXECUTE PROCEDURE TEST_8(abs(4.5));
EXECUTE PROCEDURE TEST_9(cos(1.5));
EXECUTE PROCEDURE TEST_10(atan(1));
EXECUTE PROCEDURE TEST_11(power(3,2));
EXECUTE PROCEDURE TEST_12(left('abcdef',2));
EXECUTE PROCEDURE TEST_13(RIGHT('abcdef',2)) ;
EXECUTE PROCEDURE TEST_14(TRIM('a' from 'aaabcdsaefa'));
EXECUTE PROCEDURE TEST_15(UPPER('abc'));
EXECUTE PROCEDURE TEST_16(LOWER('ABc'));
EXECUTE PROCEDURE TEST_17(DATEADD(5 year to cast('10.03.2014' as date)));
EXECUTE PROCEDURE TEST_18(DATEADD(2 hour to cast('10:35' as time)));
EXECUTE PROCEDURE TEST_19(DATEADD(2 hour to cast('10.03.2014 10:35' as timestamp)));
EXECUTE PROCEDURE TEST_20(DATEADD(5 year to cast('10.03.2014' as date)));
commit;

select * from test_table;
"""

act_2 = isql_act('db_2', test_script_2)

expected_stdout_2 = """
COL
======================================================================================================================================================
2
7
3
2
2
4
0.48
4.5
0.0707372
0.7853981633974483
9.0
ab
ef
bcdsaef
ABC
abc
2019-03-10
12:35:00
2014-03-10 12:35:00.0
2019-03-10
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
