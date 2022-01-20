#coding:utf-8

"""
ID:          issue-1517
ISSUE:       1517
TITLE:       Support BETWEEN predicate for select expressions
DESCRIPTION:
JIRA:        CORE-1095
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    set sqlda_display on;
    set planonly;
    -- Before 3.0.2 following statement failed with:
    -- Statement failed, SQLSTATE = HY004
    -- Unsupported field type specified in BETWEEN predicate.
    select 3 from rdb$database r_out where ((select count(*) from rdb$database r_chk) between ? and ?);

    ----------------------------------------------------------

    -- Following sample is from CORE-5596 (added 22.11.2017).
    -- On 2.5.x it issues:
    --   Statement failed, SQLSTATE = XX000
    --   internal Firebird consistency check ((CMP) copy: cannot remap (221), file: cmp.cpp line: 3091)
    select 1
    from rdb$database
    where
        iif(
             exists( select 1 from rdb$database )
           , 0e0
           , 0e0
           )
        between ? and ?
    ;
"""

act = isql_act('db', test_script)

expected_stdout = """
    INPUT message field count: 2
    01: sqltype: 580 INT64 Nullable scale: 0 subtype: 0 len: 8
      :  name:   alias:
      : table:   owner:
    02: sqltype: 580 INT64 Nullable scale: 0 subtype: 0 len: 8
      :  name:   alias:
      : table:   owner:

    PLAN (R_CHK NATURAL)
    PLAN (R_CHK NATURAL)
    PLAN (R_OUT NATURAL)

    OUTPUT message field count: 1
    01: sqltype: 496 LONG scale: 0 subtype: 0 len: 4
      :  name: CONSTANT  alias: CONSTANT
      : table:   owner:



    INPUT message field count: 2
    01: sqltype: 480 DOUBLE scale: 0 subtype: 0 len: 8
      :  name:   alias:
      : table:   owner:
    02: sqltype: 480 DOUBLE scale: 0 subtype: 0 len: 8
      :  name:   alias:
      : table:   owner:

    PLAN (RDB$DATABASE NATURAL)
    PLAN (RDB$DATABASE NATURAL)
    PLAN (RDB$DATABASE NATURAL)

    OUTPUT message field count: 1
    01: sqltype: 496 LONG scale: 0 subtype: 0 len: 4
      :  name: CONSTANT  alias: CONSTANT
      : table:   owner:

"""

@pytest.mark.version('>=3.0.2')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

