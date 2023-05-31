#coding:utf-8
"""
ID:          utilites.gstat.pages.secondary_pages
TITLE:       Check user tables secondary pages statistics. 
DESCRIPTION: 
NOTES: Add enough records in test tables so that gstat can use several threads.
"""

import pytest
from math import floor
from firebird.qa import *
from pathlib import Path

TEST_METRIC = 'secondary pages'

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
def test_no_records_with_versions(act: Action, gstat_helpers):
    act.gstat(switches=[])
    pages = gstat_helpers.get_stat(act.stdout, 'SMALL', TEST_METRIC)
    assert pages == 0
    pages = gstat_helpers.get_stat(act.stdout, 'LARGE', TEST_METRIC)
    assert pages == 0

@pytest.mark.version('>=3.0')
def test_records_with_versions(act: Action, gstat_helpers, conf: ConfigManager, new_config: Path):
    databases_conf=f"""
    gstat_total_versions = {act.db.db_path}
    {{
        GCPolicy=cooperative
    }}
    """
    new_config.write_text(databases_conf)
    conf.replace(new_config)

    connections = []
    for table in ('SMALL', 'LARGE'):
        protect_con = act.db.connect()
        cur = protect_con.cursor()
        cur.execute(f"SELECT * FROM {table};")
        connections.append(protect_con)

    # Change data fully to exclude delta
    small_string = small_test_string.replace('0123456789', 'abcdefghij')
    large_string = small_test_string.replace('0123456789', 'abcdefghij')

    with act.db.connect() as con:
        # Create new record version by update
        con.execute_immediate(f"UPDATE SMALL SET STR = '{small_string}' ;")
        con.execute_immediate(f"UPDATE LARGE SET STR = '{large_string}' ;")
        con.commit()
    
    for protect_con in connections:
        protect_con.close()

    # Before sweep
    act.gstat(switches=['-r'])
    pages = gstat_helpers.get_stat(act.stdout, 'SMALL', TEST_METRIC)
    assert pages == DP_QNT
    pages = gstat_helpers.get_stat(act.stdout, 'LARGE', TEST_METRIC)
    assert pages == DP_QNT  

    # After sweep
    act.gfix(switches=['-sweep', act.db.dsn])
    act.reset()

    act.gstat(switches=['-r'])
    pages = gstat_helpers.get_stat(act.stdout, 'SMALL', TEST_METRIC)
    assert pages == 0
    pages = gstat_helpers.get_stat(act.stdout, 'LARGE', TEST_METRIC)
    assert pages == 0

@pytest.mark.version('>=3.0')
def test_blob_headers(act: Action, gstat_helpers):
    
    test_script = f"""
        create table small_blob(BL_DATA BLOB);
        create table large_blob(BL_DATA BLOB);

        set term ^;
        execute block as
            declare variable i integer;
        begin
            i = {SMALL_REC_QNT};
            while (i > 0) do
            begin
                insert into SMALL_BLOB values ('{small_test_string}');
                i = i - 1;
            end
        end^

        execute block as
            declare variable i integer;
        begin
            i = {LARGE_REC_QNT};
            while (i > 0) do
            begin
                insert into LARGE_BLOB values ('{large_test_string}');
                i = i - 1;
            end
        end^

        set term ;^
        commit;
    """
    act.isql(switches=[], input=test_script)
    act.reset()

    act.gstat(switches=['-r'])
    pages = gstat_helpers.get_stat(act.stdout, 'SMALL_BLOB', TEST_METRIC)
    assert pages == DP_QNT
    pages = gstat_helpers.get_stat(act.stdout, 'LARGE_BLOB', TEST_METRIC)
    # Only header of blob data is stored on a secondary page if data is lager than the page size.
    assert pages == 159
