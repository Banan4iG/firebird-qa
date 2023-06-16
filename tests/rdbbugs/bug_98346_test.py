#coding:utf-8

"""
ID:          RS-98346
ISSUE:       https://http://tracker.red-soft.biz/issues/98346
TITLE:       ISQL does not show comments when displaying database metadata
DESCRIPTION:
"""

import pytest
from firebird.qa import *
from pathlib import Path

init_script = """
    create table TEST(ID int);
    commit;
    comment on table test is 'test commit';
    commit;
"""

db = db_factory(filename='comment.fdb', page_size=8192, init=init_script)

act = python_act('db', substitutions=[("CREATE DATABASE .*comment\\.fdb'", "CREATE DATABASE 'comment.fdb'")])

expected_stdout = """
    SET SQL DIALECT 3;
    
    /* CREATE DATABASE 'comment.fdb' PAGE_SIZE 8192 DEFAULT CHARACTER SET NONE; */

    COMMIT WORK;

    /* Table: TEST, Owner: SYSDBA */
    CREATE TABLE TEST (ID INTEGER);
    
    /* Comments for database objects. */
    COMMENT ON TABLE        TEST IS 'test commit';
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.isql(switches=['-x'])
    assert act.clean_stdout == act.clean_expected_stdout