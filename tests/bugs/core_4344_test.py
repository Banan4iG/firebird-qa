#coding:utf-8

"""
ID:          issue-4666
ISSUE:       4666
TITLE:       Error "no current record for fetch operation" when table inner join procedure inner join table
DESCRIPTION:
JIRA:        CORE-4344
FBTEST:      bugs.core_4344
"""

import pytest
from firebird.qa import *

init_script = """
    create or alter procedure sp_get_f01(a_id int) returns(f01 int) as begin end;
    create or alter procedure sp_get_f02(a_id int) returns(f01 int) as begin end;
    create or alter procedure sp_get_f03(a_id int) returns(f01 int) as begin end;
    create or alter procedure sp_get_f04(a_id int) returns(f01 int) as begin end;
    create or alter procedure sp_get_f05(a_id int) returns(f01 int) as begin end;

    recreate table test(
        id int primary key using index test_pk
        ,f01 int
        ,f02 int
        ,f03 int
        ,f04 int
        ,f05 int
    );
    commit;
    insert into test(id, f01, f02, f03, f04, f05) values( 1,  11,  22,  33,  44,  55);
    insert into test(id, f01, f02, f03, f04, f05) values( 2, 111, 222, 333, 444, 555);
    insert into test(id, f01, f02, f03, f04, f05) values( 3,1111,2222,3333,4444,5555);
    commit;

    set term ^;
    create or alter procedure sp_get_f01(a_id int) returns(f01 int) as
    begin
      for select f01 from test where id = :a_id into f01 do suspend;
    end
    ^
    create or alter procedure sp_get_f02(a_id int) returns(f02 int) as
    begin
      for select f02 from test where id = :a_id into f02 do suspend;
    end
    ^
    create or alter procedure sp_get_f03(a_id int) returns(f03 int) as
    begin
      for select f03 from test where id = :a_id into f03 do suspend;
    end
    ^
    create or alter procedure sp_get_f04(a_id int) returns(f04 int) as
    begin
      for select f04 from test where id = :a_id into f04 do suspend;
    end
    ^
    create or alter procedure sp_get_f05(a_id int) returns(f05 int) as
    begin
      for select f05 from test where id = :a_id into f05 do suspend;
    end
    ^
    set term ;^
    commit;
"""

db = db_factory(init=init_script)

test_script = """
    set list on;
    select t1.id
    from test t1
    join sp_get_f01(t1.id) on 1=1
    join test t2 using(id)
    join sp_get_f02(t2.id) on 1=1
    join test t3 using(id)
    join sp_get_f03(t3.id) on 1=1
    join test t4 using(id)
    join sp_get_f04(t4.id) on 1=1
    join test t5 using(id)
    join sp_get_f05(t5.id) on 1=1
    join sp_get_f04(t4.id) on 1=1
    join sp_get_f03(t4.id) on 1=1
    join sp_get_f05(t5.id) on 1=1
    join sp_get_f04(t4.id) on 1=1
    join sp_get_f03(t4.id) on 1=1
    join test u5 using(id)
    join test u4 using(id)
    join sp_get_f02(t4.id) on 1=1
    join sp_get_f02(t4.id) on 1=1
    join sp_get_f02(t4.id) on 1=1
    join test u3 using(id)
    join test u2 using(id)
    join sp_get_f01(t4.id) on 1=1
    join sp_get_f01(t4.id) on 1=1
    join sp_get_f01(t4.id) on 1=1
    join test u1 using(id)
    join sp_get_f01(t4.id) on 1=1
    join test v1 using(id)
    ;
"""

act = isql_act('db', test_script)

expected_stdout = """
    ID                              1
    ID                              2
    ID                              3
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

