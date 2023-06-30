#coding:utf-8

"""
ID:          java.esp.procedures.type-compability.lang-long-extreme
TITLE:       External procedure call with extreme small and extreme big bigint input parameter
DESCRIPTION: 
FBTEST:      functional.java.esp.procedures.type_compability.lang_long_extreme
"""

import pytest
from firebird.qa import *

init_script = """
CREATE TABLE TEST_TABLE (F_BIGINT BIGINT);
commit;


create procedure test(i BIGINT) 
external name 'esp.TestProcedure.LongIn(Long)'
engine java;
commit;

"""

db = db_factory(init=init_script)

test_script = """
EXECUTE PROCEDURE TEST(-9223372036854775808);
EXECUTE PROCEDURE TEST(9223372036854775807);
commit;


SELECT F_BIGINT FROM TEST_TABLE;
"""

act = isql_act('db', test_script)

expected_stdout = """ 
F_BIGINT
=====================
-9223372036854775808
9223372036854775807

"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
