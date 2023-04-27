#coding:utf-8

"""
ID:          function.create_blr.with_incorr_blr
TITLE:       Create function with incorrect BLR
DESCRIPTION:
FBTEST:      functional.function.create_blr_with_incorr_blr
"""

import pytest
from firebird.qa import *

db = db_factory()

expected_exception = """
Error while parsing function BLR_FUNC's BLR
-corrupt system table
-unsupported BLR version (expected between 4 and 5, encountered 0)
"""

act = python_act('db')

@pytest.mark.version('>=4.0')
def test_1(act: Action):
    with act.db.connect() as con:
        with con.cursor() as cur:
            with pytest.raises(Exception) as ex:
                cur.execute("create function BLR_FUNC returns int as 'ABC'")
                con.commit()

    act.expected_stdout = expected_exception
    act.stdout = str(ex.value)
    assert act.clean_stdout == act.clean_expected_stdout
