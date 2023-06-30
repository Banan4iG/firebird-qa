#coding:utf-8

"""
ID:          java.esp.procedures.argument-expression.internal-variable
TITLE:       External procedure call with input parameter as a internal variable
DESCRIPTION: 
FBTEST:      functional.java.esp.procedures.argument_expression.internal_variable
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
"""

db_1 = db_factory(init=init_script_1)

test_script_1 = """

set term !;
execute block 
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
	
	EXECUTE PROCEDURE TEST_1(INTVAR_1);
	EXECUTE PROCEDURE TEST_2(INTVAR_1);
	EXECUTE PROCEDURE TEST_3(INTVAR_1);
	EXECUTE PROCEDURE TEST_4(:INTVAR_1);
	EXECUTE PROCEDURE TEST_5(INTVAR_1);
	EXECUTE PROCEDURE TEST_6(INTVAR_1);
	EXECUTE PROCEDURE TEST_7(INTVAR_1);
	EXECUTE PROCEDURE TEST_8(INTVAR_1);
	EXECUTE PROCEDURE TEST_9(INTVAR_1);
	EXECUTE PROCEDURE TEST_10(INTVAR_1);
	EXECUTE PROCEDURE TEST_11(INTVAR_1);
	
	EXECUTE PROCEDURE TEST_12(INTVAR_2);
	EXECUTE PROCEDURE TEST_13(INTVAR_2);
	EXECUTE PROCEDURE TEST_14(INTVAR_2);
	EXECUTE PROCEDURE TEST_15(INTVAR_2);
	EXECUTE PROCEDURE TEST_16(INTVAR_2);
	EXECUTE PROCEDURE TEST_17(INTVAR_3);
	EXECUTE PROCEDURE TEST_18(INTVAR_4);
	EXECUTE PROCEDURE TEST_19(INTVAR_5);
	EXECUTE PROCEDURE TEST_20(INTVAR_3);
	EXECUTE PROCEDURE TEST_21(INTVAR_6);
	EXECUTE PROCEDURE TEST_22(INTVAR_6);
	
end!
commit!
set term ;!

select * from test_table;
"""

act_1 = isql_act('db_1', test_script_1)

expected_stdout_1 = """        
COL
===============================================================================
56
56
56
56
56
56
56.00
56.0
56.0
56.0
56.0
test
test
test
test
test
1945-04-10
05:53:00
1945-04-10 05:53:00.0
1945-04-10
COL
===============================================================================
true
true
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
"""

db_2 = db_factory(init=init_script_2)

test_script_2 = """

set term !;
execute block
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

	EXECUTE PROCEDURE TEST_1(INTVAR_1);
	EXECUTE PROCEDURE TEST_2(INTVAR_1);
	EXECUTE PROCEDURE TEST_3(INTVAR_1);
	EXECUTE PROCEDURE TEST_4(:INTVAR_1);
	EXECUTE PROCEDURE TEST_5(INTVAR_1);
	EXECUTE PROCEDURE TEST_6(INTVAR_1);
	EXECUTE PROCEDURE TEST_7(INTVAR_1);
	EXECUTE PROCEDURE TEST_8(INTVAR_1);
	EXECUTE PROCEDURE TEST_9(INTVAR_1);
	EXECUTE PROCEDURE TEST_10(INTVAR_1);
	EXECUTE PROCEDURE TEST_11(INTVAR_1);

	EXECUTE PROCEDURE TEST_12(INTVAR_2);
	EXECUTE PROCEDURE TEST_13(INTVAR_2);
	EXECUTE PROCEDURE TEST_14(INTVAR_2);
	EXECUTE PROCEDURE TEST_15(INTVAR_2);
	EXECUTE PROCEDURE TEST_16(INTVAR_2);
	EXECUTE PROCEDURE TEST_17(INTVAR_3);
	EXECUTE PROCEDURE TEST_18(INTVAR_4);
	EXECUTE PROCEDURE TEST_19(INTVAR_5);
	EXECUTE PROCEDURE TEST_20(INTVAR_3);
	EXECUTE PROCEDURE TEST_21(INTVAR_6);
	EXECUTE PROCEDURE TEST_22(INTVAR_6);

end!
commit!
set term ;!

select * from test_table;
"""

act_2 = isql_act('db_2', test_script_2)

expected_stdout_2 = """
COL
======================================================================================================================================================
56
56
56
56
56
56
56.00
56.0
56.0
56.0
56.0
test
test
test
test
test
1945-04-10
05:53:00
1945-04-10 05:53:00.0
1945-04-10
COL
======================================================================================================================================================
true
true
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
