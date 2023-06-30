#coding:utf-8

"""
ID:          java.esp.procedures.argument-expression.string-expression
TITLE:       External procedure call with input parameter as an string expression
DESCRIPTION: 
FBTEST:      functional.java.esp.procedures.argument_expression.string_expression
"""

import pytest
from firebird.qa import *

# version: 3.0

init_script_1 = """
CREATE TABLE TEST_TABLE(col varchar(150));
commit;  
 
create procedure test_1(i VARCHAR(10)) 
external name 'esp.TestProcedure.stringIn(String)'
engine java;
commit;

create procedure test_2(i VARCHAR(10)) 
external name 'esp.TestProcedure.byteIn(byte[])'
engine java;
commit;

create procedure test_3(i VARCHAR(10)) 
external name 'esp.TestProcedure.ObjectIn(Object)'
engine java;
commit;

create procedure test_4(i BLOB) 
external name 'esp.TestProcedure.sqlblobIn(java.sql.Blob)'
engine java;
commit;

create procedure test_5(i BLOB) 
external name 'esp.TestProcedure.blobIn(org.firebirdsql.jdbc.FirebirdBlob)'
engine java;
commit;

"""

db_1 = db_factory(init=init_script_1)

test_script_1 = """
EXECUTE PROCEDURE TEST_1('test '||'#1');
EXECUTE PROCEDURE TEST_2('test '||'#2');
EXECUTE PROCEDURE TEST_3('test '||'#3');
EXECUTE PROCEDURE TEST_4('test '||'#4');
EXECUTE PROCEDURE TEST_5('test '||'#5');
commit;

select * from test_table;
"""

act_1 = isql_act('db_1', test_script_1)

expected_stdout_1 = """        
COL
===============================================================================
test #1
test #2
test #3
test #4
test #5
"""

@pytest.mark.java
@pytest.mark.version('>=3.0,<4.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_stdout == act_1.clean_expected_stdout

# version: 4.0

init_script_2 = """
CREATE TABLE TEST_TABLE(col varchar(150));
commit;

create procedure test_1(i VARCHAR(10))
external name 'esp.TestProcedure.stringIn(String)'
engine java;
commit;

create procedure test_2(i VARCHAR(10))
external name 'esp.TestProcedure.byteIn(byte[])'
engine java;
commit;

create procedure test_3(i VARCHAR(10))
external name 'esp.TestProcedure.ObjectIn(Object)'
engine java;
commit;

create procedure test_4(i BLOB)
external name 'esp.TestProcedure.sqlblobIn(java.sql.Blob)'
engine java;
commit;

create procedure test_5(i BLOB)
external name 'esp.TestProcedure.blobIn(org.firebirdsql.jdbc.FirebirdBlob)'
engine java;
commit;

"""

db_2 = db_factory(init=init_script_2)

test_script_2 = """
EXECUTE PROCEDURE TEST_1('test '||'#1');
EXECUTE PROCEDURE TEST_2('test '||'#2');
EXECUTE PROCEDURE TEST_3('test '||'#3');
EXECUTE PROCEDURE TEST_4('test '||'#4');
EXECUTE PROCEDURE TEST_5('test '||'#5');
commit;

select * from test_table;
"""

act_2 = isql_act('db_2', test_script_2)

expected_stdout_2 = """
COL
======================================================================================================================================================
test #1
test #2
test #3
test #4
test #5
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
