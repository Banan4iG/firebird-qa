#coding:utf-8

"""
ID:          issue-4503
ISSUE:       4503
TITLE:       Problem with some boolean expressions not being allowed
DESCRIPTION:
JIRA:        CORE-4177
FBTEST:      bugs.core_4177
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    set list on;
    --set echo on;

    select 1 x1
    from rdb$database
    where (1=1) is true;

    select 1 x2
    from rdb$database
    where true = true = true is not false is not distinct from not false is not false is not distinct from not false is not distinct from not false = not false is not distinct from not false ;

    select 1 x3
    from rdb$database
    where not false and not false = not not not not true and not not not false = not not true and not not not not not not not false;


    select 1 x4a
    from rdb$database
    where not false and not false is not false;


    select 1 x4b
    from rdb$database
    where not false and not false = not not not false;

    -- Fails as of 3.0.0.31906 (30.06.2015).
    -- select 1 x4c
    -- from rdb$database
    -- where not false and not false is not not not false;

    -- Works fine (but failed before; uncomment 30.06.2015):
    select 1 x4d
    from rdb$database
    where not false and not false is not distinct from not false;


    -- Following lines were commented before, now (3.0.0.31906, 30.06.2015) they work fine:

    select 1 y1
    from rdb$database
    where (1=1) is true;

    select 1 y2
    from rdb$database
    where true = true = true is not false is not distinct from not false is not false is not distinct from not false is not distinct from not false = not false is not distinct from not false ;

    select 1 y3
    from rdb$database
    where not false and not false = not not not not true and not not not false = not not true and not not not not not not not false;


    select 1 y4a
    from rdb$database
    where not false and not false is not false;


    select 1 y4b
    from rdb$database
    where not false and not false = not not not false;


    recreate table test1(id int, x boolean);
    insert into test1 values(107, false);
    insert into test1 values(109, false);
    insert into test1 values(117, true );
    insert into test1 values(121, true );
    insert into test1 values(122, false);
    insert into test1 values(128, true );
    insert into test1 values(137, false);
    insert into test1 values(144, false);

    select * from test1 where x between true and true;
    select * from test1 where x between true and (not false);
    select * from test1 where x between (not false) and true;
    select * from test1 where x between (not false) and (not false);
"""

act = isql_act('db', test_script)

expected_stdout = """
    X1                              1
    X2                              1
    X3                              1
    X4A                             1
    X4B                             1
    X4D                             1
    Y1                              1
    Y2                              1
    Y3                              1
    Y4A                             1
    Y4B                             1
    ID                              117
    X                               <true>
    ID                              121
    X                               <true>
    ID                              128
    X                               <true>
    ID                              117
    X                               <true>
    ID                              121
    X                               <true>
    ID                              128
    X                               <true>
    ID                              117
    X                               <true>
    ID                              121
    X                               <true>
    ID                              128
    X                               <true>
    ID                              117
    X                               <true>
    ID                              121
    X                               <true>
    ID                              128
    X                               <true>
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
