#coding:utf-8

"""
ID:          procedure.alter_blr.without_encode
TITLE:       Alter procedure without encode
DESCRIPTION:
FBTEST:      functional.procedure.alter_blr_without_encode
"""

import pytest
from firebird.qa import *

init_script = """
    SET TERM ^;
    CREATE PROCEDURE TEST_PROC AS
    BEGIN
        POST_EVENT 'Test';
    END ^
    
    CREATE PROCEDURE BLR_PROC 
    AS
        declare variable a integer;
    BEGIN
        a = 10;
    END ^
    SET TERM ;^
    commit;
"""

db = db_factory(init=init_script)

expected_stdout = """
RDB$PROCEDURE_NAME: BLR_PROC
RDB$PROCEDURE_SOURCE:
declare variable a integer;
BEGIN
a = 10;
END
"""

expected_stderr = """
unsuccessful metadata update
-ALTER PROCEDURE BLR_PROC failed
-Error while parsing procedure BLR_PROC's BLR
"""

act = python_act('db')

@pytest.mark.version('>=4.0')
def test_1(act: Action, capsys):
    with act.db.connect() as con:
        with con.cursor() as cur:
            with pytest.raises(Exception) as ex:
                cur.execute("SELECT rdb$procedure_blr from rdb$procedures where rdb$procedure_name = 'TEST_PROC'")
                for row in cur.fetchall():
                    blr = str(row[0])[2:-2]     # Trim b-prefix
                    cur.execute(f"alter procedure BLR_PROC as '{blr}'")
                    con.commit()
            cur.execute("SELECT rdb$procedure_name,rdb$procedure_source from rdb$procedures where rdb$procedure_name = 'BLR_PROC'")
            for range in cur.fetchall():
                print(f"RDB$PROCEDURE_NAME: {range[0]}")
                print(f"RDB$PROCEDURE_SOURCE:\n{range[1]}")

    act.expected_stderr = expected_stderr
    act.expected_stdout = expected_stdout
    act.stderr = str(ex.value)
    act.stdout = capsys.readouterr().out
    assert act.clean_stderr == act.clean_expected_stderr
    assert act.clean_stdout == act.clean_expected_stdout   
