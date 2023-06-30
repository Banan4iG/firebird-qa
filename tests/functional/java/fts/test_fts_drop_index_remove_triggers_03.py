#coding:utf-8

"""
ID:          java.fts.fts-drop-index-remove-triggers-03
TITLE:       
DESCRIPTION: 
  FTS$DROP_INDEX should drop appropriate FTS$ triggers
FBTEST:      functional.java.fts.fts_drop_index_remove_triggers_03
"""

import pytest
from firebird.qa import *

# version: 3.0

db_1 = db_factory()

act_1 = python_act('db_1', substitutions=[('SQL>.*', ''), ('CON>', '')])

expected_stdout_1 = """RDB$TRIGGER_NAME
===============================
FTS$TRIG_1
"""

@pytest.mark.skip('FIXME: Not IMPLEMENTED')
@pytest.mark.java
@pytest.mark.version('>=3.0,<4.0')
def test_1(act_1: Action):
    pytest.fail("Not IMPLEMENTED")

# Original python code for this test:
# -----------------------------------
# 
# import os
# 
# fts_script_path = os.path.join(context['rdb_path'], 'misc', 'fts.sql')
# 
# init_script = """
# connect '%s';
# create role fts;
# grant default fts to sysdba;
# commit;
# connect '%s';
# input '%s';
# commit;
# """ % (dsn, dsn, fts_script_path)
# 
# test_script = """
# CONNECT '%s';
# create table a(b varchar(255), c varchar(255));
# commit;
# EXECUTE PROCEDURE FTS$CREATE_INDEX('IDX');
# commit;
# EXECUTE PROCEDURE FTS$ADD_FIELD_TO_INDEX('IDX', 'A','B');
# EXECUTE PROCEDURE FTS$ADD_FIELD_TO_INDEX('IDX', 'A','C');
# commit;
# EXECUTE PROCEDURE FTS$DROP_FIELD_FROM_INDEX('IDX', 'A','C');
# commit;
# select rdb$trigger_name from rdb$triggers where rdb$trigger_name like 'FTS$TRIG%%';
# commit;
# EXECUTE PROCEDURE FTS$DROP_INDEX('IDX');
# commit;
# set list;
# select rdb$trigger_name from rdb$triggers where rdb$trigger_name like 'FTS$TRIG%%';
# """ % dsn
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], init_script)
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script)
# -----------------------------------

# version: 4.0

db_2 = db_factory()

act_2 = python_act('db_2', substitutions=[('SQL>.*', ''), ('CON>', '')])

expected_stdout_2 = """RDB$TRIGGER_NAME
===============================================================
FTS$TRIG_1
"""

@pytest.mark.skip('FIXME: Not IMPLEMENTED')
@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    pytest.fail("Not IMPLEMENTED")

# Original python code for this test:
# -----------------------------------
# 
# import os
# 
# fts_script_path = os.path.join(context['rdb_path'], 'misc', 'fts.sql')
# 
# init_script = """
# connect '%s';
# create role fts;
# grant default fts to sysdba;
# commit;
# connect '%s';
# input '%s';
# commit;
# """ % (dsn, dsn, fts_script_path)
# 
# test_script = """
# CONNECT '%s';
# create table a(b varchar(255), c varchar(255));
# commit;
# EXECUTE PROCEDURE FTS$CREATE_INDEX('IDX');
# commit;
# EXECUTE PROCEDURE FTS$ADD_FIELD_TO_INDEX('IDX', 'A','B');
# EXECUTE PROCEDURE FTS$ADD_FIELD_TO_INDEX('IDX', 'A','C');
# commit;
# EXECUTE PROCEDURE FTS$DROP_FIELD_FROM_INDEX('IDX', 'A','C');
# commit;
# select rdb$trigger_name from rdb$triggers where rdb$trigger_name like 'FTS$TRIG%%';
# commit;
# EXECUTE PROCEDURE FTS$DROP_INDEX('IDX');
# commit;
# set list;
# select rdb$trigger_name from rdb$triggers where rdb$trigger_name like 'FTS$TRIG%%';
# """ % dsn
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], init_script)
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script)
# -----------------------------------
