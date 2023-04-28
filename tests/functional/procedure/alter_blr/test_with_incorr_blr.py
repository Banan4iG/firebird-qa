#coding:utf-8

"""
ID:          procedure.alter_blr.with_incorr_blr
TITLE:       Alter procedure with incorrect BLR
DESCRIPTION:
FBTEST:      functional.procedure.alter_blr_with_incorr_blr
"""

import pytest
from firebird.qa import *

init_script = """
    SET TERM ^;
    CREATE PROCEDURE BLR_PROC 
    AS
    BEGIN
        POST_EVENT 'Test';
    END ^	
    SET TERM ;^
    commit;
"""

db = db_factory(init=init_script)

expected_stdout = """
Error: Error while parsing procedure BLR_PROC's BLR
-corrupt system table
-unsupported BLR version (expected between 4 and 5, encountered 0)

RDB$PROCEDURE_NAME: BLR_PROC
RDB$PROCEDURE_SOURCE:
BEGIN
POST_EVENT 'Test';
END
"""

act = python_act('db')

@pytest.mark.version('>=4.0')
def test_1(act: Action, capsys):
    with act.db.connect() as con:
        with con.cursor() as cur:
            try:
                cur.execute(f"alter procedure BLR_PROC as 'ABC'")
                con.commit()
            except Exception as e:
                print("Error:", e)
    
            con.rollback()	
            cur.execute("SELECT	rdb$procedure_name,rdb$procedure_source from rdb$procedures where rdb$procedure_name = 'BLR_PROC'")
            for range in cur.fetchall():
                print(f"RDB$PROCEDURE_NAME: {range[0]}")
                print(f"RDB$PROCEDURE_SOURCE:\n{range[1]}")

    act.expected_stdout = expected_stdout
    act.stdout = capsys.readouterr().out
    assert act.clean_stdout == act.clean_expected_stdout
