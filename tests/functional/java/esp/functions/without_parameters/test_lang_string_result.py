#coding:utf-8

"""
ID:          java.esp.functions.without-parameters.lang-string-result
TITLE:       External function call with java.lang.String type of result and without input parameter
DESCRIPTION: 
  External function is declared with SQL types compatible with java.lang.String Java type.
FBTEST:      functional.java.esp.functions.without_parameters.lang_string_result
"""

import pytest
from firebird.qa import *

init_script = """
create function test_1() 
returns INTEGER
external name 'esp.TestFunction.stringOut()' 
engine java;
commit;

create function test_2() 
returns SMALLINT
external name 'esp.TestFunction.stringOut()'
engine java;
commit;


create function test_3() 
returns BIGINT
external name 'esp.TestFunction.stringOut()'
engine java;
commit;

create function test_4() 
returns NUMERIC(10,2)
external name 'esp.TestFunction.stringOut()'
engine java;
commit;

create function test_5() 
returns DECIMAL(10,2)
external name 'esp.TestFunction.stringOut()'
engine java;
commit;

create function test_6() 
returns FLOAT
external name 'esp.TestFunction.stringOut()'
engine java;
commit;

create function test_7() 
returns DOUBLE PRECISION
external name 'esp.TestFunction.stringOut()'
engine java;
commit;

create function test_8() 
returns CHAR(10)
external name 'esp.TestFunction.stringOut()'
engine java;
commit;

create function test_9() 
returns VARCHAR(10)
external name 'esp.TestFunction.stringOut()'
engine java;
commit;

create function test_10() 
returns BLOB
external name 'esp.TestFunction.stringOut()'
engine java;
commit;

create function test_11() 
returns DATE
external name 'esp.TestFunction.stringDateOut()'
engine java;
commit;

create function test_12() 
returns TIME
external name 'esp.TestFunction.stringTimeOut()'
engine java;
commit;

create function test_13() 
returns TIMESTAMP
external name 'esp.TestFunction.stringTimestampOut()'
engine java;
commit;

create function test_14() 
returns BOOLEAN
external name 'esp.TestFunction.stringBooleanOut()'
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
SELECT cast(TEST_10() as varchar(20)) as "TEST_10" FROM RDB$DATABASE;
SELECT TEST_11() FROM RDB$DATABASE;  
SELECT TEST_12() FROM RDB$DATABASE;  
SELECT TEST_13() FROM RDB$DATABASE;  
SELECT TEST_14() FROM RDB$DATABASE;
"""

act = isql_act('db', test_script)

expected_stdout = """
TEST_1
============
120
TEST_2
=======
120
TEST_3
=====================
120
TEST_4
=====================
120.34
TEST_5
=====================
120.34
TEST_6
==============
120.34000
TEST_7
=======================
120.3400000000000
TEST_8
==========
120.34
TEST_9
==========
120.34
TEST_10
====================
120.34
TEST_11
===========
2343-09-12
TEST_12
=============
12:34:56.0000
TEST_13
=========================
1956-09-12 00:00:00.0000
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
