#coding:utf-8
"""
ID:          utilites.gstat.records.deleted_records
TITLE:       Check records metrics after deleting records. 
DESCRIPTION: DESCRIPTION: Check following record metrics:
             - Total records
             - Average record length
             - Total versions
             - Max versions
NOTES: Add enough records in test tables so that gstat can use several threads.
"""

import pytest
from math import floor
from firebird.qa import *
from pathlib import Path

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
def test_1(act: Action, gstat_helpers, conf: ConfigManager, new_config: Path):

    deleted_rec_length = 9 if act.is_version('>=5.0') else 0

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

    # Before sweep
    act.gstat(switches=['-d', '-r'])
    stats=[]
    for table in ('SMALL', 'LARGE'):
        for metric in ('Average record length', 'total records', 'max versions', 'total versions'):
            stats.append(gstat_helpers.get_metric(act.stdout, table, metric))
    assert stats == [deleted_rec_length, SMALL_REC_QNT, 1, SMALL_REC_QNT, deleted_rec_length, LARGE_REC_QNT, 1, LARGE_REC_QNT]

    # After sweep
    act.gfix(switches=['-sweep', act.db.dsn])
    act.reset()

    act.gstat(switches=['-d', '-r'])
    stats=[]
    for table in ('SMALL', 'LARGE'):
        for metric in ('Average record length', 'total records', 'max versions', 'total versions'):
            stats.append(gstat_helpers.get_metric(act.stdout, table, metric))
    assert stats == [0, 0, 0, 0, 0, 0, 0, 0]
