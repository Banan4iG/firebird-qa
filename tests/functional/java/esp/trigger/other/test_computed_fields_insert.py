#coding:utf-8

"""
ID:          java.esp.trigger.other.computed-fields-insert
TITLE:       Evaluating of computed fields
DESCRIPTION: 
FBTEST:      functional.java.esp.trigger.other.computed_fields_insert
"""

import pytest
from firebird.qa import *

init_script = """
CREATE TABLE TEST_TABLE1(
	TEST1 VARCHAR(10),
	TEST2 VARCHAR(10) COMPUTED BY ('ok2'),
	TEST3 VARCHAR(10) COMPUTED BY ('ok3'||test1),
	TEST4 VARCHAR(10) COMPUTED BY ((select 'ok4' from rdb$database)),
	TEST5 VARCHAR(10) COMPUTED BY ((select 'ok5' from rdb$database)||test1)
	);
CREATE TABLE TEST_TABLE2(
	TEST1 VARCHAR(10),
	TEST2 VARCHAR(10),
	TEST3 VARCHAR(10),
	TEST4 VARCHAR(10),
	TEST5 VARCHAR(10)
	);

CREATE OR ALTER TRIGGER TEST_TRIGGER
FOR TEST_TABLE1
ACTIVE
AFTER INSERT
external name 'esp.TestTrigger.trigger_computed_fields()'
engine JAVA;
commit;

insert into test_table1(test1) values('ok1');

select * from TEST_TABLE2;
"""

db = db_factory(init=init_script)

test_script = """
select * from TEST_TABLE2;
"""

act = isql_act('db', test_script)

expected_stdout = """TEST1      TEST2      TEST3      TEST4      TEST5
========== ========== ========== ========== ==========
ok1        ok2        ok3ok1     ok4        ok5ok1
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
