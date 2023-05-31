#coding:utf-8
"""
ID:          utilites.gstat.file_blobs.without_records
TITLE:       Check file blobs statistics without records.
DESCRIPTION: 
NOTES:
"""

import pytest
from firebird.qa import *
from pathlib import Path

BLOB_SIZE = 100
BLOB_QNT = 100

init_script = """
    create table NEW(FILES varchar(200));
    create table OLD(FILES varchar(200));
    commit;
"""

db = db_factory(init = init_script)
act = python_act('db', substitutions=[('NEW \\(.*','NEW'), ('OLD \\(.*','OLD')])

expected_stdout = """
NEW (128)
    'FILES' field: 
        Links' count: 0
        Missing files' count: 0
        Unresolved links' count: 0
        Blob files' size: 0 bytes

OLD (129)
    'FILES' field: 
        Links' count: 0
        Missing files' count: 0
        Unresolved links' count: 0
        Blob files' size: 0 bytes

Total links' count: 0
Total missing files' count: 0
Total unresolved links' count: 0
Total blob files' size: 0 bytes
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action, gstat_helpers):
    act.expected_stdout = expected_stdout
    act.gstat(switches=['-b', 'NEW.FILES', 'OLD.FILES'])
    stats = gstat_helpers.get_blob_stat(act.stdout)
    act.stdout = stats
    assert act.clean_expected_stdout == act.clean_stdout
