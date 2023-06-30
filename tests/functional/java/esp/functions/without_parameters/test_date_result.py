#coding:utf-8

"""
ID:          java.esp.functions.without-parameters.date-result
TITLE:       External function call with java.sql.Date type of result and without input parameter
DESCRIPTION: 
  External function is declared with SQL types compatible with java.sql.Date Java type.
FBTEST:      functional.java.esp.functions.without_parameters.date_result
"""

import pytest
from firebird.qa import *

init_script = """

create function test_1() 
returns CHAR(15)
external name 'esp.TestFunction.dateOut()'
engine java;
commit;

create function test_2() 
returns VARCHAR(15)
external name 'esp.TestFunction.dateOut()'
engine java;
commit;

create function test_3() 
returns BLOB
external name 'esp.TestFunction.dateOut()'
engine java;
commit;

create function test_4() 
returns DATE
external name 'esp.TestFunction.dateOut()'
engine java;
commit;

create function test_5() 
returns TIMESTAMP
external name 'esp.TestFunction.dateOut()'
engine java;
commit;

"""

db = db_factory(init=init_script)

test_script = """
SELECT TEST_1() FROM RDB$DATABASE;
SELECT TEST_2() FROM RDB$DATABASE;
SELECT cast(TEST_3() as varchar(10)) as "TEST_3" FROM RDB$DATABASE;
SELECT TEST_4() FROM RDB$DATABASE;
SELECT TEST_5() FROM RDB$DATABASE;

"""

act = isql_act('db', test_script)

expected_stdout = """       
TEST_1
===============
2008-04-09
TEST_2
===============
2008-04-09
TEST_3
==========
2008-04-09
TEST_4
===========
2008-04-09
TEST_5
=========================
2008-04-09 00:00:00.0000
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
