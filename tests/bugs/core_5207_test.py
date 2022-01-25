#coding:utf-8

"""
ID:          issue-5488
ISSUE:       5488
TITLE:       ISQL -X may generate invalid GRANT USAGE statements for domains
DESCRIPTION:
  Test uses .fbk which was prepared on FB 2.5 (source .fdb contains single domain).
  After .fbk extration we start restore from it and extract metadata to log.
  Then we search metadata log for phrase 'GRANT USAGE ON DOMAIN' - it should NOT present there.
  Afterall, we try to apply extracted metadata to temp database (that was created auto by fbtest).
JIRA:        CORE-5207
"""

import pytest
import zipfile
from pathlib import Path
from firebird.qa import *

db = db_factory()

act = python_act('db')

fbk_file = temp_file('tmp_core_5207.fbk')
fdb_file = temp_file('tmp_core_5207.fdb')

@pytest.mark.version('>=3.0')
def test_1(act: Action, fbk_file: Path, fdb_file: Path, capsys):
    zipped_fbk_file = zipfile.Path(act.files_dir / 'core_5207.zip', at='core_5207.fbk')
    fbk_file.write_bytes(zipped_fbk_file.read_bytes())
    with act.connect_server() as srv:
        srv.database.restore(database=fdb_file, backup=fbk_file)
        srv.wait()
    act.isql(switches=['-x', str(fdb_file)], connect_db=False)
    metadata = act.stdout
    # Check metadata
    for line in metadata.splitlines():
        if 'GRANT USAGE ON DOMAIN' in line:
            pytest.fail(f'WRONG GRANT: {line}')
    # Apply metadata to main test database
    act.reset()
    act.isql(switches=[], input=metadata)
    assert act.clean_stdout == act.clean_expected_stdout
