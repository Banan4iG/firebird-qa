#coding:utf-8

"""
ID:          java.esp.functions.without-parameters.byte-result
TITLE:       External function call with byte[] type of result and without input parameter
DESCRIPTION: 
  External function is declared with SQL types compatible with byte[] Java type.
FBTEST:      functional.java.esp.functions.without_parameters.byte_result
"""

import pytest
from firebird.qa import *

init_script = """
create function test_1() 
returns VARCHAR(15)
external name 'esp.TestFunction.byteOut()' 
engine java;
commit;

create function test_2() 
returns CHAR(15)
external name 'esp.TestFunction.byteOut()' 
engine java;
commit;

create function test_3() 
returns BLOB
external name 'esp.TestFunction.byteOut()' 
engine java;
commit;

"""

db = db_factory(init=init_script)

test_script = """
 SELECT TEST_1() FROM RDB$DATABASE;
 SELECT TEST_2() FROM RDB$DATABASE;
 SELECT cast(TEST_3() as varchar(10)) as "TEST_3" FROM RDB$DATABASE;
 
"""

act = isql_act('db', test_script)

expected_stdout = """                 
TEST_1
===============
test
TEST_2
===============
test
TEST_3
==========
test
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
