#coding:utf-8

"""
ID:          java.esp.functions.psql-from-func.psqltrigger-from-func
TITLE:       PSQL trigger call from external function
DESCRIPTION: 
FBTEST:      functional.java.esp.functions.psql_from_func.psqltrigger_from_func
"""

import pytest
from firebird.qa import *

init_script = """
create table test_table (id bigint, name varchar(50));
 
SET TERM ^ ;
CREATE OR ALTER TRIGGER TEST_TRIGER 
FOR TEST_TABLE 
ACTIVE
BEFORE INSERT
AS
BEGIN
  IF (NEW.NAME IS NULL OR NEW.NAME = '') THEN
    NEW.NAME = 'name_from_trigger';
END^
SET TERM ; ^
commit;

CREATE FUNCTION MAINTEST(B BIGINT)
RETURNS BIGINT
EXTERNAL NAME 'esp.TestFunction.callTriggerFromFunc(Long)' 
ENGINE JAVA;
commit;
"""

db = db_factory(init=init_script)

test_script = """
 
SELECT MAINTEST(1000) FROM rdb$database;
commit;

select * from test_table;
"""

act = isql_act('db', test_script)

expected_stdout = """             
	
MAINTEST
=====================
0
ID NAME
===================== ==================================================
1000 name_from_trigger
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
