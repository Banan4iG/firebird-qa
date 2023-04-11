#coding:utf-8
"""
ID:          utilites.gfix.sweep.mark_swept
TITLE:       Check that all primary pages has been marked as swept after multitreaded sweep.
DESCRIPTION:
    Create database with page size 4096
    Create a test table with one field greater than db page size. A field must be such size to fit multiple heads on one primary page.
    Add enough records in the table to run sweep with several threads and compare primary and swept pages via gstat. They must be not equal (zero swept pages).
    Run multithreaded sweep for test db and after compare primary and swept pages. Now they must be equal.
NOTES: It's required that the MaxParallelWorkers value in firebird.conf be set not less than 4.
"""

import pytest
from firebird.qa import *
from math import floor
import re
from pathlib import Path

TREADS = 4
PAGE_SIZE = 4096
FIELD_WIDTH = 5500
DP_QNT = 8000
RECS_PER_DP = floor(PAGE_SIZE/(FIELD_WIDTH - PAGE_SIZE))
REC_QNT = RECS_PER_DP*DP_QNT


db = db_factory(page_size=PAGE_SIZE)

act = python_act('db')

def get_stat(data):
    pattern = re.compile(r'Primary pages: (\d+), secondary pages: \d+, swept pages: (\d+)')
    result = pattern.search(data)
    if result:
        return result.group(1), result.group(2)
    else:
        return

@pytest.mark.version('>=3.0')
def test_1(act: Action):
    
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

    act.gfix(switches=['-sweep', '-par', str(TREADS), act.db.dsn])
    act.reset()

    act.gstat(switches=[])
    (primary, swept) = get_stat(act.stdout)
    assert primary == swept
    act.reset()   

    # Check that flags are in a consistent state
    act.gfix(switches=['-v', '-full', '-n', act.db.dsn], combine_output=True)
    assert act.clean_stdout == ''
