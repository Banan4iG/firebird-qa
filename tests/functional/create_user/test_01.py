#coding:utf-8

"""
ID:          create_user.test_01
TITLE:       CREATE USER with correct parametres
DESCRIPTION: Check for CREATE USER sql operator with correct parametres.
FBTEST:      functional.create_user.create_user_01
"""

import pytest
from firebird.qa import *
from pathlib import Path
from string import Template

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

act = python_act('db')

conf = store_config('databases.conf')
new_config = temp_file('new_databases.conf')

dbname = 'DB_create_user_01'

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

    create_user = f"""
        CREATE USER user_srp PASSWORD 'test' FIRSTNAME 'fname' MIDDLENAME 'mname' LASTNAME 'lname' USING PLUGIN Srp;
        CREATE USER user_legacy PASSWORD 'test' FIRSTNAME 'fname' MIDDLENAME 'mname' LASTNAME 'lname' USING PLUGIN Legacy_UserManager;
        CREATE USER user_multifactor PASSWORD 'test' FIRSTNAME 'fname' MIDDLENAME 'mname' LASTNAME 'lname' USING PLUGIN {multifactor}_Manager;
        commit;
    """
    act.isql(switches=['-q'], input=create_user, combine_output=True)
    assert act.clean_stdout == ""
    # Check user in security db
    check_user = """
        set list on; 
        SELECT PLG$USER_NAME, PLG$FIRST, PLG$MIDDLE, PLG$LAST FROM PLG$SRP WHERE PLG$USER_NAME='USER_SRP';
        SELECT PLG$USER_NAME, PLG$FIRST_NAME, PLG$MIDDLE_NAME, PLG$LAST_NAME FROM PLG$USERS WHERE PLG$USER_NAME='USER_LEGACY';
        SELECT PLG$USER_NAME, PLG$FIRST, PLG$MIDDLE, PLG$LAST FROM PLG$MF WHERE PLG$USER_NAME='USER_MULTIFACTOR';
    """
    act.isql(switches=['-q', act.vars['security-db']], input=check_user, connect_db=False, combine_output=True)

    assert act.clean_stdout == act.clean_expected_stdout
    
    drop_user = f"""
        DROP USER user_srp USING PLUGIN Srp;
        DROP USER user_legacy USING PLUGIN Legacy_UserManager;
        DROP USER user_multifactor USING PLUGIN {multifactor}_Manager;
    """
    act.isql(switches=['-q'], input=drop_user)
