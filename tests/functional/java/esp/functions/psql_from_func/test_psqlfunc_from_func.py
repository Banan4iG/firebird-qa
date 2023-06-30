#coding:utf-8

"""
ID:          java.esp.functions.psql-from-func.psqlfunc-from-func
TITLE:       PSQL function call from external function
DESCRIPTION: 
FBTEST:      functional.java.esp.functions.psql_from_func.psqlfunc_from_func
"""

import pytest
from firebird.qa import *

init_script = """

SET TERM ^ ;
CREATE FUNCTION TEST(i bigint)
returns bigint
AS
BEGIN
    return i;
END^
SET TERM ; ^
commit;

CREATE FUNCTION MAINTEST(B BIGINT)
RETURNS BIGINT
EXTERNAL NAME 'esp.TestFunction.callFuncFromFunc(Long)' 
ENGINE JAVA;
commit;
"""

db = db_factory(init=init_script)

test_script = """
 
SELECT MAINTEST(10000000) FROM rdb$database;
commit;
"""

act = isql_act('db', test_script)

expected_stdout = """             
MAINTEST
=====================
10000000
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
