#coding:utf-8
"""
ID:          utilites.gstat.parallel.records
TITLE:       Check user records metrics with parallel key.
DESCRIPTION:
NOTES:       Add enough records in test tables so that gstat can use several threads.
             MaxParallelWorkers value must be set greater than 4 before running the test.
"""

import pytest
from math import floor
from firebird.qa import *
import re

PAGE_SIZE = 4096
SMALL_FIELD_WIDTH = 1500
LARGE_FIELD_WIDTH = 5500
DP_QNT = 8001
SMALL_RECS_PER_DP = floor(PAGE_SIZE/SMALL_FIELD_WIDTH)
LARGE_RECS_PER_DP = floor(PAGE_SIZE/(LARGE_FIELD_WIDTH - PAGE_SIZE))
SMALL_REC_QNT = SMALL_RECS_PER_DP*DP_QNT
LARGE_REC_QNT = LARGE_RECS_PER_DP*DP_QNT

substring='0123456789'
length = len(substring)
small_test_string=substring*(SMALL_FIELD_WIDTH//length)+substring[:SMALL_FIELD_WIDTH%length]
large_test_string=substring*(LARGE_FIELD_WIDTH//length)+substring[:LARGE_FIELD_WIDTH%length]

init_script = f"""
    create table small(str char({SMALL_FIELD_WIDTH}));
    commit;

    create table large(str char({LARGE_FIELD_WIDTH}));
    commit;
    
    -- Small records
    set term ^;
    execute block as
        declare variable i integer;
    begin
        i = {SMALL_REC_QNT};
        while (i > 0) do
        begin
            insert into small values ('{small_test_string}');
            i = i - 1;
        end
    end^

    -- Large records
    execute block as
        declare variable i integer;
    begin
        i = {LARGE_REC_QNT};
        while (i > 0) do
        begin
            insert into large values ('{large_test_string}');
            i = i - 1;
        end
    end^

    set term ;^
    commit;
"""

db = db_factory(page_size=PAGE_SIZE, init=init_script)
act = python_act('db', substitutions=[('SMALL \\(.*','SMALL'), ('LARGE \\(.*','LARGE')])

expected_stdout = f"""
LARGE (129)
    Total formats: 1, used formats: 1
    Average record length: {(LARGE_FIELD_WIDTH+4):.2f}, total records: {LARGE_REC_QNT}
    Average version length: 0.00, total versions: 0, max versions: 0
    Average unpacked length: {(LARGE_FIELD_WIDTH+4):.2f}, compression ratio: 1.00
    Big record pages: {LARGE_REC_QNT}

SMALL (128)
    Total formats: 1, used formats: 1
    Average record length: {(SMALL_FIELD_WIDTH+4):.2f}, total records: {SMALL_REC_QNT}
    Average version length: 0.00, total versions: 0, max versions: 0
    Average unpacked length: {(SMALL_FIELD_WIDTH+4):.2f}, compression ratio: 1.00
"""

@pytest.mark.version('>=5.0')
def test_1(act: Action, gstat_helpers):
    act.expected_stdout = expected_stdout
    act.gstat(switches=['-d', '-r', '-par', '4'])
    # Get stats without header
    stats = gstat_helpers.get_full_stat(act.stdout, 'Analyzing database pages')
    # Delete data pages metrics and fragments metrics
    clean_stats = re.sub('^\\s+(Primary|Average fragment|Pointer|Data|Empty|Fill|\\d+).*\\n', '', stats, flags=re.M) 
    act.stdout = clean_stats
    assert act.clean_stdout == act.clean_expected_stdout