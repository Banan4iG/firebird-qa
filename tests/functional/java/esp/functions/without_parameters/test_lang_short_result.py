#coding:utf-8

"""
ID:          java.esp.functions.without-parameters.lang-short-result
TITLE:       External function call with java.lang.Short type of result and without input parameter
DESCRIPTION: 
  External function is declared with SQL types compatible with java.lang.Short Java type.
FBTEST:      functional.java.esp.functions.without_parameters.lang_short_result
"""

import pytest
from firebird.qa import *

init_script = """
create function test_1() 
returns smallint
external name 'esp.TestFunction.ShortOut()'
engine java;
commit;

create function test_2() 
returns integer
external name 'esp.TestFunction.ShortOut()'
engine java;
commit;

create function test_3() 
returns BIGINT
external name 'esp.TestFunction.ShortOut()'
engine java;
commit;

create function test_4() 
returns NUMERIC(10,2)
external name 'esp.TestFunction.ShortOut()'
engine java;
commit;

create function test_5() 
returns DECIMAL(10,2)
external name 'esp.TestFunction.ShortOut()'
engine java;
commit;

create function test_6() 
returns FLOAT
external name 'esp.TestFunction.ShortOut()'
engine java;
commit;

create function test_7() 
returns DOUBLE PRECISION
external name 'esp.TestFunction.ShortOut()'
engine java;
commit;

create function test_8() 
returns CHAR(10)
external name 'esp.TestFunction.ShortOut()'
engine java;
commit;

create function test_9() 
returns VARCHAR(10)
external name 'esp.TestFunction.ShortOut()'
engine java;
commit;

create function test_10() 
returns BLOB
external name 'esp.TestFunction.ShortOut()'
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
"""

act = isql_act('db', test_script)

expected_stdout = """   
TEST_1
=======
10
TEST_2
============
10
TEST_3
=====================
10
TEST_4
=====================
10.00
TEST_5
=====================
10.00
TEST_6
==============
10.000000
TEST_7
=======================
10.00000000000000
TEST_8
==========
10
TEST_9
==========
10
TEST_10
====================
10
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
