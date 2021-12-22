#coding:utf-8
#
# id:           bugs.core_4802
# title:        Regression: GRANT UPDATE(<some_column>) on <T> acts like grant update on ALL columns of <T>
# decription:
# tracker_id:   CORE-4802
# min_versions: ['3.0']
# versions:     3.0
# qmid:

import pytest
from firebird.qa import db_factory, isql_act, Action, user_factory, User, role_factory, Role

# version: 3.0
# resources: None

substitutions_1 = [('GRANT.*TMP.*', ''), ('-Effective user is.*', '')]

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """
    set wng off;

    recreate table test(fld_for_seniors varchar(70), fld_for_juniors varchar(70));
    commit;

    grant select on test to PUBLIC;

    grant update(fld_for_seniors) on test to BIG_BROTHER;
    commit;

    grant update(fld_for_seniors) on test to FLD_FOR_SENIORS_UPDATER;
    grant update(fld_for_juniors) on test to FLD_FOR_JUNIORS_UPDATER;

    grant FLD_FOR_SENIORS_UPDATER to SENIOR_MNGR;
    grant FLD_FOR_JUNIORS_UPDATER to JUNIOR_MNGR;
    commit;

    show grants;

    insert into test values( 'created by '||upper(current_user), 'created by '||lower(current_user) );
    commit;
    set list on;

    --set echo on;

    connect '$(DSN)' user 'BIG_BROTHER' password '123';
    select current_user, current_role from rdb$database;
    update test set fld_for_seniors = 'updated by '||upper(current_user)||', role: '||upper(current_role);
    select * from test;

    update test set fld_for_juniors = 'updated by '||lower(current_user)||', role: '||lower(current_role);
    select * from test;
    commit;
    ---------------------------------------------------------------

    connect '$(DSN)' user 'SENIOR_MNGR' password '456' role 'FLD_FOR_SENIORS_UPDATER';
    select current_user, current_role from rdb$database;
    update test set fld_for_seniors = 'updated by '||upper(current_user)||', role: '||upper(current_role);
    select * from test;

    update test set fld_for_juniors ='updated by '||lower(current_user)||', role: '||lower(current_role);
    select * from test;
    commit;
    ---------------------------------------------------------------

    connect '$(DSN)' user 'JUNIOR_MNGR' password '789' role 'FLD_FOR_JUNIORS_UPDATER';
    select current_user, current_role from rdb$database;
    update test set fld_for_seniors = 'updated by '||upper(current_user)||', role: '||upper(current_role);
    select * from test;

    update test set fld_for_juniors ='updated by '||lower(current_user)||', role: '||lower(current_role);
    select * from test;
    commit;
"""

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    /* Grant permissions for this database */
    GRANT UPDATE (FLD_FOR_SENIORS) ON TEST TO USER BIG_BROTHER
    GRANT UPDATE (FLD_FOR_JUNIORS) ON TEST TO ROLE FLD_FOR_JUNIORS_UPDATER
    GRANT UPDATE (FLD_FOR_SENIORS) ON TEST TO ROLE FLD_FOR_SENIORS_UPDATER
    GRANT SELECT ON TEST TO PUBLIC
    GRANT FLD_FOR_JUNIORS_UPDATER TO JUNIOR_MNGR
    GRANT FLD_FOR_SENIORS_UPDATER TO SENIOR_MNGR

    USER                            BIG_BROTHER
    ROLE                            NONE
    FLD_FOR_SENIORS                 updated by BIG_BROTHER, role: NONE
    FLD_FOR_JUNIORS                 created by sysdba
    FLD_FOR_SENIORS                 updated by BIG_BROTHER, role: NONE
    FLD_FOR_JUNIORS                 created by sysdba

    USER                            SENIOR_MNGR
    ROLE                            FLD_FOR_SENIORS_UPDATER
    FLD_FOR_SENIORS                 updated by SENIOR_MNGR, role: FLD_FOR_SENIORS_UPDATER
    FLD_FOR_JUNIORS                 created by sysdba
    FLD_FOR_SENIORS                 updated by SENIOR_MNGR, role: FLD_FOR_SENIORS_UPDATER
    FLD_FOR_JUNIORS                 created by sysdba

    USER                            JUNIOR_MNGR
    ROLE                            FLD_FOR_JUNIORS_UPDATER
    FLD_FOR_SENIORS                 updated by SENIOR_MNGR, role: FLD_FOR_SENIORS_UPDATER
    FLD_FOR_JUNIORS                 created by sysdba
    FLD_FOR_SENIORS                 updated by SENIOR_MNGR, role: FLD_FOR_SENIORS_UPDATER
    FLD_FOR_JUNIORS                 updated by junior_mngr, role: fld_for_juniors_updater
"""

expected_stderr_1 = """
    Statement failed, SQLSTATE = 28000
    no permission for UPDATE access to COLUMN TEST.FLD_FOR_JUNIORS

    Statement failed, SQLSTATE = 28000
    no permission for UPDATE access to COLUMN TEST.FLD_FOR_JUNIORS

    Statement failed, SQLSTATE = 28000
    no permission for UPDATE access to COLUMN TEST.FLD_FOR_SENIORS
"""

user_1a = user_factory('db_1', name='BIG_BROTHER', password='123')
user_1b = user_factory('db_1', name='SENIOR_MNGR', password='456')
user_1c = user_factory('db_1', name='JUNIOR_MNGR', password='789')
role_1a = role_factory('db_1', name='FLD_FOR_SENIORS_UPDATER')
role_1b = role_factory('db_1', name='FLD_FOR_JUNIORS_UPDATER')

@pytest.mark.version('>=3.0')
def test_1(act_1: Action, user_1a: User, user_1b: User, user_1c: User, role_1a: Role,
           role_1b: Role):
    act_1.expected_stdout = expected_stdout_1
    act_1.expected_stderr = expected_stderr_1
    act_1.execute()
    assert act_1.clean_stderr == act_1.clean_expected_stderr
    assert act_1.clean_stdout == act_1.clean_expected_stdout

