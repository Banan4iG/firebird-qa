#coding:utf-8

"""
ID:          java.esp.functions.argument-expression.string-expression
TITLE:       External function call with input parameter as an string expression
DESCRIPTION: 
FBTEST:      functional.java.esp.functions.argument_expression.string_expression
"""

import pytest
from firebird.qa import *

init_script = """
create function test_1(i VARCHAR(10)) 
returns VARCHAR(10)
external name 'esp.TestFunction.stringInOut(String)'
engine java;
commit;

create function test_2(i VARCHAR(10)) 
returns VARCHAR(10)
external name 'esp.TestFunction.byteInOut(byte[])'
engine java;
commit;

create function test_3(i VARCHAR(10)) 
returns VARCHAR(10)
external name 'esp.TestFunction.ObjectInOut(Object)'
engine java;
commit;

create function test_4(i BLOB) 
returns BLOB
external name 'esp.TestFunction.blobInOut2(java.sql.Blob)'
engine java;
commit;

create function test_5(i BLOB) 
returns BLOB
external name 'esp.TestFunction.blobInOut(org.firebirdsql.jdbc.FirebirdBlob)'
engine java;
commit;
"""

db = db_factory(init=init_script)

test_script = """
SELECT TEST_1('test '||'#1') FROM RDB$DATABASE;
SELECT TEST_2('test '||'#2') FROM RDB$DATABASE;
SELECT TEST_3('test '||'#3') FROM RDB$DATABASE;
SELECT cast(TEST_4('test '||'#4') as varchar(10)) as "TEST_4" FROM RDB$DATABASE;
SELECT cast(TEST_5('test '||'#5') as varchar(10)) as "TEST_5" FROM RDB$DATABASE;
"""

act = isql_act('db', test_script)

expected_stdout = """        
	
TEST_1
==========
test #1
TEST_2
==========
test #2
TEST_3
==========
test #3
TEST_4
==========
test #4
TEST_5
==========
test #5
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
