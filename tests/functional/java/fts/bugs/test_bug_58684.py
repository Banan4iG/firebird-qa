#coding:utf-8

"""
ID:          java.fts.bugs.bug-58684
TITLE:       Cleared document should be removed from index
DESCRIPTION: 
FBTEST:      functional.java.fts.bugs.bug_58684
"""

import pytest
from firebird.qa import *

db = db_factory(page_size=4096)

act = python_act('db')

expected_stdout = """ 
before document clearing (expected 1):                      1
after document clearing (expected 0):                      0
"""

@pytest.mark.skip('FIXME: Not IMPLEMENTED')
@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
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
# 
# create table test(doc varchar(255));
# 
# insert into TEST values('test string');
# commit;
# 
# EXECUTE PROCEDURE FTS$CREATE_INDEX('TEST_INDEX');
# EXECUTE PROCEDURE FTS$ADD_FIELD_TO_INDEX('TEST_INDEX', 'TEST', 'DOC');
# commit;
# 
# EXECUTE PROCEDURE FTS$REINDEX('TEST_INDEX');
# commit;
# 
# """ % (dsn, dsn, fts_script_path)
# 
# test_script = """
# connect '%s';
# set heading off;
# SELECT 'before document clearing (expected 1): ', count(*) from FTS$SEARCH('TEST_INDEX', NULL, 'string', 20) join test on fts$row_id = rdb$db_key;
# update test set doc='';
# commit;
# SELECT 'after document clearing (expected 0): ', count(*) from FTS$SEARCH('TEST_INDEX', NULL, 'string', 20) join test on fts$row_id = rdb$db_key;
# """ % dsn
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], init_script)
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script)
# -----------------------------------
