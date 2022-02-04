#coding:utf-8

"""
ID:          new-database-08
TITLE:       New DB - RDB$FILES
DESCRIPTION: Check for correct content of RDB$FILES in new database.
FBTEST:      functional.basic.db.08
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    set list on;
    set count on;
    select * from rdb$files
    order by
        rdb$file_name
        ,rdb$file_sequence
    ;
"""

act = isql_act('db', test_script)

expected_stdout = """
    Records affected: 0
"""

@pytest.mark.version('>=3')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
