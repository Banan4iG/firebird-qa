#coding:utf-8
"""
ID:          utilites.gstat.records.blobs
TITLE:       Check user tables blobs statistics. 
DESCRIPTION: 
NOTES:  Add enough blobs in test tables so that gstat can use several threads.
        Blob with level 2
        Blob page pointer size = 4 bytes (32 bits)
        One secondary page may contain approximately PAGE_SIZE/4 blob pointers
        so blob size must be greater than PAGE_SIZE*PAGE_SIZE/4.
        Blob size is 4 GB for page size 4096 so its testing is meaningless.
"""

import pytest
from firebird.qa import *
from pathlib import Path

PAGE_SIZE = 4096
SMALL_FIELD_WIDTH = 1500
LARGE_FIELD_WIDTH = 5500
BLOB_QNT = 8000

substring='0123456789'
length = len(substring)
small_test_string=substring*(SMALL_FIELD_WIDTH//length)+substring[:SMALL_FIELD_WIDTH%length]
large_test_string=substring*(LARGE_FIELD_WIDTH//length)+substring[:LARGE_FIELD_WIDTH%length]

init_script_template = """
    create table {table_name}(str blob);
    commit;

    set term ^;
    execute block as
        declare variable i integer;
    begin
        i = {blob_qnt};
        while (i > 0) do
        begin
            insert into {table_name} values ('{test_string}');
            i = i - 1;
        end
    end^

    set term ;^
    commit;
"""

init_script = init_script_template.format(table_name='LARGE_BLOBS', blob_qnt=BLOB_QNT, test_string=large_test_string)

db = db_factory(page_size=PAGE_SIZE)

act = python_act('db')

@pytest.mark.version('>=3.0')
def test_level_0(act: Action, gstat_helpers):
    init_script = init_script_template.format(table_name='SMALL', blob_qnt=BLOB_QNT, test_string=small_test_string)   
    act.isql(switches=[], input=init_script)
      
    act.gstat(switches=['-d', '-r'])
    blobs = gstat_helpers.get_metric(act.stdout, 'SMALL', 'Blobs')
    assert blobs == BLOB_QNT
    length = gstat_helpers.get_metric(act.stdout, 'SMALL', 'total length')
    assert length == BLOB_QNT*SMALL_FIELD_WIDTH
    pages = gstat_helpers.get_metric(act.stdout, 'SMALL', 'blob pages')
    assert pages == 0
    level_0 = gstat_helpers.get_metric(act.stdout, 'SMALL', 'Level 0')
    assert level_0 == BLOB_QNT
    # Other levels
    level_1 = gstat_helpers.get_metric(act.stdout, 'SMALL', 'Level 1')
    assert level_1 == 0
    level_2 = gstat_helpers.get_metric(act.stdout, 'SMALL', 'Level 2')
    assert level_2 == 0

@pytest.mark.version('>=3.0')
def test_level_1(act: Action, gstat_helpers):
    init_script = init_script_template.format(table_name='LARGE', blob_qnt=BLOB_QNT, test_string=large_test_string)   
    act.isql(switches=[], input=init_script)

    act.gstat(switches=['-d', '-r'])
    blobs = gstat_helpers.get_metric(act.stdout, 'LARGE', 'Blobs')
    assert blobs == BLOB_QNT
    length = gstat_helpers.get_metric(act.stdout, 'LARGE', 'total length')
    assert length == BLOB_QNT*LARGE_FIELD_WIDTH
    pages = gstat_helpers.get_metric(act.stdout, 'LARGE', 'blob pages')
    assert pages == BLOB_QNT*2
    level_1 = gstat_helpers.get_metric(act.stdout, 'LARGE', 'Level 1')
    assert level_1 == BLOB_QNT
    # Other levels
    level_0 = gstat_helpers.get_metric(act.stdout, 'LARGE', 'Level 0')
    assert level_0 == 0
    level_2 = gstat_helpers.get_metric(act.stdout, 'LARGE', 'Level 2')
    assert level_2 == 0
