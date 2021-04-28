#coding:utf-8
#
# id:           functional.intfunc.cast.16
# title:        CAST DATE -> VARCHAR
# decription:   CAST DATE -> VARCHAR
#               Be careful about time format on FB server !
#               Universal format is not defined or not documented.
#               
#               Dependencies:
#               CREATE DATABASE
#               CAST CHAR -> DATE
#               Basic SELECT
# tracker_id:   
# min_versions: []
# versions:     1.0
# qmid:         functional.intfunc.cast.cast_16

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 1.0
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """SELECT CAST(CAST('10.2.1973' AS DATE) AS VARCHAR(40)) FROM rdb$Database;"""

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """CAST
========================================

1973-02-10"""

@pytest.mark.version('>=1.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout

