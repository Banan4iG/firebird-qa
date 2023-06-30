#coding:utf-8

"""
ID:          java.esp.procedures.type-compatibility.with-output-params.sql-date
TITLE:       External function call with java.sql.Date  type of input and output parameter
DESCRIPTION: 
  External function is declared with SQL types compatible with java.sql.Date Java type. Parameter as a constant.
FBTEST:      functional.java.esp.procedures.type_compatibility.with_output_params.sql_date
"""

import pytest
from firebird.qa import *

# version: 3.0

init_script_1 = """

create procedure test_1(i CHAR(15)) 
returns(o CHAR(15))
external name 'esp.TestProcedure.dateInOut(java.sql.Date, java.sql.Date[])'
engine java;
commit;

create procedure test_2(i VARCHAR(15)) 
returns(o VARCHAR(15))
external name 'esp.TestProcedure.dateInOut(java.sql.Date, java.sql.Date[])'
engine java;
commit;

create procedure test_3(i BLOB) 
returns(o BLOB)
external name 'esp.TestProcedure.dateInOut(java.sql.Date, java.sql.Date[])'
engine java;
commit;

create procedure test_4(i DATE) 
returns(o DATE)
external name 'esp.TestProcedure.dateInOut(java.sql.Date, java.sql.Date[])'
engine java;
commit;

create procedure test_5(i TIMESTAMP) 
returns(o TIMESTAMP)
external name 'esp.TestProcedure.dateInOut(java.sql.Date, java.sql.Date[])'
engine java;
commit;

"""

db_1 = db_factory(init=init_script_1)

test_script_1 = """
set list on;

EXECUTE PROCEDURE TEST_1('14-JUL-2007');
EXECUTE PROCEDURE TEST_1('07-14-2007');
EXECUTE PROCEDURE TEST_1('07/14/2007');
EXECUTE PROCEDURE TEST_1('2007-07-14');
EXECUTE PROCEDURE TEST_1('2007/07/14');
EXECUTE PROCEDURE TEST_1('2007.07.14');
EXECUTE PROCEDURE TEST_1('14.07.2007');
commit;

EXECUTE PROCEDURE TEST_2('25-NOV-1920');
EXECUTE PROCEDURE TEST_2('11-25-1920');
EXECUTE PROCEDURE TEST_2('11/25/1920');
EXECUTE PROCEDURE TEST_2('1920-11-25');
EXECUTE PROCEDURE TEST_2('1920/11/25');
EXECUTE PROCEDURE TEST_2('1920.11.25');
EXECUTE PROCEDURE TEST_2('25.11.1920');
commit;

select cast(o as varchar(100)) from TEST_3('1-FEB-2018');
select cast(o as varchar(100)) from TEST_3('1.02.2018');
select cast(o as varchar(100)) from TEST_3('02-01-2018');
select cast(o as varchar(100)) from TEST_3('02/01/2018');
select cast(o as varchar(100)) from TEST_3('2018/02-01');
select cast(o as varchar(100)) from TEST_3('2018/02/01');
select cast(o as varchar(100)) from TEST_3('2018.02.01');
commit;

EXECUTE PROCEDURE TEST_4('7-OCT-2100');
EXECUTE PROCEDURE TEST_4('7.10.2100');
EXECUTE PROCEDURE TEST_4('10-07-2100');
EXECUTE PROCEDURE TEST_4('10/07/2100');
EXECUTE PROCEDURE TEST_4('2100-10-07');
EXECUTE PROCEDURE TEST_4('2100/10/07');
EXECUTE PROCEDURE TEST_4('2100.10.07');
commit;

EXECUTE PROCEDURE TEST_5('19-May-1023 23:45');
EXECUTE PROCEDURE TEST_5('19.05.1023 4:35:56');
EXECUTE PROCEDURE TEST_5('05-19-1023');
EXECUTE PROCEDURE TEST_5('05/19/1023');
EXECUTE PROCEDURE TEST_5('1023-05-19');
EXECUTE PROCEDURE TEST_5('1023/05/19');
EXECUTE PROCEDURE TEST_5('1023.05.19');
commit;

"""

act_1 = isql_act('db_1', test_script_1)

expected_stdout_1 = """
O                               2007-07-14
O                               2007-07-14
O                               2007-07-14
O                               2007-07-14
O                               2007-07-14
O                               2007-07-14
O                               2007-07-14
O                               1920-11-25
O                               1920-11-25
O                               1920-11-25
O                               1920-11-25
O                               1920-11-25
O                               1920-11-25
O                               1920-11-25
CAST                            2018-02-01
CAST                            2018-02-01
CAST                            2018-02-01
CAST                            2018-02-01
CAST                            2018-02-01
CAST                            2018-02-01
CAST                            2018-02-01
O                               2100-10-07
O                               2100-10-07
O                               2100-10-07
O                               2100-10-07
O                               2100-10-07
O                               2100-10-07
O                               2100-10-07
O                               1023-05-19 00:00:00.0000
O                               1023-05-19 00:00:00.0000
O                               1023-05-19 00:00:00.0000
O                               1023-05-19 00:00:00.0000
O                               1023-05-19 00:00:00.0000
O                               1023-05-19 00:00:00.0000
O                               1023-05-19 00:00:00.0000
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
external name 'esp.TestProcedure.dateInOut(java.sql.Date, java.sql.Date[])'
engine java;
commit;

create procedure test_2(i VARCHAR(15))
returns(o VARCHAR(15))
external name 'esp.TestProcedure.dateInOut(java.sql.Date, java.sql.Date[])'
engine java;
commit;

create procedure test_3(i BLOB)
returns(o BLOB)
external name 'esp.TestProcedure.dateInOut(java.sql.Date, java.sql.Date[])'
engine java;
commit;

create procedure test_4(i DATE)
returns(o DATE)
external name 'esp.TestProcedure.dateInOut(java.sql.Date, java.sql.Date[])'
engine java;
commit;

create procedure test_5(i TIMESTAMP)
returns(o TIMESTAMP)
external name 'esp.TestProcedure.dateInOut(java.sql.Date, java.sql.Date[])'
engine java;
commit;

"""

db_2 = db_factory(init=init_script_2)

test_script_2 = """
set list on;

EXECUTE PROCEDURE TEST_1('14-JUL-2007');
EXECUTE PROCEDURE TEST_1('07-14-2007');
EXECUTE PROCEDURE TEST_1('07/14/2007');
EXECUTE PROCEDURE TEST_1('2007-07-14');
EXECUTE PROCEDURE TEST_1('2007/07/14');
EXECUTE PROCEDURE TEST_1('2007.07.14');
EXECUTE PROCEDURE TEST_1('14.07.2007');
commit;

EXECUTE PROCEDURE TEST_2('25-NOV-1920');
EXECUTE PROCEDURE TEST_2('11-25-1920');
EXECUTE PROCEDURE TEST_2('11/25/1920');
EXECUTE PROCEDURE TEST_2('1920-11-25');
EXECUTE PROCEDURE TEST_2('1920/11/25');
EXECUTE PROCEDURE TEST_2('1920.11.25');
EXECUTE PROCEDURE TEST_2('25.11.1920');
commit;

select cast(o as varchar(100)) from TEST_3('1-FEB-2018');
select cast(o as varchar(100)) from TEST_3('1.02.2018');
select cast(o as varchar(100)) from TEST_3('02-01-2018');
select cast(o as varchar(100)) from TEST_3('02/01/2018');
select cast(o as varchar(100)) from TEST_3('2018/02/01');
select cast(o as varchar(100)) from TEST_3('2018.02.01');
commit;

EXECUTE PROCEDURE TEST_4('7-OCT-2100');
EXECUTE PROCEDURE TEST_4('7.10.2100');
EXECUTE PROCEDURE TEST_4('10-07-2100');
EXECUTE PROCEDURE TEST_4('10/07/2100');
EXECUTE PROCEDURE TEST_4('2100-10-07');
EXECUTE PROCEDURE TEST_4('2100/10/07');
EXECUTE PROCEDURE TEST_4('2100.10.07');
commit;

EXECUTE PROCEDURE TEST_5('19-May-1023 23:45');
EXECUTE PROCEDURE TEST_5('19.05.1023 4:35:56');
EXECUTE PROCEDURE TEST_5('05-19-1023');
EXECUTE PROCEDURE TEST_5('05/19/1023');
EXECUTE PROCEDURE TEST_5('1023-05-19');
EXECUTE PROCEDURE TEST_5('1023/05/19');
EXECUTE PROCEDURE TEST_5('1023.05.19');
commit;

"""

act_2 = isql_act('db_2', test_script_2)

expected_stdout_2 = """
O                               2007-07-14
O                               2007-07-14
O                               2007-07-14
O                               2007-07-14
O                               2007-07-14
O                               2007-07-14
O                               2007-07-14
O                               1920-11-25
O                               1920-11-25
O                               1920-11-25
O                               1920-11-25
O                               1920-11-25
O                               1920-11-25
O                               1920-11-25
CAST                            2018-02-01
CAST                            2018-02-01
CAST                            2018-02-01
CAST                            2018-02-01
CAST                            2018-02-01
CAST                            2018-02-01
O                               2100-10-07
O                               2100-10-07
O                               2100-10-07
O                               2100-10-07
O                               2100-10-07
O                               2100-10-07
O                               2100-10-07
O                               1023-05-19 00:00:00.0000
O                               1023-05-19 00:00:00.0000
O                               1023-05-19 00:00:00.0000
O                               1023-05-19 00:00:00.0000
O                               1023-05-19 00:00:00.0000
O                               1023-05-19 00:00:00.0000
O                               1023-05-19 00:00:00.0000
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
