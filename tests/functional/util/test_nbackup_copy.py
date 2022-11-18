#coding:utf-8

"""
ID:          util.nbackup-copy
TITLE:       nbackup utility: check ability to use -copy command switch
DESCRIPTION: 
    This switch allows to make db backup without adding new record in RDB$BACKUP_HISTORY.

FBTEST:      None
"""

import pytest
from firebird.qa import *
from firebird.driver import DatabaseError
import re

init_script = """
CREATE TABLE TEST(id INT);
COMMIT;
INSERT INTO TEST VALUES(1);
INSERT INTO TEST VALUES(2);
INSERT INTO TEST VALUES(3);
"""

db = db_factory(init=init_script)
backup_db = db_factory(filename='backup.fdb', do_not_create=True)

act = python_act('db')

expected_isql_stdout = """
COUNT                           0

ID                              1
ID                              2
ID                              3
"""

@pytest.mark.version('>=4.0')
def test_1(act: Action, backup_db: Database, capsys):
    # Make full backup with copy switch
    act.nbackup(switches=['-copy', str(act.db.db_path), str(backup_db.db_path)])
    
    # Check backup history
    with act.db.connect() as con:
        with con.cursor() as cur:
            cur.execute("SELECT count(*) FROM RDB$BACKUP_HISTORY")
            act.print_data_list(cur)

    # Check backup
    pattern = re.compile(r'^I/O error during ("CreateFile \(open\)"|"open") operation for file ".*backup.fdb.delta".*Error while trying to open file.*(No such file or directory|The system cannot find the file specified)', re.S|re.I)
    with pytest.raises(DatabaseError, match=pattern):
        backup_db.connect()
    # Unlock backup
    act.nbackup(switches=['-F', str(backup_db.db_path)])
    
    # Compare databases
    act.rdbrepldiff(switches=['-SI', '-D', str(act.db.db_path), '-R', str(backup_db.db_path)], combine_output=True)
    act.expected_stdout = "Summary: no differences found"
    assert act.clean_stdout == act.clean_expected_stdout
    
    # Check test table
    with backup_db.connect() as con_2:
        with con_2.cursor() as cur:
            cur.execute("SELECT * from TEST")
            act.print_data_list(cur)

    act.expected_stdout = expected_isql_stdout
    act.stdout = capsys.readouterr().out + act.stdout
    assert act.clean_stdout == act.clean_expected_stdout
    


