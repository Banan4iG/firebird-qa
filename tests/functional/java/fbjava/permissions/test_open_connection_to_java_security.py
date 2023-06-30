#coding:utf-8

"""
ID:          java.fbjava.permissions.open-connection-to-java-security
TITLE:       Permissions granting when open connecting to java-security.fdb
DESCRIPTION: 
FBTEST:      functional.java.fbjava.permissions.open_connection_to_java_security
"""

import pytest
from firebird.qa import *

init_script = """
create role FBJAVA1;
grant default FBJAVA1 to TESTUSER;

create function prop(key varchar(255)) returns varchar(255)
external name 'java.lang.System.getProperty(java.lang.String)'
engine java;
"""

substitutions=[('SQL>.*', ''), ('CON>', ''), ('at java.*', ''), ('======*', '============')]

db = db_factory(init=init_script)
act = python_act('db', substitutions=substitutions)

java_sec_db = db_factory(filename = '#java-security.fdb', do_not_create = True, do_not_drop = True)
act_sec = python_act('java_sec_db', substitutions=substitutions)

test_user = user_factory('db', name='TESTUSER', password='test')
tmp_role = role_factory('db', name='FBJAVA1')

expected_stdout = """
PROP
====================================
<null>

PROP
====================================

Statement failed, SQLSTATE = HY000
java.security.AccessControlException: access denied ("java.util.PropertyPermission" "myproperty" "read")
at java.security.AccessControlContext.checkPermission(replaced)
at java.security.AccessController.checkPermission(replaced)
at java.lang.SecurityManager.checkPermission(replaced)
at java.lang.SecurityManager.checkPropertyAccess(replaced)
at java.lang.System.getProperty(replaced)
-At function 'PROP'
"""

expected_stderr = """
PROP
===============================================================================================================================================================================================================================================================
<null>
PROP
===============================================================================================================================================================================================================================================================
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action, act_sec: Action, test_user: User, tmp_role: Role, capsys):
    grant_script = '''
        grant default FBJAVA1 to TESTUSER; 
        GRANT EXECUTE ON FUNCTION PROP TO TESTUSER;
    '''
    act.isql(switches=['-q'], input=grant_script)

    security_fillup_list = [
        "insert into permission_group values(1000, 'mygroup')",
        "insert into permission_group_grant values(1000, '%', 'ROLE', 'FBJAVA1')",
        "insert into permission values(1000, 'java.util.PropertyPermission', 'myproperty', 'read')"]

    security_cleanup_list = [
        "delete from permission where permission_group = 1000",
        "delete from permission_group_grant where permission_group=1000",
        "delete from permission_group where id = 1000"]

    with act_sec.db.connect() as con:
        with con.cursor() as cur:
            for cmd in security_cleanup_list:
                cur.execute(cmd)
            for cmd in security_fillup_list:
                cur.execute(cmd)
            con.commit()

            act.reset()
            act.isql(switches=['-u', test_user.name, '-p', test_user.password, '-q'], combine_output=True, credentials=False, input="select prop('myproperty') from rdb$database;")
            print(act.stdout)

            for cmd in security_cleanup_list:
                cur.execute(cmd)
            con.commit()
            
            act.reset()
            act.isql(switches=['-u', test_user.name, '-p', test_user.password, '-q'], combine_output=True, credentials=False, input="select prop('myproperty') from rdb$database;")
            print(act.stdout)
    
    act.expected_stdout = expected_stdout
    act.stdout = capsys.readouterr().out
    assert act.clean_stdout == act.clean_expected_stdout
