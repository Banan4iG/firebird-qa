#coding:utf-8

"""
ID:          java.esp.functions.func-from.psqlproc
TITLE:       External function call from PSQL procedure
DESCRIPTION: 
FBTEST:      functional.java.esp.functions.func_from.psqlproc
"""

import pytest
from firebird.qa import *

init_script = """

CREATE FUNCTION TEST(B BIGINT)
RETURNS BIGINT
EXTERNAL NAME 'esp.TestFunction.LongInOut(Long)' 
ENGINE JAVA;
commit;

create table test_table(num integer);
commit;

set term !;
create procedure TEST_PSQL_PROC(i DOUBLE PRECISION)
AS
BEGIN
	INSERT INTO test_table values (TEST(:i));
END!
set term ;!



"""

db = db_factory(init=init_script)

test_script = """
 
EXECUTE PROCEDURE TEST_PSQL_PROC(124.68);
commit;

select num from test_table;
"""

act = isql_act('db', test_script)

expected_stdout = """             
NUM
============
125
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
