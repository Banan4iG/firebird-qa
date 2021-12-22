#coding:utf-8
#
# id:           bugs.core_5887
# title:        Allow the use of management statements in PSQL blocks
# decription:   
#                   ::: NB :::
#                   1. Currently test checks only ability to use SYNTAX for usage statements within PSQL blocks
#                      as it is described in '...\\doc\\sql.extensions\\README.management_statements_psql.md'.
#                      Actual affects on further work are not verified.
#                   2. Deferred check of 'alter session reset': got SQLSTATE = 25000/no transaction for request.
#                      Sent letter to dimitr et al, 09-mar-2019 13:43.
#                   3. Deferred check of 'SET TRUSTED ROLE': it is unclear for me how to implement this. 
#                      Sent Q to Alex (same letter).
#               
#                   All other cases are checked on 4.0.0.1421 and 4.0.0.1457: OK.
#               
#                   10.12.2019. Updated syntax for SET BIND. Removed (maybe temply) check of 'set time zone bind native'.
#                   Commits that changed syntax:
#                   https://github.com/FirebirdSQL/firebird/commit/ca5ee672ca3144303732d5e2b5886b32c442da91 // 08-nov-19
#                   https://github.com/FirebirdSQL/firebird/commit/08096e3b879811d0e2e87b707b260c17d1542167 // 12-dec-19
#               
#                   Checked on 4.0.0.1685, 4.0.0.1691
#               
#                
# tracker_id:   CORE-5887
# min_versions: ['4.0']
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
    set bail on;

    set term ^;
    execute block as
    begin
        begin
            execute statement 'drop role acnt';
        when any do begin end
        end
    end
    ^
    set term ;^
    commit;

    create role acnt;
    commit;

    grant acnt to sysdba;
    commit;

    ----------------------------------------------

    -- NO output should be produced by further PSQL blocks:

    set term ^;
    execute block as
    begin
        set decfloat round ceiling;
    end^

    execute block as
    begin
        set decfloat traps to Division_by_zero, Invalid_operation, Overflow;
    end^

    execute block as
    begin
        -- OLD SYNTAX: set decfloat bind native;
        -- Syntax after 11-nov-2019:
        -- https://github.com/FirebirdSQL/firebird/commit/a77295ba153e0c17061e2230d0ffdbaf08839114
        -- See also: doc/sql.extensions/README.set_bind.md:
        --     SET BIND OF type-from TO { type-to | LEGACY };
        --     SET BIND OF type NATIVE;

        set bind of decfloat to native;
        --                   ^^
        --                   +--- since 12-dec-2019
    end^

    execute block as
    begin
        set role acnt;
    end^

    execute block as
    begin
        set session idle timeout 5 minute;
    end^

    execute block as
    begin
        set statement timeout 1 minute;
    end^

    execute block as
    begin
        set time zone local;
    end^


    execute block as
    begin
        set bind of timestamp with time zone to legacy;
        set bind of time with time zone to legacy;
    end^
    ^

    execute block as
    begin
        set bind of timestamp with time zone to native;
        set bind of time with time zone to native;
    end^
    ^
    set term ;^
    commit;

    drop role acnt;
    commit;
"""

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)


@pytest.mark.version('>=4.0')
def test_1(act_1: Action):
    act_1.execute()

