#coding:utf-8

"""
ID:          java.esp.procedures.type-compatibility.with-output-params.sql-time
TITLE:       External function call with java.sql.Time  type of input and output parameters
DESCRIPTION: 
  External function is declared with SQL types compatible with java.sql.Time Java type. Parameter as a constant
FBTEST:      functional.java.esp.procedures.type_compatibility.with_output_params.sql_time
"""

import pytest
from firebird.qa import *

# version: 3.0

init_script_1 = """

create procedure test_1(i CHAR(15)) 
returns(o CHAR(15))
external name 'esp.TestProcedure.timeInOut(java.sql.Time, java.sql.Time[])'
engine java;
commit;

create procedure test_2(i VARCHAR(15)) 
returns(o VARCHAR(15))
external name 'esp.TestProcedure.timeInOut(java.sql.Time, java.sql.Time[])'
engine java;
commit;

create procedure test_3(i BLOB) 
returns(o BLOB)
external name 'esp.TestProcedure.timeInOut(java.sql.Time, java.sql.Time[])'
engine java;
commit;

create procedure test_4(i TIME) 
returns(o TIME)
external name 'esp.TestProcedure.timeInOut(java.sql.Time, java.sql.Time[])'
engine java;
commit;

create procedure test_5(i TIMESTAMP)
returns(o TIMESTAMP) 
external name 'esp.TestProcedure.timeInOut(java.sql.Time, java.sql.Time[])'
engine java;
commit;


"""

db_1 = db_factory(init=init_script_1)

test_script_1 = """
set list on; 

EXECUTE PROCEDURE TEST_1('11:58:59');
EXECUTE PROCEDURE TEST_1('11.58.59.4043');

EXECUTE PROCEDURE TEST_2('09:00:34.345');
EXECUTE PROCEDURE TEST_2('09.00.34.345');

select cast(o as varchar(100)) from TEST_3('17:34');
select cast(o as varchar(100)) from TEST_3('17.34');

EXECUTE PROCEDURE TEST_4('07:27:47');
EXECUTE PROCEDURE TEST_4('07.27.47');

EXECUTE PROCEDURE TEST_5('23.09.1935 23:49');
EXECUTE PROCEDURE TEST_5('23.09.1935 23.49');
commit;

"""

act_1 = isql_act('db_1', test_script_1, substitutions=[('\\d{4}\\-\\d{2}\\-\\d{2}', 'date')])

expected_stdout_1 = """
O                               11:58:59.0000
O                               11:58:59.4040
O                               09:00:34.3450
O                               09:00:34.3450
CAST                            17:34:00.0000
CAST                            17:34:00.0000
O                               07:27:47.0000
O                               07:27:47.0000
O                               date 23:49:00.0000
O                               date 23:49:00.0000
"""

@pytest.mark.java
@pytest.mark.version('>=3.0,<4.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_stdout == act_1.clean_expected_stdout

# version: 4.0

init_script_2 = """

create procedure test_1(i CHAR(15))
returns(o CHAR(15))
external name 'esp.TestProcedure.timeInOut(java.sql.Time, java.sql.Time[])'
engine java;
commit;

create procedure test_2(i VARCHAR(15))
returns(o VARCHAR(15))
external name 'esp.TestProcedure.timeInOut(java.sql.Time, java.sql.Time[])'
engine java;
commit;

create procedure test_3(i BLOB)
returns(o BLOB)
external name 'esp.TestProcedure.timeInOut(java.sql.Time, java.sql.Time[])'
engine java;
commit;

create procedure test_4(i TIME)
returns(o TIME)
external name 'esp.TestProcedure.timeInOut(java.sql.Time, java.sql.Time[])'
engine java;
commit;

create procedure test_5(i TIMESTAMP)
returns(o TIMESTAMP)
external name 'esp.TestProcedure.timeInOut(java.sql.Time, java.sql.Time[])'
engine java;
commit;


"""

db_2 = db_factory(init=init_script_2)

test_script_2 = """
set list on;

EXECUTE PROCEDURE TEST_1('11:58:59');

EXECUTE PROCEDURE TEST_2('09:00:34.345');

select cast(o as varchar(100)) from TEST_3('17:34');

EXECUTE PROCEDURE TEST_4('07:27:47');

EXECUTE PROCEDURE TEST_5('23.09.1935 23:49');
commit;

"""

act_2 = isql_act('db_2', test_script_2, substitutions=[('\\d{4}\\-\\d{2}\\-\\d{2}', 'date')])

expected_stdout_2 = """
O                               11:58:59.0000
O                               09:00:34.3450
CAST                            17:34:00.0000
O                               07:27:47.0000
O                               date 23:49:00.0000
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
