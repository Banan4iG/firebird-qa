#coding:utf-8

"""
ID:          java.fts.fts-20
TITLE:       
DESCRIPTION: 
  Test for full reindex.
FBTEST:      functional.java.fts.fts_20
"""

import pytest
from firebird.qa import *

# version: 3.0

substitutions_1 = [('SQL>.*', ''), ('CON>', ''), ('RDBMSDirectory@.*:', 'RDBMSDirectory...:')]

db_1 = db_factory(from_backup='fts_new.fbk')

act_1 = python_act('db_1', substitutions=substitutions_1)

expected_stdout_1 = """FTS$SCORE FTS$RELATION                    FTS$HIGHLIGHT
======================= =============================== ===============================================================================
1.578297138214111 TABLE1                          <B>fts_test_text</B>
FTS$SCORE FTS$RELATION                    FTS$HIGHLIGHT
======================= =============================== ===============================================================================
1.453887343406677 TABLE2                          <B>fts_test_text</B>
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
# EXECUTE PROCEDURE FTS$CREATE_INDEX('TEST_INDEX_1');
# EXECUTE PROCEDURE FTS$CREATE_INDEX('TEST_INDEX_2');
# commit;
# EXECUTE PROCEDURE FTS$ADD_FIELD_TO_INDEX('TEST_INDEX_1', 'TABLE1','F_VCHAR');
# EXECUTE PROCEDURE FTS$ADD_FIELD_TO_INDEX('TEST_INDEX_2', 'TABLE2','F_VCHAR');
# commit;
# INSERT INTO TABLE1(F_VCHAR) VALUES('fts_test_text');
# INSERT INTO TABLE2(F_VCHAR, ID_CHAR) VALUES('fts_test_text', 'abcd');
# COMMIT;
# EXECUTE PROCEDURE FTS$FULL_REINDEX;
# commit;
# 
# SELECT fts$score, fts$relation, FTS$HIGHLIGHT from FTS$SEARCH('TEST_INDEX_1', NULL, 'fts_test_text', 20);
# SELECT fts$score, fts$relation, FTS$HIGHLIGHT from FTS$SEARCH('TEST_INDEX_2', NULL, 'fts_test_text', 20);
# 
# EXECUTE PROCEDURE FTS$DROP_INDEX('TEST_INDEX_1');
# EXECUTE PROCEDURE FTS$DROP_INDEX('TEST_INDEX_2');
# commit;
# DELETE FROM TABLE1 WHERE F_VCHAR = 'fts_test_text';
# DELETE FROM TABLE2 WHERE F_VCHAR = 'fts_test_text';
# COMMIT;
# """ % dsn
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], init_script)
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script)
# -----------------------------------

# version: 4.0

substitutions_2 = [('SQL>.*', ''), ('CON>', ''), ('RDBMSDirectory@.*:', 'RDBMSDirectory...:')]

db_2 = db_factory(from_backup='fts_new.fbk')

act_2 = python_act('db_2', substitutions=substitutions_2)

expected_stdout_2 = """FTS$SCORE FTS$RELATION                    FTS$HIGHLIGHT
======================= =============================== ================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
3.472253799438477 TABLE1                          <B>fts_test_text</B>
FTS$SCORE FTS$RELATION                    FTS$HIGHLIGHT
======================= =============================== ================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
3.198552131652832 TABLE2                          <B>fts_test_text</B>
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
# EXECUTE PROCEDURE FTS$CREATE_INDEX('TEST_INDEX_1');
# EXECUTE PROCEDURE FTS$CREATE_INDEX('TEST_INDEX_2');
# commit;
# EXECUTE PROCEDURE FTS$ADD_FIELD_TO_INDEX('TEST_INDEX_1', 'TABLE1','F_VCHAR');
# EXECUTE PROCEDURE FTS$ADD_FIELD_TO_INDEX('TEST_INDEX_2', 'TABLE2','F_VCHAR');
# commit;
# INSERT INTO TABLE1(F_VCHAR) VALUES('fts_test_text');
# INSERT INTO TABLE2(F_VCHAR, ID_CHAR) VALUES('fts_test_text', 'abcd');
# COMMIT;
# EXECUTE PROCEDURE FTS$FULL_REINDEX;
# commit;
# 
# SELECT fts$score, fts$relation, FTS$HIGHLIGHT from FTS$SEARCH('TEST_INDEX_1', NULL, 'fts_test_text', 20);
# SELECT fts$score, fts$relation, FTS$HIGHLIGHT from FTS$SEARCH('TEST_INDEX_2', NULL, 'fts_test_text', 20);
# 
# EXECUTE PROCEDURE FTS$DROP_INDEX('TEST_INDEX_1');
# EXECUTE PROCEDURE FTS$DROP_INDEX('TEST_INDEX_2');
# commit;
# DELETE FROM TABLE1 WHERE F_VCHAR = 'fts_test_text';
# DELETE FROM TABLE2 WHERE F_VCHAR = 'fts_test_text';
# COMMIT;
# """ % dsn
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], init_script)
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script)
# -----------------------------------

# version: 5.0

substitutions_3 = [('SQL>.*', ''), ('CON>', ''), ('RDBMSDirectory@.*:', 'RDBMSDirectory...:')]

db_3 = db_factory(from_backup='fts_new.fbk')

act_3 = python_act('db_3', substitutions=substitutions_3)

expected_stdout_3 = """FTS$RELATION                    FTS$HIGHLIGHT
=============================== ================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
TABLE1                          <B>fts_test_text</B>
FTS$RELATION                    FTS$HIGHLIGHT
=============================== ================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
TABLE2                          <B>fts_test_text</B>
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
# EXECUTE PROCEDURE FTS$CREATE_INDEX('TEST_INDEX_1');
# EXECUTE PROCEDURE FTS$CREATE_INDEX('TEST_INDEX_2');
# commit;
# EXECUTE PROCEDURE FTS$ADD_FIELD_TO_INDEX('TEST_INDEX_1', 'TABLE1','F_VCHAR');
# EXECUTE PROCEDURE FTS$ADD_FIELD_TO_INDEX('TEST_INDEX_2', 'TABLE2','F_VCHAR');
# commit;
# INSERT INTO TABLE1(F_VCHAR) VALUES('fts_test_text');
# INSERT INTO TABLE2(F_VCHAR, ID_CHAR) VALUES('fts_test_text', 'abcd');
# COMMIT;
# EXECUTE PROCEDURE FTS$FULL_REINDEX;
# commit;
# 
# SELECT fts$relation, FTS$HIGHLIGHT from FTS$SEARCH('TEST_INDEX_1', NULL, 'fts_test_text', 20);
# SELECT fts$relation, FTS$HIGHLIGHT from FTS$SEARCH('TEST_INDEX_2', NULL, 'fts_test_text', 20);
# 
# EXECUTE PROCEDURE FTS$DROP_INDEX('TEST_INDEX_1');
# EXECUTE PROCEDURE FTS$DROP_INDEX('TEST_INDEX_2');
# commit;
# DELETE FROM TABLE1 WHERE F_VCHAR = 'fts_test_text';
# DELETE FROM TABLE2 WHERE F_VCHAR = 'fts_test_text';
# COMMIT;
# """ % dsn
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], init_script)
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script)
# -----------------------------------
