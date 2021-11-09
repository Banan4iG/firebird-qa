#coding:utf-8
#
# id:           bugs.core_5225
# title:        Authentication end with first plugin that has the user but auth fails; should continue with next plugin
# decription:
#                   We create two users with the same name, 1st using plugin Srp, 2nd - via Legacy.
#                   Then we try to establish subsequent attachments via ES/EDS for each of them.
#                   No error should occur.
#
#                   Confirmed exception on 3.0.0 for plugin that was specified as SECOND in firebird.conf, got:
#                       Statement failed, SQLSTATE = 42000
#                       Execute statement error at attach :
#                       335544472 : Your user name and password are not defined <...>
#                   [pcisar] 03.11.2021 The same error raised by 4.0 on Windows and Linux
#
#                   Works fine on:
#                     fb30Cs, build 3.0.4.32947: OK, 2.907s.
#                     FB30SS, build 3.0.4.32963: OK, 1.140s.
#                     FB40CS, build 4.0.0.955: OK, 3.531s.
#                     FB40SS, build 4.0.0.967: OK, 1.312s.
#
# tracker_id:   CORE-5225
# min_versions: ['3.0.1']
# versions:     3.0.1
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 3.0.1
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """
    set list on;

    create or alter user tmp$c5225 password 'srp' using plugin Srp;
    create or alter user tmp$c5225 password 'leg' using plugin Legacy_UserManager;
    commit;

    set term ^;
    execute block returns(whoami_leg varchar(31)) as
    begin
       execute statement 'select current_user from rdb$database'
       on external 'localhost:' || rdb$get_context('SYSTEM','DB_NAME')
       as user 'tmp$c5225' password 'leg'
       into whoami_leg;
       suspend;
    end
    ^
    set term ;^
    commit;

    set term ^;
    execute block returns(whoami_srp varchar(31)) as
    begin
       execute statement 'select current_user from rdb$database'
       on external 'localhost:' || rdb$get_context('SYSTEM','DB_NAME')
       as user 'tmp$c5225' password 'srp'
       into whoami_srp;
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

    drop user tmp$c5225 using plugin Srp;
    drop user tmp$c5225 using plugin Legacy_UserManager;
    commit;

  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    WHOAMI_LEG                      TMP$C5225
    WHOAMI_SRP                      TMP$C5225
  """

@pytest.mark.version('>=3.0.1')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout

