#coding:utf-8
#
# id:           functional.session.alter_session_reset_rollback
# title:        
#                   ALTER SESSION RESET: ROLLBACK current user transaction (if present) and issue warning if that transaction changes any table before reset
#                
# decription:   
#                  Test issue from CORE-5832 about ALTER SESSION RESET:
#                  "ROLLBACK current user transaction (if present) and issue warning if that transaction changes any table before reset ".
#               
#                  We create trivial table and insert one row in it.
#                  Then, without committing changes, we issue 'ALTER SESSION RESET'.
#                  Warning must be thrown after it (in STDERR) and no records must remain in the table as result.
#               
#                  NOTE. *** SET AUTODDL OFF REQUIRED ***
#                      Following is detailed explanation of this note:
#                      ========
#                          Default ISQL behaviour is to start always *TWO* transactions (for DML and second for DDL)
#                          after previous commit / rollback and before *ANY* further satement is to be executed, except
#                          those which control ISQL itself (e.g. 'SET TERM'; 'IN ...'; 'SET BAIL' etc).
#                          So, even when statement <S> has nothing to change, ISQL will start TWO transactions
#                          just before executing <S>.
#                          This means that these transactions will start even if want to run 'ALTER SESSION RESET'.
#                          This, in turn, makes one of them (which must perform DDL) be 'active and NOT current'
#                          from ALTER SESSION point of view (which is run within DML transaction).
#               
#                          According to description given in CORE-5832, ALTER SESSION throws error isc_ses_reset_err
#                          "if any open transaction exist in current conneciton, *except of current transaction* and
#                          prepared 2PC transactions which is allowed and ignored by this check".
#               
#                          So, we have to prohibit 'autostart' of DDL-transaction because otherwise ALTER SESSION will
#                          throw: "SQLSTATE = 01002 / Cannot reset user session / -There are open transactions (2 active)".
#                          This is done by 'SET AUTODDL OFF' statement at the beginning of this test script.
#                      ========
#               
#                  Thanks to Vlad for explanations (discussed 18.01.2021).
#                  Checked on 4.0.0.2307 SS/CS.
#                
# tracker_id:   
# min_versions: ['4.0.0']
# versions:     4.0
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 4.0
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """
    recreate table test(id int);
    commit;

    set list on;
    set autoddl off;
    commit;

    insert into test(id) values(1);

    --------------------
    alter session reset;
    --------------------
    set count on;
    select * from test;
  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    Records affected: 0
  """
expected_stderr_1 = """
    Session was reset with warning(s)
    -Transaction is rolled back due to session reset, all changes are lost
  """

@pytest.mark.version('>=4.0')
def test_alter_session_reset_rollback_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.expected_stderr = expected_stderr_1
    act_1.execute()
    assert act_1.clean_expected_stderr == act_1.clean_stderr
    assert act_1.clean_expected_stdout == act_1.clean_stdout

