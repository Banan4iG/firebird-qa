#coding:utf-8
#
# id:           bugs.core_2101
# title:        Bugcheck 249 when attempting to fetch outside the end-of-stream mark for the open PSQL cursor
# decription:
#                   Confirmed on WI-V2.1.7.18553 Firebird 2.1:
#                   Statement failed, SQLSTATE = XX000
#                   internal Firebird consistency check (pointer page vanished from DPM_next (249), file: dpm.cpp line: 1698)
#                   -------------------------------------------
#                   29.11.2021.
#                   Separated code for FB 4.x+ was added because of changes related to cursors introduced 26-nov-2021.
#                   Commit: "Fixed missing BOF flag, better boundary checks, code unification":
#                       https://github.com/FirebirdSQL/firebird/commit/067c8040b2c810e76e99593e792a829b25fc8d5e
#                       https://github.com/FirebirdSQL/firebird/commit/9397ebb13d65d114a053cc9ce88f3dac5d17e7eb
#
#                   After this commits FETCH beyond the last record became "quiet", i.e. does not raise error.
#                   This new behaviour led test to fall in infinite loop which made FB seems hanging.
#                   New code suggested by dimitr, letter 28.11.2021 17:48.
#                   Checked on 5.0.0.321, 4.0.1.2672
#
# tracker_id:   CORE-2101
# min_versions: ['2.5.0']
# versions:     2.5, 4.0
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 2.5
# resources: None

substitutions_1 = [('SQLSTATE.*', 'SQLSTATE'), ('line: \\d+,', 'line: x'), ('col: \\d+', 'col: y')]

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """
    create table t1 ( f1 smallint );
    set term ^ ;
    create procedure p1
    as
      declare v1 smallint;
      declare c1 cursor for ( select f1 from t1 );
    begin
      open c1;
      while (1=1) do
      begin
           fetch c1 into :v1;
           if(row_count = 1) then leave;
      end
      close c1;
    end ^
    set term ; ^
    commit;

    execute procedure p1;
"""

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stderr_1 = """
    Statement failed, SQLSTATE = HY109
    attempt to fetch past the last record in a record stream
    -At procedure 'P1' line: 19, col: 18
"""

@pytest.mark.version('>=2.5,<4.0.1')
def test_1(act_1: Action):
    act_1.expected_stderr = expected_stderr_1
    act_1.execute()
    assert act_1.clean_stderr == act_1.clean_expected_stderr

# version: 4.0
# resources: None

substitutions_2 = []

init_script_2 = """"""

db_2 = db_factory(sql_dialect=3, init=init_script_2)

test_script_2 = """
    -- since 29.11.2021.
    create table t1 ( f1 smallint );
    insert into t1 values (1);
    insert into t1 values (2);
    insert into t1 values (3);
    commit;

    set term ^ ;
    create procedure p1
    as
       declare v1 smallint;
       declare c1 cursor for ( select f1 from t1 );
    begin
       open c1;
       while (1=1) do
       begin
            fetch c1 into :v1;
            if (row_count = 0) then leave;
       end
       fetch c1 into :v1;
       close c1;
    end ^
    set term ; ^
    commit;
    execute procedure p1;
"""

act_2 = isql_act('db_2', test_script_2, substitutions=substitutions_2)

@pytest.mark.version('>=4.0.1')
def test_2(act_2: Action):
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
