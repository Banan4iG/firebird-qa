#coding:utf-8

"""
ID:          java.fbjava.permissions.change-role
TITLE:       After changing the role during the connection, the privileges remain the same
DESCRIPTION: 
FBTEST:      functional.java.fbjava.permissions.change_role
"""

import pytest
from firebird.qa import *

substitutions = [('(at\\s\\S+\\(\\S+:)([0-9]+)(\\))', ''), ('\\("java.util.PropertyPermission" "myproperty" "read"\\).*', '("java.util.PropertyPermission" "myproperty" "read")')]

init_script = """
create function prop(key varchar(255)) returns varchar(255)
external name 'java.lang.System.getProperty(java.lang.String)'
engine java;
"""

db = db_factory(init=init_script)

act = python_act('db', substitutions=substitutions)

expected_stdout = """
Connection without role. Error expected:
java.security.AccessControlException: access denied ("java.util.PropertyPermission" "myproperty" "read")
-At function 'PROP'
Connection with role FBJAVA1. Result (None) expected:
None
Changed role to FBJAVA2 but cached. Result (None) expected:
None
"""

test_user = user_factory('db', name='TESTUSER', password='test')
test_role1 = role_factory('db', name='FBJAVA1')
test_role2 = role_factory('db', name='FBJAVA2')

java_security_db = 'localhost:java-security.fdb'

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_2(act: Action, test_user: User, test_role1: Role, test_role2: Role, capsys):
    grant_script = '''
        grant FBJAVA1 to TESTUSER;
        grant FBJAVA2 to TESTUSER;
        GRANT EXECUTE ON FUNCTION PROP TO TESTUSER;
    '''
    act.isql(switches=['-q'], input=grant_script)

    security_fillup_script = '''
        delete from permission where permission_group = 1000;
        delete from permission_group_grant where permission_group=1000;
        delete from permission_group where id = 1000;
        insert into permission_group values(1000, 'mygroup');
        insert into permission_group_grant values(1000, '%', 'ROLE', 'FBJAVA1');
        insert into permission values(1000, 'java.util.PropertyPermission', 'myproperty', 'read');
    '''
    act.isql(switches=[java_security_db, '-q'], input=security_fillup_script, connect_db=False)

    with act.db.connect(user=test_user.name, password=test_user.password) as con:
        with con.cursor() as cur:
            cur.execute("select prop('myproperty') from rdb$database;")
            print("Connection without role. Error expected:")
            try:
                for row in cur.fetchall():
                    print(row[0])
            except Exception as e:
                print(e)

    with act.db.connect(user=test_user.name, password=test_user.password, role=test_role1.name) as con:
        with con.cursor() as cur:
            cur.execute("select prop('myproperty') from rdb$database;")
            print("Connection with role FBJAVA1. Result (None) expected:")
            try:
                for row in cur.fetchall():
                    print(row[0])
            except Exception as e:
                print(e)
            
            cur.execute("SET ROLE FBJAVA2;")
            cur.execute("select prop('myproperty') from rdb$database;")
            print("Changed role to FBJAVA2 but cached. Result (None) expected:")
            try:
                for row in cur.fetchall():
                    print(row[0])
            except Exception as e:
                print(e)
 
    security_cleanup_script = '''
        delete from permission where permission_group = 1000;
        delete from permission_group_grant where permission_group=1000;
        delete from permission_group where id = 1000;
    '''
    act.isql(switches=[java_security_db, '-q'], input=security_cleanup_script, connect_db=False)

    act.expected_stdout = expected_stdout
    act.stdout = capsys.readouterr().out
    assert act.clean_stdout == act.clean_expected_stdout
