#coding:utf-8

"""
ID:          decfloat.literal-interpretation
ISSUE:       5803
JIRA:        CORE-5535
TITLE:       Test interpretation of numeric literals
DESCRIPTION:
  When literal can not be fit in any of "pre-4.0" then DECFLOAT should be considered as DECFLOAT(34)
  See  doc/sql.extensions/README.data_types
  See also letter from Alex, 24.05.2017 19:28.

  Currently only double precision form of literals is checked.
  Literals with value out bigint scope are not checked - waiting for reply from Alex, letter 24.05.2017 21:16
FBTEST:      functional.datatypes.decfloat_literal_interpr
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    set list on;
    set sqlda_display on;

    select
        1e-308 as almost_zero_double_precision
    from rdb$database; -- ==> 9.999999999999999e-309 -- this is still DP

    select
        1e-309 as almost_zero_decfloat_34
    from rdb$database; -- ==> FAILS on 3.0; must be interpreted as DECFLOAT(34) on 4.0.0

    /*
    --- todo later! waiting for reply from Alex, letter 24.05.2017 21:16
    select
        -9223372036854775809 as behind_bigint_max
        ,9223372036854775808 as behind_bigint_min
    from rdb$database; -- ==> FAILS on 3.0; must be interpreted as DECFLOAT(34) on 4.0.0
    */
"""

act = isql_act('db', test_script)

expected_stdout = """
    INPUT message field count: 0
    OUTPUT message field count: 1
    01: sqltype: 480 DOUBLE scale: 0 subtype: 0 len: 8
    :  name: CONSTANT  alias: ALMOST_ZERO_DOUBLE_PRECISION
    : table:   owner:
    ALMOST_ZERO_DOUBLE_PRECISION    9.999999999999999e-309
    INPUT message field count: 0
    OUTPUT message field count: 1
    01: sqltype: 32762 DECFLOAT(34) scale: 0 subtype: 0 len: 16
    :  name: CONSTANT  alias: ALMOST_ZERO_DECFLOAT_34
    : table:   owner:
    ALMOST_ZERO_DECFLOAT_34                                             1E-309
"""

@pytest.mark.version('>=4.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
