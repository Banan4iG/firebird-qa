#coding:utf-8
#
# id:           functional.arno.indices.lower_bound_asc_02_segments_01
# title:        ASC 2-segment index lower bound
# decription:   Check if all 5 values are fetched with "equals" operator over first segment and "greater than or equal" operator on second segment.
#               2 values are bound to the upper segments and 1 value is bound to the lower segment.
# tracker_id:   
# min_versions: []
# versions:     1.5
# qmid:         functional.arno.indexes.lower_bound_asc_02_segments_01

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 1.5
# resources: None

substitutions_1 = []

init_script_1 = """CREATE TABLE Table_2_10 (
  F1 INTEGER,
  F2 INTEGER
);

COMMIT;

INSERT INTO Table_2_10 (F1, F2) VALUES (1, 1);
INSERT INTO Table_2_10 (F1, F2) VALUES (1, 2);
INSERT INTO Table_2_10 (F1, F2) VALUES (1, 3);
INSERT INTO Table_2_10 (F1, F2) VALUES (1, 4);
INSERT INTO Table_2_10 (F1, F2) VALUES (1, 5);
INSERT INTO Table_2_10 (F1, F2) VALUES (1, 6);
INSERT INTO Table_2_10 (F1, F2) VALUES (1, 7);
INSERT INTO Table_2_10 (F1, F2) VALUES (1, 8);
INSERT INTO Table_2_10 (F1, F2) VALUES (1, 9);
INSERT INTO Table_2_10 (F1, F2) VALUES (1, 10);
INSERT INTO Table_2_10 (F1, F2) VALUES (2, 1);
INSERT INTO Table_2_10 (F1, F2) VALUES (2, 2);
INSERT INTO Table_2_10 (F1, F2) VALUES (2, 3);
INSERT INTO Table_2_10 (F1, F2) VALUES (2, 4);
INSERT INTO Table_2_10 (F1, F2) VALUES (2, 5);
INSERT INTO Table_2_10 (F1, F2) VALUES (2, 6);
INSERT INTO Table_2_10 (F1, F2) VALUES (2, 7);
INSERT INTO Table_2_10 (F1, F2) VALUES (2, 8);
INSERT INTO Table_2_10 (F1, F2) VALUES (2, 9);
INSERT INTO Table_2_10 (F1, F2) VALUES (2, 10);

COMMIT;

CREATE ASC INDEX I_Table_2_10_ASC ON Table_2_10 (F1, F2);

COMMIT;
"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """SET PLAN ON;
SELECT
  t.F1,
  t.F2
FROM
  Table_2_10 t
WHERE
  t.F1 = 2 and t.F2 >= 6;"""

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """PLAN (T INDEX (I_TABLE_2_10_ASC))

          F1           F2
============ ============

           2            6
           2            7
           2            8
           2            9
           2           10
"""

@pytest.mark.version('>=1.5')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout

