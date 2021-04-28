#coding:utf-8
#
# id:           functional.intfunc.cast.05
# title:        CAST Numeric -> Numeric (Round up)
# decription:   CAST Numeric -> Numeric
#               Round up
#               
#               Dependencies:
#               CREATE DATABASE
#               Basic SELECT
# tracker_id:   
# min_versions: []
# versions:     1.0
# qmid:         functional.intfunc.cast.cast_05

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 1.0
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """SELECT CAST(1.25001 AS NUMERIC(2,1)) FROM rdb$Database;"""

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """   CAST
=======

    1.3
"""

@pytest.mark.version('>=1.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout

