#coding:utf-8

"""
ID:          java.esp.procedures.other.empty
TITLE:       Call empty external procedure without params
DESCRIPTION: 
FBTEST:      functional.java.esp.procedures.other.empty
"""

import pytest
from firebird.qa import *

init_script = """

CREATE PROCEDURE TEST
EXTERNAL NAME 'esp.TestProcedure.emptyProcedure()' 
ENGINE JAVA;
commit;
"""

db = db_factory(init=init_script)

test_script = """
EXECUTE PROCEDURE TEST;
commit;

"""

act = isql_act('db', test_script)

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.execute()
