#coding:utf-8

"""
ID:          java.fbjava.permissions.role-on-role
TITLE:       Check permissions granted to role-on-role
DESCRIPTION: 
FBTEST:      functional.java.fbjava.permissions.role_on_role
"""

import pytest
from firebird.qa import *

# version: 3.0

init_script_1 = """
create function prop(key varchar(255)) returns varchar(255)
external name 'java.lang.System.getProperty(java.lang.String)'
engine java;
"""

db_1 = db_factory(init=init_script_1)

act_1 = python_act('db_1', substitutions=[('at java.*', '')])

expected_stdout_1 = """PROP
===============================================================================
PROP
===============================================================================
<null>
"""

expected_stderr_1 = """PROP
===============================================================================
PROP
===============================================================================
<null>
"""

@pytest.mark.skip('FIXME: Not IMPLEMENTED')
@pytest.mark.java
@pytest.mark.version('>=3.0,<4.0')
def test_1(act_1: Action):
    pytest.fail("Not IMPLEMENTED")

# Original python code for this test:
# -----------------------------------
# 
# test_script = '''connect '%s';
# select prop('myproperty') from rdb$database;
# ''' % dsn
# 
# security_fillup_script = '''connect 'localhost:java-security.fdb';
# delete from permission where permission_group = 1000;
# delete from permission_group_grant where permission_group=1000;
# delete from permission_group where id = 1000;
# insert into permission_group values(1000, 'mygroup');
# insert into permission_group_grant values(1000, '%', 'ROLE', 'FBJAVA1');
# insert into permission values(1000, 'java.util.PropertyPermission', 'myproperty', 'read');
# '''
# 
# security_cleanup_script = '''connect 'localhost:java-security.fdb';
# delete from permission where permission_group = 1000;
# delete from permission_group_grant where permission_group=1000;
# delete from permission_group where id = 1000;
# '''
# 
# grant_role_script = '''connect '%s';
# create role FBJAVA1;
# create role FBJAVA2;
# grant default FBJAVA1 to FBJAVA2;
# grant default FBJAVA2 to TESTUSER;
# ''' % dsn
# 
# create_user_script = '''
# CREATE USER TESTUSER PASSWORD 'test';
# GRANT EXECUTE ON FUNCTION PROP TO TESTUSER;
# '''
# 
# drop_user_script = '''
# DROP USER TESTUSER;
# '''
# 
# runProgram('isql', [dsn, '-user', user_name, '-password', user_password, '-q'], create_user_script)
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], security_cleanup_script)
# 
# runProgram('isql', ['-user', 'TESTUSER','-password', 'test', '-q'], test_script)
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], security_fillup_script)
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], grant_role_script)
# runProgram('isql', ['-user', 'TESTUSER','-password', 'test', '-q'], test_script)
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], security_cleanup_script)
# runProgram('isql', [dsn, '-user', user_name, '-password', user_password, '-q'], drop_user_script)
# -----------------------------------

# version: 4.0

init_script_2 = """
create function prop(key varchar(255)) returns varchar(255)
external name 'java.lang.System.getProperty(java.lang.String)'
engine java;
"""

db_2 = db_factory(init=init_script_2)

act_2 = python_act('db_2', substitutions=[('at java.*', '')])

expected_stdout_2 = """PROP
===============================================================================================================================================================================================================================================================
PROP
===============================================================================================================================================================================================================================================================
<null>
"""

expected_stderr_2 = """PROP
===============================================================================================================================================================================================================================================================
PROP
===============================================================================================================================================================================================================================================================
<null>
"""

@pytest.mark.skip('FIXME: Not IMPLEMENTED')
@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    pytest.fail("Not IMPLEMENTED")

# Original python code for this test:
# -----------------------------------
# 
# test_script = '''connect '%s';
# select prop('myproperty') from rdb$database;
# ''' % dsn
# 
# security_fillup_script = '''connect 'localhost:java-security.fdb';
# delete from permission where permission_group = 1000;
# delete from permission_group_grant where permission_group=1000;
# delete from permission_group where id = 1000;
# insert into permission_group values(1000, 'mygroup');
# insert into permission_group_grant values(1000, '%', 'ROLE', 'FBJAVA1');
# insert into permission values(1000, 'java.util.PropertyPermission', 'myproperty', 'read');
# '''
# 
# security_cleanup_script = '''connect 'localhost:java-security.fdb';
# delete from permission where permission_group = 1000;
# delete from permission_group_grant where permission_group=1000;
# delete from permission_group where id = 1000;
# '''
# 
# grant_role_script = '''connect '%s';
# create role FBJAVA1;
# create role FBJAVA2;
# grant default FBJAVA1 to FBJAVA2;
# grant default FBJAVA2 to TESTUSER;
# ''' % dsn
# 
# create_user_script = '''
# CREATE USER TESTUSER PASSWORD 'test';
# GRANT EXECUTE ON FUNCTION PROP TO TESTUSER;
# '''
# 
# drop_user_script = '''
# DROP USER TESTUSER;
# '''
# 
# runProgram('isql', [dsn, '-user', user_name, '-password', user_password, '-q'], create_user_script)
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], security_cleanup_script)
# 
# runProgram('isql', ['-user', 'TESTUSER','-password', 'test', '-q'], test_script)
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], security_fillup_script)
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], grant_role_script)
# runProgram('isql', ['-user', 'TESTUSER','-password', 'test', '-q'], test_script)
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], security_cleanup_script)
# runProgram('isql', [dsn, '-user', user_name, '-password', user_password, '-q'], drop_user_script)
# -----------------------------------
