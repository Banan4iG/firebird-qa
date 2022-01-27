#coding:utf-8
#
# id:           bugs.gh_6681
# title:        error no permision occurred while ALTER USER SET TAGS on snapshot build WI-V3.0.8.33482
# decription:
#                   https://github.com/FirebirdSQL/firebird/issues/6681
#
#                   Checked on: 5.0.0.197
#
# tracker_id:
# min_versions: ['5.0']
# versions:     5.0
# qmid:         None

"""
ID:          issue-6681
ISSUE:       6681
TITLE:       Support for WHEN NOT MATCHED BY SOURCE for MERGE statement
DESCRIPTION:
JIRA:        CORE-6448
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    set list on;

    recreate table ts(id int primary key, x int);
    recreate table tt(id int primary key, x int);

    insert into ts(id, x) values(5, 500);
    insert into ts(id, x) values(4, 400);
    insert into ts(id, x) values(1, 100);
    insert into ts(id, x) values(3, 300);
    insert into ts(id, x) values(2, 200);


    insert into tt(id, x) values(3, 30);
    insert into tt(id, x) values(7, 70);
    insert into tt(id, x) values(6, 60);
    insert into tt(id, x) values(4, 40);
    insert into tt(id, x) values(5, 50);

    commit;

    merge into tt t using ts s on s.id = t.id
    when matched then update set t.x = t.x + s.x
    returning t.id as tt_id_1, t.x as tt_x_1
    ;
    rollback;

    merge into tt t using ts s on s.id = t.id
    when matched then update set t.x = t.x + s.x
    when NOT matched then insert values(-s.id, -s.x)
    returning t.id as tt_id_2, t.x as tt_x_2
    ;
    rollback;

    merge into tt t using ts s on s.id = t.id
    when matched then update set t.x = t.x + s.x
    when NOT matched BY TARGET then insert values(-10 * s.id, -10 * s.x)
    returning t.id as tt_id_3, t.x as tt_x_3
    ;
    rollback;


    merge into tt t using ts s on s.id = t.id
    when matched then update set t.x = t.x + s.x
    when NOT matched BY SOURCE then update set t.id = -100 * t.id, t.x = -100 * t.x
    returning t.id as tt_id_4, t.x as tt_x_4
    ;
    rollback;


    merge into tt t using ts s on s.id = t.id
    when matched then update set t.x = t.x + s.x
    when NOT matched BY SOURCE then delete
    when NOT matched BY TARGET then insert values(-10 * s.id, -10 * s.x)
    returning t.id as tt_id_5, t.x as tt_x_5
    ;
    rollback;

"""

act = isql_act('db', test_script)

expected_stdout = """
    TT_ID_1                         5
    TT_X_1                          550

    TT_ID_1                         4
    TT_X_1                          440

    TT_ID_1                         3
    TT_X_1                          330



    TT_ID_2                         5
    TT_X_2                          550

    TT_ID_2                         4
    TT_X_2                          440

    TT_ID_2                         -1
    TT_X_2                          -100

    TT_ID_2                         3
    TT_X_2                          330

    TT_ID_2                         -2
    TT_X_2                          -200



    TT_ID_3                         5
    TT_X_3                          550

    TT_ID_3                         4
    TT_X_3                          440

    TT_ID_3                         -10
    TT_X_3                          -1000

    TT_ID_3                         3
    TT_X_3                          330

    TT_ID_3                         -20
    TT_X_3                          -2000



    TT_ID_4                         3
    TT_X_4                          330

    TT_ID_4                         -700
    TT_X_4                          -7000

    TT_ID_4                         -600
    TT_X_4                          -6000

    TT_ID_4                         4
    TT_X_4                          440

    TT_ID_4                         5
    TT_X_4                          550



    TT_ID_5                         3
    TT_X_5                          330

    TT_ID_5                         7
    TT_X_5                          70

    TT_ID_5                         6
    TT_X_5                          60

    TT_ID_5                         4
    TT_X_5                          440

    TT_ID_5                         5
    TT_X_5                          550

    TT_ID_5                         -10
    TT_X_5                          -1000

    TT_ID_5                         -20
    TT_X_5                          -2000
"""

@pytest.mark.version('>=5.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
