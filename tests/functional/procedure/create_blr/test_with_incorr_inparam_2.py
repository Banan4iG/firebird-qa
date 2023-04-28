#coding:utf-8

"""
ID:          procedure.create_blr.with_incorr_inparam_2
TITLE:       Create procedure with incorrect input parameters
DESCRIPTION:
FBTEST:      functional.procedure.create_blr_with_incorr_inparam2
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
    SET TERM ;^
    commit;
"""

db = db_factory(init=init_script)

expected_stdout = """
RDB$PROCEDURE_NAME: BLR_PROC
RDB$PROCEDURE_SOURCE: None

Error: conversion error from string "12.12.1989"
"""

act = python_act('db')

@pytest.mark.version('>=4.0')
def test_1(act: Action, capsys):
    with act.db.connect() as con:
        with con.cursor() as cur:
            cur.execute("SELECT base64_encode(rdb$procedure_blr) from rdb$procedures where rdb$procedure_name = 'TEST_PROC'")
            for row in cur.fetchall():
                cur.execute("create procedure BLR_PROC (p1 DATE, p2 INTEGER, p3 FLOAT, p4 DOUBLE PRECISION, p5 DECIMAL(9,3), p6 NUMERIC(10,4), p7 DATE, p8 TIME, p9 TIMESTAMP, p10 CHAR(40), p11 VARCHAR(60), p12 NCHAR(70)) as '%s'"%row[0])
                con.commit()
                cur.execute("SELECT rdb$procedure_name,rdb$procedure_source, base64_encode(rdb$procedure_blr) from rdb$procedures where rdb$procedure_name = 'BLR_PROC'")
                for range in cur.fetchall():
                    if row[0]==range[2]:
                        print(f"RDB$PROCEDURE_NAME: {range[0]}")
                        print(f"RDB$PROCEDURE_SOURCE: {range[1]}")

            try:
                cur.execute("execute procedure BLR_PROC('12.12.1989',2,3,4,5,6,'12.12.1989','23:16:32.0098',' 14.07.2007 12:30','hello','world','help');")
                cur.fetchall()
            except Exception as e:
                print("Error:", e)
    
    act.expected_stdout = expected_stdout
    act.stdout = capsys.readouterr().out
    assert act.clean_stdout == act.clean_expected_stdout
