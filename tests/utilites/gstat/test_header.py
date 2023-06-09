#coding:utf-8
"""
ID:          utilites.gstat.header
TITLE:       Check gstat header for empty db.
DESCRIPTION:
NOTES:
"""

import pytest
from firebird.qa import *
import os

db = db_factory(filename='empty.fdb',page_size=8192)
act = python_act('db', substitutions=[
    ('Database ".*empty.fdb"','Database "empty.fdb"'), 
    ('execution time.*', 'Gstat execution time'),
    ('Generation\\s+.*', 'Generation'),
    ('Creation date.*', 'Creation date'),
    ('completion time.*', 'Creation date'),
    ('HW=.*OS', 'OS'),
    ('Next attachment ID.*', 'Next attachment ID'),
    ('Database GUID:\\s+\\{.*}', 'Database GUID: {}')])

expected_stdout = """
Database "empty.fdb"
Gstat execution time Thu Jun  1 12:47:36 2023

Database header page information:
	Flags			0
	Generation		6
	System Change Number	0
	Page size		8192
	Server			RedDatabase
	ODS version		{ods}
	Oldest transaction	1
	Oldest active		1
	Oldest snapshot		1
	Next transaction	1
	Autosweep gap		0
	Sequence number		0
	Next attachment ID	6
	Implementation		HW=AMD/Intel/x64 little-endian OS={os} CC=gcc
	Shadow count		0
	Page buffers		0
	Next header page	0
	Database dialect	3
	Creation date		Jun 1, 2023 9:47:36
	Attributes		

    Variable header data:
	Database GUID:	{{}}
	*END*
Gstat completion time Thu Jun  1 12:47:36 2023
"""

@pytest.mark.version('>=3.0')
def test_empty_db(act: Action, gstat_helpers):
    os_name = 'Windows' if os.name == 'nt' else 'Linux'
    ods = '13.1' if act.is_version('>=5.0') else '12.3'
    expected_result = expected_stdout.format(ods=ods, os=os_name)
    act.expected_stdout = expected_result
    act.gstat(switches=['-h'])
    assert act.clean_stdout == act.clean_expected_stdout
