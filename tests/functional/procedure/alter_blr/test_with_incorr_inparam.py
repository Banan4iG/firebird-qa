#coding:utf-8

"""
ID:          procedure.alter_blr.with_incorr_inparam
TITLE:       Alter procedure with incorrect input parameters
DESCRIPTION:
FBTEST:      functional.procedure.alter_blr_with_incorr_inparam
"""

import pytest
from firebird.qa import *

init_script = """
    SET TERM ^;
    CREATE PROCEDURE TEST_PROC(
        p1 SMALLINT, p2 INTEGER, p3 FLOAT, p4 DOUBLE PRECISION, p5 DECIMAL(9,3), p6 NUMERIC(10,4),
        p7 DATE, p8 TIME, p9 TIMESTAMP, p10 CHAR(40), p11 VARCHAR(60), p12 NCHAR(70))
    AS
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
Error: Error while parsing procedure BLR_PROC's BLR
    -corrupt system table
RDB$PROCEDURE_NAME: BLR_PROC
RDB$PROCEDURE_SOURCE: None
"""

act = python_act('db')

@pytest.mark.version('>=4.0')
def test_1(act: Action, capsys):
    with act.db.connect() as con:
        with con.cursor() as cur:
            cur.execute(f"SELECT	base64_encode(rdb$procedure_blr) from rdb$procedures where rdb$procedure_name = 'TEST_PROC'")
            for row in cur.fetchall():               
                try:
                    cur.execute(f"alter procedure BLR_PROC (p2 INTEGER, p3 FLOAT, p4 DOUBLE PRECISION, p5 DECIMAL(9,3), p6 NUMERIC(10,4), p7 DATE, p8 TIME, p9 TIMESTAMP, p10 CHAR(40), p11 VARCHAR(60), p12 NCHAR(70)) as '{row[0]}'")
                    con.commit()	
                except Exception as e:
                    print("Error:", e)
                cur.execute(f"alter procedure BLR_PROC (p1 SMALLINT, p2 INTEGER, p3 FLOAT, p4 DOUBLE PRECISION, p5 DECIMAL(9,3), p6 NUMERIC(10,4), p7 DATE, p8 TIME, p9 TIMESTAMP, p10 CHAR(40), p11 VARCHAR(60), p12 NCHAR(70)) as '{row[0]}'")
                con.commit()
        
            cur.execute("SELECT	rdb$procedure_name,rdb$procedure_source from rdb$procedures where rdb$procedure_name = 'BLR_PROC'")
            for row in cur.fetchall():
                print(f"RDB$PROCEDURE_NAME: {row[0]}")
                print(f"RDB$PROCEDURE_SOURCE: {row[1]}")

    act.expected_stdout = expected_stdout
    act.stdout = capsys.readouterr().out
    assert act.clean_stdout == act.clean_expected_stdout
