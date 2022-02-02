#coding:utf-8

"""
ID:          issue-5654
ISSUE:       5654
TITLE:       Regression: could not execute query (select from view with nested view)
DESCRIPTION:
JIRA:        CORE-5381
FBTEST:      bugs.core_5381
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    create table t1(ID bigint not null primary key);
    create table t2(ID bigint not null primary key);
    create table t3(ID bigint not null primary key);
    create table t4(ID bigint not null primary key);
    create table t5(ID bigint not null primary key);
    create table t6(ID bigint not null primary key);
    create table t7(ID bigint not null primary key);
    create table t8(ID bigint not null primary key);

    create view inner_view(ID)
    as
    select t1.ID
      from t1
      inner join t8 B on B.ID = t1.ID
      inner join t2 C on C.ID = t1.ID
      left join t4 D on D.ID = t1.ID
      inner join t5 E on E.ID = t1.ID
      left join t6 F on F.ID = t1.ID

      inner join RDB$TYPES G1 on G1.rdb$type = t1.ID
      inner join RDB$RELATIONS G2 on G2.rdb$relation_id = t1.ID
      inner join RDB$DEPENDENCIES G3 on G3.rdb$dependent_type = t1.ID
      inner join RDB$COLLATIONS G4 on G4.rdb$collation_id = t1.ID
      inner join RDB$FIELDS G5 on G5.rdb$field_type = t1.ID
      inner join RDB$CHARACTER_SETS G6 on G6.rdb$character_set_id = t1.ID
    ;

    create view test_view(ID)
    as
    select t1.ID
      from t1
      inner join inner_view on inner_view.ID = t1.ID
      inner join t7 on t7.ID = t1.ID
      left join t3 on t3.ID = t1.ID

      inner join RDB$TYPES D1 on D1.rdb$type = t1.ID
      inner join RDB$RELATIONS D2 on D2.rdb$relation_id = t1.ID
      inner join RDB$DEPENDENCIES D3 on D3.rdb$dependent_type = t1.ID
      inner join RDB$COLLATIONS D4 on D4.rdb$collation_id = t1.ID
      inner join RDB$FIELDS D5 on D5.rdb$field_type = t1.ID
    ;
    commit;

    set list on;

    set term ^;
    execute block returns( result varchar(128) ) as
        declare dts_beg timestamp;
        declare c int;
        declare elap_ms int;
        declare max_allowed_ms int = 1000;
        --                           #####
        --                             ^
        --                             |
        --                ###########################
        --                ###  T H R E S H O L D  ###
        --                ###########################
    begin
        dts_beg ='now';

        select A.ID
          from test_view A
          inner join RDB$TYPES D1 on D1.rdb$type = A.ID
          inner join RDB$RELATIONS D2 on D2.rdb$relation_id = A.ID
          inner join RDB$DEPENDENCIES D3 on D3.rdb$dependent_type = A.ID
        where A.ID = 1
        into c;
        elap_ms = datediff(millisecond from dts_beg to cast('now' as timestamp));
        result = iif(elap_ms <= max_allowed_ms, 'Acceptable.', 'TOO LONG: ' || elap_ms || ' ms - more than max allowed ' || max_allowed_ms || ' ms.' );
        suspend;
    end
    ^
    set term ;^

"""

act = isql_act('db', test_script)

expected_stdout = """
    RESULT                          Acceptable.
"""

@pytest.mark.version('>=3.0.2')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

