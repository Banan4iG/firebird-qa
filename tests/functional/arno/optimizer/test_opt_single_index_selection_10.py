#coding:utf-8

"""
ID:          optimizer.single-index-selection-09
TITLE:       Best match index selection (single segment) OR
DESCRIPTION:
  Check if it will select the index with the best selectivity.
  UNIQUE index is the best and prefer ASC index. 1 index per OR conjunction is enough and
  the equals conjunctions should be bound to the index, because it's the most selective.
FBTEST:      functional.arno.optimizer.opt_single_index_selection_10
"""

import pytest
from firebird.qa import *

init_script = """CREATE TABLE SelectionTest (
  F1 INTEGER NOT NULL
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
      (F1)
    VALUES
      (:FillID);
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
CREATE UNIQUE DESC INDEX I_F1_UNIQUE_DESC ON SelectionTest (F1);
CREATE ASC INDEX I_F1_ASC ON SelectionTest (F1);
CREATE DESC INDEX I_F1_DESC ON SelectionTest (F1);

COMMIT;
"""

db = db_factory(init=init_script)

test_script = """SET PLAN ON;
SELECT
  st.F1
FROM
  SelectionTest st
WHERE
  st.F1 = 5000 or
(st.F1 >= 1 and st.F1 <= 1000 and st.F1 = 500);"""

act = isql_act('db', test_script)

expected_stdout = """PLAN (ST INDEX (I_F1_UNIQUE_ASC, I_F1_UNIQUE_ASC))

          F1
============

500"""

@pytest.mark.version('>=3')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
