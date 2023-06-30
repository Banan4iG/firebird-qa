#coding:utf-8

"""
ID:          java.fts.fts-09
TITLE:       
DESCRIPTION: 
  Test for search in blobs.
  Search in *.xls blob.
FBTEST:      functional.java.fts.fts_09
"""

import pytest
from firebird.qa import *

# version: 3.0

db_1 = db_factory(from_backup='fts_new.fbk')

act_1 = python_act('db_1', substitutions=[('SQL>.*', ''), ('CON>', '')])

expected_stdout_1 = """FTS$SCORE FTS$RELATION                    FTS$HIGHLIGHT
======================= =============================== ===============================================================================
2.209983587265015 TABLE2                          	<B>Red</B> <B>Data</B> <B>Base</B> 2.1	51
0.6767255067825317 TABLE2                          	<B>Red</B>...	<B>Red</B>
0.6153562068939209 TABLE2                          	<B>Red</B>...	<B>Red</B>
0.4885821342468262 TABLE2                          	<B>Red</B>
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
# EXECUTE PROCEDURE FTS$ADD_FIELD_TO_INDEX('TEST_INDEX', 'TABLE2', 'F_XSL_BLOB');
# commit;
# EXECUTE PROCEDURE FTS$REINDEX('TEST_INDEX');
# commit;
# SELECT fts$score, fts$relation, FTS$HIGHLIGHT from FTS$SEARCH('TEST_INDEX', NULL, 'Red Data Base', 10);
# EXECUTE PROCEDURE FTS$DROP_INDEX('TEST_INDEX');
# commit;
# """ % dsn
# 
# runProgram('isql',['-user', user_name,'-password', user_password, '-q'],init_script)
# runProgram('isql',['-user', user_name,'-password', user_password, '-q'],test_script)
# -----------------------------------

# version: 4.0

db_2 = db_factory(from_backup='fts_new.fbk')

act_2 = python_act('db_2', substitutions=[('SQL>.*', ''), ('CON>', '')])

expected_stdout_2 = """FTS$SCORE FTS$RELATION                    FTS$HIGHLIGHT
======================= =============================== ================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
5.011581420898438 TABLE2                          	<B>Red</B> <B>Data</B> <B>Base</B> 2.1	51
1.485564470291138 TABLE2                          	<B>Red</B>...	<B>Red</B>
1.350495815277100 TABLE2                          	<B>Red</B>...	<B>Red</B>
1.071256756782532 TABLE2                          	<B>Red</B>
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
# EXECUTE PROCEDURE FTS$ADD_FIELD_TO_INDEX('TEST_INDEX', 'TABLE2', 'F_XSL_BLOB');
# commit;
# EXECUTE PROCEDURE FTS$REINDEX('TEST_INDEX');
# commit;
# SELECT fts$score, fts$relation, FTS$HIGHLIGHT from FTS$SEARCH('TEST_INDEX', NULL, 'Red Data Base', 10);
# EXECUTE PROCEDURE FTS$DROP_INDEX('TEST_INDEX');
# commit;
# """ % dsn
# 
# runProgram('isql',['-user', user_name,'-password', user_password, '-q'],init_script)
# runProgram('isql',['-user', user_name,'-password', user_password, '-q'],test_script)
# -----------------------------------

# version: 5.0

db_3 = db_factory(from_backup='fts_new.fbk')

act_3 = python_act('db_3', substitutions=[('SQL>.*', ''), ('CON>', '')])

expected_stdout_3 = """FTS$RELATION                    FTS$HIGHLIGHT
=============================== ================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
TABLE2                          	<B>Red</B> <B>Data</B> <B>Base</B> 2.1	51
TABLE2                          	<B>Red</B>...	<B>Red</B>
TABLE2                          	<B>Red</B>...	<B>Red</B>
TABLE2                          	<B>Red</B>
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
# EXECUTE PROCEDURE FTS$ADD_FIELD_TO_INDEX('TEST_INDEX', 'TABLE2', 'F_XSL_BLOB');
# commit;
# EXECUTE PROCEDURE FTS$REINDEX('TEST_INDEX');
# commit;
# SELECT fts$relation, FTS$HIGHLIGHT from FTS$SEARCH('TEST_INDEX', NULL, 'Red Data Base', 10);
# EXECUTE PROCEDURE FTS$DROP_INDEX('TEST_INDEX');
# commit;
# """ % dsn
# 
# runProgram('isql',['-user', user_name,'-password', user_password, '-q'],init_script)
# runProgram('isql',['-user', user_name,'-password', user_password, '-q'],test_script)
# -----------------------------------
