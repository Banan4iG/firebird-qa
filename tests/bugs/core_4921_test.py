#coding:utf-8

"""
ID:          issue-1956
ISSUE:       1956
TITLE:       Predicate IS [NOT] DISTINCT FROM is not pushed into unions/aggregates thus causing sub-optimal plans
DESCRIPTION:
  Implementation for 3.0 does NOT use 'set explain on' (decision after discuss with Dmitry, letter 02-sep-2015 15:42).
  Test only checks that:
  1) in case when NATURAL scan occured currently index T*_SINGLE_X is used;
  2) in case when it was only PARTIAL matching index Y*_COMPOUND_X is in use.
JIRA:        CORE-4921
FBTEST:      bugs.core_4921
"""

import pytest
from firebird.qa import *

init_script = """
    create or alter view v_test as select 1 id from rdb$database;
    commit;

    recreate table t1(x int, y int);
    create index t1_single_x on t1(x);
    create index t1_compound_x_y on t1(x, y);

    recreate table t2(x int, y int);
    create index t2_single_x on t2(x);
    create index t2_compound_x_y on t2(x, y);

    recreate table t3(x int, y int);
    create index t3_single_x on t3(x);
    create index t3_compound_x_y on t3(x, y);
    commit;

    create or alter view v_test as
    select * from t1
    union all
    select * from t2
    union all
    select * from t3;
    commit;
"""

db = db_factory(init=init_script)

test_script = """
    set planonly;
    select * from v_test where x is not distinct from 1;
    select * from v_test where x = 1 and y is not distinct from 1;
    set planonly;
"""

act = isql_act('db', test_script)

expected_stdout = """
    PLAN (V_TEST T1 INDEX (T1_SINGLE_X), V_TEST T2 INDEX (T2_SINGLE_X), V_TEST T3 INDEX (T3_SINGLE_X))
    PLAN (V_TEST T1 INDEX (T1_COMPOUND_X_Y), V_TEST T2 INDEX (T2_COMPOUND_X_Y), V_TEST T3 INDEX (T3_COMPOUND_X_Y))
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

