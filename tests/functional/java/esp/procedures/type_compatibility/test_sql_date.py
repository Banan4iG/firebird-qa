#coding:utf-8

"""
ID:          java.esp.procedures.type-compatibility.sql-date
TITLE:       External function call with java.sql.Date  type of input parameter
DESCRIPTION: 
  External function is declared with SQL types compatible with java.sql.Date Java type. Parameter as a constant.
FBTEST:      functional.java.esp.procedures.type_compatibility.sql_date
"""

import pytest
from firebird.qa import *

# version: 3.0

init_script_1 = """
CREATE TABLE TEST_TABLE (F_DATE DATE);
commit;


create procedure test_1(i CHAR(15)) 
external name 'esp.TestProcedure.dateIn(java.sql.Date)'
engine java;
commit;

create procedure test_2(i VARCHAR(15)) 
external name 'esp.TestProcedure.dateIn(java.sql.Date)'
engine java;
commit;

create procedure test_3(i BLOB) 
external name 'esp.TestProcedure.dateIn(java.sql.Date)'
engine java;
commit;

create procedure test_4(i DATE) 
external name 'esp.TestProcedure.dateIn(java.sql.Date)'
engine java;
commit;

create procedure test_5(i TIMESTAMP) 
external name 'esp.TestProcedure.dateIn(java.sql.Date)'
engine java;
commit;

"""

db_1 = db_factory(init=init_script_1)

test_script_1 = """


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

EXECUTE PROCEDURE TEST_3('1-FEB-2018');
EXECUTE PROCEDURE TEST_3('1.02.2018');
EXECUTE PROCEDURE TEST_3('02-01-2018');
EXECUTE PROCEDURE TEST_3('02/01/2018');
EXECUTE PROCEDURE TEST_3('2018/02-01');
EXECUTE PROCEDURE TEST_3('2018/02/01');
EXECUTE PROCEDURE TEST_3('2018.02.01');
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

SELECT F_DATE FROM TEST_TABLE;
"""

act_1 = isql_act('db_1', test_script_1)

expected_stdout_1 = """
F_DATE
===========
2007-07-14
2007-07-14
2007-07-14
2007-07-14
2007-07-14
2007-07-14
2007-07-14
1920-11-25
1920-11-25
1920-11-25
1920-11-25
1920-11-25
1920-11-25
1920-11-25
2018-02-01
2018-02-01
2018-02-01
2018-02-01
2018-02-01
2018-02-01
F_DATE
===========
2018-02-01
2100-10-07
2100-10-07
2100-10-07
2100-10-07
2100-10-07
2100-10-07
2100-10-07
1023-05-19
1023-05-19
1023-05-19
1023-05-19
1023-05-19
1023-05-19
1023-05-19
"""

@pytest.mark.java
@pytest.mark.version('>=3.0,<4.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_stdout == act_1.clean_expected_stdout

# version: 4.0

init_script_2 = """
CREATE TABLE TEST_TABLE (F_DATE DATE);
commit;


create procedure test_1(i CHAR(15))
external name 'esp.TestProcedure.dateIn(java.sql.Date)'
engine java;
commit;

create procedure test_2(i VARCHAR(15))
external name 'esp.TestProcedure.dateIn(java.sql.Date)'
engine java;
commit;

create procedure test_3(i BLOB)
external name 'esp.TestProcedure.dateIn(java.sql.Date)'
engine java;
commit;

create procedure test_4(i DATE)
external name 'esp.TestProcedure.dateIn(java.sql.Date)'
engine java;
commit;

create procedure test_5(i TIMESTAMP)
external name 'esp.TestProcedure.dateIn(java.sql.Date)'
engine java;
commit;

"""

db_2 = db_factory(init=init_script_2)

test_script_2 = """


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

EXECUTE PROCEDURE TEST_3('1-FEB-2018');
EXECUTE PROCEDURE TEST_3('1.02.2018');
EXECUTE PROCEDURE TEST_3('02-01-2018');
EXECUTE PROCEDURE TEST_3('02/01/2018');
EXECUTE PROCEDURE TEST_3('2018/02/01');
EXECUTE PROCEDURE TEST_3('2018.02.01');
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

SELECT F_DATE FROM TEST_TABLE;
"""

act_2 = isql_act('db_2', test_script_2)

expected_stdout_2 = """
F_DATE
===========
2007-07-14
2007-07-14
2007-07-14
2007-07-14
2007-07-14
2007-07-14
2007-07-14
1920-11-25
1920-11-25
1920-11-25
1920-11-25
1920-11-25
1920-11-25
1920-11-25
2018-02-01
2018-02-01
2018-02-01
2018-02-01
2018-02-01
2018-02-01
F_DATE
===========
2100-10-07
2100-10-07
2100-10-07
2100-10-07
2100-10-07
2100-10-07
2100-10-07
1023-05-19
1023-05-19
1023-05-19
1023-05-19
1023-05-19
1023-05-19
1023-05-19
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
