#coding:utf-8

"""
ID:          create_user.test_03
TITLE:       CREATE USER (already exists)
DESCRIPTION: Check for CREATE USER sql operator when such user already exists.
FBTEST:      functional.create_user.create_user_03
"""

import pytest
from firebird.qa import *
from pathlib import Path

db = db_factory()

expected_stderr = """
Statement failed, SQLSTATE = 23000
add record error
-violation of PRIMARY or UNIQUE KEY constraint "INTEG_5" on table "PLG$SRP"
-Problematic key value is ("PLG$USER_NAME" = 'USER_SRP')

Statement failed, SQLSTATE = 23000
add record error
-violation of PRIMARY or UNIQUE KEY constraint "INTEG_2" on table "PLG$USERS"
-Problematic key value is ("PLG$USER_NAME" = 'USER_LEGACY')

Statement failed, SQLSTATE = 23000
add record error
-violation of PRIMARY or UNIQUE KEY constraint "INTEG_11" on table "PLG$MF"
-Problematic key value is ("PLG$USER_NAME" = 'USER_MULTIFACTOR')
"""

act = python_act('db', substitutions=[("INTEG_\\d+", "INTEG_")])

conf = store_config('databases.conf')
new_config = temp_file('new_databases.conf')

dbname = 'DB_create_user_03'

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

    create_user = f"""
        CREATE USER user_srp PASSWORD 'test' FIRSTNAME 'fname' MIDDLENAME 'mname' LASTNAME 'lname' USING PLUGIN Srp;
        CREATE USER user_legacy PASSWORD 'test' FIRSTNAME 'fname' MIDDLENAME 'mname' LASTNAME 'lname' USING PLUGIN Legacy_UserManager;
        CREATE USER user_multifactor PASSWORD 'test' FIRSTNAME 'fname' MIDDLENAME 'mname' LASTNAME 'lname' USING PLUGIN {multifactor}_Manager;
        commit;
    """
    act.isql(switches=['-q'], input=create_user, combine_output=True)
    assert act.clean_stdout == ""

    act.reset()
    act.expected_stderr = expected_stderr
    act.isql(switches=['-q'], input=create_user)

    assert act.clean_stderr == act.clean_expected_stderr

    drop_user = f"""
        DROP USER user_srp USING PLUGIN Srp;
        DROP USER user_legacy USING PLUGIN Legacy_UserManager;
        DROP USER user_multifactor USING PLUGIN {multifactor}_Manager;
    """
    act.isql(switches=['-q'], input=drop_user)
