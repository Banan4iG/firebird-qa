#coding:utf-8
"""
ID:          utilites.gstat.file_blobs.several_keys
TITLE:       Check file blobs statistics.
DESCRIPTION: Specify several blob keys
NOTES:
"""

import pytest
from firebird.qa import *
from pathlib import Path

BLOB_QNT = 10
BLOB_SIZE = 10
BLOB_DATA = 'A'*BLOB_SIZE

init_script = """
    create table FIRST_T(FILES varchar(200));
    create table SECOND_T(FILES varchar(200));
    create table THIRD_T(FILES varchar(200));
    commit;
"""

insert_script = """
    set term ^;
    execute block as
        declare variable i integer;
        declare variable filename char(20);
    begin
        i = {blob_qnt};
        while (i > 0) do
        begin
            filename = 'test_blob_' || cast(i as varchar(5)) || '.txt';
            insert into {table}(FILES) select CREATE_FILE('blobs_dir', :filename, cast('{blob_data}' as blob)) from rdb$database;
            i = i - 1;
        end
    end^

    set term ;^
    commit;
"""

db = db_factory(init = init_script)
act = python_act('db', substitutions=[('FIRST_T \\(.*','FIRST_T'), ('SECOND_T \\(.*','SECOND_T'), ('THIRD_T \\(.*','THIRD_T')])

expected_stdout = f"""
FIRST_T (128)
    'FILES' field: 
        Links' count: {BLOB_QNT}
        Missing files' count: 0
        Unresolved links' count: 0
        Blob files' size: {BLOB_QNT*BLOB_SIZE} bytes

SECOND_T (129)
    'FILES' field: 
        Links' count: {BLOB_QNT}
        Missing files' count: 0
        Unresolved links' count: 0
        Blob files' size: {BLOB_QNT*BLOB_SIZE} bytes

THIRD_T (129)
    'FILES' field: 
        Links' count: {BLOB_QNT}
        Missing files' count: 0
        Unresolved links' count: 0
        Blob files' size: {BLOB_QNT*BLOB_SIZE} bytes

Total links' count: {BLOB_QNT*3}
Total missing files' count: 0
Total unresolved links' count: 0
Total blob files' size: {BLOB_QNT*BLOB_SIZE*3} bytes
"""

conf = store_config('directories.conf')
new_config = temp_file('new_directories.conf')

@pytest.mark.version('>=3.0')
def test_1(act: Action, gstat_helpers, conf: ConfigManager, new_config: Path, tmp_path: Path):   
    test_dir = tmp_path / 'blobs_dir'
    test_dir.mkdir()

    directories_conf=f"""
    database
    {{
        blobs_dir = {test_dir.resolve()}
    }}
    """

    new_config.write_text(directories_conf)
    conf.replace(new_config)

    test_script = insert_script.format(table='FIRST_T', blob_qnt=BLOB_QNT, blob_data=BLOB_DATA)
    test_script += insert_script.format(table='SECOND_T', blob_qnt=BLOB_QNT, blob_data=BLOB_DATA)
    test_script += insert_script.format(table='THIRD_T', blob_qnt=BLOB_QNT, blob_data=BLOB_DATA)

    act.isql(switches=['-q'], input=test_script)
    act.reset()

    act.expected_stdout = expected_stdout
    act.gstat(switches=['-b', 'FIRST_T.FILES', '-b', 'SECOND_T.FILES', '-b', 'THIRD_T.FILES'])
    stats = gstat_helpers.get_full_stat(act.stdout, 'Analyzing file blobs')
    act.stdout = stats
    assert act.clean_stdout == act.clean_expected_stdout
