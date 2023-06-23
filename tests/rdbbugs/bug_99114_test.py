#coding:utf-8

"""
ID:          RS-99114
ISSUE:       https://http://tracker.red-soft.biz/issues/9914
TITLE:       Incorrect work of bulk inserts with large records when restoring the database
DESCRIPTION:
    Create a table with field size exceeding db page size.
    Insert two record in the table. Record data must be poorly compressible so that the record is divided into two or more pages.
    Backup test db and restore it.
    First fragments of both records in restored db should fit on one primary page.
    Use repeated substring '0123456789'. This way we guarantee that adjacent characters will not be repeated.
"""

import pytest
from firebird.qa import *
import re

# Width of a string field in a test table.
FIELD_WIDTH = 5000
substring='0123456789'
length = len(substring)
test_string=substring*(FIELD_WIDTH//length)+substring[:FIELD_WIDTH%length]

init_script = f"""
    create table test (str varchar({FIELD_WIDTH}));
    commit;
    insert into test values('{test_string}');
    insert into test values('{test_string}');
    commit;
"""

db = db_factory(page_size=4096, init=init_script)
act = python_act('db')

restored_db = db_factory(filename='bug_99114.fdb', do_not_create=True)
backup = temp_file('bug_99114.fbk')

@pytest.mark.version('>=3.0')
def test_1(act: Action, backup, restored_db):
    substring='0123456789'
    length = len(substring)
    test_string=substring*(FIELD_WIDTH//length)+substring[:FIELD_WIDTH%length]

    act.gbak(switches=['-BACKUP_DATABASE', act.db.dsn, backup])
    act.gbak(switches=['-CREATE_DATABASE', backup, restored_db.dsn])
    act.reset()

    act.gstat(switches=['-d', restored_db.dsn], connect_db=False)
    print(act.stdout)
    pattern = re.compile(f'Primary pages: (\\d+)', flags=re.S)
    result = pattern.search(act.stdout).group(1)
    assert result == '1'