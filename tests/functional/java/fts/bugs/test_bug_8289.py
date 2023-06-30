#coding:utf-8

"""
ID:          java.fts.bugs.bug-8289
TITLE:       Procedure FTS$ADD_FIELD_TO_INDEX doesnt lead fields and table names to upper case
DESCRIPTION: 
FBTEST:      functional.java.fts.bugs.bug_8289
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
# create table TEST_TABLE1(id int primary key, str varchar(50));
# commit;
# create table TEST_TABLE2(id int primary key, str varchar(50));
# commit;
# execute procedure FTS$CREATE_INDEX('idx1', null, null);
# commit;
# execute procedure FTS$CREATE_INDEX('idx2', null, null);
# commit;
# execute procedure FTS$ADD_FIELD_TO_INDEX('idx1', 'TEST_TABLE1', 'str');
# commit;
# execute procedure FTS$ADD_FIELD_TO_INDEX('idx1', 'test_table1', 'ID');
# commit;
# execute procedure FTS$ADD_FIELD_TO_INDEX('idx2', 'test_table2', 'str');
# commit;
# execute procedure FTS$ADD_FIELD_TO_INDEX('idx2', 'test_Table2', 'Id');
# commit;
# execute procedure FTS$DROP_INDEX('idx1');
# commit;
# execute procedure FTS$DROP_INDEX('idx2');
# commit;
# """ % dsn
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], init_script)
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script)
# -----------------------------------
