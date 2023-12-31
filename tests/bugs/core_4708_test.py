#coding:utf-8

"""
ID:          issue-5016
ISSUE:       5016
TITLE:       Content of MON$EXPLAINED_PLAN in MON$STATEMENTS is truncated if exceeds the 32KB limit
DESCRIPTION:
JIRA:        CORE-4708
FBTEST:      bugs.core_4708
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    set list on;
    set blob all;
    -- This query has explained plan with length ~47 Kb (checked on WI-V3.0.0.32253).
    -- Instead of checking explained plan text it is enough only to ensure that its
    -- LENGTH is more than 32K and that text is not cuted off, i.e. it should end with
    -- phrase: Table "MON$STATEMENTS" Full Scan
    -- Another sample of query that has long plan see in core_5061.fbt
    with recursive
    rx as (
      select 1 as i from rdb$database
      union all
      select r.i+1 from rx r where r.i < 2
    )
    ,r2 as (
      select row_number() over() i
      from rx r
      full join rx r2 on r2.i=r.i
      group by r.i
      having count(*)>0
      order by r.i rows 1
    )
    select
         iif( char_length(mon$explained_plan) > 32767, 'MORE THAN 32K', 'LESS THEN 32K' ) as mon_explained_plan_len
        ,right(mon$explained_plan,32) as mon_explained_plan_tail
        ,(select count(*) from r2)
        ,(select count(*) from r2)
        ,(select count(*) from r2)
        ,(select count(*) from r2)
        ,(select count(*) from r2)
        ,(select count(*) from r2)
        ,(select count(*) from r2)
        ,(select count(*) from r2)
        ,(select count(*) from r2)
        ,(select count(*) from r2)

        ,(select count(*) from r2)
        ,(select count(*) from r2)
        ,(select count(*) from r2)
        ,(select count(*) from r2)
        ,(select count(*) from r2)
        ,(select count(*) from r2)
        ,(select count(*) from r2)
        ,(select count(*) from r2)
        ,(select count(*) from r2)
        ,(select count(*) from r2)

        ,(select count(*) from r2)
        ,(select count(*) from r2)
        ,(select count(*) from r2)
        ,(select count(*) from r2)
        ,(select count(*) from r2)
        ,(select count(*) from r2)
        ,(select count(*) from r2)
        ,(select count(*) from r2)
        --,(select count(*) from r2)
    from mon$statements s
    where
    s.mon$attachment_id = current_connection
    -- 08-may-2017: need for 4.0 Classic!
    -- Currently there is also query with RDB$AUTH_MAPPING data in mon$statements:
    and s.mon$sql_text containing 'select 1 as i'
    ;
    -- Table "MON$STATEMENTS" Full Scan
"""

act = isql_act('db', test_script, substitutions=[('MON_EXPLAINED_PLAN_TAIL.*', 'MON_EXPLAINED_PLAN_TAIL')])

expected_stdout = """
    MON_EXPLAINED_PLAN_LEN          MORE THAN 32K
    MON_EXPLAINED_PLAN_TAIL         0:4
    MON$STATEMENTS" as "S" Full Scan
    COUNT                           1
    COUNT                           1
    COUNT                           1
    COUNT                           1
    COUNT                           1
    COUNT                           1
    COUNT                           1
    COUNT                           1
    COUNT                           1
    COUNT                           1
    COUNT                           1
    COUNT                           1
    COUNT                           1
    COUNT                           1
    COUNT                           1
    COUNT                           1
    COUNT                           1
    COUNT                           1
    COUNT                           1
    COUNT                           1
    COUNT                           1
    COUNT                           1
    COUNT                           1
    COUNT                           1
    COUNT                           1
    COUNT                           1
    COUNT                           1
    COUNT                           1
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

