#coding:utf-8

"""
ID:          optimizer.multi-index-selection-02
TITLE:       Best match index selection (multi segment)
DESCRIPTION:
  Check if it will select the indexes which can be used.
  (Indexes with selectivity more than 10x the best are ignored)
  See SELECTIVITY_THRESHOLD_FACTOR in opt.cpp
FBTEST:      functional.arno.optimizer.opt_multi_index_selection_02
"""

import pytest
from firebird.qa import *

init_script = """CREATE TABLE SelectionTest (
  F1 INTEGER NOT NULL,
  F2 INTEGER NOT NULL,
  F3 INTEGER NOT NULL
);

SET TERM ^^ ;
CREATE PROCEDURE PR_SelectionTest
AS
DECLARE VARIABLE FillID INTEGER;
DECLARE VARIABLE FillF1 INTEGER;
DECLARE VARIABLE FillF2 INTEGER;
DECLARE VARIABLE FillF3 INTEGER;
BEGIN
  FillID = 1;
  WHILE (FillID <= 999) DO
  BEGIN
    FILLF1 = (FILLID / 10) * 10;
    FILLF2 = FILLID - FILLF1;
    FILLF3 = (FILLID / 150) * 150;
    INSERT INTO SelectionTest
      (F1, F2, F3)
    VALUES
      (:FILLF1, :FILLF2, :FILLF3);
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
CREATE ASC INDEX I_F1_F2_ASC ON SelectionTest (F1, F2);
CREATE ASC INDEX I_F3_F2_ASC ON SelectionTest (F3, F2);
CREATE ASC INDEX I_F1_ASC ON SelectionTest (F1);
CREATE ASC INDEX I_F3_ASC ON SelectionTest (F3);

COMMIT;
"""

db = db_factory(init=init_script)

test_script = """SET PLAN ON;
SELECT
  st.F1, st.F2, st.F3
FROM
  SelectionTest st
WHERE
  st.F1 = 150 and
  st.F2 = 0 and
  st.F3 = 150;

/*
SELECT
  i.RDB$INDEX_NAME AS INDEX_NAME,
  CAST(i.RDB$STATISTICS AS NUMERIC(18,5)) AS SELECTIVITY
FROM
  RDB$INDICES i
WHERE
  i.RDB$RELATION_NAME = 'SELECTIONTEST';
*/"""

act = isql_act('db', test_script)

expected_stdout = """PLAN (ST INDEX (I_F1_F2_ASC))

          F1           F2           F3
============ ============ ============

150            0          150"""

@pytest.mark.version('>=3')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
