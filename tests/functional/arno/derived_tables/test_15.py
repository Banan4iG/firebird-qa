#coding:utf-8

"""
ID:          derived-table-15
TITLE:       UNION inside derived table
DESCRIPTION:
"""

import pytest
from firebird.qa import *

init_script = """CREATE TABLE Table_10 (
  ID INTEGER NOT NULL,
  DESCRIPTION VARCHAR(10)
);

COMMIT;

INSERT INTO Table_10 (ID, DESCRIPTION) VALUES (0, NULL);
INSERT INTO Table_10 (ID, DESCRIPTION) VALUES (1, 'one');
INSERT INTO Table_10 (ID, DESCRIPTION) VALUES (2, 'two');
INSERT INTO Table_10 (ID, DESCRIPTION) VALUES (3, 'three');
INSERT INTO Table_10 (ID, DESCRIPTION) VALUES (4, 'four');
INSERT INTO Table_10 (ID, DESCRIPTION) VALUES (5, 'five');
INSERT INTO Table_10 (ID, DESCRIPTION) VALUES (6, 'six');
INSERT INTO Table_10 (ID, DESCRIPTION) VALUES (7, 'seven');
INSERT INTO Table_10 (ID, DESCRIPTION) VALUES (8, 'eight');
INSERT INTO Table_10 (ID, DESCRIPTION) VALUES (9, 'nine');

COMMIT;
"""

db = db_factory(init=init_script)

test_script = """SELECT
  dt.ID,
  dt.DESCRIPTION
FROM
  (SELECT t1.ID, t1.DESCRIPTION FROM Table_10 t1 WHERE t1.ID <= 4
   UNION ALL
SELECT t1.ID, t1.DESCRIPTION FROM Table_10 t1 WHERE t1.ID >= 5) dt (ID, DESCRIPTION);"""

act = isql_act('db', test_script)

expected_stdout = """          ID DESCRIPTION
============ ===========
           0 <null>
           1 one
           2 two
           3 three
           4 four
           5 five
           6 six
           7 seven
           8 eight
9 nine"""

@pytest.mark.version('>=3')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
