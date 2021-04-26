#coding:utf-8
#
# id:           bugs.core_0629
# title:        Grouping on derived fields processing NULL data kills IB
# decription:   
# tracker_id:   CORE-0629
# min_versions: ['2.5.0']
# versions:     2.5
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 2.5
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """
    set list on;

    create or alter view v_test as select 1 id from rdb$database;
    commit;

    recreate table test(
        id integer not null,
        dt_beg date,
        dt_end date,
        constraint pk_test primary key (id)
    );
    commit;

    create or alter view v_test as
    select id, extract(year from dt_beg) - extract(year from dt_end) dy
    from test;
    commit;

    insert into test values(1, '01.01.2015', null);
    insert into test values(2, '01.01.2015', '01.01.2015');
    insert into test values(3, null, null);
    insert into test values(4, null, null);
    insert into test values(5, '01.01.2015', '31.12.2014');
    commit;

    select dy from v_test group by dy;
    commit;

    -------------------------------------------

    create or alter view v_test as select 1 id from rdb$database;
    commit;
    recreate table test
    (
      a integer,
      b date,
      c computed by (extract(day from b)-extract(day from b))
    );
    commit;
    insert into test(a, b) values(1, DATE '2015-05-24');
    insert into test(a, b) values(1, null);
    commit;
    select c from test group by c;
    commit;

    create or alter view v_test as select b-b as dd from test;
    commit;
    select dd from v_test group by dd;
    commit;

    create or alter view v_test as select b-0 as dd from test;
    select dd from v_test group by dd;

    create or alter view v_test
    as select cast(b as timestamp) as dt  from test;
    select dt from v_test group by dt;

    ------------

    create or alter view v_test as select 1 id from rdb$database;
    commit;
    recreate table test(a int, b time, c computed by(cast(b as time)));
    commit;

    insert into test(a, b) values(1, '15:00:29.191');
    insert into test(a, b) values(1, null);
    commit;

    select c from test group by c;
  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    DY                              <null>
    DY                              0
    DY                              1
    
    C                               <null>
    C                               0
    
    DD                              <null>
    DD                              0
    
    DD                              <null>
    DD                              2015-05-24
    
    DT                              <null>
    DT                              2015-05-24 00:00:00.0000
    
    C                               <null>
    C                               15:00:29.1910
  """

@pytest.mark.version('>=2.5')
def test_core_0629_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout

