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
from string import Template

db = db_factory()

expected_stderr = Template("""
Statement failed, SQLSTATE = HY000
record not found for user: USER_SRP

Statement failed, SQLSTATE = HY000
record not found for user: USER_LEGACY

Statement failed, SQLSTATE = HY000
$mult_error
""")

act = python_act('db')

conf = store_config('databases.conf')
new_config = temp_file('new_databases.conf')

dbname = 'DB_create_user_05'

@pytest.mark.version('>=3.0')
def test_1(act: Action, conf: ConfigManager, new_config: Path):
    
    if act.is_version('>=4.0'):
        multifactor = 'GostPassword'
        act.expected_stderr = expected_stderr.substitute(mult_error="record not found for user: USER_MULTIFACTOR")
    else: 
        multifactor = 'Multifactor'
        act.expected_stderr = expected_stderr.substitute(mult_error="modify record error")

    databases_conf=f"""
        {dbname} = {act.db.db_path} {{
            UserManager = Srp, Legacy_UserManager, {multifactor}_Manager
            AuthServer = Srp, Legacy_Auth, {multifactor}
            WireCrypt = Disabled
        }}
    """

    new_config.write_text(databases_conf)
    conf.replace(new_config)

    alter_user = f"""
        ALTER USER user_srp PASSWORD 'test' FIRSTNAME 'afname' MIDDLENAME 'amname' LASTNAME 'alname' USING PLUGIN Srp;
        ALTER USER user_legacy PASSWORD 'test' FIRSTNAME 'afname' MIDDLENAME 'amname' LASTNAME 'alname' USING PLUGIN Legacy_UserManager;
        ALTER USER user_multifactor PASSWORD 'test' FIRSTNAME 'afname' MIDDLENAME 'amname' LASTNAME 'alname' USING PLUGIN {multifactor}_Manager;
    """
    act.isql(switches=['-q'], input=alter_user)

    assert act.clean_stderr == act.clean_expected_stderr
