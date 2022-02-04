#coding:utf-8

"""
ID:          optimizer.left-join-12
TITLE:       LEFT OUTER JOIN with distribution CASE
DESCRIPTION:
  TableX LEFT OUTER JOIN TableY with partial match. WHERE clause contains CASE expression
  based on TableY. The WHERE clause should not be distributed to the joined table.
FBTEST:      functional.arno.optimizer.opt_left_join_12
"""

import pytest
from firebird.qa import *

init_script = """CREATE TABLE Colors (
  ColorID INTEGER NOT NULL,
  ColorName VARCHAR(20)
);

CREATE TABLE Flowers (
  FlowerID INTEGER NOT NULL,
  FlowerName VARCHAR(30),
  ColorID INTEGER
);

COMMIT;

/* Value 0 represents -no value- */
INSERT INTO Colors (ColorID, ColorName) VALUES (0, 'Not defined');
INSERT INTO Colors (ColorID, ColorName) VALUES (1, 'Red');
INSERT INTO Colors (ColorID, ColorName) VALUES (2, 'Yellow');

/* insert some data with references */
INSERT INTO Flowers (FlowerID, FlowerName, ColorID) VALUES (1, 'Rose', 1);
INSERT INTO Flowers (FlowerID, FlowerName, ColorID) VALUES (2, 'Tulip', 2);
INSERT INTO Flowers (FlowerID, FlowerName, ColorID) VALUES (3, 'Gerbera', 0);
INSERT INTO Flowers (FlowerID, FlowerName, ColorID) VALUES (4, 'Blanc', NULL);

COMMIT;

/* Normally these indexes are created by the primary/foreign keys,
   but we don't want to rely on them for this test */
CREATE UNIQUE ASC INDEX PK_Colors ON Colors (ColorID);
CREATE UNIQUE ASC INDEX PK_Flowers ON Flowers (FlowerID);
CREATE ASC INDEX FK_Flowers_Colors ON Flowers (ColorID);
CREATE ASC INDEX I_Colors_Name ON Colors (ColorName);

COMMIT;
"""

db = db_factory(init=init_script)

test_script = """SET PLAN ON;
/* LEFT JOIN should return all NULLs */
SELECT
  f.FlowerName,
  c.ColorName
FROM
  Flowers f
  LEFT JOIN Colors c ON (c.ColorID = f.ColorID)
WHERE
CASE WHEN c.ColorID >= 0 THEN 0 ELSE 1 END = 1;"""

act = isql_act('db', test_script)

expected_stdout = """PLAN JOIN (F NATURAL, C INDEX (PK_COLORS))

FLOWERNAME                     COLORNAME
============================== ====================

Blanc                          <null>"""

@pytest.mark.version('>=3')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
