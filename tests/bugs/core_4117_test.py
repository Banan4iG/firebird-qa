#coding:utf-8

"""
ID:          issue-4445
ISSUE:       4445
TITLE:       COMPUTED BY field is evaluated as NULL if used as an exception parameter directly
DESCRIPTION:
  Exception with computed by field as parameter produces error message without this field
  value if this field is not a part of excpression
JIRA:        CORE-4117
FBTEST:      bugs.core_4117
"""

import pytest
from firebird.qa import *

init_script = """
    recreate table test1 (id int not null, c computed by (id * 10));
    recreate table test2 (id int not null, c computed by (id * 10));
    commit;

    set term ^;
    execute block as
    begin
      begin
      execute statement 'drop exception ex_bad_computed_field_value';
      when any do begin end
      end
    end
    ^
    set term ;^
    commit;

    create exception ex_bad_computed_field_value '';
    commit;
    insert into test1 (id) values (1);
    insert into test2 (id) values (1);
    commit;

    -- 1. exception with computed by field as parameter
    set term ^;
    create or alter trigger test1_bu for test1 active before update position 0 as
    begin
      exception ex_bad_computed_field_value new.c;
    end
    ^
    set term ;^
    commit;

    -- 2. exception with computed by field as a part of expression
    set term ^;
    create or alter trigger test2_bu for test2 active before update position 0 as
    begin
      exception ex_bad_computed_field_value new.c + 0; -- any expression
    end
    ^
    set term ;^
    commit;

    -- Confirmed on 2.5.2: statement update test1 ... will raise exception WITHOUT value:
    -- Statement failed, SQLSTATE = 42000
    -- exception 1
    -- -EX_BAD_COMPUTED_FIELD_VALUE
    -- -At trigger 'TEST1_BU' line: 3, col: 7

    -- Compare with 2.5.5:
    -- Statement failed, SQLSTATE = 42000
    -- exception 2
    -- -EX_BAD_COMPUTED_FIELD_VALUE
    -- -20 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< this is added here <<<<<<<<<<<<<
    -- -At trigger 'TEST1_BU' line: 3, col: 7

"""

db = db_factory(init=init_script)

test_script = """
    update test1 set id = 2;
    update test2 set id = 2;
"""

act = isql_act('db', test_script, substitutions=[('line: [0-9]+, col: [0-9]+', '')])

expected_stderr = """
    Statement failed, SQLSTATE = HY000
    exception 1
    -EX_BAD_COMPUTED_FIELD_VALUE
    -20
    -At trigger 'TEST1_BU' line: 3, col: 7
    Statement failed, SQLSTATE = HY000
    exception 1
    -EX_BAD_COMPUTED_FIELD_VALUE
    -20
    -At trigger 'TEST2_BU' line: 3, col: 7
"""

@pytest.mark.version('>=3')
def test_1(act: Action):
    act.expected_stderr = expected_stderr
    act.execute()
    assert act.clean_stderr == act.clean_expected_stderr

