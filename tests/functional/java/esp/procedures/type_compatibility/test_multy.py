#coding:utf-8

"""
ID:          java.esp.procedures.type-compatibility.multy
TITLE:       Call external procedure with different input param
DESCRIPTION: 
FBTEST:      functional.java.esp.procedures.type_compatibility.multy
"""

import pytest
from firebird.qa import *

init_script = """
CREATE TABLE TEST_TABLE (
	F_INTEGER INTEGER,
	F_INTEGER1 INTEGER,
	F_BIGINT BIGINT,
	F_BIGINT1 BIGINT,
	F_DOUBLE DOUBLE PRECISION,
	F_DOUBLE1 DOUBLE PRECISION,
	F_FLOAT FLOAT,
	F_FLOAT1 FLOAT,
	F_NUMERIC NUMERIC(15,2),
	F_SMALLINT SMALLINT,
	F_SMALLINT1 SMALLINT,
	F_VARCHAR VARCHAR(100),
	F_DATE DATE,
	F_TIMESTAMP TIMESTAMP,
	F_TIME TIME
);
commit;

CREATE OR ALTER PROCEDURE TEST(
	F_INTEGER INTEGER,
	F_INTEGER1 INTEGER,
	F_BIGINT BIGINT,
	F_BIGINT1 BIGINT,
	F_DOUBLE DOUBLE PRECISION,
	F_DOUBLE1 DOUBLE PRECISION,
	F_FLOAT FLOAT,
	F_FLOAT1 FLOAT,
	F_NUMERIC NUMERIC(15,2),
	F_SMALLINT SMALLINT,
	F_SMALLINT1 SMALLINT,
	F_VARCHAR VARCHAR(100),
	F_DATE DATE,
	F_TIMESTAMP TIMESTAMP,
	F_TIME TIME
)
EXTERNAL NAME 'esp.TestProcedure.multyIn(Integer, int, Long, long, Double, double, Float, float, java.math.BigDecimal, Short, short, String, java.sql.Date, java.sql.Timestamp, java.sql.Time)'
ENGINE JAVA;
commit;
"""

db = db_factory(init=init_script)

test_script = """
EXECUTE PROCEDURE TEST(1,1,1,1,1,1,1,1,1,1,1,'test','2005-01-02','2005-01-02 12:22:44','15:22:11');
commit;

set list on;

SELECT * FROM TEST_TABLE;
"""

act = isql_act('db', test_script)

expected_stdout = """   
 F_INTEGER                       1
F_INTEGER1                      1
F_BIGINT                        1
F_BIGINT1                       1
F_DOUBLE                        1.000000000000000
F_DOUBLE1                       1.000000000000000
F_FLOAT                         1
F_FLOAT1                        1
F_NUMERIC                       1.00
F_SMALLINT                      1
F_SMALLINT1                     1
F_VARCHAR                       test
F_DATE                          2005-01-02
F_TIMESTAMP                     2005-01-02 12:22:44.0000
F_TIME                          15:22:11.0000
 
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
