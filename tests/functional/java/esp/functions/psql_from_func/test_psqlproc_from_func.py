#coding:utf-8

"""
ID:          java.esp.functions.psql-from-func.psqlproc-from-func
TITLE:       PSQL procedure call from external function
DESCRIPTION: 
FBTEST:      functional.java.esp.functions.psql_from_func.psqlproc_from_func
"""

import pytest
from firebird.qa import *

init_script = """

create table test_table(num bigint);
 
set term !;
 
create procedure test(i bigint)
returns (sm bigint)
as
declare variable tmp bigint;
begin
	insert into test_table values(:i+10);
	for select num
		from test_table
		into :sm
	do
		suspend;
end!
set term ;!


CREATE FUNCTION MAINTEST(B BIGINT)
RETURNS BIGINT
EXTERNAL NAME 'esp.TestFunction.callProcFromFunc(Long)' 
ENGINE JAVA;
commit;

"""

db = db_factory(init=init_script)

test_script = """
 
SELECT MAINTEST(10000000) FROM rdb$database;
commit;
"""

act = isql_act('db', test_script)

expected_stdout = """             
MAINTEST
=====================
10000010
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
