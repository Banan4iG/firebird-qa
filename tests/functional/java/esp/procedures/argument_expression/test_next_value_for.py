#coding:utf-8

"""
ID:          java.esp.procedures.argument-expression.next-value-for
TITLE:       External procedure call with input parameter as NEXT VALUE FOR operator
DESCRIPTION: 
FBTEST:      functional.java.esp.procedures.argument_expression.next_value_for
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


CREATE GENERATOR test_gen
START WITH 2 INCREMENT 2;
"""

db_1 = db_factory(init=init_script_1)

test_script_1 = """
EXECUTE PROCEDURE TEST_1(NEXT VALUE FOR test_gen);
EXECUTE PROCEDURE TEST_2(NEXT VALUE FOR test_gen);
EXECUTE PROCEDURE TEST_3(NEXT VALUE FOR test_gen);
EXECUTE PROCEDURE TEST_4(NEXT VALUE FOR test_gen);
EXECUTE PROCEDURE TEST_5(NEXT VALUE FOR test_gen);
EXECUTE PROCEDURE TEST_6(NEXT VALUE FOR test_gen);
EXECUTE PROCEDURE TEST_7(NEXT VALUE FOR test_gen);
EXECUTE PROCEDURE TEST_8(NEXT VALUE FOR test_gen);
EXECUTE PROCEDURE TEST_9(NEXT VALUE FOR test_gen);
EXECUTE PROCEDURE TEST_10(NEXT VALUE FOR test_gen);
EXECUTE PROCEDURE TEST_11(NEXT VALUE FOR test_gen);
EXECUTE PROCEDURE TEST_12(NEXT VALUE FOR test_gen);
EXECUTE PROCEDURE TEST_13(NEXT VALUE FOR test_gen);
EXECUTE PROCEDURE TEST_14(NEXT VALUE FOR test_gen);
EXECUTE PROCEDURE TEST_15(NEXT VALUE FOR test_gen);
EXECUTE PROCEDURE TEST_16(NEXT VALUE FOR test_gen);
commit;

select * from test_table;
"""

act_1 = isql_act('db_1', test_script_1)

expected_stdout_1 = """        
COL
===============================================================================
4
6
8
10
12
14
16.00
18.0
20.0
22.0
24.0
26
28
30
32
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


CREATE GENERATOR test_gen
START WITH 2 INCREMENT 2;
commit;
"""

db_2 = db_factory(init=init_script_2)

test_script_2 = """
EXECUTE PROCEDURE TEST_1(NEXT VALUE FOR test_gen);
EXECUTE PROCEDURE TEST_2(NEXT VALUE FOR test_gen);
EXECUTE PROCEDURE TEST_3(NEXT VALUE FOR test_gen);
EXECUTE PROCEDURE TEST_4(NEXT VALUE FOR test_gen);
EXECUTE PROCEDURE TEST_5(NEXT VALUE FOR test_gen);
EXECUTE PROCEDURE TEST_6(NEXT VALUE FOR test_gen);
EXECUTE PROCEDURE TEST_7(NEXT VALUE FOR test_gen);
EXECUTE PROCEDURE TEST_8(NEXT VALUE FOR test_gen);
EXECUTE PROCEDURE TEST_9(NEXT VALUE FOR test_gen);
EXECUTE PROCEDURE TEST_10(NEXT VALUE FOR test_gen);
EXECUTE PROCEDURE TEST_11(NEXT VALUE FOR test_gen);
EXECUTE PROCEDURE TEST_12(NEXT VALUE FOR test_gen);
EXECUTE PROCEDURE TEST_13(NEXT VALUE FOR test_gen);
EXECUTE PROCEDURE TEST_14(NEXT VALUE FOR test_gen);
EXECUTE PROCEDURE TEST_15(NEXT VALUE FOR test_gen);
EXECUTE PROCEDURE TEST_16(NEXT VALUE FOR test_gen);
commit;

select * from test_table;
"""

act_2 = isql_act('db_2', test_script_2)

expected_stdout_2 = """
COL
======================================================================================================================================================
2
4
6
8
10
12
14.00
16.0
18.0
20.0
22.0
24
26
28
30
32
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
