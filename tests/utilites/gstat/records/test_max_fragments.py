#coding:utf-8
"""
ID:          utilites.gstat.records.max_fragments
TITLE:       Check user tables max fragments statistics. 
DESCRIPTION: 
NOTES: Add enough records in test tables so that gstat can use several threads.
"""

import pytest
from math import floor
from firebird.qa import *
from pathlib import Path

TEST_METRIC = 'max fragments'
FRAGMENTS_QNT = 5

PAGE_SIZE = 4096
SMALL_FIELD_WIDTH = 1500
# Note: max size of varchar field is 32765 bytes
LARGE_FIELD_WIDTH = PAGE_SIZE*(FRAGMENTS_QNT+1)
DP_QNT = 8000
SMALL_RECS_PER_DP = floor(PAGE_SIZE/SMALL_FIELD_WIDTH)
SMALL_REC_QNT = SMALL_RECS_PER_DP*DP_QNT

substring='0123456789'
length = len(substring)
small_test_string=substring*(SMALL_FIELD_WIDTH//length)+substring[:SMALL_FIELD_WIDTH%length]

init_script = f"""
    create table TEST(str char({LARGE_FIELD_WIDTH}));
    commit;
  
    -- Small records
    set term ^;
    execute block as
        declare variable i integer;
    begin
        i = {SMALL_REC_QNT};
        while (i > 0) do
        begin
            insert into TEST values ('{small_test_string}');
            i = i - 1;
        end
    end^
    set term ;^

    commit;
"""

db = db_factory(page_size=PAGE_SIZE, init=init_script)

act = python_act('db')

@pytest.mark.version('>=3.0')
def test_zero_fragments(act: Action, gstat_helpers):
    act.gstat(switches=['-r'])
    fragments = gstat_helpers.get_stat(act.stdout, 'TEST', TEST_METRIC)
    assert fragments == 0

@pytest.mark.version('>=3.0')
def test_many_fragments(act: Action, gstat_helpers):
    for i in range(FRAGMENTS_QNT):
        RECORD_WIDTH = PAGE_SIZE*FRAGMENTS_QNT+500
        test_string=substring*(RECORD_WIDTH//length)+substring[:RECORD_WIDTH%length]
        with act.db.connect() as con:
            con.execute_immediate(f"INSERT INTO TEST VALUES('{test_string}');")
            con.commit()

    act.gstat(switches=['-r'])
    versions = gstat_helpers.get_stat(act.stdout, 'TEST', TEST_METRIC)
    assert versions == FRAGMENTS_QNT
