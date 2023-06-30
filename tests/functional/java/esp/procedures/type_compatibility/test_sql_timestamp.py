#coding:utf-8

"""
ID:          java.esp.procedures.type-compatibility.sql-timestamp
TITLE:       External function call with java.sql.Timestamp  type of input parameter
DESCRIPTION: 
  External function is declared with SQL types compatible with java.sql.Timestamp Java type. Parameter as a constant
FBTEST:      functional.java.esp.procedures.type_compatibility.sql_timestamp
"""

import pytest
from firebird.qa import *

# version: 3.0

init_script_1 = """
CREATE TABLE TEST_TABLE (F_TIMESTAMP TIMESTAMP);
commit;

create procedure test_1(i CHAR(25)) 
external name 'esp.TestProcedure.timeStampIn(java.sql.Timestamp)'
engine java;
commit;

create procedure test_2(i VARCHAR(25)) 
external name 'esp.TestProcedure.timeStampIn(java.sql.Timestamp)'
engine java;
commit;

create procedure test_3(i BLOB) 
external name 'esp.TestProcedure.timeStampIn(java.sql.Timestamp)'
engine java;
commit;

create procedure test_4(i TIME) 
external name 'esp.TestProcedure.timeStampIn(java.sql.Timestamp)'
engine java;
commit;

create procedure test_5(i DATE) 
external name 'esp.TestProcedure.timeStampIn(java.sql.Timestamp)'
engine java;
commit;

create procedure test_6(i TIMESTAMP) 
external name 'esp.TestProcedure.timeStampIn(java.sql.Timestamp)'
engine java;
commit;

"""

db_1 = db_factory(init=init_script_1)

test_script_1 = """
EXECUTE PROCEDURE TEST_1('14-JUL-2007 07:27:47');
EXECUTE PROCEDURE TEST_1('07-14-2007');
EXECUTE PROCEDURE TEST_1('07/14/2007 07:27:47');
EXECUTE PROCEDURE TEST_1('2007-07-14');
EXECUTE PROCEDURE TEST_1('2007/07/14 07:27:47');
EXECUTE PROCEDURE TEST_1('2007.07.14 07.27.47');
EXECUTE PROCEDURE TEST_1('14.07.2007');
commit;

EXECUTE PROCEDURE TEST_2('25-NOV-1920 07.27.47');
EXECUTE PROCEDURE TEST_2('11-25-1920 ');
EXECUTE PROCEDURE TEST_2('11/25/1920 07.27.47');
EXECUTE PROCEDURE TEST_2('1920-11-25');
EXECUTE PROCEDURE TEST_2('1920/11/25 07.27.47');
EXECUTE PROCEDURE TEST_2('1920.11.25 07:27:47');
EXECUTE PROCEDURE TEST_2('25.11.1920');
commit;

EXECUTE PROCEDURE TEST_3('1-FEB-2018');
EXECUTE PROCEDURE TEST_3('1.02.2018 07:27:47');
EXECUTE PROCEDURE TEST_3('02-01-2018');
EXECUTE PROCEDURE TEST_3('02/01/2018');
EXECUTE PROCEDURE TEST_3('2018/02-01 07.27.47');
EXECUTE PROCEDURE TEST_3('2018/02/01');
EXECUTE PROCEDURE TEST_3('2018.02.01 07.27.47');
commit;

EXECUTE PROCEDURE TEST_4('07:27:47');
EXECUTE PROCEDURE TEST_4('07.27.47');
commit;

EXECUTE PROCEDURE TEST_5('7-OCT-2100');
EXECUTE PROCEDURE TEST_5('7.10.2100');
EXECUTE PROCEDURE TEST_5('10-07-2100');
EXECUTE PROCEDURE TEST_5('10/07/2100');
EXECUTE PROCEDURE TEST_5('2100-10-07');
EXECUTE PROCEDURE TEST_5('2100/10/07');
EXECUTE PROCEDURE TEST_5('2100.10.07');
commit;

EXECUTE PROCEDURE TEST_6('19-May-1023 23:45');
EXECUTE PROCEDURE TEST_6('19.05.1023 4:35:56');
EXECUTE PROCEDURE TEST_6('05-19-1023');
EXECUTE PROCEDURE TEST_6('05/19/1023');
EXECUTE PROCEDURE TEST_6('1023-05-19');
EXECUTE PROCEDURE TEST_6('1023/05/19');
EXECUTE PROCEDURE TEST_6('1023.05.19');
commit;


SELECT F_TIMESTAMP FROM TEST_TABLE;
"""

act_1 = isql_act('db_1', test_script_1, substitutions=[('\\d{4}-\\d{2}-\\d{2}', '')])

expected_stdout_1 = """
F_TIMESTAMP
=========================
2007-07-14 07:27:47.0000
2007-07-14 00:00:00.0000
2007-07-14 07:27:47.0000
2007-07-14 00:00:00.0000
2007-07-14 07:27:47.0000
2007-07-14 07:27:47.0000
2007-07-14 00:00:00.0000
1920-11-25 07:27:47.0000
1920-11-25 00:00:00.0000
1920-11-25 07:27:47.0000
1920-11-25 00:00:00.0000
1920-11-25 07:27:47.0000
1920-11-25 07:27:47.0000
1920-11-25 00:00:00.0000
2018-02-01 00:00:00.0000
2018-02-01 07:27:47.0000
2018-02-01 00:00:00.0000
2018-02-01 00:00:00.0000
2018-02-01 07:27:47.0000
2018-02-01 00:00:00.0000
F_TIMESTAMP
=========================
2018-02-01 07:27:47.0000
 07:27:47.0000
 07:27:47.0000
2100-10-07 00:00:00.0000
2100-10-07 00:00:00.0000
2100-10-07 00:00:00.0000
2100-10-07 00:00:00.0000
2100-10-07 00:00:00.0000
2100-10-07 00:00:00.0000
2100-10-07 00:00:00.0000
1023-05-19 23:45:00.0000
1023-05-19 04:35:56.0000
1023-05-19 00:00:00.0000
1023-05-19 00:00:00.0000
1023-05-19 00:00:00.0000
1023-05-19 00:00:00.0000
1023-05-19 00:00:00.0000
"""

@pytest.mark.java
@pytest.mark.version('>=3.0,<4.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_stdout == act_1.clean_expected_stdout

# version: 4.0

init_script_2 = """
CREATE TABLE TEST_TABLE (F_TIMESTAMP TIMESTAMP);
commit;

create procedure test_1(i CHAR(25))
external name 'esp.TestProcedure.timeStampIn(java.sql.Timestamp)'
engine java;
commit;

create procedure test_2(i VARCHAR(25))
external name 'esp.TestProcedure.timeStampIn(java.sql.Timestamp)'
engine java;
commit;

create procedure test_3(i BLOB)
external name 'esp.TestProcedure.timeStampIn(java.sql.Timestamp)'
engine java;
commit;

create procedure test_4(i TIME)
external name 'esp.TestProcedure.timeStampIn(java.sql.Timestamp)'
engine java;
commit;

create procedure test_5(i DATE)
external name 'esp.TestProcedure.timeStampIn(java.sql.Timestamp)'
engine java;
commit;

create procedure test_6(i TIMESTAMP)
external name 'esp.TestProcedure.timeStampIn(java.sql.Timestamp)'
engine java;
commit;

"""

db_2 = db_factory(init=init_script_2)

test_script_2 = """
EXECUTE PROCEDURE TEST_1('14-JUL-2007 07:27:47');
EXECUTE PROCEDURE TEST_1('07-14-2007');
EXECUTE PROCEDURE TEST_1('07/14/2007 07:27:47');
EXECUTE PROCEDURE TEST_1('2007-07-14');
EXECUTE PROCEDURE TEST_1('2007/07/14 07:27:47');
EXECUTE PROCEDURE TEST_1('14.07.2007');
commit;

EXECUTE PROCEDURE TEST_2('11-25-1920 ');
EXECUTE PROCEDURE TEST_2('1920-11-25');
EXECUTE PROCEDURE TEST_2('1920.11.25 07:27:47');
EXECUTE PROCEDURE TEST_2('25.11.1920');
commit;

EXECUTE PROCEDURE TEST_3('1-FEB-2018');
EXECUTE PROCEDURE TEST_3('1.02.2018 07:27:47');
EXECUTE PROCEDURE TEST_3('02-01-2018');
EXECUTE PROCEDURE TEST_3('02/01/2018');
EXECUTE PROCEDURE TEST_3('2018/02/01');
commit;

EXECUTE PROCEDURE TEST_4('07:27:47');
commit;

EXECUTE PROCEDURE TEST_5('7-OCT-2100');
EXECUTE PROCEDURE TEST_5('7.10.2100');
EXECUTE PROCEDURE TEST_5('10-07-2100');
EXECUTE PROCEDURE TEST_5('10/07/2100');
EXECUTE PROCEDURE TEST_5('2100-10-07');
EXECUTE PROCEDURE TEST_5('2100/10/07');
EXECUTE PROCEDURE TEST_5('2100.10.07');
commit;

EXECUTE PROCEDURE TEST_6('19-May-1023 23:45');
EXECUTE PROCEDURE TEST_6('19.05.1023 4:35:56');
EXECUTE PROCEDURE TEST_6('05-19-1023');
EXECUTE PROCEDURE TEST_6('05/19/1023');
EXECUTE PROCEDURE TEST_6('1023-05-19');
EXECUTE PROCEDURE TEST_6('1023/05/19');
EXECUTE PROCEDURE TEST_6('1023.05.19');
commit;


SELECT F_TIMESTAMP FROM TEST_TABLE;
"""

act_2 = isql_act('db_2', test_script_2, substitutions=[('\\d{4}-\\d{2}-\\d{2}', '')])

expected_stdout_2 = """
F_TIMESTAMP
=========================
2007-07-14 07:27:47.0000
2007-07-14 00:00:00.0000
2007-07-14 07:27:47.0000
2007-07-14 00:00:00.0000
2007-07-14 07:27:47.0000
2007-07-14 00:00:00.0000
1920-11-25 00:00:00.0000
2018-02-01 00:00:00.0000
2018-02-01 07:27:47.0000
2018-02-01 00:00:00.0000
2018-02-01 00:00:00.0000
2018-02-01 07:27:47.0000
2018-02-01 00:00:00.0000
2018-02-01 00:00:00.0000
2018-02-01 00:00:00.0000
2018-02-01 07:27:47.0000
2100-10-07 00:00:00.0000
2100-10-07 00:00:00.0000
2100-10-07 00:00:00.0000
2100-10-07 00:00:00.0000
F_TIMESTAMP
=========================
2100-10-07 00:00:00.0000
2100-10-07 00:00:00.0000
2100-10-07 00:00:00.0000
1023-05-19 23:45:00.0000
1023-05-19 04:35:56.0000
1023-05-19 00:00:00.0000
1023-05-19 00:00:00.0000
1023-05-19 00:00:00.0000
1023-05-19 00:00:00.0000
1023-05-19 00:00:00.0000
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
