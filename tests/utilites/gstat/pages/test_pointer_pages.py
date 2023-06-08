#coding:utf-8
"""
ID:          utilites.gstat.pages.pointer_pages
TITLE:       Check user tables pointer pages statistics. 
DESCRIPTION: Check out the increase in pointer pages after full filling
NOTES: Add enough records in test tables so that gstat can use several threads.
"""

import pytest
from math import floor, ceil
from firebird.qa import *
from pathlib import Path

TEST_METRIC = 'Pointer pages'

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

@pytest.mark.parametrize("dp_qnt", [pytest.param(808, id="1_pointer_page"), pytest.param(809, id="2_pointer_pages")])
@pytest.mark.version('>=3.0')
def test(act: Action, gstat_helpers, dp_qnt):
    
    small_rec_qnt = SMALL_RECS_PER_DP*dp_qnt
    tmp_script = test_script.format(req_qnt=small_rec_qnt, table_name='SMALL', test_string=small_test_string)
    large_rec_qnt = LARGE_RECS_PER_DP*dp_qnt
    tmp_script += test_script.format(req_qnt=large_rec_qnt, table_name='LARGE', test_string=large_test_string)

    act.isql(switches=['-q'], input=tmp_script)
    act.reset()

    expected_pages_qnt = ceil(dp_qnt/808)

    act.gstat(switches=['-d'])
    pages = gstat_helpers.get_metric(act.stdout, 'SMALL', TEST_METRIC)
    assert pages == expected_pages_qnt
    pages = gstat_helpers.get_metric(act.stdout, 'LARGE', TEST_METRIC)
    assert pages == expected_pages_qnt
