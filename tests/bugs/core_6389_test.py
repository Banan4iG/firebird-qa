#coding:utf-8

"""
ID:          issue-2352
ISSUE:       2352
TITLE:       Using binary string literal to assign to user-defined blob sub-types yield
  conversion error "filter not found to convert type 1 to type -13"
DESCRIPTION:
JIRA:        CORE-6389
FBTEST:      bugs.core_6389
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    recreate table blob13(id integer generated by default as identity primary key, blobfield blob sub_type -13);
    commit;
    -- This must pass w/o errors:
    insert into blob13 (blobfield) values (x'ab01');
"""

act = isql_act('db', test_script)

@pytest.mark.version('>=4.0')
def test_1(act: Action):
    act.execute()
