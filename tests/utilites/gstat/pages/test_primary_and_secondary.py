#coding:utf-8
"""
ID:          utilites.gstat.pages.primary_and_secondary
TITLE:       Check user tables metrics for table with primary and secondary pages.
DESCRIPTION: Check following metrics:
             - Data pages
             - Primary pages
             - Secondary pages
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

script_template = """
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

init_script = script_template.format(table_name='SMALL', field_type=f"char({SMALL_FIELD_WIDTH})", req_qnt=SMALL_REC_QNT, test_string=small_test_string)
init_script += script_template.format(table_name='LARGE', field_type=f"char({LARGE_FIELD_WIDTH})", req_qnt=LARGE_REC_QNT, test_string=large_test_string)

db = db_factory(page_size=PAGE_SIZE, init=init_script)
act = python_act('db')

conf = store_config('databases.conf')
new_config = temp_file('new_databases.conf')

@pytest.mark.version('>=3.0')
def test_1(act: Action, gstat_helpers, conf: ConfigManager, new_config: Path):
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

    # RDB3: empty pages are reserved for secondary pages separate from primary pages
    # RDB5: empty pages are reserved for primary and secondary pages together
    primary = DP_QNT
    secondary = DP_QNT
    if act.is_version('>=5.0'):
        empty = 8 - (primary + secondary)%8
        all_dp = primary + secondary + empty
    else:
        empty = (8 - primary%8) + (8 - secondary%8)
        all_dp = primary + secondary + empty


    # Before sweep
    act.gstat(switches=['-d'])
    stats=[]
    stats.append(gstat_helpers.get_metric(act.stdout, 'SMALL', 'Data pages'))
    stats.append(gstat_helpers.get_metric(act.stdout, 'LARGE', 'Data pages'))
    stats.append(gstat_helpers.get_metric(act.stdout, 'SMALL', 'Primary pages'))
    stats.append(gstat_helpers.get_metric(act.stdout, 'LARGE', 'Primary pages'))
    stats.append(gstat_helpers.get_metric(act.stdout, 'SMALL', 'secondary pages'))
    stats.append(gstat_helpers.get_metric(act.stdout, 'LARGE', 'secondary pages'))
    stats.append(gstat_helpers.get_metric(act.stdout, 'SMALL', 'Empty pages'))
    stats.append(gstat_helpers.get_metric(act.stdout, 'LARGE', 'Empty pages'))
    assert stats == [all_dp, all_dp, DP_QNT, DP_QNT, DP_QNT, DP_QNT, empty, empty]

    # After sweep
    act.gfix(switches=['-sweep', act.db.dsn])
    act.reset()

    empty = 8 - DP_QNT%8
    all_dp = DP_QNT + empty

    act.gstat(switches=['-d'])
    stats=[]
    stats.append(gstat_helpers.get_metric(act.stdout, 'SMALL', 'Data pages'))
    stats.append(gstat_helpers.get_metric(act.stdout, 'LARGE', 'Data pages'))
    stats.append(gstat_helpers.get_metric(act.stdout, 'SMALL', 'Primary pages'))
    stats.append(gstat_helpers.get_metric(act.stdout, 'LARGE', 'Primary pages'))
    stats.append(gstat_helpers.get_metric(act.stdout, 'SMALL', 'secondary pages'))
    stats.append(gstat_helpers.get_metric(act.stdout, 'LARGE', 'secondary pages'))
    stats.append(gstat_helpers.get_metric(act.stdout, 'SMALL', 'empty pages'))
    stats.append(gstat_helpers.get_metric(act.stdout, 'LARGE', 'empty pages'))
    assert stats == [all_dp, all_dp, DP_QNT, DP_QNT, 0, 0, empty, empty]
