#coding:utf-8

"""
ID:          java.esp.functions.type-compatibility.util-date
TITLE:       External function call with java.util.Date type of result and input parameter
DESCRIPTION: 
  External function is declared with SQL types compatible with java.util.Date Java type. Parameter as a constant.
FBTEST:      functional.java.esp.functions.type_compatibility.util_date
"""

import pytest
from firebird.qa import *

# version: 3.0

init_script_1 = """

create function test_1(i CHAR(15)) 
returns CHAR(15)
external name 'esp.TestFunction.utilDateInOut(java.util.Date)'
engine java;
commit;

create function test_2(i VARCHAR(15)) 
returns VARCHAR(15)
external name 'esp.TestFunction.utilDateInOut(java.util.Date)'
engine java;
commit;

create function test_3(i BLOB) 
returns BLOB
external name 'esp.TestFunction.utilDateInOut(java.util.Date)'
engine java;
commit;

create function test_4(i DATE) 
returns DATE
external name 'esp.TestFunction.utilDateInOut(java.util.Date)'
engine java;
commit;

create function test_5(i TIMESTAMP) 
returns TIMESTAMP
external name 'esp.TestFunction.utilDateInOut(java.util.Date)'
engine java;
commit;

"""

db_1 = db_factory(init=init_script_1)

test_script_1 = """
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
SELECT cast(TEST_3('2018/02-01') as varchar(20)) as "TEST_3" FROM RDB$DATABASE;
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

act_1 = isql_act('db_1', test_script_1)

expected_stdout_1 = """       
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
@pytest.mark.version('>=3.0,<4.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_stdout == act_1.clean_expected_stdout

# version: 4.0

init_script_2 = """

create function test_1(i CHAR(15))
returns CHAR(15)
external name 'esp.TestFunction.utilDateInOut(java.util.Date)'
engine java;
commit;

create function test_2(i VARCHAR(15))
returns VARCHAR(15)
external name 'esp.TestFunction.utilDateInOut(java.util.Date)'
engine java;
commit;

create function test_3(i BLOB)
returns BLOB
external name 'esp.TestFunction.utilDateInOut(java.util.Date)'
engine java;
commit;

create function test_4(i DATE)
returns DATE
external name 'esp.TestFunction.utilDateInOut(java.util.Date)'
engine java;
commit;

create function test_5(i TIMESTAMP)
returns TIMESTAMP
external name 'esp.TestFunction.utilDateInOut(java.util.Date)'
engine java;
commit;

"""

db_2 = db_factory(init=init_script_2)

test_script_2 = """
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

act_2 = isql_act('db_2', test_script_2)

expected_stdout_2 = """
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
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
