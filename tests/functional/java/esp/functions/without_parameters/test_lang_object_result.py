#coding:utf-8

"""
ID:          java.esp.functions.without-parameters.lang-object-result
TITLE:       External function call with java.lang.Object type of result and without input parameter
DESCRIPTION: 
  External function is declared with SQL types compatible with java.lang.Object Java type.
FBTEST:      functional.java.esp.functions.without_parameters.lang_object_result
"""

import pytest
from firebird.qa import *

init_script = """

create function test_1() 
returns INTEGER
external name 'esp.TestFunction.objectOut()' 
engine java;
commit;

create function test_2() 
returns SMALLINT
external name 'esp.TestFunction.objectOut()'
engine java;
commit;


create function test_3() 
returns BIGINT
external name 'esp.TestFunction.objectOut()'
engine java;
commit;

create function test_4() 
returns NUMERIC(10,2)
external name 'esp.TestFunction.objectOut()'
engine java;
commit;

create function test_5() 
returns DECIMAL(10,2)
external name 'esp.TestFunction.objectOut()'
engine java;
commit;

create function test_6() 
returns FLOAT
external name 'esp.TestFunction.objectFloatOut()'
engine java;
commit;

create function test_7() 
returns DOUBLE PRECISION
external name 'esp.TestFunction.objectDoubleOut()'
engine java;
commit;

create function test_8() 
returns CHAR(10)
external name 'esp.TestFunction.objectStrintOut()'
engine java;
commit;

create function test_9() 
returns VARCHAR(10)
external name 'esp.TestFunction.objectStrintOut()'
engine java;
commit;

create function test_10() 
returns BLOB
external name 'esp.TestFunction.objectBlobOut()'
engine java;
commit;

create function test_11() 
returns DATE
external name 'esp.TestFunction.objectDateOut()'
engine java;
commit;

create function test_12() 
returns TIME
external name 'esp.TestFunction.objectTimeOut()'
engine java;
commit;

create function test_13() 
returns TIMESTAMP
external name 'esp.TestFunction.objectTimestampOut()'
engine java;
commit;

create function test_14() 
returns BOOLEAN
external name 'esp.TestFunction.objectBooleanOut()'
engine java;
commit;
"""

db = db_factory(init=init_script)

test_script = """
SELECT TEST_1() FROM RDB$DATABASE;
SELECT TEST_2() FROM RDB$DATABASE;
SELECT TEST_3() FROM RDB$DATABASE;
SELECT TEST_4() FROM RDB$DATABASE;
SELECT TEST_5() FROM RDB$DATABASE;

SELECT TEST_6() FROM RDB$DATABASE;
SELECT TEST_7() FROM RDB$DATABASE;

SELECT TEST_8() FROM RDB$DATABASE;
SELECT TEST_9() FROM RDB$DATABASE;
SELECT cast(TEST_10() as varchar(10)) as "TEST_10" FROM RDB$DATABASE;

SELECT TEST_11() FROM RDB$DATABASE;
SELECT TEST_12() FROM RDB$DATABASE;
SELECT TEST_13() FROM RDB$DATABASE;
SELECT TEST_14() FROM RDB$DATABASE;
"""

act = isql_act('db', test_script)

expected_stdout = """          
TEST_1
============
123
TEST_2
=======
123
TEST_3
=====================
123
TEST_4
=====================
123.00
TEST_5
=====================
123.00
TEST_6
==============
123.00000
TEST_7
=======================
123.0000000000000
TEST_8
==========
hello
TEST_9
==========
hello
TEST_10
==========
hello
TEST_11
===========
2008-04-09
TEST_12
=============
10:11:12.0000
TEST_13
=========================
2008-04-10 10:11:12.0000
TEST_14
=======
<true>
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
