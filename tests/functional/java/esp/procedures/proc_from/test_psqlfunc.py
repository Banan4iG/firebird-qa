#coding:utf-8

"""
ID:          java.esp.procedures.proc-from.psqlfunc
TITLE:       External procedure call from PSQL function
DESCRIPTION: 
FBTEST:      functional.java.esp.procedures.proc_from.psqlfunc
"""

import pytest
from firebird.qa import *

init_script = """

CREATE TABLE TEST_TABLE(F_BIGINT BIGINT);
commit;

CREATE PROCEDURE TEST(B BIGINT)
EXTERNAL NAME 'esp.TestProcedure.longIn(long)' 
ENGINE JAVA;
commit;



set term !;
create function TEST_PSQL_FUNC(i DOUBLE PRECISION)
returns DOUBLE PRECISION
AS
BEGIN
	execute procedure test(i);	
	RETURN (select F_BIGINT from test_table);
END!
set term ;!
"""

db = db_factory(init=init_script)

test_script = """
 
SELECT TEST_PSQL_FUNC(100.23) FROM rdb$database;
commit;

"""

act = isql_act('db', test_script)

expected_stdout = """             
TEST_PSQL_FUNC
=======================
100.0000000000000
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
