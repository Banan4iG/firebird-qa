#coding:utf-8

"""
ID:          intfunc.date.dateadd-02
TITLE:       DATEADD function for MONTH
DESCRIPTION:
  Returns a date/time/timestamp value increased (or decreased, when negative) by the specified amount of time.
FBTEST:      functional.intfunc.date.dateadd_02
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """

    -- doc\\sql.extensions\\README.builtin_functions.txt
    -- 5) When using YEAR or MONTH and the input day is greater than the maximum possible day in the
    --    result year/month, the result day is returned in the last day of the result year/month.

    set list on;

    select dateadd(  1 month to date '2004-01-31') as leap_jan_31_plus__01_month from rdb$database;
    select dateadd(  1 month to date '2004-02-28') as leap_feb_28_plus__01_month from rdb$database;
    select dateadd(  1 month to date '2004-02-29') as leap_feb_29_plus__01_month from rdb$database;
    select dateadd( -1 month to date '2004-02-28') as leap_feb_28_minus_01_month from rdb$database;
    select dateadd( -1 month to date '2004-02-29') as leap_feb_29_minus_01_month from rdb$database;
    select dateadd( 11 month to date '2004-02-28') as leap_feb_28_plus__11_month from rdb$database;
    select dateadd( 11 month to date '2004-02-29') as leap_feb_29_plus__11_month from rdb$database;
    select dateadd( 12 month to date '2004-02-28') as leap_feb_28_plus__12_month from rdb$database;
    select dateadd( 12 month to date '2004-02-29') as leap_feb_29_plus__12_month from rdb$database;
    select dateadd(-11 month to date '2004-02-28') as leap_feb_28_minus_11_month from rdb$database;
    select dateadd(-11 month to date '2004-02-29') as leap_feb_29_minus_11_month from rdb$database;
    select dateadd(-12 month to date '2004-02-28') as leap_feb_28_minus_12_month from rdb$database;
    select dateadd(-12 month to date '2004-02-29') as leap_feb_29_minus_12_month from rdb$database;
    select dateadd( -1 month to date '2004-03-31') as leap_mar_31_minus_01_month from rdb$database;

    select dateadd(  1 month to date '2003-01-31') as nonl_jan_31_plus__01_month from rdb$database;
    select dateadd(  1 month to date '2003-02-28') as nonl_feb_28_plus__01_month from rdb$database;
    select dateadd( -1 month to date '2003-02-28') as nonl_feb_28_minus_01_month from rdb$database;
    select dateadd( 11 month to date '2003-02-28') as nonl_feb_28_plus__11_month from rdb$database;
    select dateadd( 12 month to date '2003-02-28') as nonl_feb_28_plus__12_month from rdb$database;
    select dateadd(-11 month to date '2003-02-28') as nonl_feb_28_minus_11_month from rdb$database;
    select dateadd(-12 month to date '2003-02-28') as nonl_feb_28_minus_12_month from rdb$database;
    select dateadd( -1 month to date '2003-03-31') as nonl_mar_31_minus_01_month from rdb$database;

    -- old test code:
    -- select dateadd(-1 month TO date '2008-02-06' ) as yesterday from rdb$database;
    -- select dateadd(month,-1, date '2008-02-06' ) as yesterday from rdb$database;
"""

act = isql_act('db', test_script)

expected_stdout = """
    LEAP_JAN_31_PLUS__01_MONTH      2004-02-29
    LEAP_FEB_28_PLUS__01_MONTH      2004-03-28
    LEAP_FEB_29_PLUS__01_MONTH      2004-03-29
    LEAP_FEB_28_MINUS_01_MONTH      2004-01-28
    LEAP_FEB_29_MINUS_01_MONTH      2004-01-29
    LEAP_FEB_28_PLUS__11_MONTH      2005-01-28
    LEAP_FEB_29_PLUS__11_MONTH      2005-01-31
    LEAP_FEB_28_PLUS__12_MONTH      2005-02-28
    LEAP_FEB_29_PLUS__12_MONTH      2005-02-28
    LEAP_FEB_28_MINUS_11_MONTH      2003-03-28
    LEAP_FEB_29_MINUS_11_MONTH      2003-03-29
    LEAP_FEB_28_MINUS_12_MONTH      2003-02-28
    LEAP_FEB_29_MINUS_12_MONTH      2003-02-28
    LEAP_MAR_31_MINUS_01_MONTH      2004-02-29

    NONL_JAN_31_PLUS__01_MONTH      2003-02-28
    NONL_FEB_28_PLUS__01_MONTH      2003-03-28
    NONL_FEB_28_MINUS_01_MONTH      2003-01-28
    NONL_FEB_28_PLUS__11_MONTH      2004-01-28
    NONL_FEB_28_PLUS__12_MONTH      2004-02-28
    NONL_FEB_28_MINUS_11_MONTH      2002-03-28
    NONL_FEB_28_MINUS_12_MONTH      2002-02-28
    NONL_MAR_31_MINUS_01_MONTH      2003-02-28
"""

@pytest.mark.version('>=3')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
