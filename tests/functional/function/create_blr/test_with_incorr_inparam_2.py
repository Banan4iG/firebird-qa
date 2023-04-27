#coding:utf-8

"""
ID:          function.create_blr.with_incorr_inparam_2
TITLE:       Create function with incorrect input parameters
DESCRIPTION:
FBTEST:      functional.function.create_blr_with_incorr_inparam2
"""

import pytest
from firebird.qa import *

init_script = """
    SET TERM ^;
    CREATE FUNCTION TEST_FUNC(
        p1 SMALLINT, p2 INTEGER, p3 FLOAT, p4 DOUBLE PRECISION, p5 DECIMAL(9,3), p6 NUMERIC(10,4),
        p7 DATE, p8 TIME, p9 TIMESTAMP, p10 CHAR(40), p11 VARCHAR(60), p12 NCHAR(70))
    returns integer
    AS
    BEGIN
        POST_EVENT 'Test';
        return p1;
    END ^
    SET TERM ;^
    commit;
"""

db = db_factory(init=init_script)

expected_stdout = """
RDB$FUNCTION_NAME: BLR_FUNC
RDB$FUNCTION_SOURCE: None

Error: conversion error from string "12.12.1989"
"""

act = python_act('db')

@pytest.mark.version('>=4.0')
def test_1(act: Action, capsys):
    with act.db.connect() as con:
        with con.cursor() as cur:
            cur.execute("SELECT	base64_encode(rdb$function_blr) from rdb$functions where rdb$function_name = 'TEST_FUNC'")
            for row in cur.fetchall():
                cur.execute("create function BLR_FUNC (p1 DATE, p2 INTEGER, p3 FLOAT, p4 DOUBLE PRECISION, p5 DECIMAL(9,3), p6 NUMERIC(10,4), p7 DATE, p8 TIME, p9 TIMESTAMP, p10 CHAR(40), p11 VARCHAR(60), p12 NCHAR(70)) returns integer as '%s'"%row[0])
                con.commit()
                cur.execute("SELECT	rdb$function_name,rdb$function_source, base64_encode(rdb$function_blr) from rdb$functions where rdb$function_name = 'BLR_FUNC'")
                for range in cur.fetchall():
                    if row[0]==range[2]:
                        print(f"RDB$FUNCTION_NAME: {range[0]}")
                        print(f"RDB$FUNCTION_SOURCE: {range[1]}")

            try:
                cur.execute("select BLR_FUNC('12.12.1989',2,3,4,5,6,'23.03.1934', '11:35:20', '14.07.2007 12:30', 'a', 'b', 'c') from rdb$database;")
                cur.fetchall()
            except Exception as e:
                print("Error:", e)
    
    act.expected_stdout = expected_stdout
    act.stdout = capsys.readouterr().out
    assert act.clean_stdout == act.clean_expected_stdout
