#coding:utf-8

"""
ID:          java.esp.procedures.other.noparams
TITLE:       External procedure call without params
DESCRIPTION: 
FBTEST:      functional.java.esp.procedures.other.noparams
"""

import pytest
from firebird.qa import *

init_script = """
CREATE TABLE TEST_TABLE (F_CHAR CHAR(5));
commit;

CREATE OR ALTER PROCEDURE TEST
EXTERNAL NAME 'esp.TestProcedure.procWithoutParam()' 
ENGINE JAVA;
commit;
"""

db = db_factory(init=init_script)

test_script = """
EXECUTE PROCEDURE TEST;
commit;

SELECT F_CHAR FROM TEST_TABLE;
"""

act = isql_act('db', test_script)

expected_stdout = """
F_CHAR
======
test
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
