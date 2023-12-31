#coding:utf-8

"""
ID:          issue-2245
ISSUE:       2245
TITLE:       Ability to grant role to another role
DESCRIPTION:
  ### NB ### This test was NOT completed!
  One need to check all nuances related to granting and revoking that is issued by NON sysdba user
  which was granted admin option to manupulate appropriate DB objects.
  Also, there is not clarity about issue 08/Aug/16 06:31 AM (when user Boss2 does grant-and-revoke
  sequence with some role to other user Sales but this role already was granted by _other_ user, Boss1).

  We create two users (acnt and pdsk) and two roles for them (racnt and rpdsk).
  Then we create two tables (tacnt & tpdsk) and grant access on these tables for acnt & pdsk.
  Then we create user boss, role for him (rboss) and grant IMPLICITLY access on tables tacnt and tpdsk
  to user boss via his role (rboss).
  Check is made to ensure that user boss HAS ability to read from both tables (being connected with role Rboss).
  After all, we IMPLICITLY revoke access from these tables and check again that user boss now has NO access
  on tables tacnt and tpdsk.
JIRA:        CORE-1815
FBTEST:      bugs.core_1815
"""

import pytest
from firebird.qa import *

db = db_factory()
user_boss = user_factory('db', name='tmp$c1815_boss', password='boss')
user_acnt = user_factory('db', name='tmp$c1815_acnt', password='acnt')
user_pdsk = user_factory('db', name='tmp$c1815_pdsk', password='pdsk')

test_script = """
    set wng off;
    --show version;
    --set bail on;
    --set echo on;
    set list on;

    set width whoami 16;
    set width my_role 7;
    set width r_name 10;
    set width r_owner 10;

    create or alter view v_role_info as
    select
        current_user as whoami,
        current_role as my_role,
        rdb$role_name as r_name,
        rdb$owner_name r_owner,
        rdb$role_in_use(rdb$role_name) r_in_use
    from rdb$roles
    where coalesce(rdb$system_flag,0) = 0
    ;
    commit;

    create role rboss;
    create role racnt;
    create role rpdsk;
    commit;

    grant select on v_role_info to user tmp$c1815_acnt;
    grant select on v_role_info to user tmp$c1815_pdsk;
    grant select on v_role_info to user tmp$c1815_boss;
    commit;

    grant racnt to user tmp$c1815_acnt;
    grant rpdsk to user tmp$c1815_pdsk;
    commit;

    ------------------------------------------------------------------------

    recreate table tacnt(id int, s varchar(5));
    recreate table tpdsk(id int, s varchar(5));
    commit;

    grant all on tacnt to role racnt;
    grant all on tpdsk to role rpdsk;
    commit;

    ------------------------------------------------------------------------

    grant racnt to rboss;           -- make RBOSS role able to do the same as role RACNT
    grant rpdsk to rboss;           -- make RBOSS role able to do the same as role RPDSK

    grant rboss to tmp$c1815_boss;  -- let user BOSS to use role RBOSS

    commit;
    --show grants; -- [ 1 ]

    ------------------------------------------------------------------------

    insert into tacnt(id, s) values(1,'acnt');
    insert into tpdsk(id, s) values(2,'pdsk');
    commit;

    connect '$(DSN)' user tmp$c1815_acnt password 'acnt' role 'racnt';
    select * from v_role_info;
    select current_user as whoami, a.* from tacnt a;
    commit;

    connect '$(DSN)' user tmp$c1815_pdsk password 'pdsk' role 'rpdsk';
    select * from v_role_info;
    select current_user as whoami, p.* from tpdsk p;
    commit;


    connect '$(DSN)' user tmp$c1815_boss password 'boss' role 'rboss';
    select * from v_role_info;
    commit;

    select current_user as whoami, a.* from tacnt a;
    select current_user as whoami, p.* from tpdsk p;
    commit;

    --################################################################################################

    connect '$(DSN)' user sysdba password 'masterkey';

    revoke racnt from user tmp$c1815_acnt; -- REVOKE role from *other* USER; grant to RBoss should be reserved!
    commit;

    -- check that *role* RBoss still HAS grants to both RAcnt and RPdsk roles:
    connect '$(DSN)' user tmp$c1815_boss password 'boss' role 'rboss';

    select * from v_role_info; -- should contain <true> in all three rows

    -- should PASS because we revoked role from other USER (accountant)
    -- rather than from current user (Boss) or its role (Rboss):
    select current_user as whoami, a.* from tacnt a;
    commit;

    --####################################################################################################

    connect '$(DSN)' user sysdba password 'masterkey';

    -- check that if we try to revoke role RPdsk from __USER__ Boss than
    -- this action will not has effect because this USER got access through the ROLE (i.e. indirectly):

    revoke rpdsk from user tmp$c1815_boss; -- this is no-op action! We did NOT granted role to USER!
    commit;

    connect '$(DSN)' user tmp$c1815_boss password 'boss' role 'rboss'; -- now check: is role Rboss really affected ?

    select * from v_role_info; -- should contain <true> in all lines because we did not affect __role__ RBOSS
    select current_user as whoami, p.* from tpdsk p; -- should PASS!
    commit;

    --################################################################################################

    connect '$(DSN)' user sysdba password 'masterkey';

    -- check that if we revoke access to a table from ROLE RPdsk (and this role was granted to role RBoss)
    -- then Rboss also will not be able to select from this table:

    revoke all on tpdsk from rpdsk;
    commit;

    connect '$(DSN)' user tmp$c1815_boss password 'boss' role 'rboss';

    select * from v_role_info; -- should contain <true> in all lines because we did not affect __role__ RBOSS
    select current_user as whoami, p.* from tpdsk p; -- should FAIL
    commit;

    --################################################################################################

    connect '$(DSN)' user sysdba password 'masterkey';

    -- check that if we revoke ROLE 'racnt' which was granted before to ROLE 'rboss'
    -- then user Boss will not be able to access table 'tacnt' (i.e. we revoke this access indirectly):

    revoke racnt from rboss;
    commit;

    connect '$(DSN)' user tmp$c1815_boss password 'boss' role 'rboss';

    select * from v_role_info; -- should contain <false> for line with 'racnt'
    select current_user as whoami, a.* from tacnt a; -- should FAIL
    commit;

    -- ###############################################################################################

    connect '$(DSN)' user sysdba password 'masterkey';

    -- check that if we GRANT again ROLE 'racnt' which was revoked before from ROLE 'rboss'
    -- then user Boss WILL be able to access table 'tacnt' (we grant access indirectly after revoking):

    grant racnt to rboss; -- RESTORE access for role Rboss
    commit;


    connect '$(DSN)' user tmp$c1815_boss password 'boss' role 'rboss';

    select * from v_role_info; -- should contain <true> for line with 'racnt'
    select current_user as whoami, a.* from tacnt a; -- should PASS
    commit;
"""

act = isql_act('db', test_script)

expected_stdout = """
    WHOAMI                          TMP$C1815_ACNT
    MY_ROLE                         RACNT
    R_NAME                          RBOSS
    R_OWNER                         SYSDBA
    R_IN_USE                        <false>

    WHOAMI                          TMP$C1815_ACNT
    MY_ROLE                         RACNT
    R_NAME                          RACNT
    R_OWNER                         SYSDBA
    R_IN_USE                        <true>

    WHOAMI                          TMP$C1815_ACNT
    MY_ROLE                         RACNT
    R_NAME                          RPDSK
    R_OWNER                         SYSDBA
    R_IN_USE                        <false>


    WHOAMI                          TMP$C1815_ACNT
    ID                              1
    S                               acnt


    WHOAMI                          TMP$C1815_PDSK
    MY_ROLE                         RPDSK
    R_NAME                          RBOSS
    R_OWNER                         SYSDBA
    R_IN_USE                        <false>

    WHOAMI                          TMP$C1815_PDSK
    MY_ROLE                         RPDSK
    R_NAME                          RACNT
    R_OWNER                         SYSDBA
    R_IN_USE                        <false>

    WHOAMI                          TMP$C1815_PDSK
    MY_ROLE                         RPDSK
    R_NAME                          RPDSK
    R_OWNER                         SYSDBA
    R_IN_USE                        <true>


    WHOAMI                          TMP$C1815_PDSK
    ID                              2
    S                               pdsk


    WHOAMI                          TMP$C1815_BOSS
    MY_ROLE                         RBOSS
    R_NAME                          RBOSS
    R_OWNER                         SYSDBA
    R_IN_USE                        <true>

    WHOAMI                          TMP$C1815_BOSS
    MY_ROLE                         RBOSS
    R_NAME                          RACNT
    R_OWNER                         SYSDBA
    R_IN_USE                        <true>

    WHOAMI                          TMP$C1815_BOSS
    MY_ROLE                         RBOSS
    R_NAME                          RPDSK
    R_OWNER                         SYSDBA
    R_IN_USE                        <true>


    WHOAMI                          TMP$C1815_BOSS
    ID                              1
    S                               acnt

    WHOAMI                          TMP$C1815_BOSS
    ID                              2
    S                               pdsk


    WHOAMI                          TMP$C1815_BOSS
    MY_ROLE                         RBOSS
    R_NAME                          RBOSS
    R_OWNER                         SYSDBA
    R_IN_USE                        <true>

    WHOAMI                          TMP$C1815_BOSS
    MY_ROLE                         RBOSS
    R_NAME                          RACNT
    R_OWNER                         SYSDBA
    R_IN_USE                        <true>

    WHOAMI                          TMP$C1815_BOSS
    MY_ROLE                         RBOSS
    R_NAME                          RPDSK
    R_OWNER                         SYSDBA
    R_IN_USE                        <true>


    WHOAMI                          TMP$C1815_BOSS
    ID                              1
    S                               acnt


    WHOAMI                          TMP$C1815_BOSS
    MY_ROLE                         RBOSS
    R_NAME                          RBOSS
    R_OWNER                         SYSDBA
    R_IN_USE                        <true>

    WHOAMI                          TMP$C1815_BOSS
    MY_ROLE                         RBOSS
    R_NAME                          RACNT
    R_OWNER                         SYSDBA
    R_IN_USE                        <true>

    WHOAMI                          TMP$C1815_BOSS
    MY_ROLE                         RBOSS
    R_NAME                          RPDSK
    R_OWNER                         SYSDBA
    R_IN_USE                        <true>


    WHOAMI                          TMP$C1815_BOSS
    ID                              2
    S                               pdsk


    WHOAMI                          TMP$C1815_BOSS
    MY_ROLE                         RBOSS
    R_NAME                          RBOSS
    R_OWNER                         SYSDBA
    R_IN_USE                        <true>

    WHOAMI                          TMP$C1815_BOSS
    MY_ROLE                         RBOSS
    R_NAME                          RACNT
    R_OWNER                         SYSDBA
    R_IN_USE                        <true>

    WHOAMI                          TMP$C1815_BOSS
    MY_ROLE                         RBOSS
    R_NAME                          RPDSK
    R_OWNER                         SYSDBA
    R_IN_USE                        <true>


    WHOAMI                          TMP$C1815_BOSS
    MY_ROLE                         RBOSS
    R_NAME                          RBOSS
    R_OWNER                         SYSDBA
    R_IN_USE                        <true>

    WHOAMI                          TMP$C1815_BOSS
    MY_ROLE                         RBOSS
    R_NAME                          RACNT
    R_OWNER                         SYSDBA
    R_IN_USE                        <false>

    WHOAMI                          TMP$C1815_BOSS
    MY_ROLE                         RBOSS
    R_NAME                          RPDSK
    R_OWNER                         SYSDBA
    R_IN_USE                        <true>


    WHOAMI                          TMP$C1815_BOSS
    MY_ROLE                         RBOSS
    R_NAME                          RBOSS
    R_OWNER                         SYSDBA
    R_IN_USE                        <true>

    WHOAMI                          TMP$C1815_BOSS
    MY_ROLE                         RBOSS
    R_NAME                          RACNT
    R_OWNER                         SYSDBA
    R_IN_USE                        <true>

    WHOAMI                          TMP$C1815_BOSS
    MY_ROLE                         RBOSS
    R_NAME                          RPDSK
    R_OWNER                         SYSDBA
    R_IN_USE                        <true>



    WHOAMI                          TMP$C1815_BOSS
    ID                              1
    S                               acnt
"""

expected_stderr = """
    Statement failed, SQLSTATE = 28000
    no permission for SELECT access to TABLE TPDSK
    -Effective user is TMP$C1815_BOSS

    Statement failed, SQLSTATE = 28000
    no permission for SELECT access to TABLE TACNT
    -Effective user is TMP$C1815_BOSS
"""

@pytest.mark.version('>=4.0')
def test_1(act: Action, user_boss: User, user_acnt: User, user_pdsk: User):
    act.expected_stdout = expected_stdout
    act.expected_stderr = expected_stderr
    act.execute()
    assert (act.clean_stderr == act.clean_expected_stderr and
            act.clean_stdout == act.clean_expected_stdout)

