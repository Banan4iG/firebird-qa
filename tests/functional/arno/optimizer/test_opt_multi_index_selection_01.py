#coding:utf-8
#
# id:           functional.arno.optimizer.opt_multi_index_selection_01
# title:        Unique index selection (multi segment)
# decription:   Check if it will select only the index with the unique index when equal operator is performed on all segments in index. Also prefer ASC index above DESC unique index.
#               Unique index together with equals operator will always be the best index to choose.
# tracker_id:   
# min_versions: []
# versions:     2.0
# qmid:         functional.arno.optimizer.opt_multi_index_selection_01

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 2.0
# resources: None

substitutions_1 = []

init_script_1 = """CREATE TABLE SelectionTest (
  F1 INTEGER NOT NULL,
  F2 INTEGER NOT NULL,
  F3 INTEGER
);

SET TERM ^^ ;
CREATE PROCEDURE PR_SelectionTest
AS
DECLARE VARIABLE FillID INTEGER;
DECLARE VARIABLE FillF1 INTEGER;
BEGIN
  FillID = 1;
  WHILE (FillID <= 1000) DO
  BEGIN
    FillF1 = (:FillID / 100);
    INSERT INTO SelectionTest
      (F1, F2, F3)
    VALUES
      (:FillF1, :FILLID - (:FILLF1 * 100), :FILLID);
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
CREATE UNIQUE ASC INDEX I_F1_F2_UNIQUE_ASC ON SelectionTest (F1, F2);
CREATE UNIQUE DESC INDEX I_F1_F2_UNIQUE_DESC ON SelectionTest (F1, F2);
CREATE ASC INDEX I_F1_F2_ASC ON SelectionTest (F1, F2);
CREATE DESC INDEX I_F1_F2_DESC ON SelectionTest (F1, F2);
CREATE ASC INDEX I_F2_F1_ASC ON SelectionTest (F2, F1);
CREATE DESC INDEX I_F2_F1_DESC ON SelectionTest (F2, F1);
CREATE ASC INDEX I_F1_F2_F3_ASC ON SelectionTest (F1, F2, F3);
CREATE ASC INDEX I_F2_F1_F3_ASC ON SelectionTest (F2, F1, F3);
CREATE ASC INDEX I_F3_F2_F1_ASC ON SelectionTest (F3, F2, F1);

COMMIT;
"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """SET PLAN ON;
SELECT
  st.F1, st.F2, st.F3
FROM
  SelectionTest st
WHERE
  st.F1 = 5 and
  st.F2 = 50 and
  st.F3 = 550;
"""

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """PLAN (ST INDEX (I_F1_F2_UNIQUE_ASC))

          F1           F2           F3
============ ============ ============

           5           50          550
"""

@pytest.mark.version('>=2.0')
def test_opt_multi_index_selection_01_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout

