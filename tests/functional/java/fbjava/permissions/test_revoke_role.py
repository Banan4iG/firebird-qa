#coding:utf-8

"""
ID:          java.fbjava.permissions.revoke-role
TITLE:       Privilege cancellation after role revoking
DESCRIPTION: 
FBTEST:      functional.java.fbjava.permissions.revoke_role
"""

import pytest
from firebird.qa import *

# version: 3.0

substitutions_1 = [('(at\\s\\S+\\(\\S+:)([0-9]+)(\\))', ''), ('\\("java.util.PropertyPermission" "myproperty" "read"\\).*', '("java.util.PropertyPermission" "myproperty" "read")')]

db_1 = db_factory()

act_1 = python_act('db_1', substitutions=substitutions_1)

expected_stdout_1 = """
Permissions granted. Result (None) expected:
None
Role revoked but cached. Result (None) expected:
None
Role revoked. Error expected:
('Cursor.fetchone:\\n- SQLCODE: -901\\n- java.security.AccessControlException: access denied ("java.util.PropertyPermission" "myproperty" "read")
"""

@pytest.mark.skip('FIXME: Not IMPLEMENTED')
@pytest.mark.java
@pytest.mark.version('>=3.0,<4.0')
def test_1(act_1: Action):
    pytest.fail("Not IMPLEMENTED")

# Original python code for this test:
# -----------------------------------
# 
# import fdb
# 
# create_user_script = '''
# CREATE USER TESTUSER PASSWORD 'test';
# create role FBJAVA1;
# grant default FBJAVA1 to TESTUSER;
# 
# create function prop(key varchar(255)) returns varchar(255)
# external name 'java.lang.System.getProperty(java.lang.String)'
# engine java;
# 
# GRANT EXECUTE ON FUNCTION PROP TO TESTUSER;
# '''
# 
# drop_user_script = '''
# DROP USER TESTUSER;
# '''
# 
# java_security_db = 'localhost:java-security.fdb'
# 
# security_fillup_script = '''
# delete from permission where permission_group = 1000;
# delete from permission_group_grant where permission_group=1000;
# delete from permission_group where id = 1000;
# insert into permission_group values(1000, 'mygroup');
# insert into permission_group_grant values(1000, '%', 'ROLE', 'FBJAVA1');
# insert into permission values(1000, 'java.util.PropertyPermission', 'myproperty', 'read');
# '''
# 
# security_cleanup_script = '''
# delete from permission where permission_group = 1000;
# delete from permission_group_grant where permission_group=1000;
# delete from permission_group where id = 1000;
# '''
# 
# runProgram('isql', [dsn, '-user', user_name, '-password', user_password, '-q'], create_user_script)
# 
# runProgram('isql', [java_security_db, '-user', user_name,'-password', user_password, '-q'], security_fillup_script)
# 
# con = fdb.connect(dsn, user='TESTUSER', password='test')
# cur = con.cursor()
# cur.execute("select prop('myproperty') from rdb$database;")
# print("Permissions granted. Result (None) expected:")
# try:
# 	for row in cur.fetchall():
# 		print(row[0])
# except Exception as e:
# 	print(e)	
# 
# cons = fdb.connect(dsn, user=user_name, password=user_password)
# curs = cons.cursor()
# curs.execute("revoke FBJAVA1 from TESTUSER")
# 
# print("Role revoked but cached. Result (None) expected:")
# cur.execute("select prop('myproperty') from rdb$database;")
# try:
# 	for row in cur.fetchall():
# 		print(row[0])
# except Exception as e:
# 	print(e)
# 	
# con = fdb.connect(dsn, user='TESTUSER', password='test')
# cur = con.cursor()
# cur.execute("select prop('myproperty') from rdb$database;")
# print("Role revoked. Error expected:")
# try:
# 	for row in cur.fetchall():
# 		print(row[0])
# except Exception as e:
# 	print(e)	
# 
# runProgram('isql', [java_security_db, '-user', user_name,'-password', user_password, '-q'], security_cleanup_script)
# 
# runProgram('isql', [dsn, '-user', user_name, '-password', user_password, '-q'], drop_user_script)
# 
# -----------------------------------

# version: 4.0

substitutions_2 = [('(at\\s\\S+\\(\\S+:)([0-9]+)(\\))', ''), ('\\("java.util.PropertyPermission" "myproperty" "read"\\).*', '("java.util.PropertyPermission" "myproperty" "read")')]

db_2 = db_factory()

act_2 = python_act('db_2', substitutions=substitutions_2)

expected_stdout_2 = """
Permissions granted. Result (None) expected:
None
Role revoked but cached. Result (None) expected:
None
Role revoked. Error expected:
('Cursor.fetchone:\\n- SQLCODE: -901\\n- java.security.AccessControlException: access denied ("java.util.PropertyPermission" "myproperty" "read")
"""

@pytest.mark.skip('FIXME: Not IMPLEMENTED')
@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    pytest.fail("Not IMPLEMENTED")

# Original python code for this test:
# -----------------------------------
# 
# import fdb
# 
# create_user_script = '''
# CREATE USER TESTUSER PASSWORD 'test';
# create role FBJAVA1;
# grant default FBJAVA1 to TESTUSER;
# 
# create function prop(key varchar(255)) returns varchar(255)
# external name 'java.lang.System.getProperty(java.lang.String)'
# engine java;
# 
# GRANT EXECUTE ON FUNCTION PROP TO TESTUSER;
# '''
# 
# drop_user_script = '''
# DROP USER TESTUSER;
# '''
# 
# java_security_db = 'localhost:java-security.fdb'
# 
# security_fillup_script = '''
# delete from permission where permission_group = 1000;
# delete from permission_group_grant where permission_group=1000;
# delete from permission_group where id = 1000;
# insert into permission_group values(1000, 'mygroup');
# insert into permission_group_grant values(1000, '%', 'ROLE', 'FBJAVA1');
# insert into permission values(1000, 'java.util.PropertyPermission', 'myproperty', 'read');
# '''
# 
# security_cleanup_script = '''
# delete from permission where permission_group = 1000;
# delete from permission_group_grant where permission_group=1000;
# delete from permission_group where id = 1000;
# '''
# 
# runProgram('isql', [dsn, '-user', user_name, '-password', user_password, '-q'], create_user_script)
# 
# runProgram('isql', [java_security_db, '-user', user_name,'-password', user_password, '-q'], security_fillup_script)
# 
# con = fdb.connect(dsn, user='TESTUSER', password='test')
# cur = con.cursor()
# cur.execute("select prop('myproperty') from rdb$database;")
# print("Permissions granted. Result (None) expected:")
# try:
# 	for row in cur.fetchall():
# 		print(row[0])
# except Exception as e:
# 	print(e)
# 
# cons = fdb.connect(dsn, user=user_name, password=user_password)
# curs = cons.cursor()
# curs.execute("revoke FBJAVA1 from TESTUSER")
# 
# print("Role revoked but cached. Result (None) expected:")
# cur.execute("select prop('myproperty') from rdb$database;")
# try:
# 	for row in cur.fetchall():
# 		print(row[0])
# except Exception as e:
# 	print(e)
# 
# con = fdb.connect(dsn, user='TESTUSER', password='test')
# cur = con.cursor()
# cur.execute("select prop('myproperty') from rdb$database;")
# print("Role revoked. Error expected:")
# try:
# 	for row in cur.fetchall():
# 		print(row[0])
# except Exception as e:
# 	print(e)
# 
# runProgram('isql', [java_security_db, '-user', user_name,'-password', user_password, '-q'], security_cleanup_script)
# 
# runProgram('isql', [dsn, '-user', user_name, '-password', user_password, '-q'], drop_user_script)
# 
# -----------------------------------
