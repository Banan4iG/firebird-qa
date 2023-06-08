#coding:utf-8
"""
ID:          utilites.gstat.records.record_with_versions
TITLE:       Check metrics of the table with record with many versions. 
DESCRIPTION: Check following record metrics:
             - Max versions
             - Total versions
NOTES: Add enough records in test tables so that gstat can use several threads.
"""

import pytest
from math import floor
from firebird.qa import *
from pathlib import Path

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
def test_record_with_versions(act: Action, gstat_helpers, conf: ConfigManager, new_config: Path):
    databases_conf=f"""
    gstat_total_versions = {act.db.db_path}
    {{
        GCPolicy=cooperative
    }}
    """
    new_config.write_text(databases_conf)
    conf.replace(new_config)
    
    connections = []
    for i in range(VERSIONS_QNT):
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
    
    act.gstat(switches=['-d', '-r'])
    stats = []
    for table in ('SMALL', 'LARGE'):
        for metric in ('max versions', 'total versions'):
            stats.append(gstat_helpers.get_metric(act.stdout, table, metric))
    assert stats == [VERSIONS_QNT, VERSIONS_QNT, VERSIONS_QNT, VERSIONS_QNT]
