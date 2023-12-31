#coding:utf-8

"""
ID:          tabloid.eqc-343715
TITLE:       Checking PK index is used when table is joined as driven (right) source in LEFT OUTER join from VIEW
DESCRIPTION: 
  Number of index reads per TABLE can be watched only in 3.0 by using mon$table_stats. 
     We have to ensure that table TEST1 in following queries is accessed only by its PK index, i.e. NO natural reads for it can occur.
FBTEST:      functional.tabloid.eqc_343715
"""

import pytest
from firebird.qa import *

init_script = """
    create or alter view vlast_test1_for_test3_a as select 1 id from rdb$database;
    create or alter view vlast_test1_for_test3_b as select 1 id from rdb$database;
    create or alter procedure get_last_test1_for_test3 as begin end;
    
    recreate table test2(
        id int primary key using index pk_test2_id,
        id1 int not null 
    );
    recreate table test1(
        id int primary key using index pk_test1_id
    );
    
    alter table test2 add constraint fk_test2_test1 foreign key(id1) references test1(id);
    
    recreate table test3(
        id int primary key using index pk_test3_id
    );
    
    alter table test2 add id3 integer;
    alter table test2 add constraint fk_test2_test3 foreign key(id3) references test3(id);
    
    set term ^;
    create or alter procedure get_last_test1_for_test3(id3 integer)
        returns(out_id1 integer)
    as
    begin
        for
            select t2.id1
            from test2 t2
            where t2.id3=:id3
            order by t2.id1 desc
            rows 1
            into :out_id1
        do
            suspend;
    end
    ^
    set term ;^
    commit;
    
    create or alter view vlast_test1_for_test3_a(id3, id1) as
    select
        t3.id
       ,(select p.out_id1 from get_last_test1_for_test3(t3.id) p)
    from test3 t3
    ;
    
    create or alter view vlast_test1_for_test3_b(id3, id1) as
    select
        t3.id
       ,(
            select t2.id1
            from test2 t2
            where t2.id3 = t3.id
            order by t2.id1 desc
            rows 1
        )
    from test3 t3
    ;
    commit;
  
"""

db = db_factory(from_backup='mon-stat-gathering-3_0.fbk', init=init_script)

test_script = """
    insert into test3(id) values(1);
    insert into test3(id) values(2);
    insert into test3(id) values(3);
    
    
    insert into test1(id) values(1);
           insert into test2(id, id1, id3) values(1, 1, 2);
           insert into test2(id, id1, id3) values(2, 1, 2);
           insert into test2(id, id1, id3) values(3, 1, 2);
    insert into test1(id) values(2);
           insert into test2(id, id1, id3) values(4, 2, 2);
           insert into test2(id, id1, id3) values(5, 2, 2);
    insert into test1(id) values(3);
           insert into test2(id, id1, id3) values(6, 3, 3);
           insert into test2(id, id1, id3) values(7, 3, 3);
    insert into test1(id) values(4);
           insert into test2(id, id1, id3) values(8, 4, 3);
           insert into test2(id, id1, id3) values(9, 4, 3);
    insert into test1(id) values(5);
           insert into test2(id, id1, id3) values(10, 5, 3);
           insert into test2(id, id1, id3) values(11, 5, 3);
    insert into test1(id) values(6);
           insert into test2(id, id1, id3) values(12, 6, 1);
           insert into test2(id, id1, id3) values(13, 6, 1);
           insert into test2(id, id1, id3) values(14, 6, 1);
           insert into test2(id, id1, id3) values(15, 6, 1);
    
    commit;
    
    execute procedure sp_truncate_stat;
    commit;

    execute procedure sp_gather_stat; ------- catch statistics BEFORE measured statement(s)
    commit;

    set term ^;
    execute block as
      declare c int;
    begin
      select count(*) -- v.*, t3.*, t1.*
      from vlast_test1_for_test3_a v
      join test3 t3 on t3.id=v.id3
      left join test1 t1 on t1.id=v.id1
      into c;
    
      select count(*) -- v.*, t3.*, t1.*
      from vlast_test1_for_test3_b v
      join test3 t3 on t3.id=v.id3
      left join test1 t1 on t1.id=v.id1
      into c;
    end
    ^
    set term ;^

    execute procedure sp_gather_stat;  ------- catch statistics AFTER measured statement(s)
    commit;

    -- Show results (differences of saved monitoring counters):
    -- ========================================================

    set list on;
    --set width table_name 10;
    select v.table_name, v.natural_reads, v.indexed_reads
    from v_agg_stat_tabs v
    where table_name = upper('TEST1');
"""

act = isql_act('db', test_script)

expected_stdout = """
    TABLE_NAME                      TEST1                                                                                                                                                                                                                                                                                  
    NATURAL_READS                   0
    INDEXED_READS                   6
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
