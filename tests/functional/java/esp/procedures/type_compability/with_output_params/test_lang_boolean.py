#coding:utf-8

"""
ID:          java.esp.procedures.type-compability.with-output-params.lang-boolean
TITLE:       External procedure call with java.lang.Boolean  type of input and output parameter
DESCRIPTION: 
  External procedure is declared with SQL types compatible with java.lang.Boolean  Java type. Parameter as a constant.
FBTEST:      functional.java.esp.procedures.type_compability.with_output_params.lang_boolean
"""

import pytest
from firebird.qa import *

init_script = """

create procedure test_1(i BOOLEAN) 
returns(o BOOLEAN)
external name 'esp.TestProcedure.BooleanInOut(Boolean, Boolean[])'
engine java;
commit;

create procedure test_2(i CHAR(10)) 
returns(o CHAR(10))
external name 'esp.TestProcedure.BooleanInOut(Boolean, Boolean[])'
engine java;
commit;

create procedure test_3(i VARCHAR(10)) 
returns(o VARCHAR(10))
external name 'esp.TestProcedure.BooleanInOut(Boolean, Boolean[])'
engine java;
commit;

create procedure test_4(i BLOB) 
returns(o BLOB)
external name 'esp.TestProcedure.BooleanInOut(Boolean, Boolean[])'
engine java;
commit;

"""

db = db_factory(init=init_script)

test_script = """
set list on; 
 
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

select cast(o as varchar(100)) from TEST_4('true');
select cast(o as varchar(100)) from TEST_4('false');
select cast(o as varchar(100)) from TEST_4(unknown);
select cast(o as varchar(100)) from TEST_4(null);

commit;

"""

act = isql_act('db', test_script)

expected_stdout = """
O                               <true>
O                               <false>
O                               <null>
O                               <null>
O                               TRUE
O                               FALSE
O                               <null>
O                               <null>
O                               TRUE
O                               FALSE
O                               <null>
O                               <null>
CAST                            TRUE
CAST                            FALSE
CAST                            <null>
CAST                            <null>
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
