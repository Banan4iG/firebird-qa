#coding:utf-8

"""
ID:          optimizer.sort-by-index-10
TITLE:       ORDER BY ASC using index (multi)
DESCRIPTION:
  ORDER BY X, Y
  When more fields are given in ORDER BY clause try to use a compound index.
"""

import pytest
from firebird.qa import *

init_script = """
    recreate table test_idx (
      id1 integer,
      id2 integer
    );
    insert into test_idx(id1, id2)
    select (r/10)*10, r - (r/10)*10
    from (select row_number()over() r from rdb$types rows 50);
    insert into test_idx (id1, id2) values (0, null);
    insert into test_idx (id1, id2) values (null, 0);
    insert into test_idx (id1, id2) values (null, null);
    commit;

    create asc  index idx_id1_asc      on test_idx(id1);
    create desc index idx_id1_desc     on test_idx(id1);
    create asc  index idx_id2_asc      on test_idx(id2);
    create desc index idx_id2_desc     on test_idx(id2);
    create asc  index idx_id1_id2_asc  on test_idx(id1, id2);
    create desc index idx_id1_id2_desc on test_idx(id1, id2);
    create asc  index idx_id2_id1_asc  on test_idx(id2, id1);
    create desc index idx_id2_id1_desc on test_idx(id2, id1);
    commit;
  """

db = db_factory(init=init_script)

test_script = """
    -- Queries with RANGE index scan now have in the plan only "ORDER"
    -- clause (index navigation) without bitmap building.
    -- See: http://tracker.firebirdsql.org/browse/CORE-1550
    -- ("the same index should never appear in both ORDER and INDEX parts of the same plan item")

    set plan on;
    select t.id1, t.id2
    from test_idx t
    where t.id1 = 40  -----------------                                        --- must navigate through the leaf level of idx_id1_id2_asc, *without* bitmap!
    order by  t.id1 asc, t.id2 asc; ---/
"""

act = isql_act('db', test_script, substitutions=[('=.*', '')])

expected_stdout = """
  PLAN (T ORDER IDX_ID1_ID2_ASC)

         ID1          ID2
          40            0
          40            1
          40            2
          40            3
          40            4
          40            5
          40            6
          40            7
          40            8
          40            9
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
