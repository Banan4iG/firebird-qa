#coding:utf-8

"""
ID:          java.fts.handle-corrupted-docs
TITLE:       
DESCRIPTION: 
  Raise error with DB_KEY of table with corrupted document
FBTEST:      functional.java.fts.handle_corrupted_docs
"""

import pytest
from firebird.qa import *

# version: 3.0

substitutions_1 = [('dbkey: [0-9a-f]+', 'dbkey: xxxxxxxxxxxxxxxx'), ('@[0-9a-f]+', '@xxxxxxxx'), ('\\(\\w+\\.\\w+:\\d+\\)', '')]

db_1 = db_factory(page_size=4096)

act_1 = python_act('db_1', substitutions=substitutions_1)

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
# corrupted_doc_path = os.path.join(context['files_location'], 'corrupted.odt')
# 
# init_script = """
# connect '%s';
# create table test(doc blob);
# create role fts;
# grant default fts to sysdba;
# commit;
# connect '%s';
# input '%s';
# commit;
# EXECUTE PROCEDURE FTS$CREATE_INDEX('TEST_INDEX');
# EXECUTE PROCEDURE FTS$ADD_FIELD_TO_INDEX('TEST_INDEX', 'TEST', 'DOC');
# commit;
# """ % (dsn, dsn, fts_script_path)
# 
# test_script = """
# connect '%s';
# EXECUTE PROCEDURE FTS$REINDEX('TEST_INDEX');
# """ % dsn
# 
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], init_script)
# 
# #insert corrupted document
# conn = fdb.connect(dsn=dsn, user=user_name, password=user_password)
# cur = conn.cursor()
# with open(corrupted_doc_path, 'rb') as f:
# 	cur.execute('insert into test values(?)', (f,))
# conn.commit()
# conn.close()
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script)
# -----------------------------------

# version: 4.0

substitutions_2 = [('dbkey: [0-9a-f]+', 'dbkey: xxxxxxxxxxxxxxxx'), ('@[0-9a-f]+', '@xxxxxxxx'), ('\\(\\w+\\.\\w+:\\d+\\)', '')]

db_2 = db_factory(page_size=4096)

act_2 = python_act('db_2', substitutions=substitutions_2)

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
# corrupted_doc_path = os.path.join(context['files_location'], 'corrupted.odt')
# 
# init_script = """
# connect '%s';
# create table test(doc blob);
# create role fts;
# grant default fts to sysdba;
# commit;
# connect '%s';
# input '%s';
# commit;
# EXECUTE PROCEDURE FTS$CREATE_INDEX('TEST_INDEX');
# EXECUTE PROCEDURE FTS$ADD_FIELD_TO_INDEX('TEST_INDEX', 'TEST', 'DOC');
# commit;
# """ % (dsn, dsn, fts_script_path)
# 
# test_script = """
# connect '%s';
# EXECUTE PROCEDURE FTS$REINDEX('TEST_INDEX');
# """ % dsn
# 
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], init_script)
# 
# #insert corrupted document
# conn = fdb.connect(dsn=dsn, user=user_name, password=user_password)
# cur = conn.cursor()
# with open(corrupted_doc_path, 'rb') as f:
# 	cur.execute('insert into test values(?)', (f,))
# conn.commit()
# conn.close()
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script)
# -----------------------------------

# version: 5.0

substitutions_3 = [('dbkey: [0-9a-f]+', 'dbkey: xxxxxxxxxxxxxxxx'), ('@[0-9a-f]+', '@xxxxxxxx'), ('\\(\\w+\\.\\w+:\\d+\\)', '')]

db_3 = db_factory(page_size=4096)

act_3 = python_act('db_3', substitutions=substitutions_3)

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
# corrupted_doc_path = os.path.join(context['files_location'], 'corrupted.odt')
# 
# init_script = """
# connect '%s';
# create table test(doc blob);
# create role fts;
# grant default fts to sysdba;
# commit;
# connect '%s';
# input '%s';
# commit;
# EXECUTE PROCEDURE FTS$CREATE_INDEX('TEST_INDEX');
# EXECUTE PROCEDURE FTS$ADD_FIELD_TO_INDEX('TEST_INDEX', 'TEST', 'DOC');
# commit;
# """ % (dsn, dsn, fts_script_path)
# 
# test_script = """
# connect '%s';
# EXECUTE PROCEDURE FTS$REINDEX('TEST_INDEX');
# """ % dsn
# 
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], init_script)
# 
# #insert corrupted document
# conn = fdb.connect(dsn=dsn, user=user_name, password=user_password)
# cur = conn.cursor()
# with open(corrupted_doc_path, 'rb') as f:
# 	cur.execute('insert into test values(?)', (f,))
# conn.commit()
# conn.close()
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script)
# -----------------------------------
