#coding:utf-8

"""
ID:          java.esp.bugs.bug-45573
TITLE:       Server crash after external procedure execution
DESCRIPTION: 
  If external procedure uses blobs and do not close it unfreed resourses can lead
  to crash when JVM decides to finalize blob objects. fbjava uses JnaBlob implementation, so unmanaged
  code crashing server.
FBTEST:      functional.java.esp.bugs.bug_45573
"""

import pytest
from firebird.qa import *
import os

testdb = temp_file('testdb_45573.fdb')

db_1 = db_factory()

act_1 = python_act('db_1')

expected_stdout_1 = """Attempt 1
Attempt 2
Attempt 3
Attempt 4
Attempt 5
Attempt 6u
Attempt 7
Attempt 8
Attempt 9
Attempt 10
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act_1: Action, testdb, capsys):
    script = f"""
        create database 'localhost:{str(testdb)}';
        create procedure dummy(str blob default null) external name 'esp.TestProcedure.dummyBlobIn(java.sql.Blob)' engine java;
        execute procedure dummy('test');
    """
    for i in range(10):
        print('Attempt %d' % (i+1))
        if os.path.exists(testdb):
            os.unlink(testdb)
        act_1.isql(switches=['-q'], input=script, connect_db=False)
    act_1.expected_stdout = capsys.readouterr().out
    assert act_1.clean_stdout == act_1.clean_expected_stdout
