#coding:utf-8

"""
ID:          java.esp.procedures.argument-expression.external-function
TITLE:       External procedure call with input parameter as external function
DESCRIPTION: 
FBTEST:      functional.java.esp.procedures.argument_expression.external_function
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

create procedure test_21(i BOOLEAN) 
external name 'esp.TestProcedure.booleanIn(boolean)' 
engine java;
commit;

create procedure test_22(i boolean) 
external name 'esp.TestProcedure.BooleanIn(Boolean)' 
engine java;
commit;




create function func_test_1(i INTEGER) 
returns INTEGER
external name 'esp.TestFunction.integerInOut(Integer)' 
engine java;
commit;

create function func_test_2(i DATE) 
returns DATE
external name 'esp.TestFunction.dateInOut(java.sql.Date)'
engine java;
commit;

create function func_test_3(i TIME) 
returns TIME
external name 'esp.TestFunction.timeInOut(java.sql.Time)'
engine java;
commit;

create function func_test_4(i TIMESTAMP) 
returns TIMESTAMP
external name 'esp.TestFunction.timeStampInOut(java.sql.Timestamp)'
engine java;
commit;

create function func_test_5(i BOOLEAN) 
returns BOOLEAN
external name 'esp.TestFunction.boolInOut(boolean)' 
engine java;
commit;
"""

db_1 = db_factory(init=init_script_1)

test_script_1 = """

EXECUTE PROCEDURE test_1(func_test_1(34));
EXECUTE PROCEDURE test_2(func_test_1(34));
EXECUTE PROCEDURE test_3(func_test_1(34));
EXECUTE PROCEDURE test_4(func_test_1(34));
EXECUTE PROCEDURE test_5(func_test_1(34));
EXECUTE PROCEDURE test_6(func_test_1(34));
EXECUTE PROCEDURE test_7(func_test_1(34));
EXECUTE PROCEDURE test_8(func_test_1(34));
EXECUTE PROCEDURE test_9(func_test_1(34));
EXECUTE PROCEDURE test_10(func_test_1(34));
EXECUTE PROCEDURE test_11(func_test_1(34));

EXECUTE PROCEDURE test_12(func_test_1(34));
EXECUTE PROCEDURE test_13(func_test_1(34));
EXECUTE PROCEDURE test_14(func_test_1(34));
EXECUTE PROCEDURE test_15(func_test_1(34));
EXECUTE PROCEDURE test_16(func_test_1(34));

EXECUTE PROCEDURE test_17(func_test_2('05.03.2012'));
EXECUTE PROCEDURE test_18(func_test_3('06:34'));
EXECUTE PROCEDURE test_19(func_test_4('05.03.2012 06:34'));
EXECUTE PROCEDURE test_20(func_test_2('05.03.2012'));

EXECUTE PROCEDURE test_21(func_test_5('true'));
EXECUTE PROCEDURE test_22(func_test_5(false));
commit;

select * from test_table;
"""

act_1 = isql_act('db_1', test_script_1)

expected_stdout_1 = """        
COL
===============================================================================
34
34
34
34
34
34
34.00
34.0
34.0
34.0
34.0
34
34
34
34
34
2012-03-05
06:34:00
2012-03-05 06:34:00.0
2012-03-05
COL
===============================================================================
true
false
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

create procedure test_21(i BOOLEAN)
external name 'esp.TestProcedure.booleanIn(boolean)'
engine java;
commit;

create procedure test_22(i boolean)
external name 'esp.TestProcedure.BooleanIn(Boolean)'
engine java;
commit;




create function func_test_1(i INTEGER)
returns INTEGER
external name 'esp.TestFunction.integerInOut(Integer)'
engine java;
commit;

create function func_test_2(i DATE)
returns DATE
external name 'esp.TestFunction.dateInOut(java.sql.Date)'
engine java;
commit;

create function func_test_3(i TIME)
returns TIME
external name 'esp.TestFunction.timeInOut(java.sql.Time)'
engine java;
commit;

create function func_test_4(i TIMESTAMP)
returns TIMESTAMP
external name 'esp.TestFunction.timeStampInOut(java.sql.Timestamp)'
engine java;
commit;

create function func_test_5(i BOOLEAN)
returns BOOLEAN
external name 'esp.TestFunction.boolInOut(boolean)'
engine java;
commit;
"""

db_2 = db_factory(init=init_script_2)

test_script_2 = """

EXECUTE PROCEDURE test_1(func_test_1(34));
EXECUTE PROCEDURE test_2(func_test_1(34));
EXECUTE PROCEDURE test_3(func_test_1(34));
EXECUTE PROCEDURE test_4(func_test_1(34));
EXECUTE PROCEDURE test_5(func_test_1(34));
EXECUTE PROCEDURE test_6(func_test_1(34));
EXECUTE PROCEDURE test_7(func_test_1(34));
EXECUTE PROCEDURE test_8(func_test_1(34));
EXECUTE PROCEDURE test_9(func_test_1(34));
EXECUTE PROCEDURE test_10(func_test_1(34));
EXECUTE PROCEDURE test_11(func_test_1(34));

EXECUTE PROCEDURE test_12(func_test_1(34));
EXECUTE PROCEDURE test_13(func_test_1(34));
EXECUTE PROCEDURE test_14(func_test_1(34));
EXECUTE PROCEDURE test_15(func_test_1(34));
EXECUTE PROCEDURE test_16(func_test_1(34));

EXECUTE PROCEDURE test_17(func_test_2('05.03.2012'));
EXECUTE PROCEDURE test_18(func_test_3('06:34'));
EXECUTE PROCEDURE test_19(func_test_4('05.03.2012 06:34'));
EXECUTE PROCEDURE test_20(func_test_2('05.03.2012'));

EXECUTE PROCEDURE test_21(func_test_5('true'));
EXECUTE PROCEDURE test_22(func_test_5(false));
commit;

select * from test_table;
"""

act_2 = isql_act('db_2', test_script_2)

expected_stdout_2 = """
COL
======================================================================================================================================================
34
34
34
34
34
34
34.00
34.0
34.0
34.0
34.0
34
34
34
34
34
2012-03-05
06:34:00
2012-03-05 06:34:00.0
2012-03-05
COL
======================================================================================================================================================
true
false
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
