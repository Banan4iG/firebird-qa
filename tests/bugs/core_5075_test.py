#coding:utf-8

"""
ID:          issue-5362
ISSUE:       5362
TITLE:       Regression. Triger on DISCONNECT with dynamic SQL (ES 'insert into ...'): 1) does not work in 3.0; 2) leads FB to crash when it is recreated
DESCRIPTION:
    Test does following:
    * obtains firebird.log as it was _before_ actions;
    * stores initial script for creation DB objects in file <f_sql_init> for futher applying it twice (see ticket);
    * open PIPE object and communicates with ISQL issuing commands into STDIN, three times; result is stored in var.'sqlres'
    * print variable 'sqlres'; it content must be equal to that we get in FB 2.5;
    * again apply initial DDL and then - one again launch ISQL with passing to it commands via STDIN and saving result in 'sqlres'
    * print variable 'sqlres';
    * obtains firebird.log as it is _after_ actions;
    * compare two firebird.log versions - diff must be empty.
JIRA:        CORE-5075
"""

import pytest
from difflib import unified_diff
from firebird.qa import *

db = db_factory()

act = python_act('db')

expected_stdout = """
    EVENT_ID                        1
    EVENT_NAME                      connect
    Records affected: 1
    EVENT_ID                        1
    EVENT_NAME                      connect
    EVENT_ID                        2
    EVENT_NAME                      disconnect
    EVENT_ID                        3
    EVENT_NAME                      connect
    Records affected: 3
    EVENT_ID                        1
    EVENT_NAME                      connect
    EVENT_ID                        2
    EVENT_NAME                      disconnect
    EVENT_ID                        3
    EVENT_NAME                      connect
    EVENT_ID                        4
    EVENT_NAME                      disconnect
    EVENT_ID                        5
    EVENT_NAME                      connect
    Records affected: 5
    EVENT_ID                        1
    EVENT_NAME                      connect
    Records affected: 1
"""

init_script = """
set term ^;
create or alter trigger trg_connect active on connect position 0 as
begin
end
^

create or alter trigger trg_disc active on disconnect position 0 as
begin
end
^
set term ;^
commit;

recreate sequence g;
recreate table log(
    event_id int generated by default as identity constraint pk_log primary key,
    event_name varchar(20),
    when_it_was timestamp default 'now'
);
commit;

set term ^;
execute block as
begin
    rdb$set_context('USER_SESSION','INITIAL_DDL','1');
end
^

create or alter trigger trg_connect active on connect position 0 as
begin
    execute statement 'insert into log(event_name) values(''connect'')'
    with autonomous transaction;
end
^

create or alter trigger trg_disc active on disconnect position 0 as
begin
    if ( rdb$get_context('USER_SESSION','INITIAL_DDL') is null ) then
        execute statement 'insert into log(event_name) values(''disconnect'')'
        with autonomous transaction;
end
^
set term ;^
commit;
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action, capsys):
    with act.connect_server() as srv:
        srv.info.get_log()
        log_before = srv.readlines()
    #
    act.isql(switches=['-nod'], input=init_script)
    # Tests 3x
    test_cmd = 'set list on;set count on; select event_id, event_name from log;'
    for step in range(3):
        act.reset()
        act.isql(switches=[], input=test_cmd)
        print(act.stdout)
    # Init again
    act.reset()
    act.isql(switches=['-nod'], input=init_script)
    # Test again
    act.reset()
    act.isql(switches=[], input=test_cmd)
    print(act.stdout)
    # Get log again
    with act.connect_server() as srv:
        srv.info.get_log()
        log_after = srv.readlines()
    #
    act.expected_stdout = expected_stdout
    act.stdout = capsys.readouterr().out
    assert act.clean_stdout == act.clean_expected_stdout
    assert list(unified_diff(log_before, log_after)) == []
