#coding:utf-8

"""
ID:          java.fts.fts-13
TITLE:       
DESCRIPTION: 
  Search in a field with none charset.
FBTEST:      functional.java.fts.fts_13
"""

import pytest
from firebird.qa import *

# version: 3.0

db_1 = db_factory(from_backup='fts_new.fbk')

act_1 = python_act('db_1', substitutions=[('SQL>.*', ''), ('CON>', '')])

expected_stdout_1 = """FTS$SCORE FTS$RELATION                    FTS$HIGHLIGHT
======================= =============================== ===============================================================================
1.008684277534485 TABLE3                          <B>fts_test_text</B>
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
# EXECUTE PROCEDURE FTS$ADD_FIELD_TO_INDEX('TEST_INDEX', 'TABLE3','F_CHAR');
# commit;
# INSERT INTO TABLE3(F_CHAR) VALUES('fts_test_text');
# COMMIT;
# EXECUTE PROCEDURE FTS$REINDEX('TEST_INDEX');
# commit;
# SELECT fts$score, fts$relation, FTS$HIGHLIGHT from FTS$SEARCH('TEST_INDEX', NULL, 'fts_test_text', 20);
# EXECUTE PROCEDURE FTS$DROP_INDEX('TEST_INDEX');
# commit;
# DELETE FROM TABLE3 WHERE F_CHAR = 'fts_test_text';
# COMMIT;
# """ % dsn
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], init_script)
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script)
# -----------------------------------

# version: 4.0

db_2 = db_factory(from_backup='fts_new.fbk')

act_2 = python_act('db_2', substitutions=[('SQL>.*', ''), ('CON>', '')])

expected_stdout_2 = """FTS$SCORE FTS$RELATION                    FTS$HIGHLIGHT
======================= =============================== ================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
2.219105243682861 TABLE3                          <B>fts_test_text</B>
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
# EXECUTE PROCEDURE FTS$ADD_FIELD_TO_INDEX('TEST_INDEX', 'TABLE3','F_CHAR');
# commit;
# INSERT INTO TABLE3(F_CHAR) VALUES('fts_test_text');
# COMMIT;
# EXECUTE PROCEDURE FTS$REINDEX('TEST_INDEX');
# commit;
# SELECT fts$score, fts$relation, FTS$HIGHLIGHT from FTS$SEARCH('TEST_INDEX', NULL, 'fts_test_text', 20);
# EXECUTE PROCEDURE FTS$DROP_INDEX('TEST_INDEX');
# commit;
# DELETE FROM TABLE3 WHERE F_CHAR = 'fts_test_text';
# COMMIT;
# """ % dsn
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], init_script)
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script)
# -----------------------------------

# version: 5.0

db_3 = db_factory(from_backup='fts_new.fbk')

act_3 = python_act('db_3', substitutions=[('SQL>.*', ''), ('CON>', '')])

expected_stdout_3 = """FTS$RELATION                    FTS$HIGHLIGHT
=============================== ================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
TABLE3                          <B>fts_test_text</B>
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
# EXECUTE PROCEDURE FTS$ADD_FIELD_TO_INDEX('TEST_INDEX', 'TABLE3','F_CHAR');
# commit;
# INSERT INTO TABLE3(F_CHAR) VALUES('fts_test_text');
# COMMIT;
# EXECUTE PROCEDURE FTS$REINDEX('TEST_INDEX');
# commit;
# SELECT fts$relation, FTS$HIGHLIGHT from FTS$SEARCH('TEST_INDEX', NULL, 'fts_test_text', 20);
# EXECUTE PROCEDURE FTS$DROP_INDEX('TEST_INDEX');
# commit;
# DELETE FROM TABLE3 WHERE F_CHAR = 'fts_test_text';
# COMMIT;
# """ % dsn
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], init_script)
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script)
# -----------------------------------
