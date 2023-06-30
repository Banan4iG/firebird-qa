#coding:utf-8

"""
ID:          java.esp.procedures.type-compability.lang-boolean
TITLE:       External procedure call with java.lang.Boolean  type of input parameter
DESCRIPTION: 
  External procedure is declared with SQL types compatible with java.lang.Boolean  Java type. Parameter as a constant.
FBTEST:      functional.java.esp.procedures.type_compability.lang_boolean
"""

import pytest
from firebird.qa import *

init_script = """
CREATE TABLE TEST_TABLE(F BOOLEAN);
commit;

create procedure test_1(i BOOLEAN) 
external name 'esp.TestProcedure.BooleanIn(Boolean)'
engine java;
commit;

create procedure test_2(i CHAR(10)) 
external name 'esp.TestProcedure.BooleanIn(Boolean)'
engine java;
commit;

create procedure test_3(i VARCHAR(10)) 
external name 'esp.TestProcedure.BooleanIn(Boolean)'
engine java;
commit;

create procedure test_4(i BLOB) 
external name 'esp.TestProcedure.BooleanIn(Boolean)'
engine java;
commit;

"""

db = db_factory(init=init_script)

test_script = """
 
EXECUTE PROCEDURE TEST_1(true);
EXECUTE PROCEDURE TEST_1(false);
EXECUTE PROCEDURE TEST_1(unknown);
EXECUTE PROCEDURE TEST_1(null);

EXECUTE PROCEDURE TEST_2('true');
EXECUTE PROCEDURE TEST_2('false');
EXECUTE PROCEDURE TEST_2(unknown);
EXECUTE PROCEDURE TEST_2(null);

EXECUTE PROCEDURE TEST_3('true');
EXECUTE PROCEDURE TEST_3('false');
EXECUTE PROCEDURE TEST_3(unknown);
EXECUTE PROCEDURE TEST_3(null);

EXECUTE PROCEDURE TEST_4('true');
EXECUTE PROCEDURE TEST_4('false');
EXECUTE PROCEDURE TEST_4(unknown);
EXECUTE PROCEDURE TEST_4(null);


commit;

SELECT F FROM TEST_TABLE;
"""

act = isql_act('db', test_script)

expected_stdout = """
	
F
=======
<true>
<false>
<null>
<null>
<true>
<false>
<null>
<null>
<true>
<false>
<null>
<null>
<true>
<false>
<null>
<null>
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
