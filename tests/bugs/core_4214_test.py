#coding:utf-8

"""
ID:          issue-4539
ISSUE:       4539
TITLE:       GTT should not reference permanent relation
DESCRIPTION:
JIRA:        CORE-4214
FBTEST:      bugs.core_4214
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    set autoddl off;
    commit;
    create global temporary table gtt_main(x int, y int, constraint gtt_main_unq unique(x,y) using index gtt_main_unq);
    create table fix_main(x int, y int, constraint fix_main_unq unique(x,y) using index fix_main_unq);
    create global temporary table gtt_detl(x int, y int,
      constraint gtt_detl_fk_to_gtt foreign key(x,y) references gtt_main(x, y),
      constraint gtt_detl_fk_to_fix foreign key(x,y) references fix_main(x, y)
    );
    create table fix_detl(x int, y int,
      constraint fix_detl_fk_to_fix foreign key(x,y) references fix_main(x, y),
      constraint fix_detl_fk_to_gtt foreign key(x,y) references gtt_main(x, y)
    );
"""

act = isql_act('db', test_script)

expected_stderr = """
    Statement failed, SQLSTATE = HY000
    unsuccessful metadata update
    -CREATE TABLE GTT_DETL failed
    -global temporary table "GTT_DETL" of type ON COMMIT DELETE ROWS cannot reference persistent table "FIX_MAIN"
    Statement failed, SQLSTATE = HY000
    unsuccessful metadata update
    -CREATE TABLE FIX_DETL failed
    -persistent table "FIX_DETL" cannot reference global temporary table "GTT_MAIN" of type ON COMMIT DELETE ROWS
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stderr = expected_stderr
    act.execute()
    assert act.clean_stderr == act.clean_expected_stderr
