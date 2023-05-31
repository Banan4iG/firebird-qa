#coding:utf-8
"""
ID:          utilites.gstat.pages.empty_pages
TITLE:       Check user tables empty pages statistics. 
DESCRIPTION: 
NOTES: Add enough records in test tables so that gstat can use several threads.
"""

import pytest
from math import floor
from firebird.qa import *
from pathlib import Path

TEST_METRIC = 'Empty pages'

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

init_script_template = """
    create table {table_name}(str {field_type});
    commit;

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

init_script = init_script_template.format(table_name='SMALL', field_type=f"char({SMALL_FIELD_WIDTH})", req_qnt=SMALL_REC_QNT, test_string=small_test_string)
init_script += init_script_template.format(table_name='LARGE', field_type=f"char({LARGE_FIELD_WIDTH})", req_qnt=LARGE_REC_QNT, test_string=large_test_string)

db = db_factory(page_size=PAGE_SIZE, init=init_script)

act = python_act('db')

@pytest.mark.version('>=3.0')
def test_no_records(act: Action, gstat_helpers):
    # Empty table
    with act.db.connect() as con:
        con.execute_immediate(f"create table TEST(str varchar(10));")
        con.commit()

    act.gstat(switches=[])
    pages = gstat_helpers.get_stat(act.stdout, 'TEST', TEST_METRIC)
    assert pages == 0

@pytest.mark.version('>=3.0')
def test_all_pages_filled(act: Action, gstat_helpers):  
    act.gstat(switches=[])
    pages = gstat_helpers.get_stat(act.stdout, 'SMALL', TEST_METRIC)
    assert pages == 0
    pages = gstat_helpers.get_stat(act.stdout, 'LARGE', TEST_METRIC)
    assert pages == 0

@pytest.mark.version('>=3.0')
def test_reserved_pages(act: Action, gstat_helpers):
    # Add one record in each table to reserve 8 new pages and leave 7 of them empty.
    with act.db.connect() as con:
        con.execute_immediate(f"insert into SMALL values ('{small_test_string}');")
        con.execute_immediate(f"insert into LARGE values ('{large_test_string}');")
        con.commit()
    
    act.gstat(switches=[])
    pages = gstat_helpers.get_stat(act.stdout, 'SMALL', TEST_METRIC)
    assert pages == 7
    pages = gstat_helpers.get_stat(act.stdout, 'LARGE', TEST_METRIC)
    assert pages == 7

@pytest.mark.version('>=3.0')
def test_delete_records(act: Action, gstat_helpers):
    with act.db.connect() as con:
        con.execute_immediate(f"delete from SMALL ;")
        con.execute_immediate(f"delete from LARGE ;")
        con.commit()
    act.gfix(switches=['-sweep', act.db.dsn])
    act.reset()
    act.gstat(switches=[])
    fill = gstat_helpers.get_stat(act.stdout, 'SMALL', TEST_METRIC)
    assert fill == 0
    fill = gstat_helpers.get_stat(act.stdout, 'LARGE', TEST_METRIC)
    assert fill == 0
