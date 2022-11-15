#coding:utf-8

"""
ID:          alter-database-04
TITLE:       Alter database begin/end backup. Check the state.
DESCRIPTION: 
    Check a state of db before and after 'alter database begin/end backup' commands.
FBTEST:      None
"""

import pytest
from firebird.qa import *

db = db_factory()

isql_script = """
set list on;
SELECT MON$BACKUP_STATE FROM MON$DATABASE;
ALTER DATABASE BEGIN BACKUP;
COMMIT;
SELECT MON$BACKUP_STATE FROM MON$DATABASE;
ALTER DATABASE END BACKUP;
COMMIT;
SELECT MON$BACKUP_STATE FROM MON$DATABASE;
"""

act = isql_act('db', script=isql_script)

expected_stdout = """
MON$BACKUP_STATE                0
MON$BACKUP_STATE                1
MON$BACKUP_STATE                0
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action, capsys):
    act.execute()
    act.expected_stdout = expected_stdout
    assert act.clean_stdout == act.clean_expected_stdout