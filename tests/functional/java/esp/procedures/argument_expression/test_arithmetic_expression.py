#coding:utf-8

"""
ID:          java.esp.procedures.argument-expression.arithmetic-expression
TITLE:       External procedure call with input parameter as an arithmetic expression
DESCRIPTION: 
FBTEST:      functional.java.esp.procedures.argument_expression.arithmetic_expression
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

create procedure test_12(i CHAR(10)) 
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

create procedure test_15(i INTEGER) 
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

create procedure test_18(i DATE) 
external name 'esp.TestProcedure.util_dateIn(java.util.Date)'
engine java;
commit;

create procedure test_19(i TIME) 
external name 'esp.TestProcedure.timeIn(java.sql.Time)'
engine java;
commit;
"""

db_1 = db_factory(init=init_script_1)

test_script_1 = """
EXECUTE PROCEDURE TEST_1(1+1);
EXECUTE PROCEDURE TEST_1(-3.2*2+5);

EXECUTE PROCEDURE TEST_2(1+1);
EXECUTE PROCEDURE TEST_2(-3.2*2+5);

EXECUTE PROCEDURE TEST_3(1+1);
EXECUTE PROCEDURE TEST_3(-3.2*2+5);

EXECUTE PROCEDURE TEST_4(1+1);
EXECUTE PROCEDURE TEST_4(-3.2*2+5);

EXECUTE PROCEDURE TEST_5(1+1);
EXECUTE PROCEDURE TEST_5(-3.2*2+5);

EXECUTE PROCEDURE TEST_6(1+1);
EXECUTE PROCEDURE TEST_6(-3.2*2+5);

EXECUTE PROCEDURE TEST_7(1+1);
EXECUTE PROCEDURE TEST_7(-3.2*2+5);

EXECUTE PROCEDURE TEST_8(1+1);
EXECUTE PROCEDURE TEST_8(-3.2*2+5);

EXECUTE PROCEDURE TEST_9(1+1);
EXECUTE PROCEDURE TEST_9(-3.2*2+5);

EXECUTE PROCEDURE TEST_10(1+1);
EXECUTE PROCEDURE TEST_10(-3.2*2+5);

EXECUTE PROCEDURE TEST_11(1+1);
EXECUTE PROCEDURE TEST_11(-3.2*2+5);

EXECUTE PROCEDURE TEST_12(1+1);
EXECUTE PROCEDURE TEST_12(-3.2*2+5);

EXECUTE PROCEDURE TEST_13(1+1);
EXECUTE PROCEDURE TEST_13(-3.2*2+5);

EXECUTE PROCEDURE TEST_14(1+1);
EXECUTE PROCEDURE TEST_14(-3.2*2+5);

EXECUTE PROCEDURE TEST_15(1+1);
EXECUTE PROCEDURE TEST_15(-3.2*2+5);

EXECUTE PROCEDURE TEST_16(1+1);
EXECUTE PROCEDURE TEST_16(-3.2*2+5);

EXECUTE PROCEDURE TEST_17(cast('30.09.2012' as date) +1);
EXECUTE PROCEDURE TEST_17(cast('01.10.2012' as date) -1);

EXECUTE PROCEDURE TEST_18(cast('30.09.2012' as date) +1);
EXECUTE PROCEDURE TEST_18(cast('01.10.2012' as date) - 1 );

EXECUTE PROCEDURE TEST_19(cast('04:09' as time) +1);
EXECUTE PROCEDURE TEST_19(cast('04:09' as time) -1);
commit;

select * from test_table;
"""

act_1 = isql_act('db_1', test_script_1)

expected_stdout_1 = """        
COL
===============================================================================
2
-1
2
-1
2
-1
2
-1
2
-1
2
-1
2.00
-1.40
2.0
-1.4
2.0
-1.4
2.0
-1.4
COL
===============================================================================
2.0
-1.4
2
-1.4
2
-1.4
2
-1.4
2
-1
2
-1.4
2012-10-01
2012-09-30
2012-10-01
2012-09-30
04:09:01
04:08:59
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

create procedure test_12(i CHAR(10))
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

create procedure test_15(i INTEGER)
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

create procedure test_18(i DATE)
external name 'esp.TestProcedure.util_dateIn(java.util.Date)'
engine java;
commit;

create procedure test_19(i TIME)
external name 'esp.TestProcedure.timeIn(java.sql.Time)'
engine java;
commit;
"""

db_2 = db_factory(init=init_script_2)

test_script_2 = """
EXECUTE PROCEDURE TEST_1(1+1);
EXECUTE PROCEDURE TEST_1(-3.2*2+5);

EXECUTE PROCEDURE TEST_2(1+1);
EXECUTE PROCEDURE TEST_2(-3.2*2+5);

EXECUTE PROCEDURE TEST_3(1+1);
EXECUTE PROCEDURE TEST_3(-3.2*2+5);

EXECUTE PROCEDURE TEST_4(1+1);
EXECUTE PROCEDURE TEST_4(-3.2*2+5);

EXECUTE PROCEDURE TEST_5(1+1);
EXECUTE PROCEDURE TEST_5(-3.2*2+5);

EXECUTE PROCEDURE TEST_6(1+1);
EXECUTE PROCEDURE TEST_6(-3.2*2+5);

EXECUTE PROCEDURE TEST_7(1+1);
EXECUTE PROCEDURE TEST_7(-3.2*2+5);

EXECUTE PROCEDURE TEST_8(1+1);
EXECUTE PROCEDURE TEST_8(-3.2*2+5);

EXECUTE PROCEDURE TEST_9(1+1);
EXECUTE PROCEDURE TEST_9(-3.2*2+5);

EXECUTE PROCEDURE TEST_10(1+1);
EXECUTE PROCEDURE TEST_10(-3.2*2+5);

EXECUTE PROCEDURE TEST_11(1+1);
EXECUTE PROCEDURE TEST_11(-3.2*2+5);

EXECUTE PROCEDURE TEST_12(1+1);
EXECUTE PROCEDURE TEST_12(-3.2*2+5);

EXECUTE PROCEDURE TEST_13(1+1);
EXECUTE PROCEDURE TEST_13(-3.2*2+5);

EXECUTE PROCEDURE TEST_14(1+1);
EXECUTE PROCEDURE TEST_14(-3.2*2+5);

EXECUTE PROCEDURE TEST_15(1+1);
EXECUTE PROCEDURE TEST_15(-3.2*2+5);

EXECUTE PROCEDURE TEST_16(1+1);
EXECUTE PROCEDURE TEST_16(-3.2*2+5);

EXECUTE PROCEDURE TEST_17(cast('30.09.2012' as date) +1);
EXECUTE PROCEDURE TEST_17(cast('01.10.2012' as date) -1);

EXECUTE PROCEDURE TEST_18(cast('30.09.2012' as date) +1);
EXECUTE PROCEDURE TEST_18(cast('01.10.2012' as date) - 1 );

EXECUTE PROCEDURE TEST_19(cast('04:09' as time) +1);
EXECUTE PROCEDURE TEST_19(cast('04:09' as time) -1);
commit;

select * from test_table;
"""

act_2 = isql_act('db_2', test_script_2)

expected_stdout_2 = """
COL
======================================================================================================================================================
2
-1
2
-1
2
-1
2
-1
2
-1
2
-1
2.00
-1.40
2.0
-1.4
2.0
-1.4
2.0
-1.4
COL
======================================================================================================================================================
2.0
-1.4
2
-1.4
2
-1.4
2
-1.4
2
-1
2
-1.4
2012-10-01
2012-09-30
2012-10-01
2012-09-30
04:09:01
04:08:59
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
