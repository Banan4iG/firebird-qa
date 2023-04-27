#coding:utf-8

"""
ID:          function.create_blr.with_var
TITLE:       Create function with variables
DESCRIPTION:
FBTEST:      functional.function.create_blr_with_var
"""

import pytest
from firebird.qa import *

init_script = """
    SET TERM ^;
    CREATE FUNCTION TEST_FUNC
    RETURNS integer
    AS
        DECLARE VARIABLE p1 SMALLINT;
        DECLARE VARIABLE p2 INTEGER;
        DECLARE VARIABLE p3 FLOAT;
        DECLARE VARIABLE p4 DOUBLE PRECISION;
        DECLARE VARIABLE p5 DECIMAL(9,3);
        DECLARE VARIABLE p6 NUMERIC(10,4);
        DECLARE VARIABLE p7 DATE;
        DECLARE VARIABLE p8 TIME;
        DECLARE VARIABLE p9 TIMESTAMP;
        DECLARE VARIABLE p10 CHAR(40);
        DECLARE VARIABLE p11 VARCHAR(60);
        DECLARE VARIABLE p12 NCHAR(70);
    BEGIN
        p1=1;
        p2=2;
        p3=3.4;
        p4=4.5;
        p5=5.6;
        p6=6.7;
        p7='31.8.1995';
        p8='13:45:57.1';
        p9='29.03.2002 14:46:59.9';
        p10='Text p10';
        p11='Text p11';
        p12='Text p12';
        return p6;
    END ^
    SET TERM ;^
    commit;
"""

db = db_factory(init=init_script)

expected_stdout = """
RDB$FUNCTION_NAME: BLR_FUNC
RDB$FUNCTION_SOURCE: None
BLR_FUNC: 7
"""

act = python_act('db')

@pytest.mark.version('>=4.0')
def test_1(act: Action, capsys):
    with act.db.connect() as con:
        with con.cursor() as cur:
            cur.execute("SELECT	base64_encode(rdb$function_blr) from rdb$functions where rdb$function_name = 'TEST_FUNC'")
            for row in cur.fetchall():
                cur.execute(f"create function BLR_FUNC RETURNS integer as '{row[0]}'")
                con.commit()
                cur.execute("SELECT	rdb$function_name,rdb$function_source, base64_encode(rdb$function_blr) from rdb$functions where rdb$function_name = 'BLR_FUNC'")
                for range in cur.fetchall():
                    if row[0]==range[2]:
                        print(f"RDB$FUNCTION_NAME: {range[0]}")
                        print(f"RDB$FUNCTION_SOURCE: {range[1]}")

            cur.execute("select BLR_FUNC() from rdb$database;")
            for row in cur.fetchall():
                    print(f"BLR_FUNC: {row[0]}")

    act.expected_stdout = expected_stdout
    act.stdout = capsys.readouterr().out
    assert act.clean_stdout == act.clean_expected_stdout
