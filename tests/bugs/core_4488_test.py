#coding:utf-8

"""
ID:          issue-4808
ISSUE:       4808
TITLE:       Wrong results of FOR SELECT <L> FROM <T> AS CURSOR <C> and table <T> is
  modified inside cursor's begin...end block
DESCRIPTION:
  See doc\\sql.extensions\\README.cursor_variables.txt:
  7) Reading from a cursor variable returns the current field values. That means an UPDATE (with
     WHERE CURRENT OF) also updates the fields for subsequent reads. And DELETE (with WHERE
     CURRENT OF) makes subsequent reads to return NULL.
JIRA:        CORE-4488
FBTEST:      bugs.core_4488
"""

import pytest
from firebird.qa import *

init_script = """
    recreate table t_source(id int, x int, y int, z int); commit;
    recreate table t_target(id int, x int, y int, z int); commit;
    insert into t_source values(1, 10, 100, 1000);
    insert into t_source values(2, 20, 200, 2000);
    insert into t_source values(3, 30, 300, 3000);
    commit;
"""

db = db_factory(init=init_script)

test_script = """
    --------------- 1 -----------------
    select '' as "old data of t_source:", (select count(*) from t_source) "rows in t_source", s.*
    from rdb$database b left join t_source s on 1=1;
    set term ^;
    execute block
    as
    begin
      for
      select
        id,
        x as x,
        y as y,
        z as z
      from t_source s
      as cursor cs
      do begin
        delete from t_source where current of cs; -- yes, we DELETE record BEFORE insert it's values because now they all are stored in cursor 'CS' variables
        insert into t_target values( cs.id, cs.x, cs.y, cs.z );
      end
    end
    ^ set term ;^
    select '' as "1. New data of t_source:", (select count(*) from t_source) "rows in t_source", s.*
    from rdb$database b left join t_source s on 1=1;
    select '' as "1. New data of t_target:", (select count(*) from t_target) "rows in t_target", t.*
    from rdb$database b left join t_target t on 1=1;
    rollback;

    --------------- 2 -----------------
    set term ^;
    execute block
    as
    begin
      for
      select
        id,
        x+1 as x,
        y+2 as y,
        z+3 as z
      from t_source s
      as cursor cs
      do begin
        delete from t_source where current of cs;
        insert into t_target values( cs.id, cs.x, cs.y, cs.z );
      end
    end
    ^ set term ;^

    select '' as "2. New data of t_source:", (select count(*) from t_source) "rows in t_source", s.*
    from rdb$database b left join t_source s on 1=1;
    select '' as "2. New data of t_target:", (select count(*) from t_target) "rows in t_target", t.*
    from rdb$database b left join t_target t on 1=1;

    rollback;

    --------------- 3 -----------------
    set term ^;
    execute block
    as
    begin
      for
      select
        id,
        x as x,
        y as y,
        z+1 as z
      from t_source s
      as cursor cs
      do begin
        update t_source set y=x, z=y, x=z where current of cs;
        insert into t_target values( cs.id, cs.x, cs.y, cs.z );
      end
    end
    ^ set term ;^

    select '' as "3. New data of t_source:", (select count(*) from t_source) "rows in t_source", s.*
    from rdb$database b left join t_source s on 1=1;
    select '' as "3. New data of t_target:", (select count(*) from t_target) "rows in t_target", t.*
    from rdb$database b left join t_target t on 1=1;

    rollback;
"""

act = isql_act('db', test_script, substitutions=[('=.*', '')])

expected_stdout = """
    old data of t_source:      rows in t_source           ID            X            Y            Z
    ===================== ===================== ============ ============ ============ ============
                                              3            1           10          100         1000
                                              3            2           20          200         2000
                                              3            3           30          300         3000


    1. New data of t_source:      rows in t_source           ID            X            Y            Z
    ======================== ===================== ============ ============ ============ ============
                                                 0       <null>       <null>       <null>       <null>


    1. New data of t_target:      rows in t_target           ID            X            Y            Z
    ======================== ===================== ============ ============ ============ ============
                                                 3       <null>       <null>       <null>       <null>
                                                 3       <null>       <null>       <null>       <null>
                                                 3       <null>       <null>       <null>       <null>


    2. New data of t_source:      rows in t_source           ID            X            Y            Z
    ======================== ===================== ============ ============ ============ ============
                                                 0       <null>       <null>       <null>       <null>


    2. New data of t_target:      rows in t_target           ID            X            Y            Z
    ======================== ===================== ============ ============ ============ ============
                                                 3       <null>       <null>       <null>       <null>
                                                 3       <null>       <null>       <null>       <null>
                                                 3       <null>       <null>       <null>       <null>


    3. New data of t_source:      rows in t_source           ID            X            Y            Z
    ======================== ===================== ============ ============ ============ ============
                                                 3            1         1000           10          100
                                                 3            2         2000           20          200
                                                 3            3         3000           30          300


    3. New data of t_target:      rows in t_target           ID            X            Y            Z
    ======================== ===================== ============ ============ ============ ============
                                                 3            1         1000           10          101
                                                 3            2         2000           20          201
                                                 3            3         3000           30          301
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

