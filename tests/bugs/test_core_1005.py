#coding:utf-8
#
# id:           bugs.core_1005
# title:        DISTINCT vs NULLS LAST clause: wrong order of NULLs
# decription:   
# tracker_id:   CORE-1005
# min_versions: []
# versions:     2.0.1
# qmid:         bugs.core_1005

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 2.0.1
# resources: None

substitutions_1 = []

init_script_1 = """create table T (A int, B int) ;
commit ;

insert into T values (1,1);
insert into T values (1,1);
insert into T values (2,2);
insert into T values (3,3);
insert into T values (null,null);
insert into T values (null,null);
insert into T values (4,4);
commit ;
"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """select distinct A, B from T order by A nulls last, B nulls last ;
select distinct A, B from T order by A nulls last ;
select distinct A, B from T order by B nulls last ;
"""

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """A            B
============ ============
           1            1
           2            2
           3            3
           4            4
      <null>       <null>

A            B
============ ============
           1            1
           2            2
           3            3
           4            4
      <null>       <null>

A            B
============ ============
           1            1
           2            2
           3            3
           4            4
      <null>       <null>

"""

@pytest.mark.version('>=2.0.1')
def test_core_1005_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout

