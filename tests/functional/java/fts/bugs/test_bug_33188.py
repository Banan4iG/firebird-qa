#coding:utf-8

"""
ID:          java.fts.bugs.bug-33188
TITLE:       
DESCRIPTION: 
  Executing procedure with 3 parameters call error Invalid BLOB ID
FBTEST:      functional.java.fts.bugs.bug_33188
"""

import pytest
from firebird.qa import *

db = db_factory(page_size=4096)

act = python_act('db')

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
# """ % (dsn, dsn, fts_script_path)
# 
# test_script = """
# connect '%s';
# commit;
# CREATE TABLE TEST (A integer , B varchar(10));
# commit;
# 
# EXECUTE PROCEDURE FTS$CREATE_INDEX('TEST_INDEX', null,'Test index for FTS');
# EXECUTE PROCEDURE FTS$ADD_FIELD_TO_INDEX('TEST_INDEX', 'TEST', 'A');
# EXECUTE PROCEDURE FTS$REINDEX('TEST_INDEX');
# commit;
# execute procedure FTS$DROP_INDEX('TEST_INDEX');
# commit;
# 
# """ % dsn
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], init_script)
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script)
# -----------------------------------
