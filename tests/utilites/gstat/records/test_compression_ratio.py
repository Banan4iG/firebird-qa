#coding:utf-8
"""
ID:          utilites.gstat.records.compression_ratio
TITLE:       Check user tables compression ratio statistics. 
DESCRIPTION: 
NOTES: Add enough records in test tables so that gstat can use several threads.
"""

import pytest
from math import floor
from firebird.qa import *
from pathlib import Path

TEST_METRIC = 'compression ratio'

PAGE_SIZE = 4096
SMALL_FIELD_WIDTH = 1500
LARGE_FIELD_WIDTH = 5500
DP_QNT = 8001

SMALL_RECS_PER_DP = floor(PAGE_SIZE/SMALL_FIELD_WIDTH)
LARGE_RECS_PER_DP = floor(PAGE_SIZE/(LARGE_FIELD_WIDTH - PAGE_SIZE))
SMALL_REC_QNT = SMALL_RECS_PER_DP*DP_QNT
LARGE_REC_QNT = LARGE_RECS_PER_DP*DP_QNT


script_template = """
    create table {table_name}(str char({field_width}));
    commit;
    
    -- Insert records
    set term ^;
    execute block as
        declare variable i integer;
    begin
        i = {rec_qnt};
        while (i > 0) do
        begin
            insert into {table_name} values ('{test_string}');
            i = i - 1;
        end
    end^
    set term ;^

    commit;
"""

db = db_factory(page_size=PAGE_SIZE)

act = python_act('db')

@pytest.mark.version('>=3.0')
def test_packed_records(act: Action, gstat_helpers):
    # String with repeated symbol must compressed into 9 bytes (5 data bytes and 4 service bytes).
    # For RDB3 data previosly divided into blocks of 127 bytes. 
    # So we get values:
    # - For RDB3: 53.71 and 
    # - For RDB5 167.11 and 611.56.
    if act.is_version('>=5.0'):
        small_ratio = 167.11
        large_ratio = 611.56
    else:    
        small_ratio = 53.71
        large_ratio = 61.16

    small_packed_string = 'A'*SMALL_FIELD_WIDTH
    large_packed_string = 'A'*LARGE_FIELD_WIDTH
    init_script = script_template.format(table_name='SMALL', field_width=SMALL_FIELD_WIDTH, rec_qnt=SMALL_REC_QNT, test_string=small_packed_string)   
    init_script += script_template.format(table_name='LARGE', field_width=LARGE_FIELD_WIDTH, rec_qnt=LARGE_REC_QNT, test_string=large_packed_string)
    act.isql(switches=['-q'], input=init_script)
    act.reset()
    
    act.gstat(switches=['-d', '-r'])  
    ratio = gstat_helpers.get_metric(act.stdout, 'SMALL', TEST_METRIC)
    assert ratio == small_ratio
    ratio = gstat_helpers.get_metric(act.stdout, 'LARGE', TEST_METRIC)
    assert ratio == large_ratio
