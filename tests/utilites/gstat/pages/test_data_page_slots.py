#coding:utf-8
"""
ID:          utilites.gstat.pages.data_page_slots
TITLE:       Check user tables pointer pages statistics. 
DESCRIPTION: 
NOTES: Add enough records in test tables so that gstat can use several threads.
"""

import pytest
from math import floor, ceil
from firebird.qa import *
from pathlib import Path

TEST_METRIC = 'data page slots'

MAX_DATA_PAGES = [pytest.param(x, id=f"{x}_data_pages") for x in (1, 1000, 8000)]

PAGE_SIZE = 4096
SMALL_FIELD_WIDTH = 1500
LARGE_FIELD_WIDTH = 5500
SMALL_RECS_PER_DP = floor(PAGE_SIZE/SMALL_FIELD_WIDTH)
LARGE_RECS_PER_DP = floor(PAGE_SIZE/(LARGE_FIELD_WIDTH - PAGE_SIZE))

substring='0123456789'
length = len(substring)
small_test_string=substring*(SMALL_FIELD_WIDTH//length)+substring[:SMALL_FIELD_WIDTH%length]
large_test_string=substring*(LARGE_FIELD_WIDTH//length)+substring[:LARGE_FIELD_WIDTH%length]

init_script = f"""
    create table small(str char({SMALL_FIELD_WIDTH}));
    commit;

    create table large(str char({LARGE_FIELD_WIDTH}));
    commit;
"""

test_script = """
    set term ^;
    execute block as
        declare variable i integer;
    begin
        i = {req_qnt};
        while (i > 0) do
        begin
            insert into {table_name} values ('{test_string}');
            i = i - 1;
        end
    end^

    set term ;^
    commit;
"""

db = db_factory(page_size=PAGE_SIZE, init=init_script)

act = python_act('db')

@pytest.mark.version('>=3.0')
def test_zero_records(act: Action, gstat_helpers):

    act.gstat(switches=[])
    slots = gstat_helpers.get_stat(act.stdout, 'SMALL', TEST_METRIC)
    assert slots == 0

@pytest.mark.parametrize("dp_qnt", MAX_DATA_PAGES)
@pytest.mark.version('>=3.0')
def test_many_records(act: Action, gstat_helpers, dp_qnt):
    
    small_rec_qnt = SMALL_RECS_PER_DP*dp_qnt
    tmp_script = test_script.format(req_qnt=small_rec_qnt, table_name='SMALL', test_string=small_test_string)
    large_rec_qnt = LARGE_RECS_PER_DP*dp_qnt
    tmp_script += test_script.format(req_qnt=large_rec_qnt, table_name='LARGE', test_string=large_test_string)

    act.isql(switches=['-q'], input=tmp_script)
    act.reset()

    act.gstat(switches=[])
    slots = gstat_helpers.get_stat(act.stdout, 'SMALL', TEST_METRIC)
    assert slots == dp_qnt
    slots = gstat_helpers.get_stat(act.stdout, 'LARGE', TEST_METRIC)
    assert slots == dp_qnt
