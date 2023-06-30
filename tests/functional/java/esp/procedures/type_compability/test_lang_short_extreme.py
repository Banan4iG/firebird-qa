#coding:utf-8

"""
ID:          java.esp.procedures.type-compability.lang-short-extreme
TITLE:       External procedure call with extreme small and extreme big smallint input parameter
DESCRIPTION: 
FBTEST:      functional.java.esp.procedures.type_compability.lang_short_extreme
"""

import pytest
from firebird.qa import *

init_script = """
CREATE TABLE TEST_TABLE(F_SMALLINT SMALLINT);
commit;

create procedure test(i SMALLINT) 
external name 'esp.TestProcedure.ShortIn(Short)'
engine java;
commit;


"""

db = db_factory(init=init_script)

test_script = """
EXECUTE PROCEDURE TEST(32767);
EXECUTE PROCEDURE TEST(-32768);
commit;


SELECT F_SMALLINT FROM TEST_TABLE;
"""

act = isql_act('db', test_script)

expected_stdout = """
F_SMALLINT
==========
32767
-32768
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
