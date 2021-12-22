#coding:utf-8
#
# id:           functional.index.alter.04
# title:        ALTER INDEX - INACTIVE PRIMARY KEY
# decription:   ALTER INDEX - INACTIVE PRIMARY KEY
#               
#               Dependencies:
#               CREATE DATABASE
#               CREATE TABLE with PRIMARY KEY
# tracker_id:   
# min_versions: []
# versions:     3.0
# qmid:         functional.index.alter.alter_index_04

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 3.0
# resources: None

substitutions_1 = []

init_script_1 = """CREATE TABLE t( a INTEGER NOT NULL,
                CONSTRAINT pkindx PRIMARY KEY(a)
              );
commit;"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """ALTER INDEX pkindx INACTIVE;"""

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stderr_1 = """Statement failed, SQLSTATE = 27000
unsuccessful metadata update
-ALTER INDEX PKINDX failed
-action cancelled by trigger (3) to preserve data integrity
-Cannot deactivate index used by a PRIMARY/UNIQUE constraint
"""

@pytest.mark.version('>=3.0')
def test_1(act_1: Action):
    act_1.expected_stderr = expected_stderr_1
    act_1.execute()
    assert act_1.clean_stderr == act_1.clean_expected_stderr

