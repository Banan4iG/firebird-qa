#coding:utf-8

"""
ID:          procedure.create_blr.with_incorr_outparam
TITLE:       Create procedure with incorrect output parameters
DESCRIPTION:
FBTEST:      functional.procedure.create_blr_with_incorr_outparam
"""

import pytest
from firebird.qa import *

init_script = """
    SET TERM ^;
    CREATE PROCEDURE TEST_PROC RETURNS(
        p1 SMALLINT, p2 INTEGER, p3 FLOAT, p4 DOUBLE PRECISION, p5 DECIMAL(9,3), p6 NUMERIC(10,4),
        p7 DATE, p8 TIME, p9 TIMESTAMP, p10 CHAR(40), p11 VARCHAR(60), p12 NCHAR(70))
    AS
    BEGIN
        p1=1;
        p2=2;
        p3=3.4;
        p4=4.5;
        p5=5.6;
        p6=6.7;
        p7='31.8.1995';
        p8='13:45:57.1';
        p9='29.03.2001 14:46:59.9';
        p10='Text p10';
        p11='Text p11';
        p12='Text p13';
    END ^
    SET TERM ;^
    commit;
"""

db = db_factory(init=init_script)

expected_stdout = """
Error: Error while parsing procedure BLR_PROC's BLR
-corrupt system table
"""

act = python_act('db')

@pytest.mark.version('>=4.0')
def test_1(act: Action, capsys):
    with act.db.connect() as con:
        with con.cursor() as cur:
            cur.execute(f"SELECT	base64_encode(rdb$procedure_blr) from rdb$procedures where rdb$procedure_name = 'TEST_PROC'")
            for row in cur.fetchall():               
                try:
                    cur.execute(f"create procedure BLR_PROC RETURNS(p2 INTEGER, p3 FLOAT, p4 DOUBLE PRECISION, p5 DECIMAL(9,3), p6 NUMERIC(10,4),p7 DATE, p8 TIME, p9 TIMESTAMP, p10 CHAR(40), p11 VARCHAR(60), p12 NCHAR(70)) as '{row[0]}'")
                    con.commit()	
                except Exception as e:
                    print("Error:", e)

    act.expected_stdout = expected_stdout
    act.stdout = capsys.readouterr().out
    assert act.clean_stdout == act.clean_expected_stdout
