#coding:utf-8

"""
ID:          function.create_blr.with_incorr_inparam
TITLE:       Create function with incorrect input parameters
DESCRIPTION:
FBTEST:      functional.function.create_blr_with_incorr_inparam
"""

import pytest
from firebird.qa import *

init_script = """
    SET TERM ^;
    CREATE FUNCTION TEST_FUNC(
        p1 SMALLINT, p2 INTEGER, p3 FLOAT, p4 DOUBLE PRECISION, p5 DECIMAL(9,3), p6 NUMERIC(10,4),
        p7 DATE, p8 TIME, p9 TIMESTAMP, p10 CHAR(40), p11 VARCHAR(60), p12 NCHAR(70))
    RETURNS int	
    AS
    BEGIN
        POST_EVENT 'Test';
        RETURN p4;
    END ^
    SET TERM ;^
    commit;
"""

db = db_factory(init=init_script)

expected_exception = """
Error while parsing function BLR_FUNC's BLR
-corrupt system table
"""

act = python_act('db')

@pytest.mark.version('>=4.0')
def test_1(act: Action):
    with act.db.connect() as con:
        with con.cursor() as cur:
            with pytest.raises(Exception) as ex:
                cur.execute("SELECT	base64_encode(rdb$function_blr) from rdb$functions where rdb$function_name = 'TEST_FUNC'")
                for row in cur.fetchall():
                    cur.execute(f"create function BLR_FUNC (p2 INTEGER, p3 FLOAT, p4 DOUBLE PRECISION, p5 DECIMAL(9,3), p6 NUMERIC(10,4), p7 DATE, p8 TIME, p9 TIMESTAMP, p10 CHAR(40), p11 VARCHAR(60), p12 NCHAR(70)) RETURNS int as '{row[0]}'")
                    con.commit()
                    cur.execute("SELECT	rdb$function_name,rdb$function_source, base64_encode(rdb$function_blr) from rdb$functions where rdb$function_name = 'BLR_FUNC'")
                    cur.fetchall()

    act.expected_stdout = expected_exception
    act.stdout = str(ex.value)
    assert act.clean_stdout == act.clean_expected_stdout
