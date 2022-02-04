#coding:utf-8

"""
ID:          procedure.create-03
TITLE:       CREATE PROCEDURE - Output paramaters
DESCRIPTION:
FBTEST:      functional.procedure.create.03
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """SET TERM ^;
CREATE PROCEDURE test RETURNS(
  p1 SMALLINT, p2 INTEGER, p3 FLOAT, p4 DOUBLE PRECISION, p5 DECIMAL(9,3), p6 NUMERIC(10,4),
  p7 DATE, p8 TIME, p9 TIMESTAMP, p10 CHAR(40), p11 VARCHAR(60), p12 NCHAR(70))
AS
BEGIN
  p1=1;
  p2=2;
  p3=3.4;
  p4=4.5;
  p5=5.6;
  p6=6.7;
  p7='31.8.1995';
  p8='13:45:57.1';
  p9='29.2.200 14:46:59.9';
  p10='Text p10';
  p11='Text p11';
  p12='Text p13';
END ^
SET TERM ;^
commit;
SHOW PROCEDURE test;"""

act = isql_act('db', test_script)

expected_stdout = """Procedure text:
=============================================================================
BEGIN
  p1=1;
  p2=2;
  p3=3.4;
  p4=4.5;
  p5=5.6;
  p6=6.7;
  p7='31.8.1995';
  p8='13:45:57.1';
  p9='29.2.200 14:46:59.9';
  p10='Text p10';
  p11='Text p11';
  p12='Text p13';
END
=============================================================================
Parameters:
P1                                OUTPUT SMALLINT
P2                                OUTPUT INTEGER
P3                                OUTPUT FLOAT
P4                                OUTPUT DOUBLE PRECISION
P5                                OUTPUT DECIMAL(9, 3)
P6                                OUTPUT NUMERIC(10, 4)
P7                                OUTPUT DATE
P8                                OUTPUT TIME
P9                                OUTPUT TIMESTAMP
P10                               OUTPUT CHAR(40)
P11                               OUTPUT VARCHAR(60)
P12                               OUTPUT CHAR(70) CHARACTER SET ISO8859_1"""

@pytest.mark.version('>=3')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
