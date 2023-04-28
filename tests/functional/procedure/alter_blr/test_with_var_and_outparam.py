#coding:utf-8

"""
ID:          procedure.alter_blr.with_var_outparam
TITLE:       Alter procedure with variables and output parameters
DESCRIPTION:
FBTEST:      functional.procedure.alter_blr_with_var_outparam
"""

import pytest
from firebird.qa import *

init_script = """
    SET TERM ^;
    CREATE PROCEDURE TEST_PROC RETURNS(
        p1 SMALLINT, p2 INTEGER, p3 FLOAT, p4 DOUBLE PRECISION, p5 DECIMAL(9,3), p6 NUMERIC(10,4),
        p7 DATE, p8 TIME, p9 TIMESTAMP, p10 CHAR(40), p11 VARCHAR(60), p12 NCHAR(70))
    AS
        DECLARE VARIABLE v1 SMALLINT;
        DECLARE VARIABLE v2 INTEGER;
        DECLARE VARIABLE v3 FLOAT;
        DECLARE VARIABLE v4 DOUBLE PRECISION;
        DECLARE VARIABLE v5 DECIMAL(9,3);
        DECLARE VARIABLE v6 NUMERIC(10,4);
        DECLARE VARIABLE v7 DATE;
        DECLARE VARIABLE v8 TIME;
        DECLARE VARIABLE v9 TIMESTAMP;
        DECLARE VARIABLE v10 CHAR(40);
        DECLARE VARIABLE v11 VARCHAR(60);
        DECLARE VARIABLE v12 NCHAR(70);
    BEGIN
        v1=1;
        v2=2;
        v3=3.4;
        v4=4.5;
        v5=5.6;
        v6=6.7;
        v7='31.8.1995';
        v8='13:45:57.1';
        v9='29.03.2002 14:46:59.9';
        v10='Text p10';
        v11='Text p11';
        v12='Text p12';
        p1=v1;
        p2=v2;
        p3=v3;
        p4=v4;
        p5=v5;
        p6=v6;
        p7=v7;
        p8=v8;
        p9=v9;
        p10=v10;
        p11=v11;
        p12=v12;
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

P1: 1
P2: 2
P3: 3.4000000953674316
P4: 4.5
P5: 5.6
P6: 6.7
P7: 1995-08-31
P8: 13:45:57.100000
P9: 2002-03-29 14:46:59.900000
P10: Text p10
P11: Text p11
P12: Text p12
"""

act = python_act('db')

@pytest.mark.version('>=4.0')
def test_1(act: Action, capsys):
    with act.db.connect() as con:
        with con.cursor() as cur:
            cur.execute("SELECT	base64_encode(rdb$procedure_blr) from rdb$procedures where rdb$procedure_name = 'TEST_PROC'")
            for row in cur.fetchall():
                cur.execute(f"alter procedure BLR_PROC RETURNS(p1 SMALLINT, p2 INTEGER, p3 FLOAT, p4 DOUBLE PRECISION, p5 DECIMAL(9,3), p6 NUMERIC(10,4), p7 DATE, p8 TIME, p9 TIMESTAMP, p10 CHAR(40), p11 VARCHAR(60), p12 NCHAR(70)) as '{row[0]}'")
                con.commit()
                cur.execute("SELECT	rdb$procedure_name,rdb$procedure_source, base64_encode(rdb$procedure_blr) from rdb$procedures where rdb$procedure_name = 'BLR_PROC'")
                for range in cur.fetchall():
                    if row[0]==range[2]:
                        print(f"RDB$PROCEDURE_NAME: {range[0]}")
                        print(f"RDB$PROCEDURE_SOURCE: {range[1]}")
            
            cur.execute(f"execute procedure BLR_PROC;")
            for row in cur.fetchall():
                for i, field in enumerate(row):
                    print(f"P{i+1}: {field}")	

    act.expected_stdout = expected_stdout
    act.stdout = capsys.readouterr().out
    assert act.clean_stdout == act.clean_expected_stdout
