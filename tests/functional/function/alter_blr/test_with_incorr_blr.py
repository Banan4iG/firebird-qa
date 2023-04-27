#coding:utf-8

"""
ID:          function.alter_blr.with_incorr_blr
TITLE:       Alter function with incorrect BLR
DESCRIPTION:
FBTEST:      functional.function.alter_blr_with_incorr_blr
"""

import pytest
from firebird.qa import *

init_script = """
    SET TERM ^;
    CREATE FUNCTION BLR_FUNC 
    RETURNS integer
    AS
    BEGIN
        RETURN 5;
    END ^	
    SET TERM ;^
    commit;
"""

db = db_factory(init=init_script)

expected_stdout = """
Error: Error while parsing function BLR_FUNC's BLR
    -corrupt system table
    -unsupported BLR version (expected between 4 and 5, encountered 0)
RDB$FUNCTION_NAME: BLR_FUNC
RDB$FUNCTION_SOURCE:
BEGIN
    RETURN 5;
END
"""

act = python_act('db')

@pytest.mark.version('>=4.0')
def test_1(act: Action, capsys):
    with act.db.connect() as con:
        with con.cursor() as cur:
            try:
                cur.execute(f"alter function BLR_FUNC RETURNS integer as 'ABC'")
                con.commit()
            except Exception as e:
                print("Error:", e)
    
            con.rollback()	
            cur.execute("SELECT	rdb$function_name,rdb$function_source from rdb$functions where rdb$function_name = 'BLR_FUNC'")
            for range in cur.fetchall():
                print(f"RDB$FUNCTION_NAME: {range[0]}")
                print(f"RDB$FUNCTION_SOURCE:\n{range[1]}")

    act.expected_stdout = expected_stdout
    act.stdout = capsys.readouterr().out
    assert act.clean_stdout == act.clean_expected_stdout
