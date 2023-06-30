#coding:utf-8

"""
ID:          java.esp.procedures.type-compability.with-output-params.byte
TITLE:       External procedure call with byte[] type of input and output parameter
DESCRIPTION: 
  External procedure is declared with SQL types compatible with byte[] Java type. Parameter as a constant.
FBTEST:      functional.java.esp.procedures.type_compability.with_output_params.byte
"""

import pytest
from firebird.qa import *

init_script = """

create procedure test_1(i CHAR(10)) 
returns(o CHAR(10))
external name 'esp.TestProcedure.byteInOut(byte[], byte[][])'
engine java;
commit;

create procedure test_2(i VARCHAR(10)) 
returns(o VARCHAR(10))
external name 'esp.TestProcedure.byteInOut(byte[], byte[][])'
engine java;
commit;

create procedure test_3(i BLOB) 
returns(o BLOB)
external name 'esp.TestProcedure.byteInOut(byte[], byte[][])'
engine java;
commit;

"""

db = db_factory(init=init_script)

test_script = """
set list on;
 
EXECUTE PROCEDURE TEST_1('char');
EXECUTE PROCEDURE TEST_1(null);
EXECUTE PROCEDURE TEST_2('varchar');
EXECUTE PROCEDURE TEST_2(null);
select cast(o as varchar(100)) from TEST_3('blob');
select cast(o as varchar(100)) from TEST_3(null);

commit;


"""

act = isql_act('db', test_script)

expected_stdout = """
	
O                               char
O                               <null>
O                               varchar
O                               <null>
CAST                            blob
CAST                            <null>
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
