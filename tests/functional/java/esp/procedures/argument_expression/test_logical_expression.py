#coding:utf-8

"""
ID:          java.esp.procedures.argument-expression.logical-expression
TITLE:       External procedure call with input parameter as an logical expression
DESCRIPTION: 
FBTEST:      functional.java.esp.procedures.argument_expression.logical_expression
"""

import pytest
from firebird.qa import *

# version: 3.0

init_script_1 = """
 
CREATE TABLE TEST_TABLE(col varchar(150));
commit;  
 
create procedure test_1(i boolean) 
external name 'esp.TestProcedure.booleanIn(boolean)' 
engine java;
commit;

create procedure test_2(i boolean) 
external name 'esp.TestProcedure.BooleanIn(Boolean)' 
engine java;
commit;

"""

db_1 = db_factory(init=init_script_1)

test_script_1 = """
EXECUTE PROCEDURE TEST_1(false and false);
EXECUTE PROCEDURE TEST_1(1>2 and 1!=1);

EXECUTE PROCEDURE TEST_1(false and true);
EXECUTE PROCEDURE TEST_1(10<5 and 1=1);

EXECUTE PROCEDURE TEST_1(true and true);
EXECUTE PROCEDURE TEST_1(2!=1 and 2>1);

EXECUTE PROCEDURE TEST_1(false or false);
EXECUTE PROCEDURE TEST_1(1>2 or 1!=1);

EXECUTE PROCEDURE TEST_1(false or true);
EXECUTE PROCEDURE TEST_1(10<5 or 1=1);

EXECUTE PROCEDURE TEST_1(true or true);
EXECUTE PROCEDURE TEST_1(2!=1 or 2>1);

EXECUTE PROCEDURE TEST_1(not false);
EXECUTE PROCEDURE TEST_1(not 2<1);

EXECUTE PROCEDURE TEST_1(not true);
EXECUTE PROCEDURE TEST_1(not 2>1);

EXECUTE PROCEDURE TEST_1(false and unknown);
EXECUTE PROCEDURE TEST_1(3>1 and null);

EXECUTE PROCEDURE TEST_1(true or unknown);
EXECUTE PROCEDURE TEST_1(3<10 or null);

EXECUTE PROCEDURE TEST_1(not unknown);
EXECUTE PROCEDURE TEST_1(not null);


EXECUTE PROCEDURE TEST_2(false and false);
EXECUTE PROCEDURE TEST_2(1>2 and 1!=1);

EXECUTE PROCEDURE TEST_2(false and true);
EXECUTE PROCEDURE TEST_2(10<5 and 1=1);

EXECUTE PROCEDURE TEST_2(true and true);
EXECUTE PROCEDURE TEST_2(2!=1 and 2>1);

EXECUTE PROCEDURE TEST_2(false or false);
EXECUTE PROCEDURE TEST_2(1>2 or 1!=1);

EXECUTE PROCEDURE TEST_2(false or true);
EXECUTE PROCEDURE TEST_2(10<5 or 1=1);

EXECUTE PROCEDURE TEST_2(true or true);
EXECUTE PROCEDURE TEST_2(2!=1 or 2>1);

EXECUTE PROCEDURE TEST_2(not false);
EXECUTE PROCEDURE TEST_2(not 2<1);

EXECUTE PROCEDURE TEST_2(not true);
EXECUTE PROCEDURE TEST_2(not 2>1);

EXECUTE PROCEDURE TEST_2(false and unknown);
EXECUTE PROCEDURE TEST_2(3>1 and null);

EXECUTE PROCEDURE TEST_2(true or unknown);
EXECUTE PROCEDURE TEST_2(3<10 or null);

EXECUTE PROCEDURE TEST_2(not unknown);
EXECUTE PROCEDURE TEST_2(not null);
commit;

select * from test_table;
"""

act_1 = isql_act('db_1', test_script_1)

expected_stdout_1 = """        
COL
===============================================================================
false
false
false
false
true
true
false
false
true
true
true
true
true
true
false
false
false
false
true
true
COL
===============================================================================
false
false
false
false
false
false
true
true
false
false
true
true
true
true
true
true
false
false
false
<null>
COL
===============================================================================
true
true
<null>
<null>
"""

@pytest.mark.java
@pytest.mark.version('>=3.0,<4.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_stdout == act_1.clean_expected_stdout

# version: 4.0

init_script_2 = """

CREATE TABLE TEST_TABLE(col varchar(150));
commit;

create procedure test_1(i boolean)
external name 'esp.TestProcedure.booleanIn(boolean)'
engine java;
commit;

create procedure test_2(i boolean)
external name 'esp.TestProcedure.BooleanIn(Boolean)'
engine java;
commit;

"""

db_2 = db_factory(init=init_script_2)

test_script_2 = """
EXECUTE PROCEDURE TEST_1(false and false);
EXECUTE PROCEDURE TEST_1(1>2 and 1!=1);

EXECUTE PROCEDURE TEST_1(false and true);
EXECUTE PROCEDURE TEST_1(10<5 and 1=1);

EXECUTE PROCEDURE TEST_1(true and true);
EXECUTE PROCEDURE TEST_1(2!=1 and 2>1);

EXECUTE PROCEDURE TEST_1(false or false);
EXECUTE PROCEDURE TEST_1(1>2 or 1!=1);

EXECUTE PROCEDURE TEST_1(false or true);
EXECUTE PROCEDURE TEST_1(10<5 or 1=1);

EXECUTE PROCEDURE TEST_1(true or true);
EXECUTE PROCEDURE TEST_1(2!=1 or 2>1);

EXECUTE PROCEDURE TEST_1(not false);
EXECUTE PROCEDURE TEST_1(not 2<1);

EXECUTE PROCEDURE TEST_1(not true);
EXECUTE PROCEDURE TEST_1(not 2>1);

EXECUTE PROCEDURE TEST_1(false and unknown);
EXECUTE PROCEDURE TEST_1(3>1 and null);

EXECUTE PROCEDURE TEST_1(true or unknown);
EXECUTE PROCEDURE TEST_1(3<10 or null);

EXECUTE PROCEDURE TEST_1(not unknown);
EXECUTE PROCEDURE TEST_1(not null);


EXECUTE PROCEDURE TEST_2(false and false);
EXECUTE PROCEDURE TEST_2(1>2 and 1!=1);

EXECUTE PROCEDURE TEST_2(false and true);
EXECUTE PROCEDURE TEST_2(10<5 and 1=1);

EXECUTE PROCEDURE TEST_2(true and true);
EXECUTE PROCEDURE TEST_2(2!=1 and 2>1);

EXECUTE PROCEDURE TEST_2(false or false);
EXECUTE PROCEDURE TEST_2(1>2 or 1!=1);

EXECUTE PROCEDURE TEST_2(false or true);
EXECUTE PROCEDURE TEST_2(10<5 or 1=1);

EXECUTE PROCEDURE TEST_2(true or true);
EXECUTE PROCEDURE TEST_2(2!=1 or 2>1);

EXECUTE PROCEDURE TEST_2(not false);
EXECUTE PROCEDURE TEST_2(not 2<1);

EXECUTE PROCEDURE TEST_2(not true);
EXECUTE PROCEDURE TEST_2(not 2>1);

EXECUTE PROCEDURE TEST_2(false and unknown);
EXECUTE PROCEDURE TEST_2(3>1 and null);

EXECUTE PROCEDURE TEST_2(true or unknown);
EXECUTE PROCEDURE TEST_2(3<10 or null);

EXECUTE PROCEDURE TEST_2(not unknown);
EXECUTE PROCEDURE TEST_2(not null);
commit;

select * from test_table;
"""

act_2 = isql_act('db_2', test_script_2)

expected_stdout_2 = """
COL
======================================================================================================================================================
false
false
false
false
true
true
false
false
true
true
true
true
true
true
false
false
false
false
true
true
COL
======================================================================================================================================================
false
false
false
false
false
false
true
true
false
false
true
true
true
true
true
true
false
false
false
<null>
COL
======================================================================================================================================================
true
true
<null>
<null>
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
