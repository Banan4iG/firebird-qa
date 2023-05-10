#coding:utf-8

"""
ID:          function.alter_blr.without_encode
TITLE:       Alter function without encode
DESCRIPTION:
FBTEST:      functional.function.alter_blr_without_encode
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
        return 10;
    END ^
    
    CREATE FUNCTION BLR_FUNC 
    RETURNS date
    AS
    BEGIN
        RETURN '10.11.2007';
    END ^
    SET TERM ;^
    commit;
"""

db = db_factory(init=init_script)

expected_stdout = """
RDB$FUNCTION_NAME: BLR_FUNC
RDB$FUNCTION_SOURCE:
BEGIN
RETURN '10.11.2007';
END
"""

expected_stderr = """
Error while parsing function BLR_FUNC's BLR
-corrupt system table
-unsupported BLR version (expected between 4 and 5, encountered 199)
"""

act = python_act('db')

#@pytest.mark.skip('FIXME: system table corrupt after alter function')
@pytest.mark.version('>=4.0')
def test_1(act: Action, capsys):
    with act.db.connect() as con:
        with con.cursor() as cur:
            with pytest.raises(Exception) as ex:
                cur.execute("SELECT rdb$function_blr from rdb$functions where rdb$function_name = 'TEST_FUNC';")
                for row in cur.fetchall():
                    blr = str(row[0])[2:-2]     # Trim b-prefix
                    cur.execute(f"alter function BLR_FUNC RETURNS integer as '{blr}'")
                    con.commit()
    
    with act.db.connect() as con:
        with con.cursor() as cur:
            cur.execute("SELECT rdb$function_name,rdb$function_source from rdb$functions where rdb$function_name = 'BLR_FUNC'")
            for range in cur.fetchall():
                print(f"RDB$FUNCTION_NAME: {range[0]}")
                print(f"RDB$FUNCTION_SOURCE:\n{range[1]}")

    act.expected_stderr = expected_stderr
    act.expected_stdout = expected_stdout
    act.stderr = str(ex.value)
    act.stdout = capsys.readouterr().out
    assert act.clean_stderr == act.clean_expected_stderr
    assert act.clean_stdout == act.clean_expected_stdout   
