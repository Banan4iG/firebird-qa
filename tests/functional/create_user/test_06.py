#coding:utf-8

"""
ID:          create_user.test_06
TITLE:       CREATE USER with bad user name
DESCRIPTION: Check for CREATE USER sql operator with not avalible symbols in user name.
FBTEST:      functional.create_user.create_user_06
"""

import pytest
from firebird.qa import *
from pathlib import Path

db = db_factory()

expected_stderr = """
Statement failed, SQLSTATE = 42000
Dynamic SQL Error
-SQL error code = -104
-Token unknown - line 1, column 21
-.

Statement failed, SQLSTATE = 42000
Dynamic SQL Error
-SQL error code = -104
-Token unknown - line 1, column 24
-.

Statement failed, SQLSTATE = 42000
Dynamic SQL Error
-SQL error code = -104
-Token unknown - line 1, column 29
-.
"""

act = python_act('db')

conf = store_config('databases.conf')
new_config = temp_file('new_databases.conf')

dbname = 'DB_create_user_06'

@pytest.mark.version('>=3.0')
def test_1(act: Action, conf: ConfigManager, new_config: Path):
    
    multifactor = 'GostPassword' if act.is_version('>=4.0') else 'Multifactor'

    databases_conf=f"""
        {dbname} = {act.db.db_path} {{
            UserManager = Srp, Legacy_UserManager, {multifactor}_Manager
            AuthServer = Srp, Legacy_Auth, {multifactor}
            WireCrypt = Disabled
        }}
    """
    
    new_config.write_text(databases_conf)
    conf.replace(new_config)
    
    act.expected_stderr = expected_stderr

    create_user = f"""
        CREATE USER user_srp. PASSWORD 'test' FIRSTNAME 'fname' MIDDLENAME 'mname' LASTNAME 'lname' USING PLUGIN Srp;
        CREATE USER user_legacy. PASSWORD 'test' FIRSTNAME 'fname' MIDDLENAME 'mname' LASTNAME 'lname' USING PLUGIN Legacy_UserManager;
        CREATE USER user_multifactor. PASSWORD 'test' FIRSTNAME 'fname' MIDDLENAME 'mname' LASTNAME 'lname' USING PLUGIN {multifactor}_Manager;
        commit;
    """
    act.isql(switches=['-q'], input=create_user)

    assert act.clean_stderr == act.clean_expected_stderr
