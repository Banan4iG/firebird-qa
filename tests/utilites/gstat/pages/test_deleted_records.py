#coding:utf-8
"""
ID:          utilites.gstat.pages.deleted_records
TITLE:       Check user tables metrics after deleting records. 
DESCRIPTION: DESCRIPTION: Check following data pages metrics:
             - Primary pages
             - Empty pages
NOTES: Add enough records in test tables so that gstat can use several threads.
"""

import pytest
from math import floor
from firebird.qa import *
from pathlib import Path

PAGE_SIZE = 4096
SMALL_FIELD_WIDTH = 1500
LARGE_FIELD_WIDTH = 5500
# The number of data pages must not be a multiple of 8 to get empty pages.
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
def test_1(act: Action, gstat_helpers, conf: ConfigManager, new_config: Path):  
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

    empty_pages = 8 - DP_QNT%8

    # Before sweep
    act.gstat(switches=['-d'])
    stats=[]
    stats.append(gstat_helpers.get_metric(act.stdout, 'SMALL', 'Primary pages'))
    stats.append(gstat_helpers.get_metric(act.stdout, 'LARGE', 'Primary pages'))
    stats.append(gstat_helpers.get_metric(act.stdout, 'SMALL', 'Empty pages'))
    stats.append(gstat_helpers.get_metric(act.stdout, 'LARGE', 'Empty pages'))
    assert stats == [DP_QNT, DP_QNT, empty_pages, empty_pages]

    # After sweep
    act.gfix(switches=['-sweep', act.db.dsn])
    act.reset()

    empty_after_delete = 0 if act.is_version('>=5.0') else 8

    act.gstat(switches=['-d'])
    stats=[]
    stats.append(gstat_helpers.get_metric(act.stdout, 'SMALL', 'Primary pages'))
    stats.append(gstat_helpers.get_metric(act.stdout, 'LARGE', 'Primary pages'))
    stats.append(gstat_helpers.get_metric(act.stdout, 'SMALL', 'Empty pages'))
    stats.append(gstat_helpers.get_metric(act.stdout, 'LARGE', 'Empty pages'))
    assert stats == [0, 0, empty_after_delete, empty_after_delete]
