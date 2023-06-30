#coding:utf-8

"""
ID:          java.esp.functions.without-parameters.boolean-result
TITLE:       External function call with boolean type of result and without input parameter
DESCRIPTION: 
  External function is declared with SQL types compatible with boolean Java type.
FBTEST:      functional.java.esp.functions.without_parameters.boolean_result
"""

import pytest
from firebird.qa import *

init_script = """
create function test_1() 
returns BOOLEAN
external name 'esp.TestFunction.boolOut()' 
engine java;
commit;

create function test_2() 
returns VARCHAR(10)
external name 'esp.TestFunction.boolOut()' 
engine java;
commit;


create function test_3() 
returns CHAR(10)
external name 'esp.TestFunction.boolOut()' 
engine java;
commit;

create function test_4() 
returns BLOB
external name 'esp.TestFunction.boolOut()' 
engine java;
commit;

"""

db = db_factory(init=init_script)

test_script = """
SELECT TEST_1() FROM RDB$DATABASE;

SELECT TEST_2() FROM RDB$DATABASE;

SELECT TEST_3() FROM RDB$DATABASE;

SELECT cast(TEST_4() as varchar(10)) as "TEST_4" FROM RDB$DATABASE;
"""

act = isql_act('db', test_script)

expected_stdout = """        
TEST_1
=======
<false>
TEST_2
==========
FALSE
TEST_3
==========
FALSE
TEST_4
==========
FALSE
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
