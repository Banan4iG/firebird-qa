#coding:utf-8

"""
ID:          java.fts.pool-filler-check
TITLE:       
DESCRIPTION: 
  Check trigger which fills fts$pool table
FBTEST:      functional.java.fts.pool_filler_check
"""

import pytest
from firebird.qa import *

# version: 3.0

db_1 = db_factory(from_backup='fts_new.fbk')

act_1 = python_act('db_1', substitutions=[('SQL>.*', ''), ('CON>', '')])

expected_stdout_1 = """FTS$ROW_ID       FTS$STATUS
================ ==========
80000000E3010000          1
FTS$ROW_ID       FTS$STATUS
================ ==========
80000000E3010000          1
80000000E4010000          1
FTS$ROW_ID       FTS$STATUS
================ ==========
80000000E3010000          1
80000000E4010000          1
80000000E3010000          3
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
# commit;
# EXECUTE PROCEDURE FTS$CREATE_INDEX('TEST_INDEX');
# commit;
# EXECUTE PROCEDURE FTS$ADD_FIELD_TO_INDEX('TEST_INDEX', 'TABLE1','F_VCHAR');
# commit;
# EXECUTE PROCEDURE FTS$REINDEX('TEST_INDEX');
# commit;
# INSERT INTO TABLE1(F_VCHAR) VALUES('fts_test_text1');
# COMMIT;
# select * from fts$pool;
# INSERT INTO TABLE1(F_VCHAR) VALUES('fts_test_text2');
# COMMIT;
# select * from fts$pool;
# commit;
# delete from table1 where f_vchar='fts_test_text1';
# COMMIT;
# select * from fts$pool;
# EXECUTE PROCEDURE FTS$DROP_INDEX('TEST_INDEX');
# """ % dsn
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], init_script)
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script)
# -----------------------------------

# version: 4.0

db_2 = db_factory(from_backup='fts_new.fbk')

act_2 = python_act('db_2', substitutions=[('SQL>.*', ''), ('CON>', '')])

expected_stdout_2 = """FTS$ROW_ID       FTS$STATUS
================ ==========
80000000E3010000          1
FTS$ROW_ID       FTS$STATUS
================ ==========
80000000E3010000          1
80000000E4010000          1
FTS$ROW_ID       FTS$STATUS
================ ==========
80000000E3010000          1
80000000E4010000          1
80000000E3010000          3
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
# commit;
# EXECUTE PROCEDURE FTS$CREATE_INDEX('TEST_INDEX');
# commit;
# EXECUTE PROCEDURE FTS$ADD_FIELD_TO_INDEX('TEST_INDEX', 'TABLE1','F_VCHAR');
# commit;
# EXECUTE PROCEDURE FTS$REINDEX('TEST_INDEX');
# commit;
# INSERT INTO TABLE1(F_VCHAR) VALUES('fts_test_text1');
# COMMIT;
# select * from fts$pool;
# INSERT INTO TABLE1(F_VCHAR) VALUES('fts_test_text2');
# COMMIT;
# select * from fts$pool;
# commit;
# delete from table1 where f_vchar='fts_test_text1';
# COMMIT;
# select * from fts$pool;
# EXECUTE PROCEDURE FTS$DROP_INDEX('TEST_INDEX');
# """ % dsn
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], init_script)
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script)
# -----------------------------------
