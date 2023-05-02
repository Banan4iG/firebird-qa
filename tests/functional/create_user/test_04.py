#coding:utf-8

"""
ID:          create_user.test_04
TITLE:       DROP USER (non existing)
DESCRIPTION: Check for DROP USER sql operator with non existing user.
FBTEST:      functional.create_user.create_user_04
"""

import pytest
from firebird.qa import *
from pathlib import Path

db = db_factory()

expected_stdout = """
Statement failed, SQLSTATE = HY000
record not found for user: USER_SRP

Statement failed, SQLSTATE = HY000
record not found for user: USER_LEGACY

Statement failed, SQLSTATE = HY000
record not found for user: USER_MULTIFACTOR
"""

act = python_act('db')

conf = store_config('databases.conf')
new_config = temp_file('new_databases.conf')

dbname = 'DB_create_user_04'

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

    act.expected_stdout = expected_stdout

    drop_user = f"""
        DROP USER user_srp USING PLUGIN Srp;
        DROP USER user_legacy USING PLUGIN Legacy_UserManager;
        DROP USER user_multifactor USING PLUGIN {multifactor}_Manager;
    """
    act.isql(switches=['-q'], input=drop_user, combine_output=True)

    assert act.clean_stdout == act.clean_expected_stdout
