#coding:utf-8
"""
ID:          utilites.gstat.record.average_unpacked_length
TITLE:       Check user tables average unpacked records length statistics. 
DESCRIPTION: 
NOTES: Add enough records in test tables so that gstat can use several threads.
"""

import pytest
from math import floor
from firebird.qa import *
from pathlib import Path

TEST_METRIC = 'Average unpacked length'

PAGE_SIZE = 4096
SMALL_FIELD_WIDTH = 1500
LARGE_FIELD_WIDTH = 5500
DP_QNT = 8000

SMALL_RECS_PER_DP = floor(PAGE_SIZE/SMALL_FIELD_WIDTH)
LARGE_RECS_PER_DP = floor(PAGE_SIZE/(LARGE_FIELD_WIDTH - PAGE_SIZE))
SMALL_REC_QNT = SMALL_RECS_PER_DP*DP_QNT
LARGE_REC_QNT = LARGE_RECS_PER_DP*DP_QNT
substring='0123456789'
length = len(substring)
small_test_string=substring*(SMALL_FIELD_WIDTH//length)+substring[:SMALL_FIELD_WIDTH%length]
large_test_string=substring*(LARGE_FIELD_WIDTH//length)+substring[:LARGE_FIELD_WIDTH%length]

init_script = """
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
def test_zero_records(act: Action, gstat_helpers):
    with act.db.connect() as con:
        con.execute_immediate(f"create table TEST(str varchar(10));")
        con.commit()

    act.gstat(switches=['-r'])
    length = gstat_helpers.get_stat(act.stdout, 'TEST', TEST_METRIC)
    assert length == 0

@pytest.mark.version('>=3.0')
def test_unpacked_records(act: Action, gstat_helpers):
    init_small = init_script.format(table_name='SMALL', field_width=SMALL_FIELD_WIDTH, rec_qnt=SMALL_REC_QNT, test_string=small_test_string)
    act.isql(switches=['-q'], input=init_small)
    init_large = init_script.format(table_name='LARGE', field_width=LARGE_FIELD_WIDTH, rec_qnt=LARGE_REC_QNT, test_string=large_test_string)
    act.isql(switches=['-q'], input=init_large)
    act.reset()
    
    act.gstat(switches=['-r'])
    length = gstat_helpers.get_stat(act.stdout, 'SMALL', TEST_METRIC)
    assert length == 1504
    length = gstat_helpers.get_stat(act.stdout, 'LARGE', TEST_METRIC)
    assert length == 5504

@pytest.mark.version('>=3.0')
def test_packed_records(act: Action, gstat_helpers):
    small_packed_string = 'A'*SMALL_FIELD_WIDTH
    init_small = init_script.format(table_name='SMALL', field_width=SMALL_FIELD_WIDTH, rec_qnt=SMALL_REC_QNT, test_string=small_packed_string)
    act.isql(switches=['-q'], input=init_small)
    large_packed_string = 'A'*LARGE_FIELD_WIDTH
    init_large = init_script.format(table_name='LARGE', field_width=LARGE_FIELD_WIDTH, rec_qnt=LARGE_REC_QNT, test_string=large_packed_string)
    act.isql(switches=['-q'], input=init_large)
    act.reset()
    
    act.gstat(switches=['-r'])
    length = gstat_helpers.get_stat(act.stdout, 'SMALL', TEST_METRIC)
    assert length == 1504
    length = gstat_helpers.get_stat(act.stdout, 'LARGE', TEST_METRIC)
    assert length == 5504

