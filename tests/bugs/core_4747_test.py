#coding:utf-8

"""
ID:          issue-5052
ISSUE:       5052
TITLE:       Error "invalid BLOB ID" can occur when retrieving MON$STATEMENTS.MON$SQL_TEXT
  using ES/EDS and db_connect argument is not specified
DESCRIPTION:
JIRA:        CORE-4747
FBTEST:      bugs.core_4747
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    set list on;
    set blob all;

    recreate table test(sid int, tid int, txt blob);
    commit;

    -- NB, 21.05.2017: 4.0 Classic now has record in mon$statements with data from RDB$AUTH_MAPPING table.
    -- We have to prevent appearance of this row in resultset which is to be analyzed, thus adding clause:
    -- "where s.mon$sql_text containing 'test' ..."

    insert into test(sid, tid, txt) select s.mon$statement_id, s.mon$transaction_id, s.mon$sql_text from mon$statements s where s.mon$sql_text containing 'test' rows 1;
    commit;

    set term ^;
    execute block returns( msg varchar(10), running_stt_id int, running_trn_id int, running_stt_text blob) as
        declare v_dbname varchar(255);
        declare v_stt1 varchar(1024) = 'select t.sid, t.tid, t.txt from test t';
        declare v_stt2 varchar(1024) = 'select s.mon$statement_id, s.mon$transaction_id, s.mon$sql_text from mon$statements s where s.mon$sql_text containing ''test'' and s.mon$transaction_id = current_transaction rows 1';
        declare v_usr rdb$user = 'sysdba';
        declare v_pwd varchar(20) = 'masterkey';
        declare v_trn int;
    begin
        -- NOTE: v_dbname is NOT initialized with database connection string.

        msg = 'point-1';
        execute statement (v_stt1)
        on external (v_dbname)
        as user :v_usr password :v_pwd
        into running_stt_id, running_trn_id, running_stt_text;
        suspend;

        msg = 'point-2';
        execute statement (v_stt2)
        on external (v_dbname)
        as user :v_usr password :v_pwd
        into running_stt_id, running_trn_id, running_stt_text ;
        suspend;
    end
    ^
    set term ;^
    commit;
    --                                    ||||||||||||||||||||||||||||
    -- ###################################|||  FB 4.0+, SS and SC  |||##############################
    --                                    ||||||||||||||||||||||||||||
    -- If we check SS or SC and ExtConnPoolLifeTime > 0 (config parameter FB 4.0+) then current
    -- DB (bugs.core_NNNN.fdb) will be 'captured' by firebird.exe process and fbt_run utility
    -- will not able to drop this database at the final point of test.
    -- Moreover, DB file will be hold until all activity in firebird.exe completed and AFTER this
    -- we have to wait for <ExtConnPoolLifeTime> seconds after it (discussion and small test see
    -- in the letter to hvlad and dimitr 13.10.2019 11:10).
    -- This means that one need to kill all connections to prevent from exception on cleanup phase:
    -- SQLCODE: -901 / lock time-out on wait transaction / object <this_test_DB> is in use
    -- #############################################################################################
    delete from mon$attachments where mon$attachment_id != current_connection;
    commit;

"""

act = isql_act('db', test_script,
               substitutions=[('RUNNING_STT_ID[ ]+[0-9]+', 'RUNNING_STT_ID'),
                              ('RUNNING_TRN_ID[ ]+[0-9]+', 'RUNNING_TRN_ID'),
                              ('RUNNING_STT_TEXT.*', '')])

expected_stdout = """
    MSG                             point-1
    RUNNING_STT_ID                  111
    RUNNING_TRN_ID                  219
    RUNNING_STT_TEXT                91:0
    insert into test(sid, tid, txt) select s.mon$statement_id, s.mon$transaction_id, s.mon$sql_text from mon$statements s where s.mon$sql_text containing 'test' rows 1

    MSG                             point-2
    RUNNING_STT_ID                  140
    RUNNING_TRN_ID                  224
    RUNNING_STT_TEXT                0:1
    select s.mon$statement_id, s.mon$transaction_id, s.mon$sql_text from mon$statements s where s.mon$sql_text containing 'test' and s.mon$transaction_id = current_transaction rows 1
"""

@pytest.mark.version('>=3')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

