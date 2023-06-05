#coding:utf-8
"""
ID:          utilites.gstat.records.all_metrics
TITLE:       Check all user records metrics.
DESCRIPTION: 
NOTES: Add enough records in test tables so that gstat can use several threads.
"""

import pytest
from math import floor, ceil
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

stdout_template = """
LARGE (129)
    Total formats: 1, used formats: 1
    Average record length: {large_rec_len:.2f}, total records: {large_total}
    Average version length: 0.00, total versions: 0, max versions: 0
    Average unpacked length: {large_unpacked:.2f}, compression ratio: {compression:.2f}
    Big record pages: {large_big_pages}

SMALL (128)
    Total formats: 1, used formats: 1
    Average record length: {small_rec_len:.2f}, total records: {small_total}
    Average version length: 0.00, total versions: 0, max versions: 0
    Average unpacked length: {small_unpacked:.2f}, compression ratio: {compression:.2f}
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action, gstat_helpers):
    # For RDB3 data previosly divided into blocks of 127 bytes so we get different values.
    if act.is_version('>=5.0'):
        large_rec_len = LARGE_FIELD_WIDTH+4
        compression = 1
        small_rec_len = SMALL_FIELD_WIDTH+4
    else:
        large_rec_len = LARGE_FIELD_WIDTH+ceil(LARGE_FIELD_WIDTH/127+4)
        #large_rec_len = 5540
        compression = 0.99
        small_rec_len = SMALL_FIELD_WIDTH+ceil(SMALL_FIELD_WIDTH/127)+4

    act.expected_stdout = stdout_template.format(large_rec_len=large_rec_len, large_total=LARGE_REC_QNT, \
                                                 large_unpacked=(LARGE_FIELD_WIDTH+4), compression=compression, 
                                                 large_big_pages=LARGE_REC_QNT, \
                                                 small_rec_len=small_rec_len, small_total=SMALL_REC_QNT, \
                                                 small_unpacked=(SMALL_FIELD_WIDTH+4))

    act.gstat(switches=['-d', '-r'])
    # Get stats without header
    stats = gstat_helpers.get_full_stat(act.stdout, 'Analyzing database pages')
    # Delete data pages metrics and fragments metrics
    clean_stats = re.sub('^\\s+(Primary|Average fragment|Pointer|Data|Empty|Fill|\\d+).*\\n', '', stats, flags=re.M) 
    act.stdout = clean_stats
    assert act.clean_stdout == act.clean_expected_stdout