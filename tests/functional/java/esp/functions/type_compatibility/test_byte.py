#coding:utf-8

"""
ID:          java.esp.functions.type-compatibility.byte
TITLE:       External function call with byte[] type of result and input parameter
DESCRIPTION: 
  External function is declared with SQL types compatible with byte[] Java type. Parameter as a constant.
FBTEST:      functional.java.esp.functions.type_compatibility.byte
"""

import pytest
from firebird.qa import *

init_script = """
create function test_1(i VARCHAR(15)) 
returns VARCHAR(15)
external name 'esp.TestFunction.byteInOut(byte[])' 
engine java;
commit;

create function test_2(i CHAR(15)) 
returns CHAR(15)
external name 'esp.TestFunction.byteInOut(byte[])' 
engine java;
commit;

create function test_3(i BLOB) 
returns BLOB
external name 'esp.TestFunction.byteInOut(byte[])' 
engine java;
commit;

"""

db = db_factory(init=init_script)

test_script = """
 SELECT TEST_1('varchar') FROM RDB$DATABASE;
 SELECT TEST_2('char') FROM RDB$DATABASE;
 SELECT cast(TEST_3('blob') as varchar(10)) as "TEST_3" FROM RDB$DATABASE;
 
"""

act = isql_act('db', test_script)

expected_stdout = """                 
TEST_1
===============
varchar

TEST_2
===============
char

TEST_3
==========
blob
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
