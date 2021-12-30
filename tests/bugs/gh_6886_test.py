#coding:utf-8
#
# id:           bugs.gh_6886
# title:        Differerent interfaces behaviour depending upon source of interface
# decription:   
#                   https://github.com/FirebirdSQL/firebird/issues/6886
#               
#                   Appearance of this bug was received accidentally during implemenation of test for completely unrelated issue (gh-6935).
#                   First message about presence of query to RDB$AUTH_MAPPING in MON$STATEMENTS was sent to Alex, see letter 02-sep-2021 07:19.
#                   Only FB 4.0.1 Classic was affected. There was no problem with FB 3.x and 5.x.
#               
#                   After some additional discussion it was concluded that apropriate script can serve as test for:
#                       https://github.com/FirebirdSQL/firebird/commit/11712f82039cb0318140593f433019297ae07407
#                       Branch: refs/heads/v4.0-release, 15.09.2021 17:41:
#                       "Fixed #6886: Differerent interfaces behaviour depending upon source of interface"
#               
#                   Confirmed bug on 4.0.1.2592 CS (15.09.2021): got 1 record from mon$statements with following content:
#                       ATT_ID                          3
#                       ATT_USER                        SYSDBA
#                       SQL_TEXT_BLOB_ID                0:1
#                       SELECT RDB$MAP_USING, RDB$MAP_PLUGIN, RDB$MAP_DB, RDB$MAP_FROM_TYPE,  RDB$MAP_FROM, RDB$MAP_TO_TYPE, RDB$MAP_TO FROM RDB$AUTH_MAPPING
#                       STTM_STATE                      0
#                       Records affected: 1
#               
#                   Checked 4.0.1.2602, 5.0.0.215 -- all OK, no records foudn in mon$statements.
#                
# tracker_id:   
# min_versions: ['4.0.1']
# versions:     4.0.1
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 4.0.1
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """
    set list on;
    set count on;

    commit;
    connect '$(DSN)' user sysdba password 'masterkey';
     
    set term ^;
    execute block returns(
         att_id type of column mon$attachments.mon$attachment_id
        ,att_user type of column mon$attachments.mon$user
        ,sql_text_blob_id type of column mon$statements.mon$sql_text
        ,sttm_state type of column mon$statements.mon$state
    ) as
    begin
        for
            execute statement (
                q'{
                    select a.mon$attachment_id,a.mon$user, s.mon$sql_text, s.mon$state
                    from mon$attachments a
                    join mon$statements s using(mon$attachment_id)
                    where
                        s.mon$attachment_id <> current_connection
                        and s.mon$sql_text not containing 'execute block'
                }'
            ) on external
                'localhost:' || rdb$get_context('SYSTEM', 'DB_NAME')
                as user 'SYSDBA' password 'masterkey' role left('R' || replace(uuid_to_char(gen_uuid()),'-',''),31)
        into
            att_id, att_user, sql_text_blob_id, sttm_state
        do
            suspend;
    end
    ^
    set term ;^
    commit;

    ALTER EXTERNAL CONNECTIONS POOL CLEAR ALL; -- !! mandatory otherwise database file will be kept by engine and fbtest will not able to drop it !!
    commit;
"""

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    Records affected: 0
"""

@pytest.mark.version('>=4.0.1')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_stdout == act_1.clean_expected_stdout
