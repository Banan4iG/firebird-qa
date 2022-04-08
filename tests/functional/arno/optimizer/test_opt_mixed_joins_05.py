#coding:utf-8

"""
ID:          optimizer.mixed-joins-05
TITLE:       Mixed JOINS
DESCRIPTION:
  Tables without indexes should be merged (when inner join) and those who can use a index, should use it.
FBTEST:      functional.arno.optimizer.opt_mixed_joins_05

NOTES:
    [08.04.2022] pzotov
    FB 5.0.0.455 and later: data source with greatest cardinality will be specified at left-most position
    in the plan when HASH JOIN is choosen. Because of this, two cases of expected stdout must be taken
    in account, see variables 'fb3x_checked_stdout' and 'fb5x_checked_stdout'.
    See letter from dimitr, 05.04.2022 17:38.
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

CREATE TABLE Table_500 (
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
INSERT INTO Table_500 SELECT ID FROM Table_1000 t WHERE t.ID <= 500;

COMMIT;

CREATE UNIQUE ASC INDEX PK_Table_1 ON Table_1 (ID);
CREATE UNIQUE ASC INDEX PK_Table_50 ON Table_50 (ID);
CREATE UNIQUE ASC INDEX PK_Table_500 ON Table_500 (ID);

COMMIT;
"""

db = db_factory(init=init_script)

test_script = """
set planonly;
select count(*)
from table_500 t500
	left join table_1 t1 on (t1.id = t500.id)
	join table_1000 t1000 on (t1000.id = t500.id)
	left join table_10 t10 on (t10.id = t1000.id)
	join table_50 t50 on (t50.id = t10.id)
	join table_100 t100 on (t100.id = t500.id)
;
"""

act = isql_act('db', test_script)

fb3x_checked_stdout = """
    PLAN HASH (T100 NATURAL, JOIN (JOIN (HASH (T1000 NATURAL, JOIN (T500 NATURAL, T1 INDEX (PK_TABLE_1))), T10 NATURAL), T50 INDEX (PK_TABLE_50)))
"""

fb5x_checked_stdout = """
    PLAN HASH (JOIN (JOIN (HASH (T1000 NATURAL, JOIN (T500 NATURAL, T1 INDEX (PK_TABLE_1))), T10 NATURAL), T50 INDEX (PK_TABLE_50)), T100 NATURAL)
"""



@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = fb3x_checked_stdout if act.is_version('<5') else fb5x_checked_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
