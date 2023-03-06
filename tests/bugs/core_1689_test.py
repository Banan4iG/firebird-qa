#coding:utf-8

"""
ID:          issue-2115
ISSUE:       2115
TITLE:       'There are <n> dependencies' error message shows the wrong count of dependent objects.
DESCRIPTION:
    [6.03.2023] Zuev
    Disable the test for RDB3 because it requires UDF removed from installers.
JIRA:        CORE-1689
FBTEST:      bugs.core_1689
"""

import pytest
from firebird.qa import *

# version: 3.0

init_script_1 = """
    set term ^;
    declare external function UDF30_getExactTimestamp
      timestamp
      returns parameter 1
      entry_point 'getExactTimestamp' module_name 'fbudf'^

    create table t(a int)^
    create trigger tad for t after delete as declare dummy timestamp; begin dummy = UDF30_getExactTimestamp(); end^
    create view vudf(t) as select UDF30_getExactTimestamp() from rdb$database^
    create table tudf(a int, c computed by(UDF30_getExactTimestamp()))^
    create domain dud int check(value between extract(week from UDF30_getExactTimestamp()) and 25)^
"""

db_1 = db_factory(init=init_script_1)

test_script_1 = """
    drop external function UDF30_getExactTimestamp;
"""

act_1 = isql_act('db_1', test_script_1)

expected_stderr_1 = """
    Statement failed, SQLSTATE = 38000
    unsuccessful metadata update
    -cannot delete
    -Function UDF30_GETEXACTTIMESTAMP
    -there are 4 dependencies
"""

@pytest.mark.skip("DISABLED: see notes")
@pytest.mark.version('>=3.0,<4.0')
def test_1(act_1: Action):
    act_1.expected_stderr = expected_stderr_1
    act_1.execute()
    assert act_1.clean_stderr == act_1.clean_expected_stderr

# version: 4.0

db_2 = db_factory()

test_script_2 = """
    -- See declaration sample in plugins\\udr\\UdfBackwardCompatibility.sql:
    set bail on;
    create function UDR40_getExactTimestampUTC
    returns timestamp
    external name 'udf_compat!UC_getExactTimestampUTC'
    engine udr;

    create table test_dts(
        id int,
        dts timestamp check ( datediff(minute from dts to UDR40_getExactTimestampUTC()) < 5 )
    );
    commit;

    set term ^;
    create trigger trg_test_dts_ad for test_dts after delete as
        declare dummy timestamp;
    begin
        dummy = UDR40_getExactTimestampUTC();
    end
    ^
    set term ;^
    commit;



    create view v_test as
    select UDR40_getExactTimestampUTC() as UTC_stamp  -- rdb$N, dep_type=3
    from rdb$database
    ;


    create table test_udr(a int, c computed by( UDR40_getExactTimestampUTC() )) -- rdb$N, dep_type=3
    ;

    create domain dm_test int check(value between extract(week from UDR40_getExactTimestampUTC() ) and 25) ;

    commit;

    drop function UDR40_getExactTimestampUTC;

    /*
    set count on;
    set list on;
    select rd.rdb$dependent_name, rd.rdb$dependent_type
    from rdb$dependencies rd
    where rd.rdb$depended_on_name = upper('UDR40_GETEXACTTIMESTAMPUTC')
    order by rd.rdb$dependent_name
    ;
    */
"""

act_2 = isql_act('db_2', test_script_2)

expected_stderr_2 = """
    Statement failed, SQLSTATE = 38000
    unsuccessful metadata update
    -cannot delete
    -Function UDR40_GETEXACTTIMESTAMPUTC
    -there are 6 dependencies
"""

@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stderr = expected_stderr_2
    act_2.execute()
    assert act_2.clean_stderr == act_2.clean_expected_stderr

