#coding:utf-8

"""
ID:          java.esp.procedures.type-compatibility.lang-string
TITLE:       External function call with java.lang.String type of input parameter
DESCRIPTION: 
  External function is declared with SQL types compatible with java.lang.String Java type. Parameter as a constant.
FBTEST:      functional.java.esp.procedures.type_compatibility.lang_string
"""

import pytest
from firebird.qa import *

init_script = """
CREATE TABLE TEST_TABLE(F VARCHAR(35));
commit;

create procedure test_1(i INTEGER) 
external name 'esp.TestProcedure.stringIn(String)' 
engine java;
commit;

create procedure test_2(i SMALLINT) 
external name 'esp.TestProcedure.stringIn(String)'
engine java;
commit;

create procedure test_3(i BIGINT) 
external name 'esp.TestProcedure.stringIn(String)'
engine java;
commit;

create procedure test_4(i NUMERIC(10,2)) 
external name 'esp.TestProcedure.stringIn(String)'
engine java;
commit;

create procedure test_5(i DECIMAL(10,2)) 
external name 'esp.TestProcedure.stringIn(String)'
engine java;
commit;

create procedure test_6(i FLOAT) 
external name 'esp.TestProcedure.stringIn(String)'
engine java;
commit;

create procedure test_7(i DOUBLE PRECISION) 
external name 'esp.TestProcedure.stringIn(String)'
engine java;
commit;

create procedure test_8(i CHAR(10)) 
external name 'esp.TestProcedure.stringIn(String)'
engine java;
commit;

create procedure test_9(i VARCHAR(10)) 
external name 'esp.TestProcedure.stringIn(String)'
engine java;
commit;

create procedure test_10(i BLOB) 
external name 'esp.TestProcedure.stringIn(String)'
engine java;
commit;

create procedure test_11(i DATE) 
external name 'esp.TestProcedure.stringIn(String)'
engine java;
commit;

create procedure test_12(i TIME) 
external name 'esp.TestProcedure.stringIn(String)'
engine java;
commit;

create procedure test_13(i TIMESTAMP) 
external name 'esp.TestProcedure.stringIn(String)'
engine java;
commit;

create procedure test_14(i BOOLEAN) 
external name 'esp.TestProcedure.stringIn(String)'
engine java;
commit;

"""

db = db_factory(init=init_script)

test_script = """
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

EXECUTE PROCEDURE TEST_10('BLOB');
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


SELECT F FROM TEST_TABLE;
"""

act = isql_act('db', test_script)

expected_stdout = """
F
===================================
5
-6
14
<null>
5
-6
14
<null>
5
-6
14
<null>
5.00
-5.55
14.35
<null>
5.00
-5.55
14.35
<null>
F
===================================
5.0000000
-5.5500002
14.350000
<null>
5.000000000000000
-5.550000000000000
14.35000000000000
<null>
CHAR
<null>
VARCHAR
<null>
BLOB
<null>
1956-06-15
<null>
13:49:00.0000
<null>
1956-06-15 13:49:00.0000
<null>
F
===================================
FALSE
<null>
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
