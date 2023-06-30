#coding:utf-8

"""
ID:          java.esp.procedures.type-compatibility.resultset
TITLE:       Call of external procedure which returns ResultSet
DESCRIPTION: 
FBTEST:      functional.java.esp.procedures.type_compatibility.resultset
"""

import pytest
from firebird.qa import *

# version: 3.0

init_script_1 = """
 
CREATE TABLE TEST_TABLE(F_smallint smallint,F_INTEGER integer, F_BIGINT bigint, F_FLOAT float, F_DOUBLE double precision, F_NUMERIC numeric(10,2), F_DECIMAL decimal(10,2), F_CHAR char(10), F_VARCHAR varchar(10), F_BLOB blob, F_DATE date, F_TIME time, F_TIMESTAMP timestamp, F_BOOLEAN boolean);
commit;

CREATE PROCEDURE TEST
RETURNS(F_smallint smallint,F_INTEGER integer, F_BIGINT bigint,  F_FLOAT double precision, F_DOUBLE double precision,  F_NUMERIC numeric(10,2), F_DECIMAL decimal(10,2), F_CHAR char(10), F_VARCHAR varchar(10), F_BLOB blob,  F_DATE date, F_TIME time, F_TIMESTAMP timestamp, F_BOOLEAN boolean)
EXTERNAL NAME 'esp.TestProcedure.resultsetOut()' 
ENGINE JAVA;
commit;
 
"""

db_1 = db_factory(init=init_script_1)

test_script_1 = """

set list on;
select F_smallint, F_INTEGER, F_BIGINT, cast(F_FLOAT as float) as "F_FLOAT", F_DOUBLE, F_NUMERIC, F_DECIMAL, F_CHAR, F_VARCHAR, cast(F_BLOB as varchar(100)) as "F_BLOB", F_DATE, F_TIME, F_TIMESTAMP, F_BOOLEAN from TEST;
commit;

"""

act_1 = isql_act('db_1', test_script_1)

expected_stdout_1 = """         
F_SMALLINT                      23
F_INTEGER                       34
F_BIGINT                        45
F_FLOAT                         56.400002
F_DOUBLE                        67.50000000000000
F_NUMERIC                       78.60
F_DECIMAL                       89.70
F_CHAR                          char
F_VARCHAR                       varchar
F_BLOB                          It is new value from Java
F_DATE                          2008-04-09
F_TIME                          11:34:45.0000
F_TIMESTAMP                     2008-04-09 11:34:45.0000
F_BOOLEAN                       <true>
"""

@pytest.mark.java
@pytest.mark.version('>=3.0,<4.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_stdout == act_1.clean_expected_stdout

# version: 4.0

init_script_2 = """

CREATE TABLE TEST_TABLE(F_smallint smallint,F_INTEGER integer, F_BIGINT bigint, F_FLOAT float, F_DOUBLE double precision, F_NUMERIC numeric(10,2), F_DECIMAL decimal(10,2), F_CHAR char(10), F_VARCHAR varchar(10), F_BLOB blob, F_DATE date, F_TIME time, F_TIMESTAMP timestamp, F_BOOLEAN boolean);
commit;

CREATE PROCEDURE TEST
RETURNS(F_smallint smallint,F_INTEGER integer, F_BIGINT bigint,  F_FLOAT double precision, F_DOUBLE double precision,  F_NUMERIC numeric(10,2), F_DECIMAL decimal(10,2), F_CHAR char(10), F_VARCHAR varchar(10), F_BLOB blob,  F_DATE date, F_TIME time, F_TIMESTAMP timestamp, F_BOOLEAN boolean)
EXTERNAL NAME 'esp.TestProcedure.externalResultSetOut()'
ENGINE JAVA;
commit;

"""

db_2 = db_factory(init=init_script_2)

test_script_2 = """

set list on;
select F_smallint, F_INTEGER, F_BIGINT, cast(F_FLOAT as float) as "F_FLOAT", F_DOUBLE, F_NUMERIC, F_DECIMAL, F_CHAR, F_VARCHAR, cast(F_BLOB as varchar(100)) as "F_BLOB", F_DATE, F_TIME, F_TIMESTAMP, F_BOOLEAN from TEST;
commit;

"""

act_2 = isql_act('db_2', test_script_2)

expected_stdout_2 = """
F_SMALLINT                      23
F_INTEGER                       34
F_BIGINT                        45
F_FLOAT                         56.400002
F_DOUBLE                        67.50000000000000
F_NUMERIC                       78.60
F_DECIMAL                       89.70
F_CHAR                          char
F_VARCHAR                       varchar
F_BLOB                          It is new value from Java
F_DATE                          2008-04-09
F_TIME                          11:34:45.0000
F_TIMESTAMP                     2008-04-09 11:34:45.0000
F_BOOLEAN                       <true>
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
