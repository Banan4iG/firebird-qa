#coding:utf-8
"""
ID:          utilites.gstat.records.average_version_length
TITLE:       Check user tables average version length statistics. 
DESCRIPTION: 
NOTES: Add enough records in test tables so that gstat can use several threads.
"""

import pytest
from math import floor, ceil
from firebird.qa import *
from pathlib import Path

TEST_METRIC = 'Average version length'
VERSIONS_QNT = 10

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
    create table small(str char({SMALL_FIELD_WIDTH}));
    commit;

    create table large(str char({LARGE_FIELD_WIDTH}));
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

conf = store_config('databases.conf')
new_config = temp_file('new_databases.conf')

@pytest.mark.version('>=3.0')
def test_many_records_one_version(act: Action, gstat_helpers, conf: ConfigManager, new_config: Path):
    # For RDB3 data previosly divided into blocks of 127 bytes so we get different values.
    if act.is_version('>=5.0'):
        large_rec_len = LARGE_FIELD_WIDTH+4
        small_rec_len = SMALL_FIELD_WIDTH+4
    else:
        large_rec_len = LARGE_FIELD_WIDTH+ceil(LARGE_FIELD_WIDTH/127+4)
        #large_rec_len = 5540
        small_rec_len = SMALL_FIELD_WIDTH+ceil(SMALL_FIELD_WIDTH/127)+4
    
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
        con.execute_immediate(f"UPDATE SMALL SET STR = 'Test';")
        con.execute_immediate(f"UPDATE LARGE SET STR = 'Test';")
        con.commit()

    act.gstat(switches=['-d', '-r'])
    length = gstat_helpers.get_metric(act.stdout, 'SMALL', TEST_METRIC)
    assert length == small_rec_len
    length = gstat_helpers.get_metric(act.stdout, 'LARGE', TEST_METRIC)
    assert length == large_rec_len
