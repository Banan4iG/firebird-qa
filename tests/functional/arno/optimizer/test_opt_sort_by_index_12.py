#coding:utf-8

"""
ID:          optimizer.sort-by-index-12
TITLE:       ORDER BY ASC, DESC using index (multi)
DESCRIPTION:
  ORDER BY X ASC, Y DESC
  When more fields are given in ORDER BY clause try to use a compound index, but look out
  for mixed directions.
FBTEST:      functional.arno.optimizer.opt_sort_by_index_12
"""

import pytest
from firebird.qa import db_factory, isql_act, Action

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
CREATE ASC INDEX I_Table_53_ID1_ID2_ASC ON Table_53 (ID1, ID2);
CREATE DESC INDEX I_Table_53_ID1_ID2_DESC ON Table_53 (ID1, ID2);
CREATE ASC INDEX I_Table_53_ID2_ID1_ASC ON Table_53 (ID2, ID1);
CREATE DESC INDEX I_Table_53_ID2_ID1_DESC ON Table_53 (ID2, ID1);

COMMIT;
"""

db = db_factory(init=init_script)

test_script = """SET PLAN ON;
SELECT
  t53.ID1, t53.ID2
FROM
  Table_53 t53
WHERE
  t53.ID1 BETWEEN 10 and 20 and
  t53.ID2 <= 5
ORDER BY
t53.ID1 ASC, t53.ID2 DESC;"""

act = isql_act('db', test_script)

expected_stdout = """PLAN SORT (T53 INDEX (I_TABLE_53_ID2_ASC, I_TABLE_53_ID1_ASC))

         ID1          ID2
============ ============
          10            5
          10            4
          10            3
          10            2
          10            1
          10            0
          20            5
          20            4
          20            3
          20            2
          20            1
          20            0
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
