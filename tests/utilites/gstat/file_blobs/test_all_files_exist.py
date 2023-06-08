#coding:utf-8
"""
ID:          utilites.gstat.file_blobs.all_files_exist
TITLE:       Check file blobs statistics.
DESCRIPTION: All files exist
NOTES:
"""

import pytest
from firebird.qa import *
from pathlib import Path

NEW_BLOB_QNT = 100
NEW_BLOB_SIZE = 200
NEW_BLOB_DATA = 'A'*NEW_BLOB_SIZE
OLD_BLOB_QNT = 50
OLD_BLOB_SIZE = 100
OLD_BLOB_DATA = 'B'*OLD_BLOB_SIZE

init_script = """
    create table NEW(FILES varchar(200));
    create table OLD(FILES varchar(200));
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
act = python_act('db', substitutions=[('NEW \\(.*','NEW'), ('OLD \\(.*','OLD')])

expected_stdout = f"""
NEW (128)
    'FILES' field: 
        Links' count: {NEW_BLOB_QNT}
        Missing files' count: 0
        Unresolved links' count: 0
        Blob files' size: {NEW_BLOB_QNT*NEW_BLOB_SIZE} bytes

OLD (129)
    'FILES' field: 
        Links' count: {OLD_BLOB_QNT}
        Missing files' count: 0
        Unresolved links' count: 0
        Blob files' size: {OLD_BLOB_QNT*OLD_BLOB_SIZE} bytes

Total links' count: {NEW_BLOB_QNT+OLD_BLOB_QNT}
Total missing files' count: 0
Total unresolved links' count: 0
Total blob files' size: {NEW_BLOB_QNT*NEW_BLOB_SIZE + OLD_BLOB_QNT*OLD_BLOB_SIZE} bytes
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

    test_script = insert_script.format(table='NEW', blob_qnt=NEW_BLOB_QNT, blob_data=NEW_BLOB_DATA)
    test_script += insert_script.format(table='OLD', blob_qnt=OLD_BLOB_QNT, blob_data=OLD_BLOB_DATA)

    act.isql(switches=['-q'], input=test_script)
    act.reset()

    act.expected_stdout = expected_stdout
    act.gstat(switches=['-b', 'NEW.FILES', 'OLD.FILES'])
    stats = gstat_helpers.get_full_stat(act.stdout, 'Analyzing file blobs')
    act.stdout = stats
    assert act.clean_stdout == act.clean_expected_stdout
