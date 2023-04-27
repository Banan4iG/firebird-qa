#coding:utf-8

"""
ID:          function.create_blr.with_same_name
TITLE:       Create function with the same name
DESCRIPTION:
FBTEST:      functional.function.create_blr_with_same_name
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
        return 15;
    END ^
    SET TERM ;^
"""

db = db_factory(init=init_script)

expected_exception = """
unsuccessful metadata update
-CREATE FUNCTION TEST_FUNC failed
-Function TEST_FUNC already exists
"""

act = python_act('db')

@pytest.mark.version('>=4.0')
def test_1(act: Action):
    with act.db.connect() as con:
        with con.cursor() as cur:
            with pytest.raises(Exception) as ex:
                cur.execute("SELECT	base64_encode(rdb$function_blr) from rdb$functions where rdb$function_name = 'TEST_FUNC'")
                for row in cur.fetchall():
                    cur.execute("create function TEST_FUNC RETURNS float as '%s'"%row[0])
                    con.commit()

    act.expected_stdout = expected_exception
    act.stdout = str(ex.value)
    assert act.clean_stdout == act.clean_expected_stdout