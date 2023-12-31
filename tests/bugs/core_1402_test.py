#coding:utf-8

"""
ID:          issue-1820
ISSUE:       1820
TITLE:       CREATE VIEW without column list when UNION is used
DESCRIPTION:
JIRA:        CORE-1402
FBTEST:      bugs.core_1402
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    recreate view V1 as
    select d.rdb$relation_id from rdb$database d
    union all
    select d.rdb$relation_id from rdb$database d;

    recreate view V2 as
    select d.rdb$relation_id as q from rdb$database d
    union all
    select d.rdb$relation_id as w from rdb$database d;

    recreate view V3 as
    select a from (select 1 a from rdb$database)
    union all
    select b from (select 1 b from rdb$database);

    recreate view V4 as
    select a as a1 from (select 1 a from rdb$database)
    union all
    select b as b1 from (select 1 b from rdb$database);
    commit;

    set blob all;
    set list on;

    -- Removed 'show view' commands because of core-4782 (failed on windows builds when connection charset = UTF8).
    -- Added checking query to RDB$ tables instead that views indeed DO have fields of proper type (7=smallint, 8=int):
    select
        r.rdb$relation_name v_name,
        r.rdb$view_source v_source,
        f.rdb$field_name f_name,
        ff.rdb$field_type f_type
    from rdb$relations r
    join rdb$relation_fields f using (rdb$relation_name)
    join rdb$fields ff on f.rdb$field_source = ff.rdb$field_name
    where
    r.rdb$relation_type = 1
    and r.rdb$relation_name in ('V1','V2','V3','V4')
    order by v_name, f_name;
"""

act = isql_act('db', test_script, substitutions=[('V_SOURCE.*', '')])

expected_stdout = """
    V_NAME                          V1
    V_SOURCE                        6:1e8
    select d.rdb$relation_id from rdb$database d
    union all
    select d.rdb$relation_id from rdb$database d
    F_NAME                          RDB$RELATION_ID
    F_TYPE                          7

    V_NAME                          V2
    V_SOURCE                        6:1eb
    select d.rdb$relation_id as q from rdb$database d
    union all
    select d.rdb$relation_id as w from rdb$database d
    F_NAME                          Q
    F_TYPE                          7

    V_NAME                          V3
    V_SOURCE                        6:2ce
    select a from (select 1 a from rdb$database)
    union all
    select b from (select 1 b from rdb$database)
    F_NAME                          A
    F_TYPE                          8

    V_NAME                          V4
    V_SOURCE                        6:2d1
    select a as a1 from (select 1 a from rdb$database)
    union all
    select b as b1 from (select 1 b from rdb$database)
    F_NAME                          A1
    F_TYPE                          8
"""

@pytest.mark.version('>=3')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

