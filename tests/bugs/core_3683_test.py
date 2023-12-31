#coding:utf-8

"""
ID:          issue-4032
ISSUE:       4032
TITLE:       Wrong results if the recursive query contains an embedded GROUP BY clause
DESCRIPTION:
JIRA:        CORE-3683
FBTEST:      bugs.core_3683
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    set list on;
    recreate view v_test as select 1 x from rdb$database;
    commit;

    -- ###################################### from CORE_3683  #################################

    recreate table tmp_result(seq smallint, step int, routes varchar(32000) );

    recreate table rdeps(parent varchar(32),child varchar(32), parent_type int, child_type int, f01 int);
    commit;

    recreate view v_test as
    with recursive
    rd as(
      select
         d.parent parent
        ,d.child
      from rdeps d
      group by d.parent,d.child -- <<< we need this grouping to eliminate duplicates
    )
    ,cr as(
      select 0 step,parent,child,cast(parent as varchar(32000))||'->'||child routes
      from rd
      where rd.parent='MOSCOW'

      UNION ALL

      select x.step+1,rd.parent,rd.child,x.routes||'->'||rd.child
      from cr x
      join rd on x.child=rd.parent
    )
    select step,routes from cr order by step,routes
    ;


    insert into rdeps values( 'MOSCOW', 'TULA', 0, 5, 21);
    insert into rdeps values( 'MOSCOW', 'TULA', 0, 5, 22);

    insert into rdeps values( 'TULA', 'OREL', 5, 5, 51);
    insert into rdeps values( 'TULA', 'OREL', 5, 5, 52);

    insert into rdeps values( 'TULA', 'LIPETSK', 5, 2, 71);
    insert into rdeps values( 'TULA', 'LIPETSK', 5, 2, 72);

    insert into rdeps values( 'TULA', 'RYAZAN', 5, 5, 61);
    insert into rdeps values( 'TULA', 'RYAZAN', 5, 5, 62);

    insert into rdeps values( 'OREL', 'KURSK', 5, 5, 81);
    insert into rdeps values( 'OREL', 'KURSK', 5, 5, 82);

    insert into rdeps values( 'LIPETSK','VORONEZH', 5, 2, 71);
    insert into rdeps values( 'LIPETSK','VORONEZH', 5, 2, 72);

    insert into rdeps values( 'RYAZAN','MUROM', 5, 5, 61);
    insert into rdeps values( 'RYAZAN','MUROM', 5, 5, 62);

    commit;

    set count on;

    insert into tmp_result(seq, step, routes) select 1, step,routes from v_test;
    --select * from v_test;
    commit;

    -- AFTER ADDING INDEX RESULT BECAME CORRECT:
    -- #########################################
    create index rdeps_unq on rdeps(parent, child, f01);
    commit;


    insert into tmp_result(seq, step, routes) select 2, step,routes from v_test;
    commit;

    -- check query: should return zero rows.
    select a_step, a_routes, b_step, b_routes
    from (
        select a.step as a_step, a.routes as a_routes
        from tmp_result a where a.seq=1
    ) a
    full join
    (
        select b.step as b_step, b.routes as b_routes
        from tmp_result b where b.seq=2
    ) b
    on a.a_step = b.b_step and a.a_routes = b.b_routes
    where a.a_step is null or b.b_step is null
    ;
    commit;

    set count off;

    --############################################# FROM CORE_3698: ######################################

    recreate table contacts (
        id        integer not null,
        age       integer,
        name      varchar(255),
        customer  integer not null
    );

    recreate table customers (
        id        integer not null,
        name      varchar(255),
        parentid  integer
    );

    insert into customers (id, name, parentid) values (1, 'dent', null);
    insert into customers (id, name, parentid) values (2, 'troprosys usa', null);
    insert into customers (id, name, parentid) values (3, 'gralpingro gmbh', null);
    insert into customers (id, name, parentid) values (4, 'systed', null);
    insert into customers (id, name, parentid) values (5, 'tian', null);
    insert into customers (id, name, parentid) values (6, 'logy asia', null);
    insert into customers (id, name, parentid) values (7, 'nalf devices', null);
    insert into customers (id, name, parentid) values (8, 'coak', null);
    insert into customers (id, name, parentid) values (9, 'boo consulting', null);
    insert into customers (id, name, parentid) values (10, 'gral-berlin', 3);
    insert into customers (id, name, parentid) values (11, 'gral-hamburg', 3);
    insert into customers (id, name, parentid) values (12, 'gral-munich', 3);
    insert into customers (id, name, parentid) values (13, 'gral-cologne', 3);
    insert into customers (id, name, parentid) values (14, 'logy-japan', 6);
    insert into customers (id, name, parentid) values (15, 'logy-tokyo', 14);
    insert into customers (id, name, parentid) values (16, 'logy-kyoto', 14);
    insert into customers (id, name, parentid) values (17, 'logy-tokyo-west', 15);
    insert into customers (id, name, parentid) values (18, 'logy-tokyo-east', 15);

    commit;

    insert into contacts (id, age, name, customer) values (1, 21, 'abc', 11);
    insert into contacts (id, age, name, customer) values (2, 82, 'paige chen', 8);
    insert into contacts (id, age, name, customer) values (10, 23, 'whatever', 17);
    insert into contacts (id, age, name, customer) values (11, 22, 'someone', 17);
    insert into contacts (id, age, name, customer) values (12, 23, 'manager', 17);
    insert into contacts (id, age, name, customer) values (13, 44, 'manager', 17);
    insert into contacts (id, age, name, customer) values (15, 55, 'ceo', 9);

    commit;
    alter table contacts add constraint pk_contacts primary key (id);
    alter table customers add constraint pk_customers primary key (id);

    alter table contacts add constraint fk_contacts_1 foreign key (customer) references customers (id);
    commit;

    recreate table tmp_result(seq smallint, id int, name varchar(255), avgage numeric(12,2) );

    set count on;
    /** Test Case 1, Returns 18 Rows **/
    insert into tmp_result(seq, id, name, avgage)
    with recursive c (id,name,avgage)
    as

    (
        select customers.id, customers.name, 0 as avgage from customers
            where customers.parentid is null
        union all
        select customers.id, customers.name, 0 as avgage from customers
            join c as parent on parent.id = customers.parentid
    )
    select 1, c.* from c
    ;


    /** Test Case 2, Returns 15 Rows **/

    insert into tmp_result(seq, id, name, avgage)
    with recursive c (id,name,avgage)
    as

    (
        select customers.id, customers.name, average.age as avgage from customers
            join (select customers.id as customersid, AVG( 0 * COALESCE(contacts.age,0)) as age
                    from customers
                        left join contacts on contacts.customer = customers.id
                    group by 1) as average on average.customersid = customers.id
            where customers.parentid is null
        union all
        select customers.id, customers.name, average.age as avgage from customers
            join c as parent on parent.id = customers.parentid
            join (select customers.id as customersid, AVG( 0 * COALESCE(contacts.age,0)) as age
                    from customers
                        left join contacts on contacts.customer = customers.id
                    group by 1) as average on average.customersid = customers.id
    )

    select 2, c.* from c
    ;

    --------------------------------------------------------------

    -- check query: should return zero rows.
    select a_id, a_name, a_avgage, b_id, b_name, b_avgage
    from (
        select a.id as a_id, a.name as a_name, a.avgage as a_avgage
        from tmp_result a where seq=1
    ) a
    full join
    (
        select b.id as b_id, b.name as b_name, b.avgage as b_avgage
        from tmp_result b where seq=2
    ) b
    on a.a_id is not distinct from b.b_id
    where a.a_id is null or b.b_id is null
    ;
    commit;
"""

act = isql_act('db', test_script)

expected_stdout = """
    Records affected: 7
    Records affected: 7
    Records affected: 0
    Records affected: 18
    Records affected: 18
    Records affected: 0
"""

@pytest.mark.version('>=3')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

