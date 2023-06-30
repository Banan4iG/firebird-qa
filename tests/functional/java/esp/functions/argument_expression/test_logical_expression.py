#coding:utf-8

"""
ID:          java.esp.functions.argument-expression.logical-expression
TITLE:       External function call with input parameter as an logical expression
DESCRIPTION: 
FBTEST:      functional.java.esp.functions.argument_expression.logical_expression
"""

import pytest
from firebird.qa import *

init_script = """
create function test_1(i boolean) 
returns boolean
external name 'esp.TestFunction.boolInOut(boolean)' 
engine java;
commit;

create function test_2(i boolean) 
returns boolean
external name 'esp.TestFunction.BoolInOut(Boolean)' 
engine java;
commit;



"""

db = db_factory(init=init_script)

test_script = """
SELECT TEST_1(false and false) FROM RDB$DATABASE;
SELECT TEST_1(1>2 and 1!=1) FROM RDB$DATABASE;

SELECT TEST_1(false and true) FROM RDB$DATABASE;
SELECT TEST_1(10<5 and 1=1) FROM RDB$DATABASE;

SELECT TEST_1(true and true) FROM RDB$DATABASE;
SELECT TEST_1(2!=1 and 2>1) FROM RDB$DATABASE;

SELECT TEST_1(false or false) FROM RDB$DATABASE;
SELECT TEST_1(1>2 or 1!=1) FROM RDB$DATABASE;

SELECT TEST_1(false or true) FROM RDB$DATABASE;
SELECT TEST_1(10<5 or 1=1) FROM RDB$DATABASE;

SELECT TEST_1(true or true) FROM RDB$DATABASE;
SELECT TEST_1(2!=1 or 2>1) FROM RDB$DATABASE;

SELECT TEST_1(not false) FROM RDB$DATABASE;
SELECT TEST_1(not 2<1) FROM RDB$DATABASE;

SELECT TEST_1(not true) FROM RDB$DATABASE;
SELECT TEST_1(not 2>1) FROM RDB$DATABASE;

SELECT TEST_1(false and unknown) FROM RDB$DATABASE;
SELECT TEST_1(3>1 and null) FROM RDB$DATABASE;

SELECT TEST_1(true or unknown) FROM RDB$DATABASE;
SELECT TEST_1(3<10 or null) FROM RDB$DATABASE;

SELECT TEST_1(not unknown) FROM RDB$DATABASE;
SELECT TEST_1(not null) FROM RDB$DATABASE;


SELECT TEST_2(false and false) FROM RDB$DATABASE;
SELECT TEST_2(1>2 and 1!=1) FROM RDB$DATABASE;

SELECT TEST_2(false and true) FROM RDB$DATABASE;
SELECT TEST_2(10<5 and 1=1) FROM RDB$DATABASE;

SELECT TEST_2(true and true) FROM RDB$DATABASE;
SELECT TEST_2(2!=1 and 2>1) FROM RDB$DATABASE;

SELECT TEST_2(false or false) FROM RDB$DATABASE;
SELECT TEST_2(1>2 or 1!=1) FROM RDB$DATABASE;

SELECT TEST_2(false or true) FROM RDB$DATABASE;
SELECT TEST_2(10<5 or 1=1) FROM RDB$DATABASE;

SELECT TEST_2(true or true) FROM RDB$DATABASE;
SELECT TEST_2(2!=1 or 2>1) FROM RDB$DATABASE;

SELECT TEST_2(not false) FROM RDB$DATABASE;
SELECT TEST_2(not 2<1) FROM RDB$DATABASE;

SELECT TEST_2(not true) FROM RDB$DATABASE;
SELECT TEST_2(not 2>1) FROM RDB$DATABASE;

SELECT TEST_2(false and unknown) FROM RDB$DATABASE;
SELECT TEST_2(3>1 and null) FROM RDB$DATABASE;

SELECT TEST_2(true or unknown) FROM RDB$DATABASE;
SELECT TEST_2(3<10 or null) FROM RDB$DATABASE;

SELECT TEST_2(not unknown) FROM RDB$DATABASE;
SELECT TEST_2(not null) FROM RDB$DATABASE;

"""

act = isql_act('db', test_script)

expected_stdout = """        
	
TEST_1
=======
<false>
TEST_1
=======
<false>
TEST_1
=======
<false>
TEST_1
=======
<false>
TEST_1
=======
<true>
TEST_1
=======
<true>
TEST_1
=======
<false>
TEST_1
=======
<false>
TEST_1
=======
<true>
TEST_1
=======
<true>
TEST_1
=======
<true>
TEST_1
=======
<true>
TEST_1
=======
<true>
TEST_1
=======
<true>
TEST_1
=======
<false>
TEST_1
=======
<false>
TEST_1
=======
<false>
TEST_1
=======
<false>
TEST_1
=======
<true>
TEST_1
=======
<true>
TEST_1
=======
<false>
TEST_1
=======
<false>
TEST_2
=======
<false>
TEST_2
=======
<false>
TEST_2
=======
<false>
TEST_2
=======
<false>
TEST_2
=======
<true>
TEST_2
=======
<true>
TEST_2
=======
<false>
TEST_2
=======
<false>
TEST_2
=======
<true>
TEST_2
=======
<true>
TEST_2
=======
<true>
TEST_2
=======
<true>
TEST_2
=======
<true>
TEST_2
=======
<true>
TEST_2
=======
<false>
TEST_2
=======
<false>
TEST_2
=======
<false>
TEST_2
=======
<null>
TEST_2
=======
<true>
TEST_2
=======
<true>
TEST_2
=======
<null>
TEST_2
=======
<null>
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
