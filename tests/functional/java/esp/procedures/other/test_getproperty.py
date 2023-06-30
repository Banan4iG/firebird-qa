#coding:utf-8

"""
ID:          java.esp.procedures.other.getproperty
TITLE:       Procedure gets system property
DESCRIPTION: 
FBTEST:      functional.java.esp.procedures.other.getproperty
"""

import pytest
from firebird.qa import *

init_script = """

CREATE PROCEDURE TEST(i varchar(100))
returns(o varchar(100))
EXTERNAL NAME 'esp.TestProcedure.getProperty(String, String[])' 
ENGINE JAVA;
commit;

connect 'localhost:java-security.fdb';
delete from permission where permission_group = 1000;
delete from permission_group_grant where permission_group=1000;
delete from permission_group where id = 1000;
insert into permission_group values(1000, 'mygroup');
insert into permission_group_grant values(1000, '%', 'USER', 'SYSDBA');
insert into permission values(1000, 'java.util.PropertyPermission', 'fg', 'read');
insert into permission values(1000, 'java.util.PropertyPermission', 'java.home', 'read');
commit;
"""

db = db_factory(init=init_script)

test_script = """
set list;
 
EXECUTE PROCEDURE TEST('fg');
EXECUTE PROCEDURE TEST('java.home');
commit;

connect 'localhost:java-security.fdb';
delete from permission where permission_group = 1000;
delete from permission_group_grant where permission_group=1000;
delete from permission_group where id = 1000;
commit;
"""

act = isql_act('db', test_script, substitutions=[('O.*', 'O data')])

expected_stdout = """
	
O data
O data
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
