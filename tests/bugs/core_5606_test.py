#coding:utf-8

"""
ID:          issue-5872
ISSUE:       5872
TITLE:       Add expression index name to exception message if computation failed
DESCRIPTION:
NOTES:
[24.08.2020]
  changed sequence of actions: one statement must violate requirements of only ONE index.
  Before this statement:
    insert into test(id, x, y, s) values( 4, 3, -7, 'qwerty' );
  -- did violate TWO indices: test_eval3 and test_eval5.
  The order of which of them will raise first is undefined, so this test could fail because of appearance
  "wrong" index name in its STDERR. Detected on 4.0.0.2173. Discussed with hvlad, letter 23.08.2020 16:58.
JIRA:        CORE-5606
FBTEST:      bugs.core_5606
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    recreate table test(
      id int
      ,x int
      ,y int
      ,r double precision
      ,s varchar(12) default 'DB_NAME'
    );
    create index test_eval1 on test computed by ( x/id );
    insert into test(id, x) values(0, 1);
    rollback;
    drop index test_eval1;

    create index test_eval2 on test computed by ( log10(r-15) );
    insert into test(id, r) values(1, 12);
    rollback;
    drop index test_eval2;

    create index test_eval3 on test computed by ( rdb$get_context('SYSTEM', s ) );
    insert into test(id, s) values(2, 'FOO_&_BAR');
    rollback;
    drop index test_eval3;

    create index test_eval4 on test computed by ( mod(x , (y-x) ) );
    insert into test(id, x, y) values(3, 10, 10);
    rollback;
    drop index test_eval4;

    create index test_eval5 on test computed by ( substring(s from x for id+y)  );
    insert into test(id, x, y, s) values( 4, 3, -7, 'qwerty' );
    drop index test_eval5;

    set count on;
    set list on;
    select id, s from test;
"""

act = isql_act('db', test_script)

expected_stdout = """
    Records affected: 0
"""

expected_stderr = """
    Statement failed, SQLSTATE = 22012
    Expression evaluation error for index "TEST_EVAL1" on table "TEST"
    -arithmetic exception, numeric overflow, or string truncation
    -Integer divide by zero.  The code attempted to divide an integer value by an integer divisor of zero.

    Statement failed, SQLSTATE = 42000
    Expression evaluation error for index "TEST_EVAL2" on table "TEST"
    -expression evaluation not supported
    -Argument for LOG10 must be positive

    Statement failed, SQLSTATE = 42000
    unsuccessful metadata update
    -key size exceeds implementation restriction for index "TEST_EVAL3"
    Statement failed, SQLSTATE = 42000
    unsuccessful metadata update
    -DROP INDEX TEST_EVAL3 failed
    -Index not found

    Statement failed, SQLSTATE = 22012
    Expression evaluation error for index "TEST_EVAL4" on table "TEST"
    -arithmetic exception, numeric overflow, or string truncation
    -Integer divide by zero.  The code attempted to divide an integer value by an integer divisor of zero.

    Statement failed, SQLSTATE = 22011
    Expression evaluation error for index "TEST_EVAL5" on table "TEST"
    -Invalid length parameter -3 to SUBSTRING. Negative integers are not allowed.
"""

@pytest.mark.version('>=4.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.expected_stderr = expected_stderr
    act.execute()
    assert (act.clean_stderr == act.clean_expected_stderr and
            act.clean_stdout == act.clean_expected_stdout)
