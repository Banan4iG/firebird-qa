#coding:utf-8

"""
ID:          function.create_blr.with_incorr_outtype
TITLE:       Create function with incorrect out type
DESCRIPTION:
FBTEST:      functional.function.create_blr_with_incorr_outtype
"""

import pytest
from firebird.qa import *

init_script = """
    SET TERM ^;
    CREATE FUNCTION TEST_FUNC
    RETURNS INTEGER
    AS
    BEGIN
        Return 5;
    END ^
    SET TERM ;^
    commit;
"""

db = db_factory(init=init_script)

expected_stdout = """
RDB$FUNCTION_NAME: BLR_FUNC
RDB$FUNCTION_SOURCE: None

Error: conversion error from string "5"
"""

act = python_act('db')

@pytest.mark.version('>=4.0')
def test_1(act: Action, capsys):
    with act.db.connect() as con:
        with con.cursor() as cur:
            cur.execute("SELECT	base64_encode(rdb$function_blr) from rdb$functions where rdb$function_name = 'TEST_FUNC'")
            for row in cur.fetchall():
                cur.execute(f"create function BLR_FUNC RETURNS TIMESTAMP as '{row[0]}'")
                con.commit()
                cur.execute("SELECT	rdb$function_name,rdb$function_source, base64_encode(rdb$function_blr) from rdb$functions where rdb$function_name = 'BLR_FUNC'")
                for range in cur.fetchall():
                    if row[0]==range[2]:
                        print(f"RDB$FUNCTION_NAME: {range[0]}")
                        print(f"RDB$FUNCTION_SOURCE: {range[1]}")

            try:
                cur.execute("select BLR_FUNC() from rdb$database;")
                cur.fetchall()
            except Exception as e:
                print("Error:", e)

    act.expected_stdout = expected_stdout
    act.stdout = capsys.readouterr().out
    assert act.clean_stdout == act.clean_expected_stdout
