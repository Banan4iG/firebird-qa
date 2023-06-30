#coding:utf-8

"""
ID:          java.fts.bugs.bug-12306
TITLE:       Error during execution of a search query
DESCRIPTION: 
FBTEST:      functional.java.fts.bugs.bug_12306
"""

import pytest
from firebird.qa import *

# version: 3.0

db_1 = db_factory(page_size=4096)

act_1 = python_act('db_1')

expected_stdout_1 = """ 
ID STR
============ ===============================================================================
6 record6
ID
============
6
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
# connect '%s';
# commit;
# create table TEST_TABLE(ID int primary key, STR varchar(100));
# commit;
# insert into TEST_TABLE values (1, 'record1');
# commit;
# 
# execute procedure FTS$CREATE_INDEX('idx');
# commit;
# execute procedure FTS$ADD_FIELD_TO_INDEX('idx', 'TEST_TABLE', 'STR');
# commit;
# execute procedure fts$reindex('idx');
# commit;
# insert into TEST_TABLE values (6, 'record6');
# commit;
# 
# select TEST_TABLE.* from fts$pool fts join TEST_TABLE on fts.fts$row_id=TEST_TABLE.rdb$db_key where TEST_TABLE.ID=6;
# commit;
# --execute procedure fts$reindex('idx');
# --commit;
# select B.id from fts$search('idx', 'TEST_TABLE', 'record6', 100) as A left join TEST_TABLE as B on A.fts$row_id=b.rdb$db_key where B.id=6;
# commit;
# select * from fts$pool;
# 
# execute procedure FTS$DROP_INDEX('idx');
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

expected_stdout_2 = """
ID STR
============ ====================================================================================================
6 record6
ID
============
6
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
# connect '%s';
# commit;
# create table TEST_TABLE(ID int primary key, STR varchar(100));
# commit;
# insert into TEST_TABLE values (1, 'record1');
# commit;
# 
# execute procedure FTS$CREATE_INDEX('idx');
# commit;
# execute procedure FTS$ADD_FIELD_TO_INDEX('idx', 'TEST_TABLE', 'STR');
# commit;
# execute procedure fts$reindex('idx');
# commit;
# insert into TEST_TABLE values (6, 'record6');
# commit;
# 
# select TEST_TABLE.* from fts$pool fts join TEST_TABLE on fts.fts$row_id=TEST_TABLE.rdb$db_key where TEST_TABLE.ID=6;
# commit;
# --execute procedure fts$reindex('idx');
# --commit;
# select B.id from fts$search('idx', 'TEST_TABLE', 'record6', 100) as A left join TEST_TABLE as B on A.fts$row_id=b.rdb$db_key where B.id=6;
# commit;
# select * from fts$pool;
# 
# execute procedure FTS$DROP_INDEX('idx');
# commit;
# 
# """ % dsn
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], init_script)
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script)
# -----------------------------------
