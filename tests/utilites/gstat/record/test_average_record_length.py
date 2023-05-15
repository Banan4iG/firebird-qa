#coding:utf-8
"""
ID:          utilites.gstat.record.average_record_length
TITLE:       Check user tables average record length statistics. 
DESCRIPTION: 
NOTES: Add enough records in test tables so that gstat can use several threads.
"""

import pytest
from math import floor
from firebird.qa import *
from pathlib import Path

TEST_METRIC = 'Average record length'

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

db_empty = db_factory()
db_filled = db_factory(page_size=PAGE_SIZE, init=init_script)

act = python_act('db_empty')
act2 = python_act('db_filled')

conf = store_config('databases.conf')
new_config = temp_file('new_databases.conf')

@pytest.mark.version('>=3.0')
def test_zero_records(act: Action, gstat_helpers):
    with act.db.connect() as con:
        con.execute_immediate(f"create table TEST(str varchar(10));")
        con.commit()

    act.gstat(switches=['-r'])
    length = gstat_helpers.get_stat(act.stdout, 'TEST', TEST_METRIC)
    assert length == 0

@pytest.mark.version('>=3.0')
def test_many_records(act2: Action, gstat_helpers):       
    act2.gstat(switches=['-r'])
    length = gstat_helpers.get_stat(act2.stdout, 'SMALL', TEST_METRIC)
    assert length == SMALL_FIELD_WIDTH
    length = gstat_helpers.get_stat(act2.stdout, 'LARGE', TEST_METRIC)
    assert length == LARGE_FIELD_WIDTH

@pytest.mark.version('>=3.0')
def test_delete_records_with_sweep(act2: Action, gstat_helpers):  
    with act2.db.connect() as con:
        con.execute_immediate(f"delete from SMALL;")
        con.execute_immediate(f"delete from LARGE;")
        con.commit()

    act2.gfix(switches=['-sweep', act2.db.dsn])
    act2.reset()

    act2.gstat(switches=['-r'])
    length = gstat_helpers.get_stat(act2.stdout, 'SMALL', TEST_METRIC)
    assert length == 0
    length = gstat_helpers.get_stat(act2.stdout, 'LARGE', TEST_METRIC)
    assert length == 0

@pytest.mark.version('>=3.0')
def test_delete_records_without_sweep(act2: Action, gstat_helpers, conf: ConfigManager, new_config: Path):

    databases_conf=f"""
    gstat_avg_length = {act2.db.db_path}
    {{
        GCPolicy=cooperative
    }}
    """
    new_config.write_text(databases_conf)
    conf.replace(new_config)

    with act2.db.connect() as con:
        con.execute_immediate(f"delete from SMALL;")
        con.execute_immediate(f"delete from LARGE;")
        con.commit()

    act2.gstat(switches=['-r'])
    records = gstat_helpers.get_stat(act2.stdout, 'SMALL', 'total records')
    print(records)
    print(SMALL_REC_QNT)
    length = gstat_helpers.get_stat(act2.stdout, 'SMALL', TEST_METRIC)
    assert length == 0
    length = gstat_helpers.get_stat(act2.stdout, 'LARGE', TEST_METRIC)
    assert length == 0

@pytest.mark.version('>=3.0')
def test_uncommited_records(act: Action, gstat_helpers):       
    with act.db.connect() as con:
        con.execute_immediate(f"create table TEST(str varchar(10));")
        con.commit()
        con.execute_immediate(f"insert into TEST values('Test');")
    
        act.gstat(switches=['-r'])
        length = gstat_helpers.get_stat(act.stdout, 'TEST', TEST_METRIC)
        assert length == 0
        act.reset()

        con.commit()
        act.gstat(switches=['-r'])
        length = gstat_helpers.get_stat(act.stdout, 'TEST', TEST_METRIC)
        assert length == 10
