#coding:utf-8
"""
ID:          utilites.gstat.records.uncommitted_records
TITLE:       Check record metrics of the table with uncommitted records. 
DESCRIPTION: Check following record metrics:
             - Total records
             - Average record length
             - Total versions
NOTES:
"""

import pytest
from firebird.qa import *

TEST_METRIC = ''

PAGE_SIZE = 4096
SMALL_FIELD_WIDTH = 1500

substring='0123456789'
length = len(substring)
small_test_string=substring*(SMALL_FIELD_WIDTH//length)+substring[:SMALL_FIELD_WIDTH%length]

db = db_factory(page_size=PAGE_SIZE)
act = python_act('db')

@pytest.mark.version('>=3.0')
def test_uncommited_records(act: Action, gstat_helpers):       
    with act.db.connect() as con:
        con.execute_immediate(f"create table TEST(str char(1500));")
        con.commit()
        con.execute_immediate(f"insert into TEST values('{small_test_string}');")
    
        act.gstat(switches=['-d', '-r'])
        length = gstat_helpers.get_metric(act.stdout, 'TEST', 'Average record length')
        assert length == 0
        records = gstat_helpers.get_metric(act.stdout, 'TEST', 'total records')
        assert records == 0
        versions = gstat_helpers.get_metric(act.stdout, 'TEST', 'total versions')
        assert versions == 0
        
