#coding:utf-8

"""
ID:          java.fts.case-conversion-8289
TITLE:       
DESCRIPTION: 
  Check if FTS$* procedures properly converting case of tables/fields
FBTEST:      functional.java.fts.case_conversion_8289
"""

import pytest
from firebird.qa import *

substitutions = [('SQL>.*', ''), ('CON>', ''), ('java:[0-9]+', 'java'), ('\\s*at\\s*.*', '')]

db = db_factory(from_backup='fts_new.fbk')

act = python_act('db', substitutions=substitutions)

expected_stdout = """FTS$INDEX_NAME                  TEST_INDEX1
FTS$INDEX_NAME                  TEST_INDEX2
FTS$INDEX_NAME                  TEST_index3
FTS$INDEX_NAME                  TEST_INDEX1
FTS$RELATION_NAME               TABLE1
FTS$FIELD_NAME                  F_VCHAR
FTS$INDEX_NAME                  TEST_INDEX2
FTS$RELATION_NAME               TABLE1
FTS$FIELD_NAME                  F_VCHAR
FTS$INDEX_NAME                  TEST_index3
FTS$RELATION_NAME               TABLE1
FTS$FIELD_NAME                  F_VCHAR
"""

expected_stderr = """FTS$INDEX_NAME                  TEST_INDEX1
FTS$INDEX_NAME                  TEST_INDEX2
FTS$INDEX_NAME                  TEST_index3
FTS$INDEX_NAME                  TEST_INDEX1
FTS$RELATION_NAME               TABLE1
FTS$FIELD_NAME                  F_VCHAR
FTS$INDEX_NAME                  TEST_INDEX2
FTS$RELATION_NAME               TABLE1
FTS$FIELD_NAME                  F_VCHAR
FTS$INDEX_NAME                  TEST_index3
FTS$RELATION_NAME               TABLE1
FTS$FIELD_NAME                  F_VCHAR
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
# """ % (dsn, dsn, fts_script_path)
# 
# test_script = """
# CONNECT '%s';
# commit;
# EXECUTE PROCEDURE FTS$CREATE_INDEX('TEST_INDEX1');
# EXECUTE PROCEDURE FTS$CREATE_INDEX('TEST_index2');
# EXECUTE PROCEDURE FTS$CREATE_INDEX('"TEST_index3"');
# commit;
# 
# EXECUTE PROCEDURE FTS$ADD_FIELD_TO_INDEX('TEST_INDEX1', 'TABLE1', 'F_VCHAR');
# EXECUTE PROCEDURE FTS$ADD_FIELD_TO_INDEX('TEST_INDEX2', 'table1', 'f_vchar');
# EXECUTE PROCEDURE FTS$ADD_FIELD_TO_INDEX('TEST_index3', 'table1', 'f_vchar');
# EXECUTE PROCEDURE FTS$ADD_FIELD_TO_INDEX('"TEST_index3"', 'table1', 'f_vchar');
# commit;
# 
# set list;
# select fts$index_name from fts$indices;
# select fts$index_name, fts$relation_name, fts$field_name from fts$index_segments;
# 
# EXECUTE PROCEDURE FTS$REINDEX('test_index1');
# EXECUTE PROCEDURE FTS$REINDEX('TEST_INDEX2');
# EXECUTE PROCEDURE FTS$REINDEX('"TEST_index3"');
# EXECUTE PROCEDURE FTS$REINDEX('TEST_index3');
# 
# EXECUTE PROCEDURE FTS$DROP_FIELD_FROM_INDEX('TEST_INDEX1', 'TABLE1', 'F_VCHAR');
# EXECUTE PROCEDURE FTS$DROP_FIELD_FROM_INDEX('TEST_INDEX2', 'table1', 'f_vchar');
# EXECUTE PROCEDURE FTS$DROP_FIELD_FROM_INDEX('"TEST_index3"', 'table1', 'f_vchar');
# commit;
# 
# select fts$index_name, fts$relation_name, fts$field_name from fts$index_segments;
# 
# EXECUTE PROCEDURE FTS$DROP_INDEX('TEST_index1');
# EXECUTE PROCEDURE FTS$DROP_INDEX('TEST_INDEX2');
# EXECUTE PROCEDURE FTS$DROP_INDEX('"TEST_index3"');
# commit;
# 
# select fts$index_name from fts$indices;
# """ % dsn
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], init_script)
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script)
# -----------------------------------
