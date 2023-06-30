#coding:utf-8

"""
ID:          java.esp.procedures.type-compatibility.with-output-params.lang-object
TITLE:       External function call with java.lang.Object type of input and output parameters
DESCRIPTION: 
  External function is declared with SQL types compatible with java.lang.Object Java type. Parameter as a constant.
FBTEST:      functional.java.esp.procedures.type_compatibility.with_output_params.lang_object
"""

import pytest
from firebird.qa import *

init_script = """

create procedure test_1(i INTEGER) 
returns(o INTEGER)
external name 'esp.TestProcedure.ObjectInOut(Object, Object[])' 
engine java;
commit;

create procedure test_2(i SMALLINT) 
returns(o SMALLINT)
external name 'esp.TestProcedure.ObjectInOut(Object, Object[])'
engine java;
commit;

create procedure test_3(i BIGINT) 
returns(o BIGINT)
external name 'esp.TestProcedure.ObjectInOut(Object, Object[])'
engine java;
commit;

create procedure test_4(i NUMERIC(10,2)) 
returns(o NUMERIC(10,2))
external name 'esp.TestProcedure.ObjectInOut(Object, Object[])'
engine java;
commit;

create procedure test_5(i DECIMAL(10,2)) 
returns(o DECIMAL(10,2))
external name 'esp.TestProcedure.ObjectInOut(Object, Object[])'
engine java;
commit;

create procedure test_6(i FLOAT) 
returns(o FLOAT)
external name 'esp.TestProcedure.ObjectInOut(Object, Object[])'
engine java;
commit;

create procedure test_7(i DOUBLE PRECISION) 
returns(o DOUBLE PRECISION)
external name 'esp.TestProcedure.ObjectInOut(Object, Object[])'
engine java;
commit;

create procedure test_8(i CHAR(10)) 
returns(o CHAR(10))
external name 'esp.TestProcedure.ObjectInOut(Object, Object[])'
engine java;
commit;

create procedure test_9(i VARCHAR(10)) 
returns(o VARCHAR(10))
external name 'esp.TestProcedure.ObjectInOut(Object, Object[])'
engine java;
commit;

create procedure test_10(i blob) 
returns(o blob)
external name 'esp.TestProcedure.ObjectInOut(Object, Object[])'
engine java;
commit;

create procedure test_11(i DATE) 
returns(o DATE)
external name 'esp.TestProcedure.ObjectInOut(Object, Object[])'
engine java;
commit;

create procedure test_12(i TIME) 
returns(o TIME)
external name 'esp.TestProcedure.ObjectInOut(Object, Object[])'
engine java;
commit;

create procedure test_13(i TIMESTAMP) 
returns(o TIMESTAMP)
external name 'esp.TestProcedure.ObjectInOut(Object, Object[])'
engine java;
commit;

create procedure test_14(i BOOLEAN) 
returns(o BOOLEAN)
external name 'esp.TestProcedure.ObjectInOut(Object, Object[])'
engine java;
commit;
"""

db = db_factory(init=init_script)

test_script = """
set list on; 
 
EXECUTE PROCEDURE TEST_1(5);
EXECUTE PROCEDURE TEST_1(-5.55);
EXECUTE PROCEDURE TEST_1(14.35);
EXECUTE PROCEDURE TEST_1(null);
commit;

EXECUTE PROCEDURE TEST_2(5);
EXECUTE PROCEDURE TEST_2(-5.55);
EXECUTE PROCEDURE TEST_2(14.35);
EXECUTE PROCEDURE TEST_2(null);
commit;

EXECUTE PROCEDURE TEST_3(5);
EXECUTE PROCEDURE TEST_3(-5.55);
EXECUTE PROCEDURE TEST_3(14.35);
EXECUTE PROCEDURE TEST_3(null);
commit;

EXECUTE PROCEDURE TEST_4(5);
EXECUTE PROCEDURE TEST_4(-5.55);
EXECUTE PROCEDURE TEST_4(14.35);
EXECUTE PROCEDURE TEST_4(null);
commit;

EXECUTE PROCEDURE TEST_5(5);
EXECUTE PROCEDURE TEST_5(-5.55);
EXECUTE PROCEDURE TEST_5(14.35);
EXECUTE PROCEDURE TEST_5(null);
commit;

EXECUTE PROCEDURE TEST_6(5);
EXECUTE PROCEDURE TEST_6(-5.55);
EXECUTE PROCEDURE TEST_6(14.35);
EXECUTE PROCEDURE TEST_6(null);
commit;

EXECUTE PROCEDURE TEST_7(5);
EXECUTE PROCEDURE TEST_7(-5.55);
EXECUTE PROCEDURE TEST_7(14.35);
EXECUTE PROCEDURE TEST_7(null);
commit;

EXECUTE PROCEDURE TEST_8('CHAR');
EXECUTE PROCEDURE TEST_8(null);
commit;

EXECUTE PROCEDURE TEST_9('VARCHAR');
EXECUTE PROCEDURE TEST_9(null);
commit;

select cast(o as varchar(100)) from TEST_10('BLOB');
EXECUTE PROCEDURE TEST_10(null);
commit;

EXECUTE PROCEDURE TEST_11('15.06.1956');
EXECUTE PROCEDURE TEST_11(null);
commit;

EXECUTE PROCEDURE TEST_12('13:49');
EXECUTE PROCEDURE TEST_12(null);
commit;

EXECUTE PROCEDURE TEST_13('15.06.1956 13:49');
EXECUTE PROCEDURE TEST_13(null);
commit;

EXECUTE PROCEDURE TEST_14(false);
EXECUTE PROCEDURE TEST_14(null);
commit;

"""

act = isql_act('db', test_script)

expected_stdout = """          
O                               5
O                               -6
O                               14
O                               <null>
O                               5
O                               -6
O                               14
O                               <null>
O                               5
O                               -6
O                               14
O                               <null>
O                               5.00
O                               -5.55
O                               14.35
O                               <null>
O                               5.00
O                               -5.55
O                               14.35
O                               <null>
O                               5
O                               -5.5500002
O                               14.35
O                               <null>
O                               5.000000000000000
O                               -5.550000000000000
O                               14.35000000000000
O                               <null>
O                               CHAR
O                               <null>
O                               VARCHAR
O                               <null>
CAST                            BLOB
O                               <null>
O                               1956-06-15
O                               <null>
O                               13:49:00.0000
O                               <null>
O                               1956-06-15 13:49:00.0000
O                               <null>
O                               <false>
O                               <null>
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
