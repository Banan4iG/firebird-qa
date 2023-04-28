#coding:utf-8

"""
ID:          RS-100024
ISSUE:       https://http://tracker.red-soft.biz/issues/100024
TITLE:       File deletion is not canceled when transaction state is rolled back
DESCRIPTION:
    1. Create two test tables with a forein key reference.
    2. Create a test file by CREATE_FILE and store the file path.
    3. In one psql block:
        - Delete the test file 
        - Try to delete records from a test table with a foreign key reference to get an error.
        This must roll back the transaction to its initial state before psql block execution.
    4. Commit transaction and check the file EXISTS.
"""

import pytest
from firebird.qa import *
from pathlib import Path

init_script = """
    create table TEST_PRIMARY(
        ID int not null primary key,
        PRIMARY_MESSAGE varchar(20)
    );
    insert into TEST_PRIMARY VALUES(1, 'Primary comment');
    commit;

    create table TEST_SECONDARY(
        ID_PRIMARY int references TEST_PRIMARY (ID),
        SECONDARY_MESSAGE VARCHAR(20)
    );
    insert into TEST_SECONDARY values(1, 'Secondary comment');
    commit;
"""

db = db_factory(init=init_script)

act = python_act('db', substitutions=[('INTEG_\\d+','INTEG_'), ('At block line.*', 'At block line')])

conf = store_config('directories.conf')
new_config = temp_file('new_directories.conf')

expected_stderr = """
    Statement failed, SQLSTATE = 23000
    violation of FOREIGN KEY constraint "INTEG_83" on table "TEST_SECONDARY"
    -Foreign key references are present for the record
    -Problematic key value is ("ID" = 1)
    -At block line
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

    new_config.write_text(directories_conf)
    conf.replace(new_config)

    with act.db.connect() as con:
        with con.cursor() as cur:
            cur.execute("select create_file('test_dir', 'test.txt', cast('Hello World!' as blob)) from rdb$database;")
            testFile = str(cur.fetch_next()[0]).strip()
            con.commit()
            assert testFile

    testFilePath = tmp_path / testFile
    assert testFilePath.exists()

    script=f"""
        set term !;
        execute block as
        begin
            delete_file('{testFile}');
            delete from TEST_PRIMARY;
        end!
        commit!
        set term ;!
    """

    act.expected_stderr = expected_stderr
    act.isql(switches=['-q'], input=script)
    assert act.clean_stderr == act.clean_expected_stderr

    assert testFilePath.exists()