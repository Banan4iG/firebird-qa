#coding:utf-8

"""
ID:          optimizer.mixed-joins-04
TITLE:       Mixed JOINS
DESCRIPTION:
  Tables without indexes should be merged (when inner join) and those who can use a index, should use it.
FBTEST:      functional.arno.optimizer.opt_mixed_joins_04
"""

import pytest
from firebird.qa import *

init_script = """CREATE TABLE Table_1 (
  ID INTEGER NOT NULL
);

CREATE TABLE Table_10 (
  ID INTEGER NOT NULL
);

CREATE TABLE Table_50 (
  ID INTEGER NOT NULL
);

CREATE TABLE Table_100 (
  ID INTEGER NOT NULL
);

CREATE TABLE Table_1000 (
  ID INTEGER NOT NULL
);

SET TERM ^^ ;
CREATE PROCEDURE PR_FillTable_10
AS
DECLARE VARIABLE FillID INTEGER;
BEGIN
  FillID = 1;
  WHILE (FillID <= 10) DO
  BEGIN
    INSERT INTO Table_10 (ID) VALUES (:FillID);
    FillID = FillID + 1;
  END
END
^^

CREATE PROCEDURE PR_FillTable_100
AS
DECLARE VARIABLE FillID INTEGER;
BEGIN
  FillID = 1;
  WHILE (FillID <= 100) DO
  BEGIN
    INSERT INTO Table_100 (ID) VALUES (:FillID);
    FillID = FillID + 1;
  END
END
^^

CREATE PROCEDURE PR_FillTable_1000
AS
DECLARE VARIABLE FillID INTEGER;
BEGIN
  FillID = 1;
  WHILE (FillID <= 1000) DO
  BEGIN
    INSERT INTO Table_1000 (ID) VALUES (:FillID);
    FillID = FillID + 1;
  END
END
^^
SET TERM ; ^^

COMMIT;

INSERT INTO Table_1 (ID) VALUES (1);
EXECUTE PROCEDURE PR_FillTable_10;
EXECUTE PROCEDURE PR_FillTable_100;
EXECUTE PROCEDURE PR_FillTable_1000;
INSERT INTO Table_50 SELECT ID FROM Table_100 t WHERE t.ID <= 50;

COMMIT;

CREATE UNIQUE ASC INDEX PK_Table_1 ON Table_1 (ID);
CREATE UNIQUE ASC INDEX PK_Table_50 ON Table_50 (ID);

COMMIT;
"""

db = db_factory(sql_dialect=3, init=init_script)

test_script = """SET PLAN ON;
SELECT
  Count(*)
FROM
  Table_10 t10
  LEFT JOIN Table_1 t1 ON (t1.ID = t10.ID)
  JOIN Table_100 t100 ON (t100.ID = t10.ID)
  LEFT JOIN Table_50 t50 ON (t50.ID = t100.ID)
JOIN Table_1000 t1000 ON (t1000.ID = t100.ID);"""

act = isql_act('db', test_script)

expected_stdout = """PLAN HASH (T1000 NATURAL, JOIN (HASH (T100 NATURAL, JOIN (T10 NATURAL, T1 INDEX (PK_TABLE_1))), T50 INDEX (PK_TABLE_50)))

                COUNT
=====================
                   10
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
