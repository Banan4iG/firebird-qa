#coding:utf-8
#
# id:           functional.trigger.create.08
# title:        CREATE TRIGGER AFTER DELETE POSITION 12
# decription:   CREATE TRIGGER AFTER DELETE POSITION 12
#               
#               Dependencies:
#               CREATE DATABASE
#               CREATE TABLE
# tracker_id:   
# min_versions: []
# versions:     2.0
# qmid:         functional.trigger.create.create_trigger_08

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 2.0
# resources: None

substitutions_1 = [('\\+.*', ''), ('\\=.*', ''), ('Trigger text.*', '')]

init_script_1 = """CREATE TABLE tb(id INT);"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """SET TERM ^;
CREATE TRIGGER test FOR tb AFTER DELETE POSITION 12 AS
BEGIN
END^
SET TERM ;^
SHOW TRIGGER test;"""

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """Triggers on Table TB:
TEST, Sequence: 12, Type: AFTER DELETE, Active
AS
BEGIN
END
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""

@pytest.mark.version('>=2.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_stdout == act_1.clean_expected_stdout

