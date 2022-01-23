#coding:utf-8

"""
ID:          issue-4412
ISSUE:       4412
TITLE:       Regression: Group by fails if subselect-column is involved
DESCRIPTION:
JIRA:        CORE-4084
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    set planonly;
    select
        iif(d is null, 10, 0) + sys as sys,
        count(*)
    from (
        select
            ( select d.rdb$relation_id from rdb$database d ) as d,
            coalesce(r.rdb$system_flag, 0) as sys
        from rdb$relations r
    )
    group by 1;
"""

act = isql_act('db', test_script)

expected_stdout = """
    PLAN (D NATURAL)
    PLAN SORT (R NATURAL)
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

