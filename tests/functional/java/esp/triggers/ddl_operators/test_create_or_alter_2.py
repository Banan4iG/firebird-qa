#coding:utf-8

"""
ID:          java.esp.triggers.ddl-operators.create-or-alter-2
TITLE:       Testing CREATE OR ALTER operator for external trigger when trigger is not created
DESCRIPTION: 
FBTEST:      functional.java.esp.triggers.ddl_operators.create_or_alter_2
"""

import pytest
from firebird.qa import *

init_script = """
 
CREATE TABLE TEST_TABLE(f_integer integer);
commit; 
 
"""

db = db_factory(init=init_script)

test_script = """

create or alter trigger TEST_TRIGGER
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
