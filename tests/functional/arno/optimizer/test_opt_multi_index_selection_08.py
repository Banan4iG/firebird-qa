#coding:utf-8

"""
ID:          optimizer.multi-index-selection-07
TITLE:       Best match index selection (multi segment)
DESCRIPTION:
  STARTING WITH can also use a index and it should in fact be possible to use a compound
  index. Of course the STARTING WITH conjunction can only be bound the end (of all possible
  matches, same as >, >=, <, <=).
FBTEST:      functional.arno.optimizer.opt_multi_index_selection_08
"""

import pytest
from firebird.qa import *

init_script = """CREATE TABLE SelectionTest (
  F1 INTEGER NOT NULL,
  F2 VARCHAR(18)
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
      (F1, F2)
    VALUES
      ((:FillID / 100) * 100,
       :FILLID - ((:FillID / 100) * 100));
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
CREATE ASC INDEX I_F1_ASC ON SelectionTest (F1);
CREATE DESC INDEX I_F1_DESC ON SelectionTest (F1);
CREATE ASC INDEX I_F2_ASC ON SelectionTest (F2);
CREATE DESC INDEX I_F2_DESC ON SelectionTest (F2);
CREATE ASC INDEX I_F1_F2_ASC ON SelectionTest (F1, F2);
CREATE DESC INDEX I_F1_F2_DESC ON SelectionTest (F1, F2);
CREATE ASC INDEX I_F2_F1_ASC ON SelectionTest (F2, F1);
CREATE DESC INDEX I_F2_F1_DESC ON SelectionTest (F2, F1);

COMMIT;
"""

db = db_factory(init=init_script)

test_script = """SET PLAN ON;
SELECT
  st.F1, st.F2
FROM
  SelectionTest st
WHERE
  st.F1 = 100 and
st.F2 STARTING WITH '55';"""

act = isql_act('db', test_script)

expected_stdout = """PLAN (ST INDEX (I_F1_F2_ASC))

          F1 F2
============ ==================

100 55"""

@pytest.mark.version('>=3')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
