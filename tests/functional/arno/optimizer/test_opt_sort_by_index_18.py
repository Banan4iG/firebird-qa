#coding:utf-8

"""
ID:          optimizer.sort-by-index-18
TITLE:       ORDER BY ASC using index (single) and WHERE clause
DESCRIPTION:
  WHERE X = 1 ORDER BY Y
  Index for both X and Y should be used when available.
FBTEST:      functional.arno.optimizer.opt_sort_by_index_18
"""

import pytest
from firebird.qa import *

init_script = """CREATE TABLE Table_53 (
  ID1 INTEGER,
  ID2 INTEGER
);

SET TERM ^^ ;
CREATE PROCEDURE PR_FillTable_53
AS
DECLARE VARIABLE FillID INTEGER;
DECLARE VARIABLE FillID1 INTEGER;
BEGIN
  FillID = 1;
  WHILE (FillID <= 50) DO
  BEGIN
    FillID1 = (FillID / 10) * 10;
    INSERT INTO Table_53
      (ID1, ID2)
    VALUES
      (:FillID1, :FillID - :FillID1);
    FillID = FillID + 1;
  END
  INSERT INTO Table_53 (ID1, ID2) VALUES (0, NULL);
  INSERT INTO Table_53 (ID1, ID2) VALUES (NULL, 0);
  INSERT INTO Table_53 (ID1, ID2) VALUES (NULL, NULL);
END
^^
SET TERM ; ^^

COMMIT;

EXECUTE PROCEDURE PR_FillTable_53;

COMMIT;

CREATE ASC INDEX I_Table_53_ID1_ASC ON Table_53 (ID1);
CREATE DESC INDEX I_Table_53_ID1_DESC ON Table_53 (ID1);
CREATE ASC INDEX I_Table_53_ID2_ASC ON Table_53 (ID2);
CREATE DESC INDEX I_Table_53_ID2_DESC ON Table_53 (ID2);

COMMIT;
"""

db = db_factory(init=init_script)

test_script = """SET PLAN ON;
SELECT
  t53.ID2,
  t53.ID1
FROM
  Table_53 t53
WHERE
  t53.ID1 = 30
ORDER BY
t53.ID2 ASC;"""

act = isql_act('db', test_script)

expected_stdout = """PLAN (T53 ORDER I_TABLE_53_ID2_ASC INDEX (I_TABLE_53_ID1_ASC))

         ID2          ID1
============ ============

           0           30
           1           30
           2           30
           3           30
           4           30
           5           30
           6           30
           7           30
           8           30
9           30"""

@pytest.mark.version('>=3')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
