#coding:utf-8

"""
ID:          java.esp.functions.func-from.trigger
TITLE:       External function call from external trigger
DESCRIPTION: 
FBTEST:      functional.java.esp.functions.func_from.trigger
"""

import pytest
from firebird.qa import *

init_script = """

CREATE FUNCTION TEST()
RETURNS varchar(10)
EXTERNAL NAME 'esp.TestFunction.colname()' 
ENGINE JAVA;
commit;

CREATE TRIGGER TEST_TRIGGER 
FOR TEST_TABLE ACTIVE
BEFORE UPDATE
EXTERNAL NAME 'esp.TestTrigger.callFuncFromTrigger()'
engine JAVA;
commit;

create table test_table (str varchar(50));
commit;
"""

db = db_factory(init=init_script)

test_script = """
 
INSERT INTO TEST_TABLE VALUES ('It is old value');
UPDATE TEST_TABLE SET str='It is new value';

select str from test_table;
"""

act = isql_act('db', test_script)

expected_stdout = """             
	
STR
==================================================
test
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
