#coding:utf-8

"""
ID:          issue-1797
ISSUE:       1797
TITLE:       Invalid parameter type when using it in CHAR_LENGTH function
DESCRIPTION:
JIRA:        CORE-1379
FBTEST:      bugs.core_1379
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
set list on;
    set term ^;
    execute block returns(r int) as
		declare c varchar(1) = '';
    begin
        execute statement ('select 1 from rdb$database where char_length(?) = 1') (1) into r;
        suspend;
		execute statement ('select 1 from rdb$database where char_length(?) = 0') ('') into r;
        suspend;
		execute statement ('select 1 from rdb$database where char_length(?) = 0') (c) into r;
        suspend;
    end
    ^
    set term ;^
"""

act = isql_act('db', test_script, substitutions=[('-At block line: [\\d]+, col: [\\d]+', '-At block line')])

expected_stdout = """
R                               1
R                               1
R                               1
"""

@pytest.mark.version('>=3')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

