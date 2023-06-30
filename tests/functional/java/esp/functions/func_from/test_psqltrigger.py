#coding:utf-8

"""
ID:          java.esp.functions.func-from.psqltrigger
TITLE:       External function call from PSQL trigger
DESCRIPTION: 
FBTEST:      functional.java.esp.functions.func_from.psqltrigger
"""

import pytest
from firebird.qa import *

init_script = """
CREATE TABLE TEST_TABLE(
	ID NUMERIC(15) PRIMARY KEY,
	NAME VARCHAR(50) );
commit;

create function test_fun()
returns varchar(10)
external name 'esp.TestFunction.colname()' 
engine java;
commit;

set term ^ ;
create or alter trigger test_triger 
for test_table 
active
before insert
as
begin
  if (new.name is null or new.name = '') then
    new.name = test_fun();
end^
set term ; ^
commit;
"""

db = db_factory(init=init_script)

test_script = """
INSERT INTO TEST_TABLE(ID) VALUES (1);
commit;

SELECT NAME FROM TEST_TABLE WHERE ID=1;
"""

act = isql_act('db', test_script)

expected_stdout = """
NAME
==================================================
test
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
