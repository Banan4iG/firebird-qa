#coding:utf-8

"""
ID:          create_user.test_05
TITLE:       ALTER USER (non existing)
DESCRIPTION: Check for ALTER USER sql operator with non existing user.
FBTEST:      functional.create_user.create_user_05
"""

import pytest
from firebird.qa import *
from pathlib import Path

db = db_factory()

expected_stderr = """
Statement failed, SQLSTATE = HY000
record not found for user: USER_SRP

Statement failed, SQLSTATE = HY000
record not found for user: USER_LEGACY

Statement failed, SQLSTATE = HY000
modify record error
"""

act = python_act('db')

conf = store_config('databases.conf')
new_config = temp_file('new_databases.conf')

dbname = 'DB_create_user_05'

@pytest.mark.version('>=3.0')
def test_1(act: Action, conf: ConfigManager, new_config: Path):
    
    databases_conf=f"""
        {dbname} = {act.db.db_path} {{
            UserManager = Srp, Legacy_UserManager, Multifactor_Manager
            AuthServer = Srp, Legacy_Auth, Multifactor
            WireCrypt = Disabled
        }}
    """

    new_config.write_text(databases_conf)
    conf.replace(new_config)

    act.expected_stderr = expected_stderr

    alter_user = """
        ALTER USER user_srp PASSWORD 'test' FIRSTNAME 'afname' MIDDLENAME 'amname' LASTNAME 'alname' USING PLUGIN Srp;
        ALTER USER user_legacy PASSWORD 'test' FIRSTNAME 'afname' MIDDLENAME 'amname' LASTNAME 'alname' USING PLUGIN Legacy_UserManager;
        ALTER USER user_multifactor PASSWORD 'test' FIRSTNAME 'afname' MIDDLENAME 'amname' LASTNAME 'alname' USING PLUGIN Multifactor_Manager;
    """
    act.isql(switches=['-q'], input=alter_user)

    assert act.clean_stderr == act.clean_expected_stderr
