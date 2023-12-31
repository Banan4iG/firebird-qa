#coding:utf-8

"""
ID:          issue-5201
ISSUE:       5201
TITLE:       MERGE / HASH JOINs produce incorrect results when VARCHAR join keys differ only by trailing spaces
DESCRIPTION:
JIRA:        CORE-4909
FBTEST:      bugs.core_4909
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    create or alter view v_test as select 1  id from rdb$database;
    commit;
    recreate table test (
        v varchar(10),
        x integer
    );
    recreate table show (
        t1_v_repl varchar(10),
        t1_x integer,
        t2_v_repl varchar(10),
        t2_x integer
    );
    commit;

    create or alter view v_test as
    select
         replace(t1.v, ' ', '0') as t1_v_repl
        ,t1.x as t1_x
        ,replace(t2.v, ' ', '0') as t2_v_repl
        ,t2.x as t2_x
    from test t1
    join test t2 on t1.v = t2.v;
    commit;

    insert into test (v, x) values ('ww', 1);
    insert into test (v, x) values ('ww ', 2);
    commit;

    create index test_v on test(v);
    commit;

    alter index test_v inactive;
    commit;

    set list on;

    delete from show;

    --set plan on;
    insert into show
    select * from v_test;
    set plan off;
    commit;

    select 'index_inactive' as msg, s.* from show s order by t1_v_repl, t2_v_repl;
    commit;

    alter index test_v active;
    commit;

    delete from show;

    --set plan on;
    insert into show
    select * from v_test;
    set plan off;
    commit;

    select 'index_active' as msg, s.* from show s order by t1_v_repl, t2_v_repl;
    commit;
"""

act = isql_act('db', test_script)

expected_stdout = """
    MSG                             index_inactive
    T1_V_REPL                       ww
    T1_X                            1
    T2_V_REPL                       ww
    T2_X                            1

    MSG                             index_inactive
    T1_V_REPL                       ww
    T1_X                            1
    T2_V_REPL                       ww0
    T2_X                            2

    MSG                             index_inactive
    T1_V_REPL                       ww0
    T1_X                            2
    T2_V_REPL                       ww
    T2_X                            1

    MSG                             index_inactive
    T1_V_REPL                       ww0
    T1_X                            2
    T2_V_REPL                       ww0
    T2_X                            2

    MSG                             index_active
    T1_V_REPL                       ww
    T1_X                            1
    T2_V_REPL                       ww
    T2_X                            1

    MSG                             index_active
    T1_V_REPL                       ww
    T1_X                            1
    T2_V_REPL                       ww0
    T2_X                            2

    MSG                             index_active
    T1_V_REPL                       ww0
    T1_X                            2
    T2_V_REPL                       ww
    T2_X                            1

    MSG                             index_active
    T1_V_REPL                       ww0
    T1_X                            2
    T2_V_REPL                       ww0
    T2_X                            2
"""

@pytest.mark.version('>=3')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

