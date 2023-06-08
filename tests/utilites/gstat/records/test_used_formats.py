#coding:utf-8
"""
ID:          utilites.gstat.records.total_formats
TITLE:       Check user tables used formats statistics. 
DESCRIPTION: 
NOTES: Add enough records in test tables so that gstat can use several threads.
"""

import pytest
from math import floor
from firebird.qa import *

TEST_METRIC = 'used formats'

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
    create table small(str varchar({SMALL_FIELD_WIDTH}));
    commit;

    create table large(str varchar({LARGE_FIELD_WIDTH}));
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
act = python_act('db')

@pytest.mark.version('>=3.0')
def test_several_formats(act: Action, gstat_helpers):
    MAX_FORMATS = 253
    with act.db.connect() as con:
        for i in range(1, MAX_FORMATS):
            con.execute_immediate(f"ALTER TABLE SMALL ADD new{i} varchar(10);")
            con.execute_immediate(f"ALTER TABLE LARGE ADD new{i} varchar(10);")
            con.commit()
            if i > MAX_FORMATS//2:
                con.execute_immediate(f"INSERT INTO SMALL(new{i}) values('Test');")
                con.execute_immediate(f"INSERT INTO LARGE(new{i}) values('Test');")
                con.commit()

    act.gstat(switches=['-d', '-r'])
    formats = gstat_helpers.get_metric(act.stdout, 'SMALL', TEST_METRIC)
    assert formats == MAX_FORMATS//2+1
    formats = gstat_helpers.get_metric(act.stdout, 'LARGE', TEST_METRIC)
    assert formats == MAX_FORMATS//2+1
