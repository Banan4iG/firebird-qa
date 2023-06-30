#coding:utf-8

"""
ID:          java.esp.functions.without-parameters.time-result
TITLE:       External function call with java.sql.Time type of result and without input parameter
DESCRIPTION: 
  External function is declared with SQL types compatible with java.sql.Time Java type.
FBTEST:      functional.java.esp.functions.without_parameters.time_result
"""

import pytest
from firebird.qa import *

substitutions = [('\\d{4}-\\d{2}-\\d{2}\\s\\d{2}:\\d{2}:\\d{2}\\.\\d{4}', '10:11:12.0000')]

init_script = """
create function test_1() 
returns CHAR(15)
external name 'esp.TestFunction.timeOut()'
engine java;
commit;

create function test_2() 
returns VARCHAR(15)
external name 'esp.TestFunction.timeOut()'
engine java;
commit;

create function test_3() 
returns BLOB
external name 'esp.TestFunction.timeOut()'
engine java;
commit;

create function test_4() 
returns TIME
external name 'esp.TestFunction.timeOut()'
engine java;
commit;

create function test_5() 
returns TIMESTAMP
external name 'esp.TestFunction.timeOut()'
engine java;
commit;
"""

db = db_factory(init=init_script)

test_script = """
 
SELECT TEST_1() FROM RDB$DATABASE;
SELECT TEST_2() FROM RDB$DATABASE;
SELECT cast(TEST_3() as varchar(15)) as "TEST_3" FROM RDB$DATABASE;
SELECT TEST_4() FROM RDB$DATABASE;
SELECT TEST_5() FROM RDB$DATABASE;
"""

act = isql_act('db', test_script, substitutions=substitutions)

expected_stdout = """         
TEST_1
===============
10:11:12.0000
TEST_2
===============
10:11:12.0000
TEST_3
===============
10:11:12.0000
TEST_4
=============
10:11:12.0000
TEST_5
=========================
10:11:12.0000
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
