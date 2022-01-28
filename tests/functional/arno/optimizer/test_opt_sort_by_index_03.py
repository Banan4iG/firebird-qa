#coding:utf-8

"""
ID:          optimizer.sort-by-index-03
TITLE:       ORDER BY ASC using index (non-unique)
DESCRIPTION:
  ORDER BY X
  When a index can be used for sorting, use it.
"""

import pytest
from firebird.qa import *

init_script = """CREATE TABLE Table_66 (
  ID INTEGER
);

SET TERM ^^ ;
CREATE PROCEDURE PR_FillTable_66
AS
DECLARE VARIABLE FillID INTEGER;
BEGIN
  FillID = 2147483647;
  WHILE (FillID > 0) DO
  BEGIN
    INSERT INTO Table_66 (ID) VALUES (:FillID);
    FillID = FillID / 2;
  END
  INSERT INTO Table_66 (ID) VALUES (NULL);
  INSERT INTO Table_66 (ID) VALUES (0);
  INSERT INTO Table_66 (ID) VALUES (NULL);
  FillID = -2147483648;
  WHILE (FillID < 0) DO
  BEGIN
    INSERT INTO Table_66 (ID) VALUES (:FillID);
    FillID = FillID / 2;
  END
END
^^
SET TERM ; ^^

COMMIT;

EXECUTE PROCEDURE PR_FillTable_66;

COMMIT;

CREATE ASC INDEX I_Table_66_ASC ON Table_66 (ID);
CREATE DESC INDEX I_Table_66_DESC ON Table_66 (ID);

COMMIT;
"""

db = db_factory(init=init_script)

test_script = """SET PLAN ON;
SELECT
  ID
FROM
  Table_66 t66
ORDER BY
t66.ID ASC;"""

act = isql_act('db', test_script)

expected_stdout = """PLAN (T66 ORDER I_TABLE_66_ASC)

          ID
============
      <null>
      <null>
 -2147483648
 -1073741824
  -536870912
  -268435456
  -134217728
   -67108864
   -33554432
   -16777216
    -8388608
    -4194304
    -2097152
    -1048576
     -524288
     -262144
     -131072
      -65536
      -32768
      -16384

          ID
============
       -8192
       -4096
       -2048
       -1024
        -512
        -256
        -128
         -64
         -32
         -16
          -8
          -4
          -2
          -1
           0
           1
           3
           7
          15
          31

          ID
============
          63
         127
         255
         511
        1023
        2047
        4095
        8191
       16383
       32767
       65535
      131071
      262143
      524287
     1048575
     2097151
     4194303
     8388607
    16777215
    33554431

          ID
============
    67108863
   134217727
   268435455
   536870911
  1073741823
2147483647"""

@pytest.mark.version('>=3')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
