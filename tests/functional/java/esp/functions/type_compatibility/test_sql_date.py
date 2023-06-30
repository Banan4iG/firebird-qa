#coding:utf-8

"""
ID:          java.esp.functions.type-compatibility.sql-date
TITLE:       External function call with java.sql.Date type of result and input parameter
DESCRIPTION: 
  External function is declared with SQL types compatible with java.sql.Date Java type. Parameter as a constant.
FBTEST:      functional.java.esp.functions.type_compatibility.sql_date
"""

import pytest
from firebird.qa import *

init_script = """

create function test_1(i CHAR(15)) 
returns CHAR(15)
external name 'esp.TestFunction.dateInOut(java.sql.Date)'
engine java;
commit;

create function test_2(i VARCHAR(15)) 
returns VARCHAR(15)
external name 'esp.TestFunction.dateInOut(java.sql.Date)'
engine java;
commit;

create function test_3(i BLOB) 
returns BLOB
external name 'esp.TestFunction.dateInOut(java.sql.Date)'
engine java;
commit;

create function test_4(i DATE) 
returns DATE
external name 'esp.TestFunction.dateInOut(java.sql.Date)'
engine java;
commit;

create function test_5(i TIMESTAMP) 
returns TIMESTAMP
external name 'esp.TestFunction.dateInOut(java.sql.Date)'
engine java;
commit;

"""

db = db_factory(init=init_script)

test_script = """
SELECT TEST_1('14-JUL-2007') FROM RDB$DATABASE;
SELECT TEST_1('07-14-2007') FROM RDB$DATABASE;
SELECT TEST_1('07/14/2007') FROM RDB$DATABASE;
SELECT TEST_1('2007-07-14') FROM RDB$DATABASE;
SELECT TEST_1('2007/07/14') FROM RDB$DATABASE;
SELECT TEST_1('2007.07.14') FROM RDB$DATABASE;
SELECT TEST_1('14.07.2007') FROM RDB$DATABASE;


SELECT TEST_2('25-NOV-1920') FROM RDB$DATABASE;
SELECT TEST_2('11-25-1920') FROM RDB$DATABASE;
SELECT TEST_2('11/25/1920') FROM RDB$DATABASE;
SELECT TEST_2('1920-11-25') FROM RDB$DATABASE;
SELECT TEST_2('1920/11/25') FROM RDB$DATABASE;
SELECT TEST_2('1920.11.25') FROM RDB$DATABASE;
SELECT TEST_2('25.11.1920') FROM RDB$DATABASE;

SELECT cast(TEST_3('1-FEB-2018') as varchar(20)) as "TEST_3" FROM RDB$DATABASE;
SELECT cast(TEST_3('1.02.2018') as varchar(20)) as "TEST_3" FROM RDB$DATABASE;
SELECT cast(TEST_3('02-01-2018') as varchar(20)) as "TEST_3" FROM RDB$DATABASE;
SELECT cast(TEST_3('02/01/2018') as varchar(20)) as "TEST_3" FROM RDB$DATABASE;

SELECT cast(TEST_3('2018/02/01') as varchar(20)) as "TEST_3" FROM RDB$DATABASE;
SELECT cast(TEST_3('2018.02.01') as varchar(20)) as "TEST_3" FROM RDB$DATABASE;

SELECT TEST_4('7-OCT-2100') FROM RDB$DATABASE;
SELECT TEST_4('7.10.2100') FROM RDB$DATABASE;
SELECT TEST_4('10-07-2100') FROM RDB$DATABASE;
SELECT TEST_4('10/07/2100') FROM RDB$DATABASE;
SELECT TEST_4('2100-10-07') FROM RDB$DATABASE;
SELECT TEST_4('2100/10/07') FROM RDB$DATABASE;
SELECT TEST_4('2100.10.07') FROM RDB$DATABASE;

SELECT TEST_5('19-May-1023 23:45') FROM RDB$DATABASE;
SELECT TEST_5('19.05.1023 4:35:56') FROM RDB$DATABASE;
SELECT TEST_5('05-19-1023') FROM RDB$DATABASE;
SELECT TEST_5('05/19/1023') FROM RDB$DATABASE;
SELECT TEST_5('1023-05-19') FROM RDB$DATABASE;
SELECT TEST_5('1023/05/19') FROM RDB$DATABASE;
SELECT TEST_5('1023.05.19') FROM RDB$DATABASE;

"""

act = isql_act('db', test_script)

expected_stdout = """       
TEST_1
===============
2007-07-14
TEST_1
===============
2007-07-14
TEST_1
===============
2007-07-14
TEST_1
===============
2007-07-14
TEST_1
===============
2007-07-14
TEST_1
===============
2007-07-14
TEST_1
===============
2007-07-14
TEST_2
===============
1920-11-25
TEST_2
===============
1920-11-25
TEST_2
===============
1920-11-25
TEST_2
===============
1920-11-25
TEST_2
===============
1920-11-25
TEST_2
===============
1920-11-25
TEST_2
===============
1920-11-25
TEST_3
====================
2018-02-01
TEST_3
====================
2018-02-01
TEST_3
====================
2018-02-01
TEST_3
====================
2018-02-01
TEST_3
====================
2018-02-01
TEST_3
====================
2018-02-01
TEST_4
===========
2100-10-07
TEST_4
===========
2100-10-07
TEST_4
===========
2100-10-07
TEST_4
===========
2100-10-07
TEST_4
===========
2100-10-07
TEST_4
===========
2100-10-07
TEST_4
===========
2100-10-07
TEST_5
=========================
1023-05-19 00:00:00.0000
TEST_5
=========================
1023-05-19 00:00:00.0000
TEST_5
=========================
1023-05-19 00:00:00.0000
TEST_5
=========================
1023-05-19 00:00:00.0000
TEST_5
=========================
1023-05-19 00:00:00.0000
TEST_5
=========================
1023-05-19 00:00:00.0000
TEST_5
=========================
1023-05-19 00:00:00.0000
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
