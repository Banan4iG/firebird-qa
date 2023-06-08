#coding:utf-8
"""
ID:          utilites.gstat.parallel.pages
TITLE:       Check user tables data page metrics with parallel key. 
DESCRIPTION:
NOTES:       Add enough records in test tables so that gstat can use several threads.
             MaxParallelWorkers value must be set greater than 4 before running the test.
"""

import pytest
from math import floor, ceil
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

PP_QNT = ceil(DP_QNT/808)
EMPTY_QNT = 8 - DP_QNT%8

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

db = db_factory(page_size=PAGE_SIZE)
act = python_act('db', substitutions=[
    ('SMALL \\(.*','SMALL'), 
    ('LARGE \\(.*','LARGE'), 
    ('Primary pointer page: \\d+','Primary pointer page:'),
    ('Index root page: \\d+','Index root page:')
    ])  

stdout_template = """
LARGE (129)
    Primary pointer page: 2036, Index root page: 2037
    Pointer pages: {pp}, data page slots: {dp}
    Data pages: {dp}, average fill: {large_af}%
    Primary pages: {pr}, secondary pages: 0, swept pages: 0
    Empty pages: {ep}, full pages: {fp}
    Fill distribution:
	 0 - 19% = {ep}
	20 - 39% = 0
	40 - 59% = 0
	60 - 79% = {pr}
	80 - 99% = 0

SMALL (128)
    Primary pointer page: 228, Index root page: 229
    Pointer pages: {pp}, data page slots: {dp}
    Data pages: {dp}, average fill: 75%
    Primary pages: {dp}, secondary pages: 0, swept pages: 0
    Empty pages: {ep}, full pages: {fp}
    Fill distribution:
	 0 - 19% = {ep}
	20 - 39% = 0
	40 - 59% = 0
	60 - 79% = {pr}
	80 - 99% = 0
"""

conf = store_config('databases.conf')
new_config = temp_file('new_databases.conf')

@pytest.mark.version('>=5.0')
def test_1(act: Action, gstat_helpers, conf: ConfigManager, new_config: Path):
    databases_conf=f"""
        gstat_avg_length = {act.db.db_path}
        {{
            GCPolicy=cooperative
        }}
    """
    new_config.write_text(databases_conf)
    conf.replace(new_config)

    # For RDB3 data previosly divided into blocks of 127 bytes so we get different values.
    large_af = 72 if act.is_version('>=5.0') else 75

    # Init test db after a configuration replacement to ensure that you get zero swept pages
    act.isql(switches=['-q'], input=init_script)
    act.reset()

    act.expected_stdout = stdout_template.format(pp=PP_QNT, dp=(DP_QNT+EMPTY_QNT), pr=DP_QNT, ep=EMPTY_QNT, fp=(DP_QNT-1), large_af=large_af)
    act.gstat(switches=['-d', '-par', '4'])
    stats = gstat_helpers.get_full_stat(act.stdout, 'Analyzing database pages')
    act.stdout = stats
    assert act.clean_stdout == act.clean_expected_stdout
