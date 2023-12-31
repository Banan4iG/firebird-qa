#coding:utf-8

"""
ID:          issue-5403
ISSUE:       5403
TITLE:       Support autocommit mode in SET TRANSACTION statement
DESCRIPTION:
  Test starts transaction by issuing ISQL command with 'auto commit' clause and check then
  whether transaction data are written in the table, despite of final rollback.
JIRA:        CORE-5119
FBTEST:      bugs.core_5119
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    --  Checked on: 4.0.0.32371
    recreate table test(id int generated by default as identity, tx int default current_transaction);
    commit;
    set transaction auto commit;
    insert into test default values;
    insert into test default values;
    insert into test default values;
    rollback;
    set count on;
    set list on;
    select id, rank()over(order by tx) tx from test;
"""

act = isql_act('db', test_script)

expected_stdout = """
    ID                              1
    TX                              1
    ID                              2
    TX                              2
    ID                              3
    TX                              3
    Records affected: 3
"""

@pytest.mark.version('>=4.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

