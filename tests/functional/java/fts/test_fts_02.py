#coding:utf-8

"""
ID:          java.fts.fts-02
TITLE:       
DESCRIPTION: 
FBTEST:      functional.java.fts.fts_02
"""

import pytest
from firebird.qa import *

# version: 3.0

substitutions_1 = [('SQL>.*', ''), ('CON>', ''), ('.java:.*\\)', '.java:(replaced))')]

db_1 = db_factory(from_backup='fts_new.fbk')

act_1 = python_act('db_1', substitutions=substitutions_1)

expected_stdout_1 = """FTS$SCORE FTS$RELATION                    FTS$HIGHLIGHT
======================= =============================== ===============================================================================
"""

expected_stderr_1 = """FTS$SCORE FTS$RELATION                    FTS$HIGHLIGHT
======================= =============================== ===============================================================================
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
# INSERT INTO TABLE1(F_VCHAR) VALUES('fts_test_text');
# COMMIT;
# SELECT fts$score, fts$relation, FTS$HIGHLIGHT from FTS$SEARCH('TEST_INDEX', NULL, 'fts_test_text', 500);
# EXECUTE PROCEDURE FTS$DROP_INDEX('TEST_INDEX');
# commit;
# DELETE FROM TABLE1 WHERE F_VCHAR = 'fts_test_text';
# COMMIT;
# """ % dsn
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], init_script)
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script)
# -----------------------------------

# version: 4.0

substitutions_2 = [('SQL>.*', ''), ('CON>', ''), ('.java:.*\\)', '.java:(replaced))')]

db_2 = db_factory(from_backup='fts_new.fbk')

act_2 = python_act('db_2', substitutions=substitutions_2)

expected_stdout_2 = """FTS$SCORE FTS$RELATION                    FTS$HIGHLIGHT
  ======================= =============================== ================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
"""

expected_stderr_2 = """FTS$SCORE FTS$RELATION                    FTS$HIGHLIGHT
  ======================= =============================== ================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
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
# EXECUTE PROCEDURE FTS$ADD_FIELD_TO_INDEX('TEST_INDEX', 'TABLE1','F_VCHAR');
# commit;
# INSERT INTO TABLE1(F_VCHAR) VALUES('fts_test_text');
# COMMIT;
# SELECT fts$score, fts$relation, FTS$HIGHLIGHT from FTS$SEARCH('TEST_INDEX', NULL, 'fts_test_text', 500);
# EXECUTE PROCEDURE FTS$DROP_INDEX('TEST_INDEX');
# commit;
# DELETE FROM TABLE1 WHERE F_VCHAR = 'fts_test_text';
# COMMIT;
# """ % dsn
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], init_script)
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script)
# -----------------------------------

# version: 5.0

substitutions_3 = [('SQL>.*', ''), ('CON>', ''), ('.java:.*\\)', '.java:(replaced))')]

db_3 = db_factory(from_backup='fts_new.fbk')

act_3 = python_act('db_3', substitutions=substitutions_3)

expected_stdout_3 = """FTS$RELATION                    FTS$HIGHLIGHT
  =============================== ================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
"""

expected_stderr_3 = """FTS$RELATION                    FTS$HIGHLIGHT
  =============================== ================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
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
# EXECUTE PROCEDURE FTS$ADD_FIELD_TO_INDEX('TEST_INDEX', 'TABLE1','F_VCHAR');
# commit;
# INSERT INTO TABLE1(F_VCHAR) VALUES('fts_test_text');
# COMMIT;
# SELECT fts$relation, FTS$HIGHLIGHT from FTS$SEARCH('TEST_INDEX', NULL, 'fts_test_text', 500);
# EXECUTE PROCEDURE FTS$DROP_INDEX('TEST_INDEX');
# commit;
# DELETE FROM TABLE1 WHERE F_VCHAR = 'fts_test_text';
# COMMIT;
# """ % dsn
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], init_script)
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script)
# -----------------------------------
