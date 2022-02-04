#coding:utf-8

"""
ID:          fkey.primary.insert-13
FBTEST:      functional.fkey.primary.insert_pk_13
TITLE:       Check correct work fix with foreign key
DESCRIPTION:
  Check foreign key work.
  Master transaction deletes record from master_table without commit.
  Detail transaction inserts record in detail_table
  Expected: error primary key field in master_table has been changed.
"""

import pytest
from firebird.qa import *

init_script = """
    recreate table t_detl(id int);
    commit;
    recreate table t_main(
         id int constraint t_main_pk primary key using index t_main_pk
    );
    commit;
    recreate table t_detl(
        id int constraint t_detl_pk primary key using index t_detl_pk,
        master_pk_id int constraint fk_tdetl_tmain references t_main(id) using index fk_tdetl_tmain
    );
    commit;
    insert into t_main(id) values(1);
    commit;
  """

db = db_factory(init=init_script)

test_script = """
    commit;
    set transaction no wait;
    set term ^;
    execute block as
    begin
        delete from t_main where id = 1;
        in autonomous transaction do
        insert into t_detl(id, master_pk_id) values(100, 1);
    end
    ^
    set term ;^
"""

act = isql_act('db', test_script, substitutions=[('-At block line: [\\d]+, col: [\\d]+',
                                                  '-At block line')])

expected_stderr = """
    Statement failed, SQLSTATE = 23000
    violation of FOREIGN KEY constraint "FK_TDETL_TMAIN" on table "T_DETL"
    -Foreign key reference target does not exist
    -Problematic key value is ("MASTER_PK_ID" = 1)
    -At block line: 5, col: 9
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stderr = expected_stderr
    act.execute()
    assert act.clean_stderr == act.clean_expected_stderr
