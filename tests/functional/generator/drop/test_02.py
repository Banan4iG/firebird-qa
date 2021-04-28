#coding:utf-8
#
# id:           functional.generator.drop.02
# title:        DROP GENERATOR - in use
# decription:   DROP GENERATOR
#               
#               Dependencies:
#               CREATE DATABASE
#               CREATE GENERATOR
#               CREATE PROCEDURE
# tracker_id:   
# min_versions: []
# versions:     2.5.0
# qmid:         functional.generator.drop.drop_generator_02

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 2.5.0
# resources: None

substitutions_1 = []

init_script_1 = """CREATE GENERATOR test;
SET TERM ^;
CREATE PROCEDURE a AS
DECLARE VARIABLE id INT;
BEGIN
  id=GEN_ID(test,1);
END ^
SET TERM ;^
commit;"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """DROP GENERATOR test;"""

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stderr_1 = """Statement failed, SQLSTATE = 42000

unsuccessful metadata update
-cannot delete
-GENERATOR TEST
-there are 1 dependencies
"""

@pytest.mark.version('>=2.5.0')
def test_1(act_1: Action):
    act_1.expected_stderr = expected_stderr_1
    act_1.execute()
    assert act_1.clean_expected_stderr == act_1.clean_stderr

