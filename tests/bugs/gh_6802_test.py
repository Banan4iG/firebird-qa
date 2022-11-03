#coding:utf-8

"""
ID:          issue-6802
ISSUE:       6802
TITLE:       When the statement timeout is set, it causes the lock manager to delay
  reporting deadlocks until timeout is expired
DESCRIPTION:
NOTES:
[20.05.2021]
  adjusted expected_stderr for case-2: non-suppressed exception raises instead of issuing gdscode.
FBTEST:      bugs.gh_6802
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    set list on;
    recreate global temporary table gt(f01 int) on commit preserve rows;
    commit;
    insert into gt values(1);
    commit;
    set term ^;
    create or alter procedure sp_test_waiting_time( a_expected_wait int ) returns(was_waiting_acceptable varchar(100)) as
    begin
        for
            select iif( waited_for_sec between expected_wait and expected_wait + 1
                        ,'Acceptable.'
                        ,'NO, UNEXPECTED: ' || waited_for_sec || ' - out of scope: ' || expected_wait || '...' || (expected_wait+1)
                      )
            from (
                select
                    datediff(second from cast( rdb$get_context('USER_SESSION', 'DTS_BEG') as timestamp) to cast('now' as timestamp)) as waited_for_sec
                   ,:a_expected_wait as expected_wait
                --  ^^
                -- #################################################
                -- ### EXPECTED TIME TO WAIT FOR LOCK RESOLUTION ###
                -- #################################################
                from rdb$database
            )
        into was_waiting_acceptable
        do
            suspend;
    end
    ^
    set term ;^
    commit;

    -- set echo on;

    -- ####################### 
    -- ###  c a s e   N 2  ###
    -- ####################### 
    -- Initial state:
    --    * statement_timeout < deadlocktimeout
    --    * Tx lock resolution = WAIT
    -- Expected result:
    --    * non-supressed exception "SQLSTATE = HY008 / operation was cancelled / -Attachment level timeout expired."
    --      ::: NOTE ::: EXCEPTION 'operation was cancelled' (isc_cancelled, gds = 335544794) can not be supressed in when-block!
    --      See letter from Vlad, 15.05.2021 19:42.
    --      NB:  gdscode = 335544336 issued on console on 5.0.0.29, but on 5.0.0.43 it is not so.
    --    * waiting for 4..5 sec (i.e. <StatementTimeout> seconds rather than DeadLockTimeout);

    SET STATEMENT TIMEOUT 4 second;
    commit;

    set transaction read write read committed record_version;

    delete from gt;
    set term ^;
    execute block returns(raised_gds_02 int) as
    begin
        rdb$set_context('USER_SESSION','DTS_BEG', cast('now' as timestamp));
        begin
            in autonomous transaction
            do update gt set f01=-1;

        when any do
            begin
                raised_gds_02 = gdscode;
            end
        end

        suspend;
    end
    ^
    set term ;^
    select was_waiting_acceptable as waiting_time_02 from sp_test_waiting_time( cast(rdb$get_context('SYSTEM', 'STATEMENT_TIMEOUT') as int) / 1000 );
    rollback;
"""

act = isql_act('db', test_script, substitutions=[('[ \t]+', ' ')])

expected_stdout = """
    WAITING_TIME_02                 Acceptable.
"""

expected_stderr = """
    Statement failed, SQLSTATE = HY008
    operation was cancelled
    -Attachment level timeout expired.
"""

@pytest.mark.version('>=5.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.expected_stderr = expected_stderr
    act.execute()
    assert (act.clean_stderr == act.clean_expected_stderr and
            act.clean_stdout == act.clean_expected_stdout)
