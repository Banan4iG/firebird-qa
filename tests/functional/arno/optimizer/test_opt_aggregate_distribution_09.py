#coding:utf-8

"""
ID:          optimizer.aggregate-distribution-09
TITLE:       Try to deliver HAVING CLAUSE conjunctions to the WHERE clause
DESCRIPTION:
  Comparisons which doesn't contain (anywhere hiding in the expression) aggregate-functions
  should be delivered to the where clause. The underlying aggregate stream could possible
  use it for a index and speed it up.
FBTEST:      functional.arno.optimizer.opt_aggregate_distribution_09
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
INSERT INTO Colors (ColorID, ColorName) VALUES (2, 'White');
INSERT INTO Colors (ColorID, ColorName) VALUES (3, 'Blue');
INSERT INTO Colors (ColorID, ColorName) VALUES (4, 'Yellow');
INSERT INTO Colors (ColorID, ColorName) VALUES (5, 'Black');
INSERT INTO Colors (ColorID, ColorName) VALUES (6, 'Purple');

/* insert some data with references */
INSERT INTO Flowers (FlowerID, FlowerName, ColorID) VALUES (1, 'Red Rose', 1);
INSERT INTO Flowers (FlowerID, FlowerName, ColorID) VALUES (2, 'White Rose', 2);
INSERT INTO Flowers (FlowerID, FlowerName, ColorID) VALUES (3, 'Blue Rose', 3);
INSERT INTO Flowers (FlowerID, FlowerName, ColorID) VALUES (4, 'Yellow Rose', 4);
INSERT INTO Flowers (FlowerID, FlowerName, ColorID) VALUES (5, 'Black Rose', 5);
INSERT INTO Flowers (FlowerID, FlowerName, ColorID) VALUES (6, 'Red Tulip', 1);
INSERT INTO Flowers (FlowerID, FlowerName, ColorID) VALUES (7, 'White Tulip', 2);
INSERT INTO Flowers (FlowerID, FlowerName, ColorID) VALUES (8, 'Yellow Tulip', 4);
INSERT INTO Flowers (FlowerID, FlowerName, ColorID) VALUES (9, 'Blue Gerbera', 3);
INSERT INTO Flowers (FlowerID, FlowerName, ColorID) VALUES (10, 'Purple Gerbera', 6);

COMMIT;

/* Normally these indexes are created by the primary/foreign keys,
   but we don't want to rely on them for this test */
CREATE UNIQUE ASC INDEX PK_Colors ON Colors (ColorID);
CREATE UNIQUE ASC INDEX PK_Flowers ON Flowers (FlowerID);
CREATE ASC INDEX FK_Flowers_Colors ON Flowers (ColorID);

COMMIT;
"""

db = db_factory(init=init_script)

test_script = """SET PLAN ON;
SELECT
  f.ColorID,
  c.ColorName,
  Count(*)
FROM
  Flowers f
  LEFT JOIN Colors c ON (c.ColorID = f.ColorID)
GROUP BY
  f.ColorID, c.ColorName
HAVING
f.ColorID <= 4;"""

act = isql_act('db', test_script)

expected_stdout = """PLAN SORT (JOIN (F INDEX (FK_FLOWERS_COLORS), C INDEX (PK_COLORS)))

     COLORID COLORNAME                            COUNT
============ ==================== =====================
           1 Red                                      2
           2 White                                    2
           3 Blue                                     2
           4 Yellow                                   2
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
