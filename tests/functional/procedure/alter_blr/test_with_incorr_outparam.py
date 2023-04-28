#coding:utf-8

"""
ID:          procedure.alter_blr.with_incorr_outparam
TITLE:       Alter procedure with incorrect output parameters
DESCRIPTION:
FBTEST:      functional.procedure.alter_blr_with_incorr_outparam
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

P1: 1
P2: 2
P3: 3.4000000953674316
P4: 4.5
P5: 5.6
P6: 6.7
P7: 1995-08-31
P8: 13:45:57.100000
P9: 2001-03-29 14:46:59.900000
P10: Text p10
P11: Text p11
P12: Text p13
"""

act = python_act('db')

@pytest.mark.version('>=4.0')
def test_1(act: Action, capsys):
    with act.db.connect() as con:
        with con.cursor() as cur:
            cur.execute(f"SELECT	base64_encode(rdb$procedure_blr) from rdb$procedures where rdb$procedure_name = 'TEST_PROC'")
            for row in cur.fetchall():               
                try:
                    cur.execute(f"alter procedure BLR_PROC RETURNS(p2 INTEGER, p3 FLOAT, p4 DOUBLE PRECISION, p5 DECIMAL(9,3), p6 NUMERIC(10,4),p7 DATE, p8 TIME, p9 TIMESTAMP, p10 CHAR(40), p11 VARCHAR(60), p12 NCHAR(70)) as '{row[0]}'")
                    con.commit()	
                except Exception as e:
                    print("Error:", e)
                cur.execute(f"alter procedure BLR_PROC RETURNS(p1 SMALLINT, p2 INTEGER, p3 FLOAT, p4 DOUBLE PRECISION, p5 DECIMAL(9,3), p6 NUMERIC(10,4),p7 DATE, p8 TIME, p9 TIMESTAMP, p10 CHAR(40), p11 VARCHAR(60), p12 NCHAR(70)) as '{row[0]}'")
                con.commit()
        
            cur.execute("SELECT	rdb$procedure_name,rdb$procedure_source, base64_encode(rdb$procedure_blr) from rdb$procedures where rdb$procedure_name = 'BLR_PROC'")
            for row in cur.fetchall():
                print(f"RDB$PROCEDURE_NAME: {row[0]}")
                print(f"RDB$PROCEDURE_SOURCE: {row[1]}")

            cur.execute(f"execute procedure BLR_PROC;")
            for row in cur.fetchall():
                for i, field in enumerate(row):
                    print(f"P{i+1}: {field}")

    act.expected_stdout = expected_stdout
    act.stdout = capsys.readouterr().out
    assert act.clean_stdout == act.clean_expected_stdout
