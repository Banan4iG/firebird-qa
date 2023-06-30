#coding:utf-8

"""
ID:          java.esp.procedures.type-compability.byte
TITLE:       External procedure call with byte[] type of input parameter
DESCRIPTION: 
  External procedure is declared with SQL types compatible with byte[] Java type. Parameter as a constant.
FBTEST:      functional.java.esp.procedures.type_compability.byte
"""

import pytest
from firebird.qa import *

init_script = """
CREATE TABLE TEST_TABLE(F varchar(20));
commit;


create procedure test_1(i CHAR(10)) 
external name 'esp.TestProcedure.byteIn(byte[])'
engine java;
commit;

create procedure test_2(i VARCHAR(10)) 
external name 'esp.TestProcedure.byteIn(byte[])'
engine java;
commit;

create procedure test_3(i BLOB) 
external name 'esp.TestProcedure.byteIn(byte[])'
engine java;
commit;

"""

db = db_factory(init=init_script)

test_script = """
 
EXECUTE PROCEDURE TEST_1('char');
EXECUTE PROCEDURE TEST_1(null);
EXECUTE PROCEDURE TEST_2('varchar');
EXECUTE PROCEDURE TEST_2(null);
EXECUTE PROCEDURE TEST_3('blob');
EXECUTE PROCEDURE TEST_3(null);
commit;

SELECT F FROM TEST_TABLE;
"""

act = isql_act('db', test_script)

expected_stdout = """
	
F
====================
char
<null>
varchar
<null>
blob
<null>
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
