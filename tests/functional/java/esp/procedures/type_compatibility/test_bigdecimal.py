#coding:utf-8

"""
ID:          java.esp.procedures.type-compatibility.bigdecimal
TITLE:       External function call with java.math.BigDecimal  type of input parameter
DESCRIPTION: 
  External function is declared with SQL types compatible with java.math.BigDecimal Java type. Parameter as a constant.
FBTEST:      functional.java.esp.procedures.type_compatibility.bigdecimal
"""

import pytest
from firebird.qa import *

init_script = """
CREATE TABLE TEST_TABLE(F_NUMERIC NUMERIC(15,2));
commit;

create procedure test_1(i SMALLINT) 
external name 'esp.TestProcedure.bigDecimalIn(java.math.BigDecimal)'
engine java;
commit;

create procedure test_2(i INTEGER) 
external name 'esp.TestProcedure.bigDecimalIn(java.math.BigDecimal)'
engine java;
commit;

create procedure test_3(i BIGINT) 
external name 'esp.TestProcedure.bigDecimalIn(java.math.BigDecimal)'
engine java;
commit;

create procedure test_4(i NUMERIC(10,2)) 
external name 'esp.TestProcedure.bigDecimalIn(java.math.BigDecimal)'
engine java;
commit;

create procedure test_5(i DECIMAL(10,2)) 
external name 'esp.TestProcedure.bigDecimalIn(java.math.BigDecimal)'
engine java;
commit;

create procedure test_6(i FLOAT) 
external name 'esp.TestProcedure.bigDecimalIn(java.math.BigDecimal)'
engine java;
commit;

create procedure test_7(i DOUBLE PRECISION) 
external name 'esp.TestProcedure.bigDecimalIn(java.math.BigDecimal)'
engine java;
commit;

create procedure test_8(i CHAR(10)) 
external name 'esp.TestProcedure.bigDecimalIn(java.math.BigDecimal)'
engine java;
commit;

create procedure test_9(i VARCHAR(10)) 
external name 'esp.TestProcedure.bigDecimalIn(java.math.BigDecimal)'
engine java;
commit;

create procedure test_10(i BLOB) 
external name 'esp.TestProcedure.bigDecimalIn(java.math.BigDecimal)'
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

EXECUTE PROCEDURE TEST_8(5);
EXECUTE PROCEDURE TEST_8(-5.55);
EXECUTE PROCEDURE TEST_8(14.35);
EXECUTE PROCEDURE TEST_8(null);
commit;

EXECUTE PROCEDURE TEST_9(5);
EXECUTE PROCEDURE TEST_9(-5.55);
EXECUTE PROCEDURE TEST_9(14.35);
EXECUTE PROCEDURE TEST_9(null);
commit;

EXECUTE PROCEDURE TEST_10(5);
EXECUTE PROCEDURE TEST_10(-5.55);
EXECUTE PROCEDURE TEST_10(14.35);
EXECUTE PROCEDURE TEST_10(null);
commit;

SELECT F_NUMERIC FROM TEST_TABLE;
"""

act = isql_act('db', test_script)

expected_stdout = """
F_NUMERIC
=====================
5.00
-6.00
14.00
<null>
5.00
-6.00
14.00
<null>
5.00
-6.00
14.00
<null>
5.00
-5.55
14.35
<null>
5.00
-5.55
14.35
<null>
F_NUMERIC
=====================
5.00
-5.55
14.35
<null>
5.00
-5.55
14.35
<null>
5.00
-5.55
14.35
<null>
5.00
-5.55
14.35
<null>
5.00
-5.55
14.35
<null>
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
