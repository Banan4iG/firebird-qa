#coding:utf-8

"""
ID:          java.fts.bugs.bug-61208
TITLE:       Reindexing must be executed if old version of index is used
DESCRIPTION: 
FBTEST:      functional.java.fts.bugs.bug_61208
"""

import pytest
from firebird.qa import *

# version: 3.0

db_1 = db_factory()

act_1 = python_act('db_1', substitutions=[('SQL>.*', ''), ('CON>', '')])

expected_stdout_1 = """
FTS$SCORE FTS$RELATION                    FTS$HIGHLIGHT
======================= =============================== ===============================================================================
0.04789113998413086 TABLE1                          <B>fts_test_string</B>
0.04789113998413086 TABLE1                          <B>fts_test_string</B>
0.04789113998413086 TABLE1                          <B>fts_test_string</B>
0.04789113998413086 TABLE1                          <B>fts_test_string</B>
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
# import shutil
# import ntpath
# import threading
# import time
# 
# fts_script_path = os.path.join(context['rdb_path'], 'misc', 'fts.sql')
# fbjava_yaml_path = os.path.join(context['rdb_path'], 'fbjava.yaml')
# 
# bak_fbjava_yaml = os.path.join(context['rdb_path'], 'fbjava.yaml.bak')
# 
# if os.path.isfile(bak_fbjava_yaml):
#     os.remove(bak_fbjava_yaml)
# 
# shutil.copy(fbjava_yaml_path, bak_fbjava_yaml)
# 
# DBName = dsn
# DBPath = db_filename
# DBFile = DBPath
# 
# global fts_dir
# fts_dir = context['temp_directory'] + "/fts_dir"
# if os.name == 'nt': # Windows
#     DBFile = "\\".*" + ntpath.basename(DBPath).upper() + "\\""
#     fts_dir = "C:/Windows/TEMP/fts_dir/"
# 
# f_dbconf = open(fbjava_yaml_path, 'a')
# f_dbconf.seek(0, 2)
# f_dbconf.write("\\n\\n")
# f_dbconf.write("databases:")
# f_dbconf.write("\\n  " + DBFile + ":")
# f_dbconf.write("\\n    options:")
# f_dbconf.write("\\n      ftsDirectory:")
# f_dbconf.write("\\n        - " + fts_dir)
# f_dbconf.close()
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
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], init_script % (DBName, DBName, fts_script_path))
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
# """
# 
# test_script_reindex = """
# CONNECT '%s';
# commit;
# EXECUTE PROCEDURE FTS$REINDEX('TEST_INDEX');
# commit;
# """
# 
# test_script_insert = """
# CONNECT '%s';
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
# test_script_select = """
# CONNECT '%s';
# commit;
# SELECT FIRST 10 FTS$SCORE, FTS$RELATION, FTS$HIGHLIGHT from FTS$SEARCH('TEST_INDEX', NULL, '%s', 200);
# commit;
# """
# 
# test_script_drop = """
# CONNECT '%s';
# commit;
# EXECUTE PROCEDURE FTS$DROP_FIELD_FROM_INDEX('TEST_INDEX', 'TABLE1', 'F_VCHAR');
# commit;
# EXECUTE PROCEDURE FTS$DROP_INDEX('TEST_INDEX');
# commit;
# DELETE FROM TABLE1 WHERE F_VCHAR = '%s';
# commit;
# """
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script_init % DBName)
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script_insert % (DBName, 2, 'fts_test_string'))
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script_reindex % DBName)
# 
# time.sleep(3)
# file_filter = ['segment']
# global fn
# file_names = [fn for fn in os.listdir(fts_dir + "/TEST_INDEX/")
#                 if any(fn.startswith(prefix) for prefix in file_filter)]
# f = open(fts_dir + "/TEST_INDEX/" + file_names[0], 'r')
# 
# cur = db_conn.cursor()
# cur.execute("INSERT INTO TABLE1(F_VCHAR) VALUES('fts_test_string')")
# db_conn.commit()
# cur.close()
# 
# try:
#     cur2 = db_conn.cursor()
#     cur2.execute("SELECT FIRST 10 FTS$SCORE, FTS$RELATION, FTS$HIGHLIGHT from FTS$SEARCH('TEST_INDEX', NULL, 'fts_test_string', 200)")
#     cur2.fetchone()
#     db_conn.commit()
#     cur2.close()
# except Exception as e:
#     print(e)
# db_conn.commit()
# 
# cur = db_conn.cursor()
# cur.execute("INSERT INTO TABLE1(F_VCHAR) VALUES('fts_test_string')")
# db_conn.commit()
# cur.close()
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script_select % (DBName, 'fts_test_string'))
# 
# db_conn.close()
# 
# f.close()
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script_drop % (DBName, 'fts_test_string'))
# -----------------------------------

# version: 4.0

db_2 = db_factory()

act_2 = python_act('db_2', substitutions=[('SQL>.*', ''), ('CON>', '')])

expected_stdout_2 = """
FTS$SCORE FTS$RELATION                    FTS$HIGHLIGHT
======================= =============================== ================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
0.1053605154156685 TABLE1                          <B>fts_test_string</B>
0.1053605154156685 TABLE1                          <B>fts_test_string</B>
0.1053605154156685 TABLE1                          <B>fts_test_string</B>
0.1053605154156685 TABLE1                          <B>fts_test_string</B>
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
# import shutil
# import ntpath
# import threading
# import time
# 
# fts_script_path = os.path.join(context['rdb_path'], 'misc', 'fts.sql')
# databases_conf_path = os.path.join(context['rdb_path'], 'databases.conf')
# bak_databases_conf = os.path.join(context['rdb_path'], 'databases.conf.bak')
# 
# if os.path.isfile(bak_databases_conf):
#     os.remove(bak_databases_conf)
# 
# shutil.copy(databases_conf_path, bak_databases_conf)
# 
# DBName = dsn
# DBPath = db_filename
# DBFile = DBPath
# 
# global fts_dir
# fts_dir = context['temp_directory'] + "/fts_dir"
# if os.name == 'nt': # Windows
#     DBFile = "" + ntpath.basename(DBPath).upper() + ""
#     fts_dir = "C:/Windows/TEMP/fts_dir/"
# 
# f_dbconf = open(databases_conf_path, 'a')
# f_dbconf.seek(0, 2)
# f_dbconf.write("\\n\\n")
# f_dbconf.write(DBFile + " = " + DBPath)
# f_dbconf.write("\\n{")
# f_dbconf.write("\\n    FTSDirectory = " + fts_dir)
# f_dbconf.write("\\n}")
# f_dbconf.close()
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
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], init_script % (DBName, DBName, fts_script_path))
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
# """
# 
# test_script_reindex = """
# CONNECT '%s';
# commit;
# EXECUTE PROCEDURE FTS$REINDEX('TEST_INDEX');
# commit;
# """
# 
# test_script_insert = """
# CONNECT '%s';
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
# test_script_select = """
# CONNECT '%s';
# commit;
# SELECT FIRST 10 FTS$SCORE, FTS$RELATION, FTS$HIGHLIGHT from FTS$SEARCH('TEST_INDEX', NULL, '%s', 200);
# commit;
# """
# 
# test_script_drop = """
# CONNECT '%s';
# commit;
# EXECUTE PROCEDURE FTS$DROP_FIELD_FROM_INDEX('TEST_INDEX', 'TABLE1', 'F_VCHAR');
# commit;
# EXECUTE PROCEDURE FTS$DROP_INDEX('TEST_INDEX');
# commit;
# DELETE FROM TABLE1 WHERE F_VCHAR = '%s';
# commit;
# """
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script_init % DBName)
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script_insert % (DBName, 2, 'fts_test_string'))
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script_reindex % DBName)
# 
# time.sleep(3)
# file_filter = ['segment']
# global fn
# file_names = [fn for fn in os.listdir(fts_dir + "/TEST_INDEX/")
#                 if any(fn.startswith(prefix) for prefix in file_filter)]
# f = open(fts_dir + "/TEST_INDEX/" + file_names[0], 'r')
# 
# 
# cur = db_conn.cursor()
# cur.execute("INSERT INTO TABLE1(F_VCHAR) VALUES('fts_test_string')")
# db_conn.commit()
# cur.close()
# 
# try:
#     cur2 = db_conn.cursor()
#     cur2.execute("SELECT FIRST 10 FTS$SCORE, FTS$RELATION, FTS$HIGHLIGHT from FTS$SEARCH('TEST_INDEX', NULL, 'fts_test_string', 200)")
#     cur2.fetchone()
#     db_conn.commit()
#     cur2.close()
# except Exception as e:
#     print(e)
# db_conn.commit()
# 
# cur = db_conn.cursor()
# cur.execute("INSERT INTO TABLE1(F_VCHAR) VALUES('fts_test_string')")
# db_conn.commit()
# cur.close()
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script_select % (DBName, 'fts_test_string'))
# 
# db_conn.close()
# 
# f.close()
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script_drop % (DBName, 'fts_test_string'))
# -----------------------------------

# version: 5.0

db_3 = db_factory()

act_3 = python_act('db_3', substitutions=[('SQL>.*', ''), ('CON>', '')])

expected_stdout_3 = """
FTS$SCORE FTS$RELATION                    FTS$HIGHLIGHT
======================= =============================== ================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
0.04789113998413086 TABLE1                          <B>fts_test_string</B>
0.04789113998413086 TABLE1                          <B>fts_test_string</B>
0.04789113998413086 TABLE1                          <B>fts_test_string</B>
0.04789113998413086 TABLE1                          <B>fts_test_string</B>
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
# import threading
# import time
# 
# fts_script_path = os.path.join(context['rdb_path'], 'misc', 'fts.sql')
# databases_conf_path = os.path.join(context['rdb_path'], 'databases.conf')
# bak_databases_conf_path = os.path.join(context['rdb_path'], 'databases.conf.bak')
# 
# if os.path.isfile(bak_databases_conf_path):
#     os.remove(bak_databases_conf_path)
# 
# shutil.copy2(databases_conf_path, bak_databases_conf_path)
# 
# DBName = dsn
# DBPath = db_filename
# DBFile = ntpath.basename(DBPath).upper()
# 
# fts_dir = context['temp_directory'] + "/fts_dir_61208"
# 
# f_dbconf = open(databases_conf_path, 'a')
# f_dbconf.seek(0, 2)
# f_dbconf.write("\\n\\n")
# f_dbconf.write(DBFile + " = " + DBPath)
# f_dbconf.write("\\n{")
# f_dbconf.write("\\n    FTSDirectory = " + fts_dir)
# f_dbconf.write("\\n}")
# f_dbconf.close()
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
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], init_script % (DBName, DBName, fts_script_path))
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
# """
# 
# test_script_reindex = """
# CONNECT '%s';
# commit;
# EXECUTE PROCEDURE FTS$REINDEX('TEST_INDEX');
# commit;
# """
# 
# test_script_insert = """
# CONNECT '%s';
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
# test_script_select = """
# CONNECT '%s';
# commit;
# SELECT FIRST 10 FTS$SCORE, FTS$RELATION, FTS$HIGHLIGHT from FTS$SEARCH('TEST_INDEX', NULL, '%s', 200);
# commit;
# """
# 
# test_script_drop = """
# CONNECT '%s';
# commit;
# EXECUTE PROCEDURE FTS$DROP_FIELD_FROM_INDEX('TEST_INDEX', 'TABLE1', 'F_VCHAR');
# commit;
# EXECUTE PROCEDURE FTS$DROP_INDEX('TEST_INDEX');
# commit;
# DELETE FROM TABLE1 WHERE F_VCHAR = '%s';
# commit;
# """
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script_init % DBName)
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script_insert % (DBName, 2, 'fts_test_string'))
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script_reindex % DBName)
# 
# time.sleep(3)
# file_filter = ['segment']
# global fn
# file_names = [fn for fn in os.listdir(fts_dir + "/TEST_INDEX/")
#                 if any(fn.startswith(prefix) for prefix in file_filter)]
# f = open(fts_dir + "/TEST_INDEX/" + file_names[0], 'r')
# 
# 
# cur = db_conn.cursor()
# cur.execute("INSERT INTO TABLE1(F_VCHAR) VALUES('fts_test_string')")
# db_conn.commit()
# cur.close()
# 
# try:
#     cur2 = db_conn.cursor()
#     cur2.execute("SELECT FIRST 10 FTS$SCORE, FTS$RELATION, FTS$HIGHLIGHT from FTS$SEARCH('TEST_INDEX', NULL, 'fts_test_string', 200)")
#     cur2.fetchone()
#     db_conn.commit()
#     cur2.close()
# except Exception as e:
#     print(e)
# db_conn.commit()
# 
# cur = db_conn.cursor()
# cur.execute("INSERT INTO TABLE1(F_VCHAR) VALUES('fts_test_string')")
# db_conn.commit()
# cur.close()
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script_select % (DBName, 'fts_test_string'))
# 
# db_conn.close()
# 
# f.close()
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script_drop % (DBName, 'fts_test_string'))
# 
# #-- Clean up files ---------------------------------------------------------
# 
# os.unlink(databases_conf_path)
# os.rename(bak_databases_conf_path, databases_conf_path)
# -----------------------------------
