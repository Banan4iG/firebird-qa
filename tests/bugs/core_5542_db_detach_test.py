#coding:utf-8

"""
ID:          issue-5810-B
ISSUE:       5810
TITLE:       Database-level triggers related to TRANSACTION events (i.e. start, commit and
  rollback) do not take in account their POSITION index (when more than one trigger for
  the same event type is defined)
DESCRIPTION:
  This test does check only for 'DATABASE DISCONNECT' case (though it worked Ok before this bug was found).
JIRA:        CORE-5542
FBTEST:      bugs.core_5542_db_detach
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    set list on;

    set term ^;
    create or alter trigger trg_db_deattach_beta inactive on disconnect position 0 as begin end
    ^
    create or alter trigger trg_db_deattach_anna inactive on disconnect position 0 as begin end
    ^
    create or alter trigger trg_db_deattach_ciao inactive on disconnect position 0 as begin end
    ^
    commit
    ^
    drop trigger trg_db_deattach_beta
    ^
    drop trigger trg_db_deattach_anna
    ^
    drop trigger trg_db_deattach_ciao
    ^

    recreate table tsignal( id integer )
    ^
    recreate table trg_log( id integer, msg varchar(20) );
    ^

    execute block as
    begin
        execute statement 'drop sequence g';
        when any do begin end
    end
    ^
    set term ;^
    commit;

    set autoddl off;
    set bail on;

    create sequence g;
    commit;

    set term ^;
    create trigger trg_log_bi for trg_log active before insert position 0 as
    begin
        new.id = coalesce( new.id, gen_id(g,1) );
    end
    ^
    set term ;^
    commit;

    ------------------------------------------------------------------------

    set term ^;
    create or alter trigger trg_db_deattach_ciao active on disconnect position 111 as
    begin
        if ( exists(select * from tsignal) ) then
            insert into trg_log(msg) values('trigger tx_ciao');
    end
    ^

    create or alter trigger trg_db_deattach_anna active on disconnect position 22 as
    begin
        if ( exists(select * from tsignal) ) then
            insert into trg_log(msg) values('trigger tx_anna');
    end
    ^

    create or alter trigger trg_db_deattach_beta active on disconnect position 3 as
    begin
        if ( exists(select * from tsignal) ) then
            insert into trg_log(msg) values('trigger tx_beta');
    end
    ^

    set term ;^
    commit;

    insert into tsignal(id) values(1); -- this will allow triggers to INSERT rows into TRG_LOG table.
    commit;

    connect '$(DSN)' user 'SYSDBA' password 'masterkey';


    select
         r.rdb$trigger_name
        ,r.rdb$trigger_sequence
        ,r.rdb$trigger_type
    from rdb$triggers r
    where r.rdb$trigger_name starting with upper('trg_db_deattach')
    order by r.rdb$trigger_sequence
    ;

    set count on;
    select * from trg_log;

"""

act = isql_act('db', test_script)

expected_stdout = """
    RDB$TRIGGER_NAME                TRG_DB_DEATTACH_BETA
    RDB$TRIGGER_SEQUENCE            3
    RDB$TRIGGER_TYPE                8193
    RDB$TRIGGER_NAME                TRG_DB_DEATTACH_ANNA
    RDB$TRIGGER_SEQUENCE            22
    RDB$TRIGGER_TYPE                8193
    RDB$TRIGGER_NAME                TRG_DB_DEATTACH_CIAO
    RDB$TRIGGER_SEQUENCE            111
    RDB$TRIGGER_TYPE                8193
    ID                              1
    MSG                             trigger tx_beta
    ID                              2
    MSG                             trigger tx_anna
    ID                              3
    MSG                             trigger tx_ciao
    Records affected: 3
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
