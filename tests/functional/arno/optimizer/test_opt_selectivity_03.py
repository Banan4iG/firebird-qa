#coding:utf-8
#
# id:           functional.arno.optimizer.opt_selectivity_03
# title:        SELECTIVITY - INDEX INACTIVE / ACTIVE
# decription:   Check if selectivity is calculated correctly.
# tracker_id:   
# min_versions: []
# versions:     2.0
# qmid:         functional.arno.optimizer.opt_selectivity_03

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 2.0
# resources: None

substitutions_1 = []

init_script_1 = """CREATE TABLE SelectivityTest (
  F1 INTEGER NOT NULL,
  F2 INTEGER,
  F5 INTEGER,
  F50 INTEGER
);

SET TERM ^^ ;
CREATE PROCEDURE PR_SelectivityTest
AS
DECLARE VARIABLE FillID INTEGER;
BEGIN
  FillID = 1;
  WHILE (FillID <= 1000) DO
  BEGIN
    INSERT INTO SelectivityTest
      (F1, F2, F5, F50)
    VALUES
      (:FillID,
       (:FILLID / 2) * 2,
       (:FILLID / 5) * 5,
       (:FILLID / 50) * 50);
    FillID = FillID + 1;
  END
END
^^
SET TERM ; ^^

COMMIT;

/* Create indexes */
CREATE UNIQUE ASC INDEX I_F01_ASC ON SelectivityTest (F1);
CREATE UNIQUE DESC INDEX I_F01_DESC ON SelectivityTest (F1);
CREATE ASC INDEX I_F02_ASC ON SelectivityTest (F2);
CREATE DESC INDEX I_F02_DESC ON SelectivityTest (F2);
CREATE ASC INDEX I_F05_ASC ON SelectivityTest (F5);
CREATE DESC INDEX I_F05_DESC ON SelectivityTest (F5);
CREATE ASC INDEX I_F50_ASC ON SelectivityTest (F50);
CREATE DESC INDEX I_F50_DESC ON SelectivityTest (F50);

COMMIT;

/* Deactivate indexes */
ALTER INDEX I_F01_ASC INACTIVE;
ALTER INDEX I_F01_DESC INACTIVE;
ALTER INDEX I_F02_ASC INACTIVE;
ALTER INDEX I_F02_DESC INACTIVE;
ALTER INDEX I_F05_ASC INACTIVE;
ALTER INDEX I_F05_DESC INACTIVE;
ALTER INDEX I_F50_ASC INACTIVE;
ALTER INDEX I_F50_DESC INACTIVE;

COMMIT;

/* Fill table with data */
EXECUTE PROCEDURE PR_SelectivityTest;

COMMIT;

/* Activate indexes */
ALTER INDEX I_F01_ASC ACTIVE;
ALTER INDEX I_F01_DESC ACTIVE;
ALTER INDEX I_F02_ASC ACTIVE;
ALTER INDEX I_F02_DESC ACTIVE;
ALTER INDEX I_F05_ASC ACTIVE;
ALTER INDEX I_F05_DESC ACTIVE;
ALTER INDEX I_F50_ASC ACTIVE;
ALTER INDEX I_F50_DESC ACTIVE;

COMMIT;
"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """SET PLAN OFF;
SELECT
  CAST(RDB$INDEX_NAME AS CHAR(31)) AS INDEX_NAME,
  CAST(RDB$STATISTICS AS NUMERIC(18,5)) AS SELECTIVITY
FROM
  RDB$INDICES
WHERE
  RDB$RELATION_NAME = 'SELECTIVITYTEST'
ORDER BY
  RDB$INDEX_NAME;
"""

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """INDEX_NAME                                SELECTIVITY
=============================== =====================

I_F01_ASC                                     0.00100
I_F01_DESC                                    0.00100
I_F02_ASC                                     0.00200
I_F02_DESC                                    0.00200
I_F05_ASC                                     0.00498
I_F05_DESC                                    0.00498
I_F50_ASC                                     0.04762
I_F50_DESC                                    0.04762
"""

@pytest.mark.version('>=2.0')
def test_opt_selectivity_03_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout

