#coding:utf-8
"""
ID:          utilites.gstat.records.total_fragments
TITLE:       Check user tables total fragments statistics. 
DESCRIPTION: 
NOTES: Add enough records in test tables so that gstat can use several threads.
"""

import pytest
from math import floor
from firebird.qa import *
from pathlib import Path

TEST_METRIC = 'total fragments'

PAGE_SIZE = 4096
SMALL_FIELD_WIDTH = 1500
LARGE_FIELD_WIDTH = 5500
HUGE_FIELD_WIDTH = 10500

DP_QNT = 8001
SMALL_RECS_PER_DP = floor(PAGE_SIZE/SMALL_FIELD_WIDTH)
LARGE_RECS_PER_DP = floor(PAGE_SIZE/(LARGE_FIELD_WIDTH - PAGE_SIZE))
HUGE_RECS_PER_DP = floor(PAGE_SIZE/(HUGE_FIELD_WIDTH - 2*PAGE_SIZE))
SMALL_REC_QNT = SMALL_RECS_PER_DP*DP_QNT
LARGE_REC_QNT = LARGE_RECS_PER_DP*DP_QNT
HUGE_REC_QNT = HUGE_RECS_PER_DP*DP_QNT

substring='0123456789'
length = len(substring)
small_test_string=substring*(SMALL_FIELD_WIDTH//length)+substring[:SMALL_FIELD_WIDTH%length]
large_test_string=substring*(LARGE_FIELD_WIDTH//length)+substring[:LARGE_FIELD_WIDTH%length]
huge_test_string=substring*(HUGE_FIELD_WIDTH//length)+substring[:HUGE_FIELD_WIDTH%length]

script_template = """
    create table {tb_name}(str char({field_width}));
    commit;
  
    -- Small records
    set term ^;
    execute block as
        declare variable i integer;
    begin
        i = {rec_qnt};
        while (i > 0) do
        begin
            insert into {tb_name} values ('{test_string}');
            i = i - 1;
        end
    end^
    set term ;^

    commit;
"""

init_script = script_template.format(tb_name="SMALL", field_width=SMALL_FIELD_WIDTH, rec_qnt=SMALL_REC_QNT, test_string=small_test_string)
init_script += script_template.format(tb_name="LARGE", field_width=LARGE_FIELD_WIDTH, rec_qnt=LARGE_REC_QNT, test_string=large_test_string)
init_script += script_template.format(tb_name="HUGE", field_width=HUGE_FIELD_WIDTH, rec_qnt=HUGE_REC_QNT, test_string=huge_test_string)

db = db_factory(page_size=PAGE_SIZE, init=init_script)
act = python_act('db')

@pytest.mark.version('>=3.0')
def test_1(act: Action, gstat_helpers):
    act.gstat(switches=['-d', '-r'])
    stats = []
    stats.append(gstat_helpers.get_metric(act.stdout, 'SMALL', TEST_METRIC))
    stats.append(gstat_helpers.get_metric(act.stdout, 'LARGE', TEST_METRIC))
    stats.append(gstat_helpers.get_metric(act.stdout, 'HUGE', TEST_METRIC))
    assert stats == [0, LARGE_REC_QNT, HUGE_REC_QNT*2]    
