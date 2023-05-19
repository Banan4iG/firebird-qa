#coding:utf-8
"""
ID:          utilites.gstat.record.total_versions
TITLE:       Check user tables total versions statistics. 
DESCRIPTION: 
NOTES: Add enough records in test tables so that gstat can use several threads.
        
"""

import pytest
from math import floor
from firebird.qa import *
from pathlib import Path

TEST_METRIC = 'total versions'
MAX_VERSIONS = [pytest.param(x, id=f"{x}_versions") for x in (10, 100, 1000)]

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
    create table small(id int, str varchar({SMALL_FIELD_WIDTH}));
    commit;

    create table large(id int, str varchar({LARGE_FIELD_WIDTH}));
    commit;
    
    -- Small records
    set term ^;
    execute block as
        declare variable i integer;
    begin
        i = {SMALL_REC_QNT};
        while (i > 0) do
        begin
            insert into small values (:i, '{small_test_string}');
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
            insert into large values (:i, '{large_test_string}');
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
def test_zero_versions(act: Action, gstat_helpers):       
    act.gstat(switches=['-r'])
    records = gstat_helpers.get_stat(act.stdout, 'SMALL', TEST_METRIC)
    assert records == 0
    records = gstat_helpers.get_stat(act.stdout, 'LARGE', TEST_METRIC)
    assert records == 0

@pytest.mark.parametrize("version_qnt", MAX_VERSIONS)
@pytest.mark.version('>=3.0')
def test_many_records_one_version(act: Action, gstat_helpers, version_qnt, conf: ConfigManager, new_config: Path):
    databases_conf=f"""
    gstat_total_versions = {act.db.db_path}
    {{
        GCPolicy=cooperative
    }}
    """
    new_config.write_text(databases_conf)
    conf.replace(new_config)
    
    with act.db.connect() as con:
        # Update specified number of records to get old record versions
        con.execute_immediate(f"UPDATE SMALL SET STR = 'Test' WHERE ID <= {version_qnt};")
        con.execute_immediate(f"UPDATE LARGE SET STR = 'Test' WHERE ID <= {version_qnt};")
        con.commit()

    act.gstat(switches=['-r'])
    versions = gstat_helpers.get_stat(act.stdout, 'SMALL', TEST_METRIC)
    assert versions == version_qnt
    versions = gstat_helpers.get_stat(act.stdout, 'LARGE', TEST_METRIC)
    assert versions == version_qnt

#@pytest.mark.parametrize("thread_qnt", [pytest.param(1, id="1_thread"), pytest.param(4, id="4_thread")])
@pytest.mark.parametrize("version_qnt", [pytest.param(10, id="10_versions"), pytest.param(100, id="100_versions")])
@pytest.mark.version('>=3.0')
def test_one_record_many_versions(act: Action, gstat_helpers, version_qnt, conf: ConfigManager, new_config: Path):
    databases_conf=f"""
    gstat_total_versions = {act.db.db_path}
    {{
        GCPolicy=cooperative
    }}
    """
    new_config.write_text(databases_conf)
    conf.replace(new_config)
    
    connections = []
    for i in range(version_qnt):
        with act.db.connect() as con:
            # Select updated record for each version.
            protect_con = act.db.connect()
            cur_small = protect_con.cursor()
            cur_small.execute("SELECT STR FROM SMALL WHERE ID = 1;")
            cur_large = protect_con.cursor()
            cur_large.execute("SELECT STR FROM LARGE WHERE ID = 1;")
            connections.append(protect_con)
            # Create new record version by update
            con.execute_immediate(f"UPDATE SMALL SET STR = 'Test' WHERE ID = 1;")
            con.execute_immediate(f"UPDATE LARGE SET STR = 'Test' WHERE ID = 1;")
            con.commit()
    
    for protect_con in connections:
        protect_con.close()
    
    act.gstat(switches=['-r'])
    versions = gstat_helpers.get_stat(act.stdout, 'SMALL', TEST_METRIC)
    assert versions == version_qnt
    versions = gstat_helpers.get_stat(act.stdout, 'LARGE', TEST_METRIC)
    assert versions == version_qnt

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

    act.gstat(switches=['-r'])
    versions = gstat_helpers.get_stat(act.stdout, 'SMALL', TEST_METRIC)
    assert versions == SMALL_REC_QNT
    versions = gstat_helpers.get_stat(act.stdout, 'LARGE', TEST_METRIC)
    assert versions == LARGE_REC_QNT

@pytest.mark.version('>=3.0')
def test_delete_records_with_sweep(act: Action, gstat_helpers):

    with act.db.connect() as con:
        con.execute_immediate(f"delete from SMALL;")
        con.execute_immediate(f"delete from LARGE;")
        con.commit()

    act.gfix(switches=['-sweep', act.db.dsn])
    act.reset()

    act.gstat(switches=['-r'])
    versions = gstat_helpers.get_stat(act.stdout, 'SMALL', TEST_METRIC)
    assert versions == 0
    versions = gstat_helpers.get_stat(act.stdout, 'LARGE', TEST_METRIC)
    assert versions == 0