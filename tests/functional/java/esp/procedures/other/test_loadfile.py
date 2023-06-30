#coding:utf-8

"""
ID:          java.esp.procedures.other.loadfile
TITLE:       Working with the file system
DESCRIPTION: 
  Reading a file and inserting its contents into a table in a blob type field
FBTEST:      functional.java.esp.procedures.other.loadfile
"""

import pytest
from firebird.qa import *

init_script = """
 
CREATE TABLE TEST_TABLE(F_BLOB BLOB);
commit;

CREATE PROCEDURE TEST(s varchar(200))
EXTERNAL NAME 'esp.TestProcedure.loadFile(String)' 
ENGINE JAVA;
commit; 


"""

db = db_factory(init=init_script)

act = python_act('db')

expected_stdout = """
F_BLOB
=================
80:0
==============================================================================
F_BLOB:
BLOB display set to subtype 1. This BLOB: subtype = 0
==============================================================================
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    file_dir = act.files_dir / 'for_test_loadfile.txt'
    setup_permissions = f"""
        delete from permission where permission_group = 1000;
        delete from permission_group_grant where permission_group=1000;
        delete from permission_group where id = 1000;
        insert into permission_group values(1000, 'mygroup');
        insert into permission_group_grant values(1000, '%', 'USER', 'SYSDBA');
        insert into permission values(1000, 'java.io.FilePermission', '{str(file_dir)}', 'read');
        commit;
    """
    act.isql(switches=['localhost:java-security.fdb', '-q'], input=setup_permissions, connect_db=False)

    script=f"""	
        execute procedure test('{str(file_dir)}');
        commit;
        select * from TEST_TABLE;
    """
    act.reset()
    act.expected_stdout = expected_stdout
    act.isql(switches=['-q'], input=script)
    assert act.clean_stdout == act.clean_expected_stdout

    revoke_permissions = """
        delete from permission where permission_group = 1000;
        delete from permission_group_grant where permission_group=1000;
        delete from permission_group where id = 1000;
        commit;
    """
    act.isql(switches=['localhost:java-security.fdb', '-q'], input=revoke_permissions, connect_db=False)

