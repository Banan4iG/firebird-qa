#coding:utf-8

"""
ID:          java.esp.procedures.type-compatibility.sql-time
TITLE:       External function call with java.sql.Time  type of input parameter
DESCRIPTION: 
  External function is declared with SQL types compatible with java.sql.Time Java type. Parameter as a constant
FBTEST:      functional.java.esp.procedures.type_compatibility.sql_time
"""

import pytest
from firebird.qa import *

# version: 3.0

init_script_1 = """
CREATE TABLE TEST_TABLE (F_TIME TIME);
commit;

create procedure test_1(i CHAR(15)) 
external name 'esp.TestProcedure.timeIn(java.sql.Time)'
engine java;
commit;

create procedure test_2(i VARCHAR(15)) 
external name 'esp.TestProcedure.timeIn(java.sql.Time)'
engine java;
commit;

create procedure test_3(i BLOB) 
external name 'esp.TestProcedure.timeIn(java.sql.Time)'
engine java;
commit;

create procedure test_4(i TIME) 
external name 'esp.TestProcedure.timeIn(java.sql.Time)'
engine java;
commit;

create procedure test_5(i TIMESTAMP) 
external name 'esp.TestProcedure.timeIn(java.sql.Time)'
engine java;
commit;


"""

db_1 = db_factory(init=init_script_1)

test_script_1 = """

EXECUTE PROCEDURE TEST_1('11:58:59');
EXECUTE PROCEDURE TEST_1('11.58.59.4043');

EXECUTE PROCEDURE TEST_2('09:00:34.345');
EXECUTE PROCEDURE TEST_2('09.00.34.345');

EXECUTE PROCEDURE TEST_3('17:34');
EXECUTE PROCEDURE TEST_3('17.34');

EXECUTE PROCEDURE TEST_4('07:27:47');
EXECUTE PROCEDURE TEST_4('07.27.47');

EXECUTE PROCEDURE TEST_5('23.09.1935 23:49');
EXECUTE PROCEDURE TEST_5('23.09.1935 23.49');
commit;

SELECT F_TIME FROM TEST_TABLE;
"""

act_1 = isql_act('db_1', test_script_1)

expected_stdout_1 = """
F_TIME
=============
11:58:59.0000
11:58:59.4040
09:00:34.3450
09:00:34.3450
17:34:00.0000
17:34:00.0000
07:27:47.0000
07:27:47.0000
23:49:00.0000
23:49:00.0000
"""

@pytest.mark.java
@pytest.mark.version('>=3.0,<4.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_stdout == act_1.clean_expected_stdout

# version: 4.0

init_script_2 = """
CREATE TABLE TEST_TABLE (F_TIME TIME);
commit;

create procedure test_1(i CHAR(15))
external name 'esp.TestProcedure.timeIn(java.sql.Time)'
engine java;
commit;

create procedure test_2(i VARCHAR(15))
external name 'esp.TestProcedure.timeIn(java.sql.Time)'
engine java;
commit;

create procedure test_3(i BLOB)
external name 'esp.TestProcedure.timeIn(java.sql.Time)'
engine java;
commit;

create procedure test_4(i TIME)
external name 'esp.TestProcedure.timeIn(java.sql.Time)'
engine java;
commit;

create procedure test_5(i TIMESTAMP)
external name 'esp.TestProcedure.timeIn(java.sql.Time)'
engine java;
commit;


"""

db_2 = db_factory(init=init_script_2)

test_script_2 = """

EXECUTE PROCEDURE TEST_1('11:58:59');

EXECUTE PROCEDURE TEST_2('09:00:34.345');

EXECUTE PROCEDURE TEST_3('17:34');

EXECUTE PROCEDURE TEST_4('07:27:47');

EXECUTE PROCEDURE TEST_5('23.09.1935 23:49');
commit;

SELECT F_TIME FROM TEST_TABLE;
"""

act_2 = isql_act('db_2', test_script_2)

expected_stdout_2 = """
F_TIME
=============
11:58:59.0000
09:00:34.3450
17:34:00.0000
07:27:47.0000
23:49:00.0000
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
