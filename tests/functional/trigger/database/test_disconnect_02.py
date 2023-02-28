#coding:utf-8

"""
ID:          trigger.database.trigger_on_disconnect_02
TITLE:       ON DISCONNECT trigger must fire during database shutdown (gfix -shut full -force 0).
DESCRIPTION: 
    Improvement was introduced 06-apr-2023, commit:
    https://github.com/FirebirdSQL/firebird/commit/d64868cdcd91450e3c58aa9bfa9c1090912ac358
    Test creates table 'detach_audit' which is fulfilled from ON DISCONNECT trigger if current user not SYSDBA.
    We create non-privileged user ('tmp_worker') and make connection to database.
    During that, we change DB state to shutdown which *must* cause firing trigger and adding
    record to 'detach_audit' table (and, according to doc, engine always starts autonomous transaction for that).
    Finally, we bring DB online and check that table 'detach_audit' has ONE record (containing name of non-priv user).
NOTES:
    [28.02.2023] pzotov
    Confirmed missed trigger firing on 5.0.0.459 (05-apr-2023): table 'detach_audit' remained empty.
    Checked on 5.0.0.961 - all OK.
"""

import pytest
from firebird.qa import *
from firebird.driver import ShutdownMode, ShutdownMethod, DatabaseError
import time

tmp_worker = user_factory('db', name='tmp_worker', password='123')
db = db_factory()
act = python_act('db')

expected_stdout = """
    ID                              1
    WHO                             TMP_WORKER
    Records affected: 1
"""

@pytest.mark.version('>=5.0')
def test_1(act: Action, tmp_worker: User):

    init_sql  = f"""
        recreate table detach_audit(
            id int generated always as identity
            ,dts timestamp default 'now'
            ,who varchar(31) default current_user
        );
        commit;
        grant select, insert on detach_audit to public;

        set term ^;
        create trigger trg_disconnect on disconnect as
        begin
           if ( current_user != '{act.db.user}' ) then
               insert into detach_audit default values;
        end
        ^
        set term ;^
        commit;
    """

    act.expected_stdout = ''
    act.isql(switches=['-q'], input = init_sql, combine_output = True)
    assert act.clean_stdout == act.clean_expected_stdout
    act.reset()

    with act.connect_server() as srv, act.db.connect(user = tmp_worker.name, password = tmp_worker.password) as con_worker:
        srv.database.shutdown(database=act.db.db_path, mode=ShutdownMode.FULL, method=ShutdownMethod.FORCED, timeout=0)
        srv.database.bring_online(database=act.db.db_path)

    act.expected_stdout = expected_stdout
    act.isql(switches=['-q'], input = 'set count on;set list on;select id,who from detach_audit;', combine_output = True)
    assert act.clean_stdout == act.clean_expected_stdout
