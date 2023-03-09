#coding:utf-8

"""
ID:          optimizer.multi-index-selection-06
TITLE:       Best match index selection (multi segment)
DESCRIPTION:
  Check if it will select the index with the best selectivity and with the biggest segment match. 
  Prefer "lower and upper bound" (but not the same value (BETWEEN)) above only upper or lower bound ( >=, >, <, <=).
FBTEST:      functional.arno.optimizer.opt_multi_index_selection_06
"""

import pytest
from firebird.qa import *

init_script = """CREATE TABLE SelectionTest (
  F1 INTEGER NOT NULL,
  F2 INTEGER,
  F3 INTEGER
);

SET TERM ^^ ;
CREATE PROCEDURE PR_SelectionTest
AS
DECLARE VARIABLE FillID INTEGER;
BEGIN
  FillID = 1;
  WHILE (FillID <= 1000) DO
  BEGIN
    INSERT INTO SelectionTest
      (F1, F2, F3)
    VALUES
      (:FillID, (:FILLID / 2) * 2, :FILLID);
    FillID = FillID + 1;
  END
END
^^
SET TERM ; ^^

COMMIT;

/* Fill table with data */
EXECUTE PROCEDURE PR_SelectionTest;

COMMIT;

/* Create indexes */
CREATE UNIQUE ASC INDEX I_F1_UNIQUE_ASC ON SelectionTest (F1);
CREATE ASC INDEX I_F1_ASC ON SelectionTest (F1);
CREATE ASC INDEX I_F2_ASC ON SelectionTest (F2);
CREATE ASC INDEX I_F3_ASC ON SelectionTest (F3);
CREATE ASC INDEX I_F1_F2_ASC ON SelectionTest (F1, F2);
CREATE ASC INDEX I_F1_F3_ASC ON SelectionTest (F1, F3);
CREATE ASC INDEX I_F1_F2_F3_ASC ON SelectionTest (F1, F2, F3);
CREATE ASC INDEX I_F1_F3_F2_ASC ON SelectionTest (F1, F3, F2);
CREATE ASC INDEX I_F2_F1_ASC ON SelectionTest (F2, F1);
CREATE ASC INDEX I_F2_F3_ASC ON SelectionTest (F2, F3);
CREATE ASC INDEX I_F2_F1_F3_ASC ON SelectionTest (F2, F1, F3);
CREATE ASC INDEX I_F2_F3_F1_ASC ON SelectionTest (F2, F3, F1);
CREATE ASC INDEX I_F3_F1_ASC ON SelectionTest (F3, F1);
CREATE ASC INDEX I_F3_F2_ASC ON SelectionTest (F3, F2);
CREATE ASC INDEX I_F3_F1_F2_ASC ON SelectionTest (F3, F1, F2);
CREATE ASC INDEX I_F3_F2_F1_ASC ON SelectionTest (F3, F2, F1);

COMMIT;
"""

db = db_factory(init=init_script)

test_script = """SET PLAN ON;
SELECT
  st.F1, st.F2, st.F3
FROM
  SelectionTest st
WHERE
  st.F1 >= 99 and st.F1 <= 101 and
  st.F2 >= 99 and
  st.F3 = 100;"""

act = isql_act('db', test_script)

expected_stdout = """PLAN (ST INDEX (I_F3_F2_ASC))

          F1           F2           F3
============ ============ ============

         100          100          100"""

@pytest.mark.version('>=3,<4')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
