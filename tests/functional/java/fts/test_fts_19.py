#coding:utf-8

"""
ID:          java.fts.fts-19
TITLE:       
DESCRIPTION: 
  Test for completely index removing
FBTEST:      functional.java.fts.fts_19
"""

import pytest
from firebird.qa import *

# version: 3.0

db_1 = db_factory(from_backup='fts_new.fbk')

act_1 = python_act('db_1', substitutions=[('SQL>.*.*', ''), ('CON>', '')])

expected_stdout_1 = """FTS$SCORE FTS$RELATION                    FTS$HIGHLIGHT
======================= =============================== ===============================================================================
0.3663582801818848 TABLE1                           <B>Control</B>... <B>Control</B>
0.3663582801818848 TABLE1                           <B>Control</B>... <B>Control</B>
0.3519524335861206 TABLE1                           <B>Control</B>... <B>CONTROL</B>
0.3519524335861206 TABLE1                           <B>Control</B>... <B>CONTROL</B>
0.2604897320270538 TABLE1                           <B>Control</B>
0.2347523570060730 TABLE1                          =&quot;<B>Control</B>
Index removed completely
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
# EXECUTE PROCEDURE FTS$ADD_FIELD_TO_INDEX('TEST_INDEX', 'TABLE1', 'F_DOC_BLOB');
# commit;
# EXECUTE PROCEDURE FTS$REINDEX('TEST_INDEX');
# commit;
# SELECT fts$score, fts$relation, FTS$HIGHLIGHT from FTS$SEARCH('TEST_INDEX', NULL, 'Control', 7);
# EXECUTE PROCEDURE FTS$DROP_INDEX('TEST_INDEX');
# commit;
# 
# """ % dsn
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], init_script)
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script)
# 
# 
# (fb_path, sec2) = os.path.split(context['isc4_path'])
# idx_path = os.path.join(fb_path, 'index.tmp/TEST_INDEX')
# 
# 
# if os.path.exists(idx_path):
# 	print('Index does not completely removed')
# else:
# print('Index removed completely')
# -----------------------------------

# version: 4.0

db_2 = db_factory(from_backup='fts_new.fbk')

act_2 = python_act('db_2', substitutions=[('SQL>.*.*', ''), ('CON>', '')])

expected_stdout_2 = """FTS$SCORE FTS$RELATION                    FTS$HIGHLIGHT
======================= =============================== ================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
0.8167163133621216 TABLE1                           <B>Control</B>... <B>Control</B>
0.8167163133621216 TABLE1                           <B>Control</B>... <B>Control</B>
0.7746293544769287 TABLE1                           <B>Control</B>... <B>CONTROL</B>
0.7746293544769287 TABLE1                           <B>Control</B>... <B>CONTROL</B>
0.5531942844390869 TABLE1                           <B>Control</B>
0.5167883038520813 TABLE1                          ="<B>Control</B>
Index removed completely
"""

@pytest.mark.skip('FIXME: Not IMPLEMENTED')
@pytest.mark.java
@pytest.mark.version('>=4.0,<5.0')
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
# EXECUTE PROCEDURE FTS$ADD_FIELD_TO_INDEX('TEST_INDEX', 'TABLE1', 'F_DOC_BLOB');
# commit;
# EXECUTE PROCEDURE FTS$REINDEX('TEST_INDEX');
# commit;
# SELECT fts$score, fts$relation, FTS$HIGHLIGHT from FTS$SEARCH('TEST_INDEX', NULL, 'Control', 7);
# EXECUTE PROCEDURE FTS$DROP_INDEX('TEST_INDEX');
# commit;
# 
# """ % dsn
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], init_script)
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script)
# 
# 
# (fb_path, sec2) = os.path.split(context['isc4_path'])
# idx_path = os.path.join(fb_path, 'index.tmp/TEST_INDEX')
# 
# 
# if os.path.exists(idx_path):
# 	print('Index does not completely removed')
# else:
# print('Index removed completely')
# -----------------------------------

# version: 5.0

db_3 = db_factory(from_backup='fts_new.fbk')

act_3 = python_act('db_3', substitutions=[('SQL>.*.*', ''), ('CON>', '')])

expected_stdout_3 = """FTS$RELATION                    FTS$HIGHLIGHT
=============================== ================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
TABLE1                           <B>Control</B>... <B>Control</B>
TABLE1                           <B>Control</B>... <B>Control</B>
TABLE1                           <B>Control</B>... <B>CONTROL</B>
TABLE1                           <B>Control</B>... <B>CONTROL</B>
TABLE1                           <B>Control</B>
TABLE1                          =&quot;<B>Control</B>
Index removed completely
"""

@pytest.mark.skip('FIXME: Not IMPLEMENTED')
@pytest.mark.java
@pytest.mark.version('>=5.0')
def test_3(act_3: Action):
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
# EXECUTE PROCEDURE FTS$ADD_FIELD_TO_INDEX('TEST_INDEX', 'TABLE1', 'F_DOC_BLOB');
# commit;
# EXECUTE PROCEDURE FTS$REINDEX('TEST_INDEX');
# commit;
# SELECT fts$relation, FTS$HIGHLIGHT from FTS$SEARCH('TEST_INDEX', NULL, 'Control', 7);
# EXECUTE PROCEDURE FTS$DROP_INDEX('TEST_INDEX');
# commit;
# 
# """ % dsn
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], init_script)
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script)
# 
# 
# (fb_path, sec2) = os.path.split(context['isc4_path'])
# idx_path = os.path.join(fb_path, 'index.tmp/TEST_INDEX')
# 
# 
# if os.path.exists(idx_path):
# 	print('Index does not completely removed')
# else:
# print('Index removed completely')
# -----------------------------------
