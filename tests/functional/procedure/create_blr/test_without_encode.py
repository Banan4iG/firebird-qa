#coding:utf-8

"""
ID:          procedure.create_blr.without_encode
TITLE:       Create procedure without encode
DESCRIPTION:
FBTEST:      functional.procedure.create_blr_without_encode
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
-CREATE PROCEDURE BLR_PROC failed
-Error while parsing procedure BLR_PROC's BLR
"""

act = python_act('db')

@pytest.mark.version('>=4.0')
def test_1(act: Action):

    with act.db.connect() as con:
        with con.cursor() as cur:
            with pytest.raises(Exception) as ex:
                cur.execute("SELECT rdb$procedure_blr from rdb$procedures where rdb$procedure_name = 'TEST_PROC'")
                for row in cur.fetchall():
                    blr = str(row[0])[2:-2]     # Trim b-prefix
                    cur.execute(f"create procedure BLR_PROC as '{blr}'")
                    con.commit()

    act.expected_stdout = expected_exception
    act.stdout = str(ex.value)
    assert act.clean_stdout == act.clean_expected_stdout
    