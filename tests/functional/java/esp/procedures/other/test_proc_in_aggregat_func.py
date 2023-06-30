#coding:utf-8

"""
ID:          java.esp.procedures.other.proc-in-aggregat-func
TITLE:       Using external procedure in aggregate function
DESCRIPTION: 
FBTEST:      functional.java.esp.procedures.other.proc_in_aggregat_func
"""

import pytest
from firebird.qa import *

# version: 3.0

init_script_1 = """
CREATE TABLE TEST_TABLE(F bigint);
commit;

CREATE PROCEDURE TEST_1(i bigint)
returns(o bigint)
EXTERNAL NAME 'esp.TestProcedure.insertValue(Long, Long[])' 
ENGINE JAVA;
commit;

CREATE PROCEDURE TEST_2
returns(o smallint)
EXTERNAL NAME 'esp.TestProcedure.testERS(Short[])' 
ENGINE JAVA;
commit;

CREATE PROCEDURE TEST_3(i float)
returns(o float)
EXTERNAL NAME 'esp.TestProcedure.doubleInOut(double,double[])' 
ENGINE JAVA;
commit;


"""

db_1 = db_factory(init=init_script_1)

test_script_1 = """

select MAX(o) from TEST_1(100);

select MAX(o) from TEST_2;

select max(o) from TEST_3(123.34);

"""

act_1 = isql_act('db_1', test_script_1)

expected_stdout_1 = """
MAX
=====================
110
MAX
=======
5
MAX
==============
123.34000

"""

@pytest.mark.java
@pytest.mark.version('>=3.0,<4.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_stdout == act_1.clean_expected_stdout

# version: 4.0

init_script_2 = """
CREATE TABLE TEST_TABLE(F bigint);
commit;

CREATE PROCEDURE TEST_1(i bigint)
returns(o bigint)
EXTERNAL NAME 'esp.TestProcedure.insertValueReturnERS(Long, Long[])'
ENGINE JAVA;
commit;

CREATE PROCEDURE TEST_2
returns(o smallint)
EXTERNAL NAME 'esp.TestProcedure.testERS(Short[])'
ENGINE JAVA;
commit;

CREATE PROCEDURE TEST_3(i float)
returns(o float)
EXTERNAL NAME 'esp.TestProcedure.doubleInOut(double,double[])'
ENGINE JAVA;
commit;


"""

db_2 = db_factory(init=init_script_2)

test_script_2 = """

select MAX(o) from TEST_1(100);

select MAX(o) from TEST_2;

select max(o) from TEST_3(123.34);

"""

act_2 = isql_act('db_2', test_script_2)

expected_stdout_2 = """
MAX
=====================
110
MAX
=======
5
MAX
==============
123.34000

"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
