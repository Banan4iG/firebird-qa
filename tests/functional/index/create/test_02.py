#coding:utf-8

"""
ID:          index.create-02
TITLE:       CREATE UNIQUE INDEX
DESCRIPTION:
FBTEST:      functional.index.create.02
"""

import pytest
from firebird.qa import *

init_script = """CREATE TABLE t( a INTEGER);
commit;
"""

db = db_factory(init=init_script)

test_script = """CREATE UNIQUE INDEX test ON t(a);
SHOW INDEX test;"""

act = isql_act('db', test_script)

expected_stdout = """TEST UNIQUE INDEX ON T(A)"""

@pytest.mark.version('>=3')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
