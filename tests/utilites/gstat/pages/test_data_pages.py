#coding:utf-8
"""
ID:          utilites.gstat.pages.data_pages
TITLE:       Check user tables data pages statistics. 
DESCRIPTION: 
NOTES: Add enough records in test tables so that gstat can use several threads.
"""

import pytest
from math import floor
from firebird.qa import *
from pathlib import Path

TEST_METRIC = 'Data pages'

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

db = db_factory(page_size=PAGE_SIZE)

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
def test_only_primary(act: Action, gstat_helpers):
    test_script = init_script.format(table_name='SMALL', field_type=f"char({SMALL_FIELD_WIDTH})", req_qnt=SMALL_REC_QNT, test_string=small_test_string)
    test_script += init_script.format(table_name='LARGE', field_type=f"char({LARGE_FIELD_WIDTH})", req_qnt=LARGE_REC_QNT, test_string=large_test_string)
                                     
    act.isql(switches=[], input=test_script)
    act.reset()

    act.gstat(switches=[])
    pages = gstat_helpers.get_stat(act.stdout, 'SMALL', TEST_METRIC)
    assert pages == DP_QNT
    pages = gstat_helpers.get_stat(act.stdout, 'LARGE', TEST_METRIC)
    assert pages == (DP_QNT)

@pytest.mark.version('>=3.0')
def test_primary_and_secondary(act: Action, gstat_helpers, conf: ConfigManager, new_config: Path):
    databases_conf=f"""
    gstat_total_versions = {act.db.db_path}
    {{
        GCPolicy=cooperative
    }}
    """
    new_config.write_text(databases_conf)
    conf.replace(new_config)

    test_script = init_script.format(table_name='SMALL', field_type=f"char({SMALL_FIELD_WIDTH})", req_qnt=SMALL_REC_QNT, test_string=small_test_string)
    test_script += init_script.format(table_name='LARGE', field_type=f"char({LARGE_FIELD_WIDTH})", req_qnt=LARGE_REC_QNT, test_string=large_test_string)
                                     
    act.isql(switches=[], input=test_script)
    act.reset()

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
    assert pages == (DP_QNT*2)
    pages = gstat_helpers.get_stat(act.stdout, 'LARGE', TEST_METRIC)
    assert pages == (DP_QNT*2)

@pytest.mark.version('>=3.0')
def test_blob_headers(act: Action, gstat_helpers):
    test_script = init_script.format(table_name='SMALL_BLOB', field_type=f"blob", req_qnt=SMALL_REC_QNT, test_string=small_test_string)
    test_script += init_script.format(table_name='LARGE_BLOB', field_type=f"blob", req_qnt=LARGE_REC_QNT, test_string=large_test_string)
    
    act.isql(switches=[], input=test_script)
    act.reset()

    act.gstat(switches=['-r'])
    pages = gstat_helpers.get_stat(act.stdout, 'SMALL_BLOB', TEST_METRIC)
    # Data pages includes primary pages with records containing blob id and secondary pages with blob data
    assert pages == 8256
    pages = gstat_helpers.get_stat(act.stdout, 'LARGE_BLOB', TEST_METRIC)
    # Only header of blob data is stored on a secondary page if data is lager than the page size.
    assert pages == 416
