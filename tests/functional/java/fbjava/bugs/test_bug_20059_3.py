#coding:utf-8

"""
ID:          java.fbjava.bugs.bug-20059-3
TITLE:       Checking the possibility of restoring a database with the fbjava engine turned off, when the database has external procedures, functions and triggers on Java. Functions, procedures, and triggers have dependencies (see #48701). Functionality of the procedures, functions and triggers is checked.
DESCRIPTION: 
FBTEST:      functional.java.fbjava.bugs.bug_20059_3
"""

import pytest
from firebird.qa import *
from pathlib import Path
import time

db = db_factory(do_not_create=True)

act = python_act('db')

expected_stdout = """
FUNC_1
=====================
-300
PSQL_FUNC_1
=======================
100.0000000000000
"""

backup_filename = 'bug_20059_2.fbk'

conf = store_config('plugins.conf')
new_config = temp_file('new_plugins.conf')

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action, conf: ConfigManager, new_config: Path):
    script = """
        SELECT FUNC_1(-300) FROM rdb$database;
        commit;
        SELECT PSQL_FUNC_1(100.23) FROM rdb$database;
        commit;
        
        EXECUTE PROCEDURE proc_1(3400);
        EXECUTE PROCEDURE psql_proc_1(-100);
        
        
        create table table_for_trigger(id integer);
        commit;
        
        EXECUTE PROCEDURE MAINTEST(124.68);
        commit;
    """

    new_config.write_text('#empty config')
    conf.replace(new_config)

    # run gbak in embedded mode
    backup = act.vars['backups'] / backup_filename
    act.gbak(switches=['-c', '-rep', str(backup), act.db.dsn])
  
    act.reset()
    act.expected_stdout = expected_stdout
    act.isql(switches=['-q'], input=script)
    assert act.clean_stdout == act.clean_expected_stdout
