#coding:utf-8

"""
ID:          issue-4788
ISSUE:       4788
TITLE:       FB3: CREATE USER GRANT ADMIN ROLE does not work
DESCRIPTION:
JIRA:        CORE-4468
FBTEST:      bugs.core_4468
"""

import pytest
from firebird.qa import *

substitutions = [('.*delete record.*', 'delete record'),
                 ('TABLE PLG\\$VIEW_USERS', 'TABLE PLG'),
                 ('TABLE PLG\\$SRP_VIEW', 'TABLE PLG'),
                 ('-OZZY_OSBOURNE is not grantor of (role|Role|ROLE) on RDB\\$ADMIN to OZZY_OSBOURNE.',
                  '-OZZY_OSBOURNE is not grantor of ROLE on RDB$ADMIN to OZZY_OSBOURNE.'),
                 ('-Effective user is.*', '')]

init_script = """
    -- ::: NB ::: Name of table in STDERR depends on value of UserManager = { Srp | Legacy_UserManager }.
    -- For 'Srp' it will be 'PLG$SRP_VIEW', for Legacy_UserManager -- PLG$VIEW_USERS.
    -- Because of this, section 'substitution' has been added in order to ignore rest part of line
    -- after words 'TABLE PLG'.
    -- Also, text in message about deletion fault differs in case of UserManager setting:
    -- 'find/delete record error' - for Legacy_UserManager
    -- 'delete record error' = for Srp
    -- This is minor bug in Legacy_UserManager but it will be remain 'as is', see letter from Alex 03-jun-2015 19:51.
    recreate view v_users as
    select current_user who_am_i, current_role whats_my_role, u.sec$user_name non_sysdba_user_name, u.sec$admin non_sysdba_has_admin_role
    from rdb$database
    left join sec$users u on u.sec$user_name in ( upper('ozzy_osbourne'), upper('bon_scott') );
"""

db = db_factory(init=init_script)

# Well, we need to create/drop users in test script, but next user fioxtures are
# defined to make sure that no user will be left behind in case the test fails
user_ozzy = user_factory('db', name='ozzy_osbourne', password='123', admin=True, do_not_create=True)
user_scott = user_factory('db', name='bon_scott', password='456', do_not_create=True)

test_script = """
    set wng off;
    set list on;
    set count on;

    select 'start' msg, v.* from v_users v;
    commit;

    create or alter user ozzy_osbourne password '123'
    grant admin role -- this is mandatory because it gives him admin role in Security DB
    ;
    revoke all on all from ozzy_osbourne;
    grant rdb$admin to ozzy_osbourne; -- this is also mandatory: it gives him admin role in ($dsn) database
    commit;

    select 'step-1' msg, v.* from v_users v;
    commit;

    -- When 'ozzy_osbourne' connects to database ($dsn), there is no way for engine to recognize that this user
    -- has been granted with admin role in 'CREATE USER ... GRANT ADMIN ROLE' statement. So, user has to specify
    -- `role 'RDB$ADMIN'` in order to connect as ADMIN.
    -- But with RDB$ADMIN only he can create objects in THAT database (tables etc), but not other USERS!
    -- Thats why he should also be granted with admin role in 'CREATE USER ...' - see above.
    connect '$(DSN)' user 'OZZY_OSBOURNE' password '123' role 'RDB$ADMIN';
    commit;

    -- Users are stored in Security DB,  *not* in "this" database!
    -- So, following statement will pass only if 'ozzy_osbourne' has been granted by 'admin role'
    -- in his own 'create user' phase:
    create or alter user bon_scott password '456' revoke admin role;
    commit;

    select 'step-2' msg, v.* from v_users v;

    alter user bon_scott grant admin role;
    commit;
    show grants;

    select 'step-3' msg, v.* from v_users v;

    grant rdb$admin to bon_scott;
    commit;

    show grants;

    alter user bon_scott revoke admin role;
    commit;

    select 'step-4' msg, v.* from v_users v;
    commit;

    revoke rdb$admin from bon_scott;
    commit;

    show grants;

    drop user bon_scott;
    commit;

    select 'step-5' msg, v.* from v_users v;
    commit;

    -- User removes admin role from himself:

    -- 1. This will FAIL:
    -- -REVOKE failed
    -- -OZZY_OSBOURNE is not grantor of Role on RDB$ADMIN to OZZY_OSBOURNE.
    revoke rdb$admin from ozzy_osbourne;
    commit;

    -- 2 This will PASS, and it MUST be so (see letter from Alex, 03-jun-2015 19:46)
    alter user ozzy_osbourne revoke admin role;
    commit;

    show grants;

    select 'step-6' msg, v.* from v_users v;
    commit;

    -- And after previous action he can not drop himself because now he is NOT member of admin role:
    -- Statement failed, SQLSTATE = 28000
    -- find/delete record error
    -- -no permission for DELETE access to TABLE PLG$VIEW_USERS
    drop user ozzy_osbourne;
    commit;

    select 'step-7' msg, v.* from v_users v;
    commit;

    -- Trying reconnect with role RDB$ADMIN:
    connect '$(DSN)' user 'OZZY_OSBOURNE' password '123' role 'RDB$ADMIN';
    commit;

    select 'step-8' msg, v.* from v_users v;
    commit;

    show grants;
    commit;

    connect '$(DSN)' user 'SYSDBA' password 'masterkey';
    drop user ozzy_osbourne;
    commit;

    select 'final' msg, v.* from v_users v;
    commit;
"""

act = isql_act('db', test_script, substitutions=substitutions)

expected_stdout = """
    MSG                             start
    WHO_AM_I                        SYSDBA
    WHATS_MY_ROLE                   NONE
    NON_SYSDBA_USER_NAME            <null>
    NON_SYSDBA_HAS_ADMIN_ROLE       <null>
    Records affected: 1

    MSG                             step-1
    WHO_AM_I                        SYSDBA
    WHATS_MY_ROLE                   NONE
    NON_SYSDBA_USER_NAME            OZZY_OSBOURNE
    NON_SYSDBA_HAS_ADMIN_ROLE       <true>

    Records affected: 1


    MSG                             step-2
    WHO_AM_I                        OZZY_OSBOURNE
    WHATS_MY_ROLE                   RDB$ADMIN
    NON_SYSDBA_USER_NAME            OZZY_OSBOURNE
    NON_SYSDBA_HAS_ADMIN_ROLE       <true>

    MSG                             step-2
    WHO_AM_I                        OZZY_OSBOURNE
    WHATS_MY_ROLE                   RDB$ADMIN
    NON_SYSDBA_USER_NAME            BON_SCOTT
    NON_SYSDBA_HAS_ADMIN_ROLE       <false>


    Records affected: 2

    /* Grant permissions for this database */
    GRANT RDB$ADMIN TO OZZY_OSBOURNE

    MSG                             step-3
    WHO_AM_I                        OZZY_OSBOURNE
    WHATS_MY_ROLE                   RDB$ADMIN
    NON_SYSDBA_USER_NAME            OZZY_OSBOURNE
    NON_SYSDBA_HAS_ADMIN_ROLE       <true>

    MSG                             step-3
    WHO_AM_I                        OZZY_OSBOURNE
    WHATS_MY_ROLE                   RDB$ADMIN
    NON_SYSDBA_USER_NAME            BON_SCOTT
    NON_SYSDBA_HAS_ADMIN_ROLE       <true>


    Records affected: 2

    /* Grant permissions for this database */
    GRANT RDB$ADMIN TO BON_SCOTT GRANTED BY OZZY_OSBOURNE
    GRANT RDB$ADMIN TO OZZY_OSBOURNE

    MSG                             step-4
    WHO_AM_I                        OZZY_OSBOURNE
    WHATS_MY_ROLE                   RDB$ADMIN
    NON_SYSDBA_USER_NAME            OZZY_OSBOURNE
    NON_SYSDBA_HAS_ADMIN_ROLE       <true>

    MSG                             step-4
    WHO_AM_I                        OZZY_OSBOURNE
    WHATS_MY_ROLE                   RDB$ADMIN
    NON_SYSDBA_USER_NAME            BON_SCOTT
    NON_SYSDBA_HAS_ADMIN_ROLE       <false>


    Records affected: 2

    /* Grant permissions for this database */
    GRANT RDB$ADMIN TO OZZY_OSBOURNE

    MSG                             step-5
    WHO_AM_I                        OZZY_OSBOURNE
    WHATS_MY_ROLE                   RDB$ADMIN
    NON_SYSDBA_USER_NAME            OZZY_OSBOURNE
    NON_SYSDBA_HAS_ADMIN_ROLE       <true>


    Records affected: 1

    /* Grant permissions for this database */
    GRANT RDB$ADMIN TO OZZY_OSBOURNE

    MSG                             step-6
    WHO_AM_I                        OZZY_OSBOURNE
    WHATS_MY_ROLE                   RDB$ADMIN
    NON_SYSDBA_USER_NAME            OZZY_OSBOURNE
    NON_SYSDBA_HAS_ADMIN_ROLE       <false>


    Records affected: 1

    MSG                             step-7
    WHO_AM_I                        OZZY_OSBOURNE
    WHATS_MY_ROLE                   RDB$ADMIN
    NON_SYSDBA_USER_NAME            OZZY_OSBOURNE
    NON_SYSDBA_HAS_ADMIN_ROLE       <false>


    Records affected: 1

    MSG                             step-8
    WHO_AM_I                        OZZY_OSBOURNE
    WHATS_MY_ROLE                   RDB$ADMIN
    NON_SYSDBA_USER_NAME            OZZY_OSBOURNE
    NON_SYSDBA_HAS_ADMIN_ROLE       <false>


    Records affected: 1

    /* Grant permissions for this database */
    GRANT RDB$ADMIN TO OZZY_OSBOURNE

    MSG                             final
    WHO_AM_I                        SYSDBA
    WHATS_MY_ROLE                   NONE
    NON_SYSDBA_USER_NAME            <null>
    NON_SYSDBA_HAS_ADMIN_ROLE       <null>


    Records affected: 1
"""

expected_stderr = """
    Statement failed, SQLSTATE = 42000
    unsuccessful metadata update
    -REVOKE failed
    -OZZY_OSBOURNE is not grantor of Role on RDB$ADMIN to OZZY_OSBOURNE.

    Statement failed, SQLSTATE = 28000
    delete record error
    -no permission for DELETE access to TABLE PLG$VIEW_USERS
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action, user_ozzy: User, user_scott: User):
    act.expected_stdout = expected_stdout
    act.expected_stderr = expected_stderr
    act.execute()
    assert (act.clean_stderr == act.clean_expected_stderr and
            act.clean_stdout == act.clean_expected_stdout)

