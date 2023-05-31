#coding:utf-8
"""
ID:          utilites.gstat.index.average_prefix_and_data_length
TITLE:       Check the average index prefix and data length
DESCRIPTION: 
NOTES:
"""

import pytest
from firebird.qa import *
from pathlib import Path
import string

PAGE_SIZE = 4096
create_table = """
    create table TEST (id int, str char(100));
    commit;
"""

init_script = ""
source_string = string.ascii_uppercase

id = 0
for letter in source_string:
    temp_string = letter + 'A'*89
    temp_script = f"""
        insert into TEST values({id}, '{temp_string}');
    """
    init_script += temp_script
    id += 1
init_script += "commit;"

db = db_factory(page_size=PAGE_SIZE, init=create_table)
act = python_act('db')

create_index = "create INDEX IDX_TEST on TEST(STR); commit;"

@pytest.mark.version('>=3.0')
def test_no_records(act: Action, gstat_helpers): 
    act.isql(switches=[], input=create_index)
    act.reset()

    act.gstat(switches=['-i'])
    prefix_length = gstat_helpers.get_stat(act.stdout, 'TEST', 'Average prefix length')
    assert prefix_length == 0
    data_length = gstat_helpers.get_stat(act.stdout, 'TEST', 'average data length')
    assert data_length == 0

@pytest.mark.version('>=3.0')
def test_without_prefix(act: Action, gstat_helpers):   
    act.isql(switches=[], input=(init_script+create_index))
    act.reset()
    act.gstat(switches=['-i'])
    prefix_length = gstat_helpers.get_stat(act.stdout, 'TEST', 'Average prefix length')
    assert prefix_length == 0
    data_length = gstat_helpers.get_stat(act.stdout, 'TEST', 'average data length')
    assert data_length == 90

@pytest.mark.version('>=3.0')
def test_with_prefix(act: Action, gstat_helpers):
    act.isql(switches=[], input=(init_script*2+create_index))
    act.reset()
    act.gstat(switches=['-i'])
    prefix_length = gstat_helpers.get_stat(act.stdout, 'TEST', 'Average prefix length')
    assert prefix_length == 45
    data_length = gstat_helpers.get_stat(act.stdout, 'TEST', 'average data length')
    assert data_length == 45
