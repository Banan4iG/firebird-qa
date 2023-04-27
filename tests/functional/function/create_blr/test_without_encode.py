#coding:utf-8

"""
ID:          function.create_blr.without_encode
TITLE:       Create function without encode
DESCRIPTION:
FBTEST:      functional.function.create_blr_without_encode
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
        RETURN 171;
    END ^
    SET TERM ;^
    commit;
"""

db = db_factory(init=init_script)

expected_exception = """
unsuccessful metadata update
-CREATE FUNCTION BLR_FUNC failed
-Error while parsing function BLR_FUNC's BLR
"""

act = python_act('db')

@pytest.mark.version('>=4.0')
def test_1(act: Action):

    with act.db.connect() as con:
        with con.cursor() as cur:
            with pytest.raises(Exception) as ex:
                cur.execute("SELECT rdb$function_blr from rdb$functions where rdb$function_name = 'TEST_FUNC';")
                for row in cur.fetchall():
                    blr = str(row[0])[2:-2]     # Trim b-prefix
                    cur.execute(f"create function BLR_FUNC RETURNS integer as '{blr}'")
                    con.commit()

    act.expected_stdout = expected_exception
    act.stdout = str(ex.value)
    assert act.clean_stdout == act.clean_expected_stdout
    