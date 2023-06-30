#coding:utf-8

"""
ID:          java.fbjava.permissions.caching
TITLE:       Check if permissions cached for attachment
DESCRIPTION: 
FBTEST:      functional.java.fbjava.permissions.caching
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

expected_stdout = """No permissions granted. Error expected:
java.security.AccessControlException: access denied ("java.util.PropertyPermission" "myproperty" "read")
-At function 'PROP'
Permissions granted but cached. Error expected:
java.security.AccessControlException: access denied ("java.util.PropertyPermission" "myproperty" "read")
-At function 'PROP'
Permissions granted. Result (None) expected:
None
Permissions revoked but cached. Result (None) expected:
None
"""

test_script = "select prop('myproperty') from rdb$database;"

test_user = user_factory('db', name='TESTUSER', password='test')
tmp_role = role_factory('db', name='FBJAVA1')

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action, test_user: User, tmp_role: Role, capsys):
    grant_script = '''
        grant default FBJAVA1 to TESTUSER; 
        GRANT EXECUTE ON FUNCTION PROP TO TESTUSER;
    '''
    act.isql(switches=['-q'], input=grant_script)

    with act.db.connect(user=test_user.name, password=test_user.password) as con:
        with con.cursor() as cur:
            cur.execute(test_script)
            print("No permissions granted. Error expected:")
            try:
                cur.fetchall()
            except Exception as e:
                print(e)
            
            security_fillup_script = '''
                connect 'localhost:java-security.fdb';
                delete from permission where permission_group = 1000;
                delete from permission_group_grant where permission_group=1000;
                delete from permission_group where id = 1000;
                insert into permission_group values(1000, 'mygroup');
                insert into permission_group_grant values(1000, '%', 'ROLE', 'FBJAVA1');
                insert into permission values(1000, 'java.util.PropertyPermission', 'myproperty', 'read');
            '''
            act.isql(switches=['-q'], input=security_fillup_script, connect_db=False)

            print("Permissions granted but cached. Error expected:")
            cur.execute(test_script)
            try:
                cur.fetchall()
            except Exception as e:
                print(e)

    with act.db.connect() as con:
        with con.cursor() as cur:
            cur.execute(test_script)
            print("Permissions granted. Result (None) expected:")
            try:
                for row in cur.fetchall():
                    print(row[0])
            except Exception as e:
                print(e)		
            
            security_cleanup_script = '''
                connect 'localhost:java-security.fdb';
                delete from permission where permission_group = 1000;
                delete from permission_group_grant where permission_group=1000;
                delete from permission_group where id = 1000;
            '''
            act.isql(switches=['-q'], input=security_cleanup_script, connect_db=False)

            drop_user_script = 'DROP USER TESTUSER;'
            act.isql(switches=['-q'], input=drop_user_script)

            print("Permissions revoked but cached. Result (None) expected:")
            cur.execute(test_script)
            try:
                for row in cur.fetchall():
                    print(row[0])
            except Exception as e:
                print(e)

    act.expected_stdout = expected_stdout
    act.stdout = capsys.readouterr().out
    assert act.clean_stdout == act.clean_expected_stdout

    

    

