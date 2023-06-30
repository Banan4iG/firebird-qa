#coding:utf-8

"""
ID:          java.esp.triggers.ddl-operators.drop
TITLE:       Testing DROP operator for external trigger
DESCRIPTION: 
FBTEST:      functional.java.esp.triggers.ddl_operators.drop
"""

import pytest
from firebird.qa import *

init_script = """
 
CREATE TABLE TEST_TABLE(f_integer integer);
commit; 
 
create trigger TEST_TRIGGER
for TEST_TABLE
active
before insert
external name 'esp.TestTrigger.increaseValueBy100()'
engine java;
commit;
"""

db = db_factory(init=init_script)

test_script = """
insert into TEST_TABLE values (100);
commit;

drop trigger TEST_TRIGGER;
commit;

insert into TEST_TABLE values (100);
commit;

select * from TEST_TABLE;
"""

act = isql_act('db', test_script)

expected_stdout = """                   
F_INTEGER
============
200
100
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
