#coding:utf-8

"""
ID:          java.fbjava.permissions.predefined-values
TITLE:       Testing of predefined values in the ARG1 field in PERMISSION table
DESCRIPTION: 
FBTEST:      functional.java.fbjava.permissions.predefined_values
"""

import pytest
from firebird.qa import *

# version: 3.0

init_script_1 = """ 
CREATE PROCEDURE TEST(s varchar(200))
EXTERNAL NAME 'esp.TestProcedure.readFile(String)' 
ENGINE JAVA;
commit; 
"""

db_1 = db_factory(init=init_script_1)

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
# file_dir = os.path.join('doc', 'README.Optimizer.txt')
# full_path_file = os.path.join(context['rdb_path'], file_dir) 
# 
# separator = ""
# if os.name == 'posix':
# 	separator = "/"
# elif os.name == 'nt':
# 	separator = "\\\\"
# else:
# 	raise Exception('Unsupported os %s' % os.name)
#  
# create_user_script = """
# CREATE USER TESTUSER PASSWORD 'test';
# GRANT EXECUTE ON PROCEDURE TEST TO TESTUSER;
# """
# 
# drop_user_script = """
# DROP USER TESTUSER;
# """
# 
# setup_permissions = """
# delete from permission_group_grant where permission_group=1000;
# delete from permission_group where id = 1000;
# commit;
# insert into permission_group values(1000, 'mygroup');
# insert into permission_group_grant values(1000, '%%', 'USER', 'TESTUSER');
# commit;
# """
# 
# revoke_permissions = """
# delete from permission where permission_group = 1000;
# delete from permission_group_grant where permission_group=1000;
# delete from permission_group where id = 1000;
# commit;
# """
# 
# def access_check (full_path_file,predefined_value):
# 	script="""	
# 		execute procedure test('%s');
# 		commit;
# 	""" %(full_path_file)
# 	insert_delete_permissions = """
# 		delete from permission where permission_group = 1000;
# 		commit;
# 		insert into permission values(1000, 'java.io.FilePermission', '%s', 'read'); 
# 		commit;
# 	""" %(predefined_value)
# 	runProgram('isql', ['localhost:java-security.fdb', '-user', user_name, '-password', user_password, '-q'], insert_delete_permissions)
# 	runProgram('isql', [dsn,'-user', 'TESTUSER', '-password', 'test', '-q'], script)
# 
# runProgram('isql', [dsn, '-user', user_name, '-password', user_password, '-q'], create_user_script)
# 
# runProgram('isql', ['localhost:java-security.fdb', '-user', user_name, '-password', user_password, '-q'], setup_permissions)
# access_check (full_path_file,'$(install)'+separator+file_dir)
# access_check (full_path_file,'$(root)'+separator+file_dir)
# access_check (full_path_file,'$(jar)'+separator+'..'+separator+file_dir)
# runProgram('isql', ['localhost:java-security.fdb', '-user', user_name, '-password', user_password, '-q'], revoke_permissions)
# 
# runProgram('isql', [dsn, '-user', user_name, '-password', user_password, '-q'], drop_user_script)
# -----------------------------------

# version: 4.0

init_script_2 = """
CREATE PROCEDURE TEST(s varchar(200))
EXTERNAL NAME 'esp.TestProcedure.readFile(String)'
ENGINE JAVA;
commit;
"""

db_2 = db_factory(init=init_script_2)

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
# file_dir = os.path.join('doc', 'README.Optimizer.txt')
# full_path_file = os.path.join(context['rdb_path'], file_dir)
# 
# separator = ""
# if os.name == 'posix':
# 	separator = "/"
# elif os.name == 'nt':
# 	separator = "\\\\"
# else:
# 	raise Exception('Unsupported os %s' % os.name)
# 
# create_user_script = """
# CREATE USER TESTUSER PASSWORD 'test';
# GRANT EXECUTE ON PROCEDURE TEST TO TESTUSER;
# """
# 
# drop_user_script = """
# DROP USER TESTUSER;
# """
# 
# setup_permissions = """
# delete from permission_group_grant where permission_group=1000;
# delete from permission_group where id = 1000;
# commit;
# insert into permission_group values(1000, 'mygroup');
# insert into permission_group_grant values(1000, '%%', 'USER', 'TESTUSER');
# commit;
# """
# 
# revoke_permissions = """
# delete from permission where permission_group = 1000;
# delete from permission_group_grant where permission_group=1000;
# delete from permission_group where id = 1000;
# commit;
# """
# 
# def access_check (full_path_file,predefined_value):
# 	script="""
# 		execute procedure test('%s');
# 		commit;
# 	""" %(full_path_file)
# 	insert_delete_permissions = """
# 		delete from permission where permission_group = 1000;
# 		commit;
# 		insert into permission values(1000, 'java.io.FilePermission', '%s', 'read');
# 		commit;
# 	""" %(predefined_value)
# 	runProgram('isql', ['localhost:java-security.fdb', '-user', user_name, '-password', user_password, '-q'], insert_delete_permissions)
# 	runProgram('isql', [dsn,'-user', 'TESTUSER', '-password', 'test', '-q'], script)
# 
# runProgram('isql', [dsn, '-user', user_name, '-password', user_password, '-q'], create_user_script)
# 
# runProgram('isql', ['localhost:java-security.fdb', '-user', user_name, '-password', user_password, '-q'], setup_permissions)
# access_check (full_path_file,'$(install)'+separator+file_dir)
# access_check (full_path_file,'$(root)'+separator+file_dir)
# access_check (full_path_file,'$(jar)'+separator+'..'+separator+file_dir)
# runProgram('isql', ['localhost:java-security.fdb', '-user', user_name, '-password', user_password, '-q'], revoke_permissions)
# 
# runProgram('isql', [dsn, '-user', user_name, '-password', user_password, '-q'], drop_user_script)
# -----------------------------------
