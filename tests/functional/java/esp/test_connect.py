#coding:utf-8

"""
ID:          java.esp.connect
TITLE:       Get context of CONNECT trigger
DESCRIPTION: 
FBTEST:      functional.java.esp.connect
"""

import pytest
from firebird.qa import *
import os

db = db_factory()
act = python_act('db')

script = '''
CREATE FUNCTION func_1(B BIGINT)
RETURNS BIGINT
EXTERNAL NAME 'esp.TestFunction.LongInOut(Long)' 
ENGINE JAVA;
commit;

set term !;
create function PSQL_FUNC_1(i DOUBLE PRECISION)
returns DOUBLE PRECISION
AS
BEGIN
	RETURN func_1(i);
END!
set term ;!

 
CREATE TABLE TEST_TABLE(F_BIGINT BIGINT);
commit;

CREATE OR ALTER PROCEDURE proc_1(B BIGINT)
EXTERNAL NAME 'esp.TestProcedure.longIn(long)' 
ENGINE JAVA;
commit;

SET TERM ^ ;
CREATE OR ALTER PROCEDURE PSQL_PROC_1(B BIGINT)
AS
BEGIN
  EXECUTE PROCEDURE proc_1(B);
END^
SET TERM ; ^
commit;

CREATE TABLE CONTEXT_TABLE(context VARCHAR(2000));
commit;

CREATE OR ALTER TRIGGER trigger_1 
ACTIVE
BEFORE CREATE TABLE or ALTER TABLE or DROP TABLE
external name 'esp.TestTrigger.getContext()'
engine JAVA;
commit;

create table test_table12(id integer); 
commit;


CREATE FUNCTION TEST(B FLOAT)
RETURNS FLOAT
EXTERNAL NAME 'esp.TestFunction.floatInOut(float)' 
ENGINE JAVA;
commit;

CREATE PROCEDURE MAINTEST(B FLOAT)
EXTERNAL NAME 'esp.TestProcedure.callFuncFromProcedure(float)' 
ENGINE JAVA;
commit;

'''

backup = temp_file('bug_20059_2.fbk')

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action, backup):
    act.isql(switches=['-q'], input=script)
    act.gbak(switches=['-b', act.db.dsn, str(backup)])
    assert act.clean_stdout == ""
