#coding:utf-8

"""
ID:          function.create_blr.without_parameters
TITLE:       Create function without parameters
DESCRIPTION:
FBTEST:      functional.function.create_blr_without_param
"""

import pytest
from firebird.qa import *

init_script = """
    SET TERM ^;
    CREATE FUNCTION TEST_FUNC
    RETURNS integer
    AS
    BEGIN
        POST_EVENT 'Test';
        return 901;
    END ^
    SET TERM ;^
    commit;
"""

db = db_factory(init=init_script)

expected_stdout = """
RDB$FUNCTION_NAME: BLR_FUNC
RDB$FUNCTION_SOURCE: None
BLR_FUNC: 901
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
