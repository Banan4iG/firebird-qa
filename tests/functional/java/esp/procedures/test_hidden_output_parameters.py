#coding:utf-8

"""
ID:          java.esp.procedures.hidden-output-parameters
TITLE:       Call of ESP which returns ResultSet with output parameters generated from procedure metadata
DESCRIPTION: 
FBTEST:      functional.java.esp.procedures.hidden_output_parameters
"""

import pytest
from firebird.qa import *

# version: 4.0

init_script_1 = """
CREATE OR ALTER PROCEDURE P2IN1OUT (
  IN1 INTEGER = 1,
  IN2 INTEGER = 2
) RETURNS (
  RESULT INTEGER
)
  EXTERNAL NAME 'example.Procedures.p2in1out(int, int)
    !jdbc:default:connection'
  ENGINE JAVA;
COMMIT;
"""

db_1 = db_factory(init=init_script_1)

test_script_1 = """
SELECT * FROM P2IN1OUT(1,10);
"""

act_1 = isql_act('db_1', test_script_1)

expected_stdout_1 = """         
      RESULT
============
           1
           2
           3
           4
           5
           6
           7
           8
           9
10
"""

@pytest.mark.java
@pytest.mark.version('>=4.0,<4.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_stdout == act_1.clean_expected_stdout

# version: 4.0

init_script_2 = """
 
CREATE OR ALTER PROCEDURE P2IN2OUT (
  IN1 INTEGER = 1,
  IN2 INTEGER = 2
) RETURNS (
  RES1 INTEGER,
  RES2 VARCHAR(20)
)
  EXTERNAL NAME 'example.Procedures.p2in2out(int, int)
    !jdbc:default:connection'
  ENGINE JAVA;
COMMIT;

"""

db_2 = db_factory(init=init_script_2)

test_script_2 = """
SELECT * FROM P2IN2OUT(1,10);
"""

act_2 = isql_act('db_2', test_script_2)

expected_stdout_2 = """         
        RES1 RES2
============ ====================
           1 String value: 1
           2 String value: 2
           3 String value: 3
           4 String value: 4
           5 String value: 5
           6 String value: 6
           7 String value: 7
           8 String value: 8
           9 String value: 9
10 String value: 10
"""

@pytest.mark.java
@pytest.mark.version('>=4.0,<4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout

# version: 4.0

init_script_3 = """

CREATE OR ALTER PROCEDURE P2IN3OUT (
  IN1 INTEGER = 1,
  IN2 INTEGER = 2
) RETURNS (
  RES1 INTEGER,
  RES2 VARCHAR(20),
  RES3 TIMESTAMP
)
  EXTERNAL NAME 'example.Procedures.p2in3out(int, int)
    !jdbc:default:connection'
  ENGINE JAVA;
COMMIT;

"""

db_3 = db_factory(init=init_script_3)

test_script_3 = """
SELECT * FROM P2IN3OUT(1,10);
"""

act_3 = isql_act('db_3', test_script_3)

expected_stdout_3 = """
        RES1 RES2                                      RES3
============ ==================== =========================
           1 String value: 1      2020-10-13 15:49:00.0000
           2 String value: 2      2020-10-13 15:49:00.0000
           3 String value: 3      2020-10-13 15:49:00.0000
           4 String value: 4      2020-10-13 15:49:00.0000
           5 String value: 5      2020-10-13 15:49:00.0000
           6 String value: 6      2020-10-13 15:49:00.0000
           7 String value: 7      2020-10-13 15:49:00.0000
           8 String value: 8      2020-10-13 15:49:00.0000
           9 String value: 9      2020-10-13 15:49:00.0000
10 String value: 10     2020-10-13 15:49:00.0000
"""

@pytest.mark.java
@pytest.mark.version('>=4.0,<4.0')
def test_3(act_3: Action):
    act_3.expected_stdout = expected_stdout_3
    act_3.execute()
    assert act_3.clean_stdout == act_3.clean_expected_stdout

# version: 4.0

init_script_4 = """

CREATE OR ALTER PROCEDURE P2IN3OUT_CUSTOM (
  IN1 INTEGER = 1,
  IN2 INTEGER = 2
) RETURNS (
  RES1 INTEGER,
  RES2 VARCHAR(20),
  RES3 TIMESTAMP
)
  EXTERNAL NAME 'example.Procedures.p2in3out(int, int) -> ( Integer, String, java.sql.Timestamp )
    !jdbc:default:connection'
  ENGINE JAVA;
COMMIT;

"""

db_4 = db_factory(init=init_script_4)

test_script_4 = """
SELECT * FROM P2IN3OUT_CUSTOM(1,10);
"""

act_4 = isql_act('db_4', test_script_4)

expected_stdout_4 = """
        RES1 RES2                                      RES3
============ ==================== =========================
           1 String value: 1      2020-10-13 15:49:00.0000
           2 String value: 2      2020-10-13 15:49:00.0000
           3 String value: 3      2020-10-13 15:49:00.0000
           4 String value: 4      2020-10-13 15:49:00.0000
           5 String value: 5      2020-10-13 15:49:00.0000
           6 String value: 6      2020-10-13 15:49:00.0000
           7 String value: 7      2020-10-13 15:49:00.0000
           8 String value: 8      2020-10-13 15:49:00.0000
           9 String value: 9      2020-10-13 15:49:00.0000
10 String value: 10     2020-10-13 15:49:00.0000
"""

@pytest.mark.java
@pytest.mark.version('>=4.0,<4.0')
def test_4(act_4: Action):
    act_4.expected_stdout = expected_stdout_4
    act_4.execute()
    assert act_4.clean_stdout == act_4.clean_expected_stdout

# version: 4.0

init_script_5 = """

CREATE OR ALTER PROCEDURE TEST_PRIMITIVES (
  IN1 INTEGER = 1,
  IN2 INTEGER = 2,
  IN3 TIMESTAMP = '2020-10-13 15:49:00.0000'
) RETURNS (
  RES1 INTEGER,
  RES2 VARCHAR(20),
  RES3 TIMESTAMP,
  RES4 VARBINARY(20),
  RES5 SMALLINT,
  RES6 BIGINT,
  RES7 FLOAT,
  RES8 DECIMAL(3,2),
  RES9 BOOLEAN
)
  EXTERNAL NAME 'example.Procedures.testPrimitives(int, int, Timestamp) -> ( Integer, String, Timestamp, byte[], short, long, float, double, boolean )
    !jdbc:default:connection'
  ENGINE JAVA;
COMMIT;

"""

db_5 = db_factory(init=init_script_5)

test_script_5 = """
SET LIST ON;
SELECT * FROM TEST_PRIMITIVES;
"""

act_5 = isql_act('db_5', test_script_5)

expected_stdout_5 = """

RES1                            1
RES2                            String value: 1
RES3                            2020-10-15 17:51:00.0000
RES4                            537472696E672076616C75653A2031
RES5                            42
RES6                            4242
RES7                            424.42401
RES8                            424.42
RES9                            <false>

RES1                            2
RES2                            String value: 2
RES3                            2020-10-16 18:52:00.0000
RES4                            537472696E672076616C75653A2032
RES5                            84
RES6                            8484
RES7                            848.84802
RES8                            848.84
RES9                            <true>
"""

@pytest.mark.java
@pytest.mark.version('>=4.0,<4.0')
def test_5(act_5: Action):
    act_5.expected_stdout = expected_stdout_5
    act_5.execute()
    assert act_5.clean_stdout == act_5.clean_expected_stdout

# version: 4.0

init_script_6 = """

CREATE OR ALTER PROCEDURE TEST_PRIMITIVES_AUTO (
  IN1 INTEGER = 1,
  IN2 INTEGER = 2,
  IN3 TIMESTAMP = '2020-10-13 15:49:00.0000'
) RETURNS (
  RES1 INTEGER,
  RES2 VARCHAR(20),
  RES3 TIMESTAMP,
  RES4 VARBINARY(20),
  RES5 SMALLINT,
  RES6 BIGINT,
  RES7 FLOAT,
  RES8 DECIMAL(3,2),
  RES9 BOOLEAN
)
  EXTERNAL NAME 'example.Procedures.testPrimitivesAuto(int, int, Timestamp)
    !jdbc:default:connection'
  ENGINE JAVA;
COMMIT;

"""

db_6 = db_factory(init=init_script_6)

test_script_6 = """
SELECT * FROM TEST_PRIMITIVES_AUTO;
"""

act_6 = isql_act('db_6', test_script_6)

expected_stdout_6 = """

RES1                            1
RES2                            String value: 1
RES3                            2020-10-15 17:51:00.0000
RES4                            537472696E672076616C75653A2031
RES5                            42
RES6                            4242
RES7                            424.42401
RES8                            424.42
RES9                            <false>

RES1                            2
RES2                            String value: 2
RES3                            2020-10-16 18:52:00.0000
RES4                            537472696E672076616C75653A2032
RES5                            84
RES6                            8484
RES7                            848.84802
RES8                            848.84
RES9                            <true>
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_6(act_6: Action):
    act_6.expected_stdout = expected_stdout_6
    act_6.execute()
    assert act_6.clean_stdout == act_6.clean_expected_stdout
