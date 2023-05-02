#coding:utf-8

"""
ID:          create_user.test_07
TITLE:       ALTER USER specifying user name only
DESCRIPTION: Check for ALTER USER sql operator with specifying user name only.
FBTEST:      functional.create_user.create_user_07
"""

import pytest
from firebird.qa import *
from pathlib import Path

db = db_factory()

expected_stdout = """
PLG$USER_NAME                   USER_SRP
PLG$FIRST                       fname
PLG$MIDDLE                      mname
PLG$LAST                        lname

PLG$USER_NAME                   USER_LEGACY
PLG$FIRST_NAME                  fname
PLG$MIDDLE_NAME                 mname
PLG$LAST_NAME                   lname

PLG$USER_NAME                   USER_MULTIFACTOR
PLG$FIRST                       fname
PLG$MIDDLE                      mname
PLG$LAST                        lname
"""

expected_stderr = """
Statement failed, SQLSTATE = 42000
unsuccessful metadata update
-ALTER USER USER_SRP failed
-ALTER USER requires at least one clause to be specified

Statement failed, SQLSTATE = 42000
unsuccessful metadata update
-ALTER USER USER_LEGACY failed
-ALTER USER requires at least one clause to be specified

Statement failed, SQLSTATE = 42000
unsuccessful metadata update
-ALTER USER USER_MULTIFACTOR failed
-ALTER USER requires at least one clause to be specified
"""

act = python_act('db')

conf = store_config('databases.conf')
new_config = temp_file('new_databases.conf')

dbname = 'DB_create_user_07'

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
    act.isql(switches=['-q'], input=create_user)

    act.reset()
    act.expected_stderr = expected_stderr

    alter_user = f"""
        ALTER USER user_srp USING PLUGIN Srp;
        ALTER USER user_legacy USING PLUGIN Legacy_UserManager;
        ALTER USER user_multifactor USING PLUGIN {multifactor}_Manager;
    """
    act.isql(switches=['-q'], input=alter_user)

    assert act.clean_stderr == act.clean_expected_stderr
    
    act.reset()
    act.expected_stdout = expected_stdout

    # Check user in security db
    check_user = """
        set list on; 
        SELECT PLG$USER_NAME, PLG$FIRST, PLG$MIDDLE, PLG$LAST FROM PLG$SRP WHERE PLG$USER_NAME='USER_SRP';
        SELECT PLG$USER_NAME, PLG$FIRST_NAME, PLG$MIDDLE_NAME, PLG$LAST_NAME FROM PLG$USERS WHERE PLG$USER_NAME='USER_LEGACY';
        SELECT PLG$USER_NAME, PLG$FIRST, PLG$MIDDLE, PLG$LAST FROM PLG$MF WHERE PLG$USER_NAME='USER_MULTIFACTOR';
    """
    act.isql(switches=['-q', act.vars['security-db']], input=check_user, connect_db=False)

    assert act.clean_stdout == act.clean_expected_stdout

    drop_user = f"""
        DROP USER user_srp USING PLUGIN Srp;
        DROP USER user_legacy USING PLUGIN Legacy_UserManager;
        DROP USER user_multifactor USING PLUGIN {multifactor}_Manager;
    """
    act.isql(switches=['-q'], input=drop_user)
