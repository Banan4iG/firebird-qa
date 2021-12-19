#coding:utf-8
#
# id:           bugs.core_0885
# title:        It is impossible to take away rights on update of a column
# decription:
# tracker_id:   CORE-885
# min_versions: ['3.0']
# versions:     3.0
# qmid:

import pytest
from firebird.qa import db_factory, isql_act, Action, user_factory, User, role_factory, Role

# version: 3.0
# resources: None

substitutions_1 = [('-Effective user is.*', '')]

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """
    set wng off;
    set list on;

    recreate table test(id int, text varchar(30), changed_by_user varchar(31), changed_by_role varchar(31));
    commit;

    set term ^;
    create trigger test_biu for test active before insert or update position 0 as
    begin
        new.changed_by_user = current_user;
        new.changed_by_role = current_role;
    end
    ^
    set term ;^
    commit;

    insert into test(id, text) values(1, 'Initial data, added by SYSDBA');
    insert into test(id, text) values(2, 'Initial data, added by SYSDBA');
    insert into test(id, text) values(3, 'Initial data, added by SYSDBA');
    select * from test;
    commit;

    grant select on test to public;
    grant create role to john_senior;
    grant update(text) on test to john_senior with grant option;
    commit;

    ----------------------------------------

    --set echo on;
    --show grants;
    connect '$(DSN)' user 'JOHN_SENIOR' password 'sen';
    create role modifier;
    commit;
    grant update (text) on test to modifier; -- this CAN be done by john_senior because he was granted to control access on this field
    grant modifier to mick_junior; -- this CAN be done by john_senior because he CREATED role 'modifier' and thus he is MEMBER of it.
    commit;
    --show grants;

    connect '$(DSN)' user 'MICK_JUNIOR' password 'jun' role 'MODIFIER';
    select current_user, current_role from rdb$database;
    update test set text = 'Update-1: through the ROLE' where id = 1;
    select * from test;

    commit;

    connect '$(DSN)' user 'JOHN_SENIOR' password 'sen';
    select current_user, current_role from rdb$database;
    update test set text = 'Update-2: directly by USER' where id = 2;
    select * from test;
    commit;

    connect '$(DSN)' user 'JOHN_SENIOR' password 'sen';

    -- ###########################################################################################
    -- ###   H e r e    w e    R E V O K E    r i g h t   t o    u p d a t e     c o l u m n   ###
    -- ###########################################################################################
    -- ::: NB ::: See CORE-4836:
    -- As of WI-T3.0.0.31873, if we want to revoke privilege on certain COLUMN update, we must do
    -- it immediatelly after reconnect, NO issuing any DML here (like `select * from test` etc).

    revoke update(text) on test from modifier; -------------  ###########   R E V O K E   ########
    commit;

    connect '$(DSN)' user 'MICK_JUNIOR' password 'jun' role 'MODIFIER';
    select current_user, current_role from rdb$database;
    update test set text = 'Update-3: again using ROLE' where id = 3;
    select * from test;

    commit;

    connect '$(DSN)' user 'SYSDBA' password 'masterkey';

    --drop role modifier;
    drop table test;
    commit;
  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    ID                              1
    TEXT                            Initial data, added by SYSDBA
    CHANGED_BY_USER                 SYSDBA
    CHANGED_BY_ROLE                 NONE
    ID                              2
    TEXT                            Initial data, added by SYSDBA
    CHANGED_BY_USER                 SYSDBA
    CHANGED_BY_ROLE                 NONE
    ID                              3
    TEXT                            Initial data, added by SYSDBA
    CHANGED_BY_USER                 SYSDBA
    CHANGED_BY_ROLE                 NONE


    USER                            MICK_JUNIOR
    ROLE                            MODIFIER
    ID                              1
    TEXT                            Update-1: through the ROLE
    CHANGED_BY_USER                 MICK_JUNIOR
    CHANGED_BY_ROLE                 MODIFIER
    ID                              2
    TEXT                            Initial data, added by SYSDBA
    CHANGED_BY_USER                 SYSDBA
    CHANGED_BY_ROLE                 NONE
    ID                              3
    TEXT                            Initial data, added by SYSDBA
    CHANGED_BY_USER                 SYSDBA
    CHANGED_BY_ROLE                 NONE

    USER                            JOHN_SENIOR
    ROLE                            NONE
    ID                              1
    TEXT                            Update-1: through the ROLE
    CHANGED_BY_USER                 MICK_JUNIOR
    CHANGED_BY_ROLE                 MODIFIER
    ID                              2
    TEXT                            Update-2: directly by USER
    CHANGED_BY_USER                 JOHN_SENIOR
    CHANGED_BY_ROLE                 NONE
    ID                              3
    TEXT                            Initial data, added by SYSDBA
    CHANGED_BY_USER                 SYSDBA
    CHANGED_BY_ROLE                 NONE

    USER                            MICK_JUNIOR
    ROLE                            MODIFIER
    ID                              1
    TEXT                            Update-1: through the ROLE
    CHANGED_BY_USER                 MICK_JUNIOR
    CHANGED_BY_ROLE                 MODIFIER
    ID                              2
    TEXT                            Update-2: directly by USER
    CHANGED_BY_USER                 JOHN_SENIOR
    CHANGED_BY_ROLE                 NONE
    ID                              3
    TEXT                            Initial data, added by SYSDBA
    CHANGED_BY_USER                 SYSDBA
    CHANGED_BY_ROLE                 NONE
"""

expected_stderr_1 = """
    Statement failed, SQLSTATE = 28000
    no permission for UPDATE access to TABLE TEST
"""

user_1_senior = user_factory('db_1', name='john_senior', password='sen')
user_1_junior = user_factory('db_1', name='mick_junior', password='jun')
role_1 = role_factory('db_1', name='modifier', do_not_create=True)

@pytest.mark.version('>=3.0')
def test_1(act_1: Action, user_1_senior: User, user_1_junior: User, role_1: Role):
    act_1.expected_stdout = expected_stdout_1
    act_1.expected_stderr = expected_stderr_1
    act_1.execute()
    assert act_1.clean_expected_stderr == act_1.clean_stderr
    assert act_1.clean_expected_stdout == act_1.clean_stdout

