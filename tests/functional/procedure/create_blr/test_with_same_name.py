#coding:utf-8

"""
ID:          procedure.create_blr.with_same_name
TITLE:       Create procedure with the same name
DESCRIPTION:
FBTEST:      functional.procedure.create_blr_with_same_name
"""

import pytest
from firebird.qa import *

init_script = """
    SET TERM ^;
    CREATE PROCEDURE TEST_PROC AS
    BEGIN
        POST_EVENT 'Test';
    END ^
    SET TERM ;^
    commit;
"""

db = db_factory(init=init_script)

expected_exception = """
unsuccessful metadata update
-CREATE PROCEDURE TEST_PROC failed
-Procedure TEST_PROC already exists
"""

act = python_act('db')

@pytest.mark.version('>=4.0')
def test_1(act: Action):
    with act.db.connect() as con:
        with con.cursor() as cur:
            with pytest.raises(Exception) as ex:
                cur.execute("SELECT base64_encode(rdb$procedure_blr) from rdb$procedures where rdb$procedure_name = 'TEST_PROC'")
                for row in cur.fetchall():
                    cur.execute("create procedure TEST_PROC as '%s'"%row[0])
                    con.commit()

    act.expected_stdout = expected_exception
    act.stdout = str(ex.value)
    assert act.clean_stdout == act.clean_expected_stdout