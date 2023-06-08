#coding:utf-8
"""
ID:          utilites.gstat.pages.blob_headers
TITLE:       Check user tables metrics for table with blobs.
DESCRIPTION: Check following metrics:
             - Primary pages
             - Secondary pages
NOTES: Add enough records in test tables so that gstat can use several threads.
"""

import pytest
from math import floor
from firebird.qa import *

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

init_script = script_template.format(table_name='SMALL_BLOB', field_type=f"blob", req_qnt=SMALL_REC_QNT, test_string=small_test_string)
init_script += script_template.format(table_name='LARGE_BLOB', field_type=f"blob", req_qnt=LARGE_REC_QNT, test_string=large_test_string)

db = db_factory(page_size=PAGE_SIZE, init=init_script)
act = python_act('db')

@pytest.mark.version('>=3.0')
def test_blob_headers(act: Action, gstat_helpers):
    primary = 250 if act.is_version('>=5.0') else 214
    act.gstat(switches=['-d'])
    stats=[]
    # Data pages includes primary pages with records containing blob id and secondary pages with blob data
    stats.append(gstat_helpers.get_metric(act.stdout, 'SMALL', 'Primary pages'))
    stats.append(gstat_helpers.get_metric(act.stdout, 'LARGE', 'Primary pages'))
    stats.append(gstat_helpers.get_metric(act.stdout, 'SMALL', 'secondary pages'))
    # Only header of blob data is stored on a secondary page if data is lager than the page size.
    stats.append(gstat_helpers.get_metric(act.stdout, 'LARGE', 'secondary pages'))
    assert stats == [primary, primary, DP_QNT, 159]
