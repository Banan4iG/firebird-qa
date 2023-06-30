#coding:utf-8

"""
ID:          java.esp.procedures.other.emptywithinputparam
TITLE:       Call empty external procedure with input param
DESCRIPTION: 
FBTEST:      functional.java.esp.procedures.other.emptywithinputparam
"""

import pytest
from firebird.qa import *

init_script = """

CREATE PROCEDURE TEST(i integer)
EXTERNAL NAME 'esp.TestProcedure.emptyProcedureWithInParam(int)' 
ENGINE JAVA;
commit;
"""

db = db_factory(init=init_script)

test_script = """
EXECUTE PROCEDURE TEST(10);
commit;

"""

act = isql_act('db', test_script)

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.execute()
