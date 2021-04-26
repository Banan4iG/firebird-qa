#coding:utf-8
#
# id:           bugs.core_5495
# title:        New users or changed passwords in legacy authentication do not work in Firebird 4
# decription:   
#                   Confirmed bug on WI-T4.0.0.546, got:
#                      Statement failed, SQLSTATE = 28000
#                      Your user name and password are not defined. Ask your database administrator <...>
#                   Used config:
#                      AuthServer = Legacy_Auth,Srp
#                      AuthClient = Legacy_Auth,Srp,Win_Sspi
#                      WireCrypt = Disabled
#                      UserManager = Srp, Legacy_UserManager
#                   Checked on WI-T4.0.0.549 - works fine.
#                
# tracker_id:   CORE-5495
# min_versions: ['4.0']
# versions:     4.0
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 4.0
# resources: None

substitutions_1 = [('TCPv.*', 'TCP')]

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """
    set list on;
    set bail on;
    create user tmp$c5495 password '123' using plugin Legacy_UserManager;
    commit;
    connect '$(DSN)' user tmp$c5495 password '123';
    --select mon$user,mon$remote_address,mon$remote_protocol,mon$client_version,mon$remote_version,mon$auth_method from mon$attachments 
    select mon$user,mon$remote_protocol,mon$auth_method from mon$attachments 
    where mon$attachment_id=current_connection;
    commit;
    connect '$(DSN)' user SYSDBA password 'masterkey';
    commit;
    drop user tmp$c5495 using plugin Legacy_UserManager;
    commit;
  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
     MON$USER                        TMP$C5495
     MON$REMOTE_PROTOCOL             TCP
     MON$AUTH_METHOD                 Legacy_Auth
  """

@pytest.mark.version('>=4.0')
def test_core_5495_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout

