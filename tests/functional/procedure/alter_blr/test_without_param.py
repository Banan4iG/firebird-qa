#coding:utf-8

"""
ID:          procedure.alter_blr.without_param
TITLE:       Alter procedure without parameter
DESCRIPTION:
FBTEST:      functional.procedure.alter_blr_without_param
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
RDB$PROCEDURE_SOURCE: None
"""

act = python_act('db')

@pytest.mark.version('>=4.0')
def test_1(act: Action, capsys):
    with act.db.connect() as con:
        with con.cursor() as cur:
            cur.execute("SELECT base64_encode(rdb$procedure_blr) from rdb$procedures where rdb$procedure_name = 'TEST_PROC'")
            for row in cur.fetchall():
                cur.execute(f"alter procedure BLR_PROC as '{row[0]}'")
                con.commit()
                cur.execute("SELECT rdb$procedure_name,rdb$procedure_source, base64_encode(rdb$procedure_blr) from rdb$procedures where rdb$procedure_name = 'BLR_PROC'")
                for range in cur.fetchall():
                    if row[0]==range[2]:
                        print(f"RDB$PROCEDURE_NAME: {range[0]}")
                        print(f"RDB$PROCEDURE_SOURCE: {range[1]}")


    act.expected_stdout = expected_stdout
    act.stdout = capsys.readouterr().out
    assert act.clean_stdout == act.clean_expected_stdout
