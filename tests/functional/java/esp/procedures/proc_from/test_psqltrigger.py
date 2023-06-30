#coding:utf-8

"""
ID:          java.esp.procedures.proc-from.psqltrigger
TITLE:       External procedure call from PSQL trigger
DESCRIPTION: 
FBTEST:      functional.java.esp.procedures.proc_from.psqltrigger
"""

import pytest
from firebird.qa import *

init_script = """

CREATE TABLE TEST_TABLE(F_BIGINT BIGINT);
commit;

create table test_table2(f integer);
commit;

CREATE PROCEDURE TEST(B integer)
EXTERNAL NAME 'esp.TestProcedure.intIntable2(int)' 
ENGINE JAVA;
commit;

set term ^ ;
create or alter trigger test_triger 
for test_table 
active
before insert
as
begin
	execute procedure test(3);
end^
set term ; ^
commit;


"""

db = db_factory(init=init_script)

test_script = """

 
INSERT INTO TEST_TABLE(F_BIGINT) VALUES (1);
commit;

SELECT F_BIGINT FROM TEST_TABLE;

SELECT F FROM TEST_TABLE2;
"""

act = isql_act('db', test_script)

expected_stdout = """
F_BIGINT
=====================
1
F
============
3
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
