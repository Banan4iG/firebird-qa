#coding:utf-8

"""
ID:          create-file-01
FBTEST:      rdbfunc.create_file_01
TITLE:       Test for function CREATE_FILE()
DESCRIPTION: Creates file in directory from directories.conf
"""

import pytest
from firebird.qa import *
from pathlib import Path

db = db_factory()

act = python_act('db', substitutions=[('test_dir/.*', 'test_dir/'), ('=+', '======')])

conf = store_config('directories.conf')
new_config = temp_file('new_directories.conf')

expected_stdout = """
CREATE_FILE
=========================
test_dir/
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action, conf: ConfigManager, new_config: Path, tmp_path: Path):
    test_dir = tmp_path / 'test_dir'
    test_dir.mkdir()

    directories_conf=f"""
    database
    {{
        test_dir = {test_dir.resolve()}
    }}
    """

    print(directories_conf)

    new_config.write_text(directories_conf)

    conf.replace(new_config)

    script="select CREATE_FILE('test_dir', 'test_file.txt', cast('Testing create_file() function' as blob)) from rdb$database;"

    act.expected_stdout = expected_stdout
    act.isql(switches=['-q'], input=script)
    assert act.clean_stdout == act.clean_expected_stdout
