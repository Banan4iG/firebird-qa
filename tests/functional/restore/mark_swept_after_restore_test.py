#coding:utf-8
"""
ID:          restore.mark_swept_after_restore
TITLE:       Check that all primary pages has been marked as swept after db restore.
DESCRIPTION: See: https://tracker.red-soft.ru/issues/98299
    Create database with page size 4096
    Create a test table with one field greater than db page size. A field must be such size to fit multiple heads on one primary page.
    Add records in the table and compare primary and swept pages via gstat. They must be not equal (zero swept pages).
    Backup/restore test db and compare primary and swept pages. Now they must be equal.
"""

import pytest
from firebird.qa import *
from math import floor
import re
from pathlib import Path

PAGE_SIZE = 4096
FIELD_WIDTH = 5500
DP_QNT = 100
RECS_PER_DP = floor(PAGE_SIZE/(FIELD_WIDTH - PAGE_SIZE))
REC_QNT = RECS_PER_DP*DP_QNT

db = db_factory(page_size=PAGE_SIZE)
fbk_tmp = temp_file('mark_swept_after_restore.fbk')
fdb_tmp = temp_file('mark_swept_after_restore.fdb')

act = python_act('db')

def get_stat(data):
    pattern = re.compile(r'Primary pages: (\d+), secondary pages: \d+, swept pages: (\d+)')
    result = pattern.search(data)
    if result:
        return result.group(1), result.group(2)
    else:
        return

@pytest.mark.version('>=5.0')
def test_1(act: Action, fbk_tmp: Path, fdb_tmp: Path):
    
    substring='0123456789'
    length = len(substring)
    test_string=substring*(FIELD_WIDTH//length)+substring[:FIELD_WIDTH%length]

    create_script = f"""
        create table test(str varchar({FIELD_WIDTH}));
        commit;
        
        set term ^;
        execute block as
            declare variable i integer;
        begin
            i = {REC_QNT};
            while (i > 0) do
            begin
                insert into test values ('{test_string}');
                i = i - 1;
            end
        end^
        set term ;^
        commit;
    """

    act.isql(switches=['-q'], input=create_script)
    act.reset()

    act.gstat(switches=[])
    (primary, swept) = get_stat(act.stdout)
    assert primary != swept
    act.reset()

    act.gbak(switches=['-b', act.db.dsn, str(fbk_tmp)])
    act.reset()

    act.gbak(switches=['-rep', str(fbk_tmp), str(fdb_tmp)])
    act.reset()

    restore_db = act.get_dsn(fdb_tmp)

    act.gstat(switches=[restore_db], connect_db=False)
    (primary, swept) = get_stat(act.stdout)
    assert primary == swept
    act.reset()

    # Check that flags are in a consistent state
    act.gfix(switches=['-v', '-full', '-n', restore_db], combine_output=True)
    assert act.clean_stdout == ''
