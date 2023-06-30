#coding:utf-8

"""
ID:          java.esp.procedures.other.get-inout-param
TITLE:       Procedure sets output parameter values
DESCRIPTION: 
FBTEST:      functional.java.esp.procedures.other.get_inout_param
"""

import pytest
from firebird.qa import *

init_script = """


CREATE OR ALTER PROCEDURE TEST(i integer, i1 varchar(100))
returns(o varchar(23))
EXTERNAL NAME 'esp.TestContext.getInOutParam(Object, Object, String[])' 
ENGINE JAVA;
commit;
"""

db = db_factory(init=init_script)

test_script = """
EXECUTE PROCEDURE TEST(23, 'fdgh');
commit;

"""

act = isql_act('db', test_script)

expected_stdout = """
O
=======================
23, fdgh / b
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
