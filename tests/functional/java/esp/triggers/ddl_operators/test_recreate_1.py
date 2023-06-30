#coding:utf-8

"""
ID:          java.esp.triggers.ddl-operators.recreate-1
TITLE:       Testing RECREATE operator for external trigger when trigger is not created
DESCRIPTION: 
FBTEST:      functional.java.esp.triggers.ddl_operators.recreate_1
"""

import pytest
from firebird.qa import *

init_script = """
 
CREATE TABLE TEST_TABLE(f_integer integer);
commit; 

"""

db = db_factory(init=init_script)

test_script = """

recreate trigger TEST_TRIGGER
for TEST_TABLE
active
before insert
external name 'esp.TestTrigger.increaseValueBy1000()'
engine java;
commit;

insert into TEST_TABLE values (100);
commit;

select * from TEST_TABLE;
"""

act = isql_act('db', test_script)

expected_stdout = """  
	
F_INTEGER
============
1100
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
