#coding:utf-8

"""
ID:          java.fts.fts-search-multiple-databases
TITLE:       
DESCRIPTION: 
  Search multiple databases by index with the same name. A separate directory
  should be created for each database with a FTS index.
FBTEST:      functional.java.fts.fts_search_multiple_databases
"""

import pytest
from firebird.qa import *

# version: 3.0

db_1 = db_factory()

act_1 = python_act('db_1', substitutions=[('SQL>.*', ''), ('CON>', '')])

expected_stdout_1 = """
FTS$SCORE FTS$RELATION                    FTS$HIGHLIGHT
======================= =============================== ===============================================================================
0.03955062106251717 TABLE1                          <B>fts_test_string</B>
0.03955062106251717 TABLE1                          <B>fts_test_string</B>
0.03955062106251717 TABLE1                          <B>fts_test_string</B>
0.03955062106251717 TABLE1                          <B>fts_test_string</B>
0.03955062106251717 TABLE1                          <B>fts_test_string</B>
FTS$SCORE FTS$RELATION                    FTS$HIGHLIGHT
======================= =============================== ===============================================================================
0.02114546112716198 TABLE1                          <B>RandomValuesForInput</B>
0.02114546112716198 TABLE1                          <B>RandomValuesForInput</B>
0.02114546112716198 TABLE1                          <B>RandomValuesForInput</B>
0.02114546112716198 TABLE1                          <B>RandomValuesForInput</B>
0.02114546112716198 TABLE1                          <B>RandomValuesForInput</B>
0.02114546112716198 TABLE1                          <B>RandomValuesForInput</B>
0.02114546112716198 TABLE1                          <B>RandomValuesForInput</B>
0.02114546112716198 TABLE1                          <B>RandomValuesForInput</B>
0.02114546112716198 TABLE1                          <B>RandomValuesForInput</B>
0.02114546112716198 TABLE1                          <B>RandomValuesForInput</B>
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
# fbjava_yaml_path = os.path.join(context['rdb_path'], 'fbjava.yaml')
# jvm_path = os.path.join(context['rdb_path'], 'jvm.args')
# 
# if os.name == 'nt': # Windows
#     f_jvm = open(jvm_path, 'a')
#     f_jvm.seek(0, 2)
#     f_jvm.write("\\n-Djava.io.tmpdir=C:/tmp")
#     f_jvm.write("\\n-Dfts.directory=C:/tmp")
#     f_jvm.close()
#     os.putenv('TMPDIR', 'C:/tmp')
#     os.putenv('TEMP', 'C:/tmp')
#     os.putenv('TMP', 'C:/tmp')
# 
# DBName1 = dsn[:-4]+"1.fdb"
# DBName2 = dsn[:-4]+"2.fdb"
# DBPath1 = db_filename[:-4]+"1.fdb"
# DBPath2 = db_filename[:-4]+"2.fdb"
# 
# runProgram('isql', ['-user', user_name, '-password', user_password, '-q'], "create database '%s';" %DBName1)
# runProgram('isql', ['-user', user_name, '-password', user_password, '-q'], "create database '%s';" %DBName2)
# 
# init_script = """
# connect '%s';
# create role fts;
# grant default fts to sysdba;
# commit;
# connect '%s';
# input '%s';
# commit;
# """
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], init_script % (DBName1, DBName1, fts_script_path))
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], init_script % (DBName2, DBName2, fts_script_path))
# 
# test_script_init_reindex = """
# CONNECT '%s';
# commit;
# CREATE TABLE TABLE1(F_VCHAR VARCHAR(200));
# commit;
# EXECUTE PROCEDURE FTS$CREATE_INDEX('TEST_INDEX');
# commit;
# EXECUTE PROCEDURE FTS$ADD_FIELD_TO_INDEX('TEST_INDEX', 'TABLE1', 'F_VCHAR');
# commit;
# SET TERM ^;
# EXECUTE BLOCK
# AS
# DECLARE I INT = 0;
# BEGIN
#   WHILE (I < '%d') DO
#   BEGIN
#     INSERT INTO TABLE1(F_VCHAR) VALUES('%s');
#     I = I + 1;
#   END
# END^
# SET TERM ;^
# commit;
# EXECUTE PROCEDURE FTS$REINDEX('TEST_INDEX');
# commit;
# """
# 
# test_script_select_drop = """
# CONNECT '%s';
# commit;
# SELECT FTS$SCORE, FTS$RELATION, FTS$HIGHLIGHT from FTS$SEARCH('TEST_INDEX', NULL, '%s', 200);
# commit;
# EXECUTE PROCEDURE FTS$DROP_FIELD_FROM_INDEX('TEST_INDEX', 'TABLE1', 'F_VCHAR');
# commit;
# EXECUTE PROCEDURE FTS$DROP_INDEX('TEST_INDEX');
# commit;
# DELETE FROM TABLE1 WHERE F_VCHAR = '%s';
# commit;
# """
# 
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script_init_reindex % (DBName1, 5, 'fts_test_string'))
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script_init_reindex % (DBName2, 10, 'RandomValuesForInput'))
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script_select_drop % (DBName1, 'fts_test_string', 'fts_test_string'))
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script_select_drop % (DBName2, 'RandomValuesForInput', 'RandomValuesForInput'))
# 
# if os.path.isfile(DBPath1):
#     os.remove(DBPath1);
# if os.path.isfile(DBPath2):
# os.remove(DBPath2);
# -----------------------------------

# version: 4.0

db_2 = db_factory()

act_2 = python_act('db_2', substitutions=[('SQL>.*', ''), ('CON>', '')])

expected_stdout_2 = """
FTS$SCORE FTS$RELATION                    FTS$HIGHLIGHT
======================= =============================== ================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
0.08701137453317642 TABLE1                          <B>fts_test_string</B>
0.08701137453317642 TABLE1                          <B>fts_test_string</B>
0.08701137453317642 TABLE1                          <B>fts_test_string</B>
0.08701137453317642 TABLE1                          <B>fts_test_string</B>
0.08701137453317642 TABLE1                          <B>fts_test_string</B>
FTS$SCORE FTS$RELATION                    FTS$HIGHLIGHT
======================= =============================== ================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
0.04652001708745956 TABLE1                          <B>RandomValuesForInput</B>
0.04652001708745956 TABLE1                          <B>RandomValuesForInput</B>
0.04652001708745956 TABLE1                          <B>RandomValuesForInput</B>
0.04652001708745956 TABLE1                          <B>RandomValuesForInput</B>
0.04652001708745956 TABLE1                          <B>RandomValuesForInput</B>
0.04652001708745956 TABLE1                          <B>RandomValuesForInput</B>
0.04652001708745956 TABLE1                          <B>RandomValuesForInput</B>
0.04652001708745956 TABLE1                          <B>RandomValuesForInput</B>
0.04652001708745956 TABLE1                          <B>RandomValuesForInput</B>
0.04652001708745956 TABLE1                          <B>RandomValuesForInput</B>
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
# jvm_path = os.path.join(context['rdb_path'], 'jvm.args')
# 
# if os.name == 'nt': # Windows
#     f_jvm = open(jvm_path, 'a')
#     f_jvm.seek(0, 2)
#     f_jvm.write("\\n-Djava.io.tmpdir=C:/tmp")
#     f_jvm.write("\\n-Dfts.directory=C:/tmp")
#     f_jvm.close()
# 
# DBName1 = dsn[:-4]+"1.fdb"
# DBName2 = dsn[:-4]+"2.fdb"
# DBPath1 = db_filename[:-4]+"1.fdb"
# DBPath2 = db_filename[:-4]+"2.fdb"
# 
# runProgram('isql', ['-user', user_name, '-password', user_password, '-q'], "create database '%s';" %DBName1)
# runProgram('isql', ['-user', user_name, '-password', user_password, '-q'], "create database '%s';" %DBName2)
# 
# init_script = """
# connect '%s';
# create role fts;
# grant default fts to sysdba;
# commit;
# connect '%s';
# input '%s';
# commit;
# """
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], init_script % (DBName1, DBName1, fts_script_path))
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], init_script % (DBName2, DBName2, fts_script_path))
# 
# test_script_init_reindex = """
# CONNECT '%s';
# commit;
# CREATE TABLE TABLE1(F_VCHAR VARCHAR(200));
# commit;
# EXECUTE PROCEDURE FTS$CREATE_INDEX('TEST_INDEX');
# commit;
# EXECUTE PROCEDURE FTS$ADD_FIELD_TO_INDEX('TEST_INDEX', 'TABLE1', 'F_VCHAR');
# commit;
# SET TERM ^;
# EXECUTE BLOCK
# AS
# DECLARE I INT = 0;
# BEGIN
#   WHILE (I < '%d') DO
#   BEGIN
#     INSERT INTO TABLE1(F_VCHAR) VALUES('%s');
#     I = I + 1;
#   END
# END^
# SET TERM ;^
# commit;
# EXECUTE PROCEDURE FTS$REINDEX('TEST_INDEX');
# commit;
# """
# 
# test_script_select_drop = """
# CONNECT '%s';
# commit;
# SELECT FTS$SCORE, FTS$RELATION, FTS$HIGHLIGHT from FTS$SEARCH('TEST_INDEX', NULL, '%s', 200);
# commit;
# EXECUTE PROCEDURE FTS$DROP_FIELD_FROM_INDEX('TEST_INDEX', 'TABLE1', 'F_VCHAR');
# commit;
# EXECUTE PROCEDURE FTS$DROP_INDEX('TEST_INDEX');
# commit;
# DELETE FROM TABLE1 WHERE F_VCHAR = '%s';
# commit;
# """
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script_init_reindex % (DBName1, 5, 'fts_test_string'))
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script_init_reindex % (DBName2, 10, 'RandomValuesForInput'))
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script_select_drop % (DBName1, 'fts_test_string', 'fts_test_string'))
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script_select_drop % (DBName2, 'RandomValuesForInput', 'RandomValuesForInput'))
# 
# if os.path.isfile(DBPath1):
#     os.remove(DBPath1);
# if os.path.isfile(DBPath2):
# os.remove(DBPath2);
# -----------------------------------

# version: 5.0

db_3 = db_factory()

act_3 = python_act('db_3', substitutions=[('SQL>.*', ''), ('CON>', '')])

expected_stdout_3 = """
FTS$SCORE FTS$RELATION                    FTS$HIGHLIGHT
======================= =============================== ================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
0.03955062106251717 TABLE1                          <B>fts_test_string</B>
0.03955062106251717 TABLE1                          <B>fts_test_string</B>
0.03955062106251717 TABLE1                          <B>fts_test_string</B>
0.03955062106251717 TABLE1                          <B>fts_test_string</B>
0.03955062106251717 TABLE1                          <B>fts_test_string</B>
FTS$SCORE FTS$RELATION                    FTS$HIGHLIGHT
======================= =============================== ================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
0.02114546112716198 TABLE1                          <B>RandomValuesForInput</B>
0.02114546112716198 TABLE1                          <B>RandomValuesForInput</B>
0.02114546112716198 TABLE1                          <B>RandomValuesForInput</B>
0.02114546112716198 TABLE1                          <B>RandomValuesForInput</B>
0.02114546112716198 TABLE1                          <B>RandomValuesForInput</B>
0.02114546112716198 TABLE1                          <B>RandomValuesForInput</B>
0.02114546112716198 TABLE1                          <B>RandomValuesForInput</B>
0.02114546112716198 TABLE1                          <B>RandomValuesForInput</B>
0.02114546112716198 TABLE1                          <B>RandomValuesForInput</B>
0.02114546112716198 TABLE1                          <B>RandomValuesForInput</B>
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
# import shutil
# import ntpath
# 
# fts_script_path = os.path.join(context['rdb_path'], 'misc', 'fts.sql')
# jvm_path = os.path.join(context['rdb_path'], 'jvm.args')
# 
# databases_conf_path = os.path.join(context['rdb_path'], 'databases.conf')
# bak_databases_conf_path = os.path.join(context['rdb_path'], 'databases.conf.bak')
# 
# if os.path.isfile(bak_databases_conf_path):
#     os.remove(bak_databases_conf_path)
# shutil.copy2(databases_conf_path, bak_databases_conf_path)
# 
# DBName1 = dsn[:-4]+"1.fdb"
# DBName2 = dsn[:-4]+"2.fdb"
# DBPath1 = db_filename[:-4]+"1.fdb"
# DBPath2 = db_filename[:-4]+"2.fdb"
# DBFile1 = ntpath.basename(DBPath1).upper()
# DBFile2 = ntpath.basename(DBPath2).upper()
# 
# fts_dir = context['temp_directory'] + "/fts_dir_smd"
# 
# f_dbconf = open(databases_conf_path, 'a')
# f_dbconf.seek(0, 2)
# f_dbconf.write("\\n\\n")
# f_dbconf.write(DBFile1 + " = " + DBPath1)
# f_dbconf.write("\\n{")
# f_dbconf.write("\\n    FTSDirectory = " + fts_dir + "1")
# f_dbconf.write("\\n}")
# f_dbconf.write("\\n\\n")
# f_dbconf.write(DBFile2 + " = " + DBPath2)
# f_dbconf.write("\\n{")
# f_dbconf.write("\\n    FTSDirectory = " + fts_dir + "2")
# f_dbconf.write("\\n}")
# f_dbconf.close()
# 
# runProgram('isql', ['-user', user_name, '-password', user_password, '-q'], "create database '%s';" %DBName1)
# runProgram('isql', ['-user', user_name, '-password', user_password, '-q'], "create database '%s';" %DBName2)
# runProgram('gfix', ['-user', user_name,'-password', user_password, '-g', DBPath2])
# 
# init_script = """
# connect '%s';
# create role fts;
# grant default fts to sysdba;
# commit;
# connect '%s';
# input '%s';
# commit;
# """
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], init_script % (DBName1, DBName1, fts_script_path))
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], init_script % (DBName2, DBName2, fts_script_path))
# 
# test_script_init = """
# CONNECT '%s';
# commit;
# CREATE TABLE TABLE1(F_VCHAR VARCHAR(200));
# commit;
# EXECUTE PROCEDURE FTS$CREATE_INDEX('TEST_INDEX');
# commit;
# EXECUTE PROCEDURE FTS$ADD_FIELD_TO_INDEX('TEST_INDEX', 'TABLE1', 'F_VCHAR');
# commit;
# SET TERM ^;
# EXECUTE BLOCK
# AS
# DECLARE I INT = 0;
# BEGIN
#   WHILE (I < '%d') DO
#   BEGIN
#     INSERT INTO TABLE1(F_VCHAR) VALUES('%s');
#     I = I + 1;
#   END
# END^
# SET TERM ;^
# commit;
# """
# 
# test_script_reindex = """
# CONNECT '%s';
# commit;
# EXECUTE PROCEDURE FTS$REINDEX('TEST_INDEX');
# commit;
# """
# 
# test_script_select_drop = """
# CONNECT '%s';
# commit;
# SELECT FTS$SCORE, FTS$RELATION, FTS$HIGHLIGHT from FTS$SEARCH('TEST_INDEX', NULL, '%s', 200);
# commit;
# EXECUTE PROCEDURE FTS$DROP_FIELD_FROM_INDEX('TEST_INDEX', 'TABLE1', 'F_VCHAR');
# commit;
# EXECUTE PROCEDURE FTS$DROP_INDEX('TEST_INDEX');
# commit;
# DELETE FROM TABLE1 WHERE F_VCHAR = '%s';
# commit;
# """
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script_init % (DBName1, 5, 'fts_test_string'))
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script_init % (DBName2, 10, 'RandomValuesForInput'))
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script_reindex % (DBName1))
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script_reindex % (DBName2))
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script_select_drop % (DBName1, 'fts_test_string', 'fts_test_string'))
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script_select_drop % (DBName2, 'RandomValuesForInput', 'RandomValuesForInput'))
# 
# #-- Clean up files ---------------------------------------------------------
# 
# os.unlink(databases_conf_path)
# os.rename(bak_databases_conf_path, databases_conf_path)
# 
# if os.path.isfile(DBPath1):
#     os.remove(DBPath1);
# if os.path.isfile(DBPath2):
# os.remove(DBPath2);
# -----------------------------------
