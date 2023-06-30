#coding:utf-8

"""
ID:          java.fts.bugs.bug-33189
TITLE:       Server crash when using calculated fields in external triggers
DESCRIPTION: 
FBTEST:      functional.java.fts.bugs.bug_33189
"""

import pytest
from firebird.qa import *

# version: 3.0

db_1 = db_factory(page_size=4096)

act_1 = python_act('db_1')

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
# connect '%s';
# commit;
# CREATE TABLE TEST (A INTEGER COMPUTED BY (1), B varchar(10), C INTEGER COMPUTED BY (2));
# commit;
# 
# EXECUTE PROCEDURE FTS$CREATE_INDEX('TEST_INDEX', 'Russian');
# EXECUTE PROCEDURE FTS$ADD_FIELD_TO_INDEX('TEST_INDEX', 'TEST', 'B');
# EXECUTE PROCEDURE FTS$REINDEX('TEST_INDEX');
# commit;
# 
# insert into TEST(B) values(null);
# insert into TEST(B) values('value');
# 
# execute procedure FTS$DROP_INDEX('TEST_INDEX');
# commit;
# 
# """ % dsn
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], init_script)
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script)
# -----------------------------------

# version: 4.0

db_2 = db_factory(page_size=4096)

act_2 = python_act('db_2')

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
# connect '%s';
# commit;
# CREATE TABLE TEST (A INTEGER COMPUTED BY (1), B varchar(10), C INTEGER COMPUTED BY (2));
# commit;
# 
# EXECUTE PROCEDURE FTS$CREATE_INDEX('TEST_INDEX', 'Russian');
# EXECUTE PROCEDURE FTS$ADD_FIELD_TO_INDEX('TEST_INDEX', 'TEST', 'B');
# EXECUTE PROCEDURE FTS$REINDEX('TEST_INDEX');
# commit;
# 
# insert into TEST(B) values(null);
# insert into TEST(B) values('value');
# 
# execute procedure FTS$DROP_INDEX('TEST_INDEX');
# commit;
# 
# """ % dsn
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], init_script)
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script)
# -----------------------------------
