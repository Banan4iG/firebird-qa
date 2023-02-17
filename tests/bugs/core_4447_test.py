#coding:utf-8

"""
ID:          issue-4767
ISSUE:       4767
TITLE:       Positioned UPDATE statement prohibits index usage for the subsequent cursor field references
DESCRIPTION:
JIRA:        CORE-4447
FBTEST:      bugs.core_4447
"""

import pytest
from firebird.qa import *
from string import Template

init_script = """
  recreate table ts(id int, x int, y int, z int, constraint ts_pk_id primary key (id) );
  recreate table tt(x int, y int, z int, constraint tt_pk_xy primary key (x,y) );
  commit;

  insert into ts
  select row_number()over(), rand()*10, rand()*10, rand()*10
  from rdb$types;
  commit;

  insert into tt select distinct x,y,0 from ts;
  commit;
"""

db = db_factory(init=init_script)

test_script = """
  set planonly;
  set term ^;
  execute block as
  begin
    for select id,x,y,z from ts as cursor c
    do begin
       update ts set id = id where current of c; -- <<<<<<<<<<<<<<< ::: NB ::: we lock record in source using "current of" clause
       update tt t set t.z = t.z + c.z where t.x=c.x and t.y = c.y;
    end
  end
  ^ set term ;^
  set planonly;
"""

act = isql_act('db', test_script, substitutions=[('-- line(:)? \d+, col(umn)?(:)? \d+', '-- line, column')])

expected_stdout_template = """
  $plan_sub
  PLAN (T INDEX (TT_PK_XY))
  $plan_sub
  PLAN (C TS NATURAL)
"""
expected_stdout = Template(expected_stdout_template)
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    plan_sub = '-- line, column' if act.is_version('>4.0') else ''
    act.expected_stdout = expected_stdout.substitute(plan_sub=plan_sub)
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

