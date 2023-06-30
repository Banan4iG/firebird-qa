#coding:utf-8

"""
ID:          java.esp.procedures.argument-expression.aggregate-function
TITLE:       External procedure call with input parameter as a aggregate function
DESCRIPTION: 
FBTEST:      functional.java.esp.procedures.argument_expression.aggregate_function
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


create table help_table(id integer unique, number integer, name varchar(20), d date, t time, ts timestamp, flag boolean);
insert into help_table values(1, 23, 'Ann', '04.12.1839', '23:45', '04.12.1839 23:45', true);
insert into help_table values(2, 46, 'Peter', '23.05.2000', '09:36', '23.05.2000 09:36', false);
commit;
"""

db_1 = db_factory(init=init_script_1)

test_script_1 = """


EXECUTE PROCEDURE test_1((select max(number) from help_table));
EXECUTE PROCEDURE test_2((select min(number) from help_table));
EXECUTE PROCEDURE test_3((select max(number) from help_table));
EXECUTE PROCEDURE test_4((select min(number) from help_table));
EXECUTE PROCEDURE test_5((select max(number) from help_table));
EXECUTE PROCEDURE test_6((select min(number) from help_table));
EXECUTE PROCEDURE test_7((select max(number) from help_table));
EXECUTE PROCEDURE test_8((select min(number) from help_table));
EXECUTE PROCEDURE test_9((select max(number) from help_table));
EXECUTE PROCEDURE test_10((select min(number) from help_table));
EXECUTE PROCEDURE test_11((select max(number) from help_table));
EXECUTE PROCEDURE test_12((select list(name) from help_table));
EXECUTE PROCEDURE test_13((select list(name) from help_table));
EXECUTE PROCEDURE test_14((select list(name) from help_table));
EXECUTE PROCEDURE test_15((select list(name) from help_table));
EXECUTE PROCEDURE test_16((select list(name) from help_table));
EXECUTE PROCEDURE test_17((select max(d) from help_table));
EXECUTE PROCEDURE test_18((select max(t) from help_table));
EXECUTE PROCEDURE test_19((select max(ts) from help_table));
EXECUTE PROCEDURE test_20((select max(d) from help_table));
EXECUTE PROCEDURE test_21((select max(flag) from help_table));
EXECUTE PROCEDURE test_22((select min(flag) from help_table));
commit;

select * from test_table;
"""

act_1 = isql_act('db_1', test_script_1)

expected_stdout_1 = """        
COL
===============================================================================
46
23
46
23
46
23
46.00
23.0
46.0
23.0
46.0
Ann,Peter
Ann,Peter
Ann,Peter
Ann,Peter
Ann,Peter
2000-05-23
23:45:00
2000-05-23 09:36:00.0
2000-05-23
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


create table help_table(id integer unique, number integer, name varchar(20), d date, t time, ts timestamp, flag boolean);
insert into help_table values(1, 23, 'Ann', '04.12.1839', '23:45', '04.12.1839 23:45', true);
insert into help_table values(2, 46, 'Peter', '23.05.2000', '09:36', '23.05.2000 09:36', false);
commit;
"""

db_2 = db_factory(init=init_script_2)

test_script_2 = """


EXECUTE PROCEDURE test_1((select max(number) from help_table));
EXECUTE PROCEDURE test_2((select min(number) from help_table));
EXECUTE PROCEDURE test_3((select max(number) from help_table));
EXECUTE PROCEDURE test_4((select min(number) from help_table));
EXECUTE PROCEDURE test_5((select max(number) from help_table));
EXECUTE PROCEDURE test_6((select min(number) from help_table));
EXECUTE PROCEDURE test_7((select max(number) from help_table));
EXECUTE PROCEDURE test_8((select min(number) from help_table));
EXECUTE PROCEDURE test_9((select max(number) from help_table));
EXECUTE PROCEDURE test_10((select min(number) from help_table));
EXECUTE PROCEDURE test_11((select max(number) from help_table));
EXECUTE PROCEDURE test_12((select list(name) from help_table));
EXECUTE PROCEDURE test_13((select list(name) from help_table));
EXECUTE PROCEDURE test_14((select list(name) from help_table));
EXECUTE PROCEDURE test_15((select list(name) from help_table));
EXECUTE PROCEDURE test_16((select list(name) from help_table));
EXECUTE PROCEDURE test_17((select max(d) from help_table));
EXECUTE PROCEDURE test_18((select max(t) from help_table));
EXECUTE PROCEDURE test_19((select max(ts) from help_table));
EXECUTE PROCEDURE test_20((select max(d) from help_table));
EXECUTE PROCEDURE test_21((select max(flag) from help_table));
EXECUTE PROCEDURE test_22((select min(flag) from help_table));
commit;

select * from test_table;
"""

act_2 = isql_act('db_2', test_script_2)

expected_stdout_2 = """
COL
======================================================================================================================================================
46
23
46
23
46
23
46.00
23.0
46.0
23.0
46.0
Ann,Peter
Ann,Peter
Ann,Peter
Ann,Peter
Ann,Peter
2000-05-23
23:45:00
2000-05-23 09:36:00.0
2000-05-23
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
