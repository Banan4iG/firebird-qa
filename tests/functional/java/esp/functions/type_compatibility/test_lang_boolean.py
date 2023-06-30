#coding:utf-8

"""
ID:          java.esp.functions.type-compatibility.lang-boolean
TITLE:       External function call with java.lang.Boolean type of result and input parameter
DESCRIPTION: 
  External function is declared with SQL types compatible with java.lang.Boolean Java type. Parameter as a constant.
FBTEST:      functional.java.esp.functions.type_compatibility.lang_boolean
"""

import pytest
from firebird.qa import *

init_script = """
create function test_1(i boolean) 
returns boolean
external name 'esp.TestFunction.BoolInOut(Boolean)' 
engine java;
commit;

create function test_2(i varchar(10)) 
returns varchar(10)
external name 'esp.TestFunction.BoolInOut(Boolean)' 
engine java;
commit;


create function test_3(i char(10)) 
returns char(10)
external name 'esp.TestFunction.BoolInOut(Boolean)' 
engine java;
commit;

create function test_4(i blob) 
returns blob
external name 'esp.TestFunction.BoolInOut(Boolean)' 
engine java;
commit;

"""

db = db_factory(init=init_script)

test_script = """
SELECT TEST_1(true) FROM RDB$DATABASE;
SELECT TEST_1(false) FROM RDB$DATABASE;
SELECT TEST_1(unknown) FROM RDB$DATABASE;
SELECT TEST_1(null) FROM RDB$DATABASE;

SELECT TEST_2('true') FROM RDB$DATABASE;
SELECT TEST_2('false') FROM RDB$DATABASE;
SELECT TEST_2(unknown) FROM RDB$DATABASE;
SELECT TEST_2(null) FROM RDB$DATABASE;

SELECT TEST_3('true') FROM RDB$DATABASE;
SELECT TEST_3('false') FROM RDB$DATABASE;
SELECT TEST_3(unknown) FROM RDB$DATABASE;
SELECT TEST_3(null) FROM RDB$DATABASE;

SELECT cast(TEST_4('true') as varchar(10)) as "TEST_4" FROM RDB$DATABASE;
SELECT cast(TEST_4('false') as varchar(10)) as "TEST_4" FROM RDB$DATABASE;
SELECT TEST_4(unknown) FROM RDB$DATABASE;
SELECT TEST_4(null) FROM RDB$DATABASE;
"""

act = isql_act('db', test_script)

expected_stdout = """        
TEST_1
=======
<true>
TEST_1
=======
<false>
TEST_1
=======
<null>
TEST_1
=======
<null>

TEST_2
==========
TRUE
TEST_2
==========
FALSE
TEST_2
==========
<null>
TEST_2
==========
<null>

TEST_3
==========
TRUE
TEST_3
==========
FALSE
TEST_3
==========
<null>
TEST_3
==========
<null>

TEST_4
==========
TRUE
TEST_4
==========
FALSE
TEST_4
=================
<null>
TEST_4
=================
<null>
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
