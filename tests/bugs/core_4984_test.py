#coding:utf-8

"""
ID:          issue-5275
ISSUE:       5275
TITLE:       Ordering by compound index together with a range condition gives wrong results
DESCRIPTION:
JIRA:        CORE-4984
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    -- Confirmed on WI-V3.0.0.32081: wrong output for CHECKED_RESULT_1, CHECKED_RESULT_3 & CHECKED_RESULT_4
    -- (but this was only for ASC index; for DESC index all was fine).
    -- Since WI-V3.0.0.32137 result is correct.

    recreate table test_idx(
        id integer not null,
        val integer,
        create_date date,
        primary key (id)
    );
    commit;

    insert into test_idx values(1,1,'2016-01-01');
    insert into test_idx values(2,1,'2015-01-02');
    insert into test_idx values(3,2,'1999-09-09');
    insert into test_idx values(4,2,'2015-02-02');
    insert into test_idx values(5,3,'2015-03-01');
    insert into test_idx values(6,3,'2015-03-02');
    insert into test_idx values(7,4,'2015-04-01');
    commit;

    set list on;

    select 'natural_scan' as msg, cast(min(create_date) as date) as expected_result from test_idx where val >=1 and val <=3;
    commit;

    create index idx_val_create_date_asc on test_idx (val, create_date);
    commit;

    select 'index_scan_ascending' as msg, cast(min(create_date) as date) as checked_result_1
    from test_idx where val >=1 and val <=3;
    select 'index_scan_ascending' as msg, cast(min(create_date) as date) as checked_result_2
    from (select * from test_idx where val > 0 and val < 4 order by val);
    select 'index_scan_ascending' as msg, cast(min(create_date) as date) as checked_result_3
    from test_idx where 4 > val and 0 < val;
    select 'index_scan_ascending' as msg, cast(min(create_date) as date) as checked_result_4
    from test_idx where val between 1 and 3;
    select 'index_scan_ascending' as msg, cast(min(create_date) as date) as checked_result_5
    from test_idx where val in (1,2,3);
    commit;

    drop index idx_val_create_date_asc;
    commit;

    connect '$(DSN)' user 'SYSDBA' password 'masterkey';

    create descending index idx_val_create_date_desc on test_idx (val, create_date);
    commit;

    select 'index_scan_descending' as msg, cast(min(create_date) as date) as checked_result_1
    from test_idx where val >=1 and val <=3;
    select 'index_scan_descending' as msg, cast(min(create_date) as date) as checked_result_2
    from (select * from test_idx where val > 0 and val < 4 order by val desc);
    select 'index_scan_descending' as msg, cast(min(create_date) as date) as checked_result_3
    from test_idx where 4 > val and 0 < val;
    select 'index_scan_descending' as msg, cast(min(create_date) as date) as checked_result_4
    from test_idx where val between 1 and 3;
    select 'index_scan_descending' as msg, cast(min(create_date) as date) as checked_result_5
    from test_idx where val in (1,2,3);

    commit;
"""

act = isql_act('db', test_script)

expected_stdout = """
    MSG                             natural_scan
    EXPECTED_RESULT                 1999-09-09

    MSG                             index_scan_ascending
    CHECKED_RESULT_1                1999-09-09
    MSG                             index_scan_ascending
    CHECKED_RESULT_2                1999-09-09
    MSG                             index_scan_ascending
    CHECKED_RESULT_3                1999-09-09
    MSG                             index_scan_ascending
    CHECKED_RESULT_4                1999-09-09
    MSG                             index_scan_ascending
    CHECKED_RESULT_5                1999-09-09

    MSG                             index_scan_descending
    CHECKED_RESULT_1                1999-09-09
    MSG                             index_scan_descending
    CHECKED_RESULT_2                1999-09-09
    MSG                             index_scan_descending
    CHECKED_RESULT_3                1999-09-09
    MSG                             index_scan_descending
    CHECKED_RESULT_4                1999-09-09
    MSG                             index_scan_descending
    CHECKED_RESULT_5                1999-09-09
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
