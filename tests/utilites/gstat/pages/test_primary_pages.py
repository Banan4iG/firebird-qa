#coding:utf-8
"""
ID:          utilites.gstat.pages.primary_pages
TITLE:       Check user tables primary pages statistics. 
DESCRIPTION: 
NOTES: Add enough records in test tables so that gstat can use several threads.
"""

import pytest
from math import floor
from firebird.qa import *
from pathlib import Path

TEST_METRIC = 'Primary pages'

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

init_script = f"""
    create table small(str char({SMALL_FIELD_WIDTH}));
    commit;

    create table large(str char({LARGE_FIELD_WIDTH}));
    commit;

    set term ^;
    execute block as
        declare variable i integer;
    begin
        i = {SMALL_REC_QNT};
        while (i > 0) do
        begin
            insert into SMALL values ('{small_test_string}');
            i = i - 1;
        end
    end^

    execute block as
        declare variable i integer;
    begin
        i = {LARGE_REC_QNT};
        while (i > 0) do
        begin
            insert into LARGE values ('{large_test_string}');
            i = i - 1;
        end
    end^

    set term ;^
    commit;
"""

db = db_factory(page_size=PAGE_SIZE, init=init_script)

act = python_act('db')

conf = store_config('databases.conf')
new_config = temp_file('new_databases.conf')

@pytest.mark.version('>=3.0')
def test_no_records(act: Action, gstat_helpers):
    with act.db.connect() as con:
        con.execute_immediate(f"create table TEST(str varchar(10));")
        con.commit()

    act.gstat(switches=[])
    pages = gstat_helpers.get_stat(act.stdout, 'TEST', TEST_METRIC)
    assert pages == 0

@pytest.mark.version('>=3.0')
def test_many_records(act: Action, gstat_helpers):
    act.gstat(switches=[])
    pages = gstat_helpers.get_stat(act.stdout, 'SMALL', TEST_METRIC)
    assert pages == DP_QNT
    pages = gstat_helpers.get_stat(act.stdout, 'LARGE', TEST_METRIC)
    assert pages == DP_QNT

@pytest.mark.version('>=3.0')
def test_many_records(act: Action, gstat_helpers):
    act.gstat(switches=[])
    pages = gstat_helpers.get_stat(act.stdout, 'SMALL', TEST_METRIC)
    assert pages == DP_QNT
    pages = gstat_helpers.get_stat(act.stdout, 'LARGE', TEST_METRIC)
    assert pages == DP_QNT

@pytest.mark.version('>=3.0')
def test_uncommited_records(act: Action, gstat_helpers):       
    with act.db.connect() as con:
        con.execute_immediate(f"create table TEST(str char(10));")
        con.commit()
        con.execute_immediate(f"insert into TEST values ('Test');")
        act.gstat(switches=[])
        pages = gstat_helpers.get_stat(act.stdout, 'TEST', TEST_METRIC)
        assert pages == 0
        act.reset()

        con.commit()
        act.gstat(switches=[])
        pages = gstat_helpers.get_stat(act.stdout, 'TEST', TEST_METRIC)
        assert pages == 1

@pytest.mark.version('>=3.0')
def test_delete_records_with_sweep(act: Action, gstat_helpers):

    with act.db.connect() as con:
        con.execute_immediate(f"delete from SMALL;")
        con.execute_immediate(f"delete from LARGE;")
        con.commit()

    act.gfix(switches=['-sweep', act.db.dsn])
    act.reset()

    act.gstat(switches=[])
    pages = gstat_helpers.get_stat(act.stdout, 'SMALL', TEST_METRIC)
    assert pages == 0
    pages = gstat_helpers.get_stat(act.stdout, 'LARGE', TEST_METRIC)
    assert pages == 0

@pytest.mark.version('>=3.0')
def test_delete_records_without_sweep(act: Action, gstat_helpers, conf: ConfigManager, new_config: Path):
    databases_conf=f"""
    gstat_avg_length = {act.db.db_path}
    {{
        GCPolicy=cooperative
    }}
    """
    new_config.write_text(databases_conf)
    conf.replace(new_config)

    with act.db.connect() as con:
        con.execute_immediate(f"delete from SMALL;")
        con.execute_immediate(f"delete from LARGE;")
        con.commit()

    act.gstat(switches=[])
    pages = gstat_helpers.get_stat(act.stdout, 'SMALL', TEST_METRIC)
    assert pages == DP_QNT
    pages = gstat_helpers.get_stat(act.stdout, 'LARGE', TEST_METRIC)
    assert pages == DP_QNT
