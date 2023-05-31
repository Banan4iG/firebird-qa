#coding:utf-8
"""
ID:          utilites.gstat.index.average_key_length
TITLE:       Check the average index key length. 
DESCRIPTION: 
NOTES:
    Key length includes from 1 to 5 bytes (length of prefix or data length value) in addition to the length of data and prefix.
    Even if prefix length is zero, 1 byte is added to the average key length.
"""

import pytest
from firebird.qa import *
from pathlib import Path
import string

METRIC = 'Average key length'

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
    length = gstat_helpers.get_stat(act.stdout, 'TEST', METRIC)
    assert length == 0

@pytest.mark.version('>=3.0')
def test_without_prefix(act: Action, gstat_helpers):   
    # Insert only unique records to get zero value of average prefix
    act.isql(switches=[], input=(init_script+create_index))
    act.reset()
    # One byte for zero prefix and one byte for data length
    act.gstat(switches=['-i'])
    length = gstat_helpers.get_stat(act.stdout, 'TEST', METRIC)
    assert length == 92

@pytest.mark.version('>=3.0')
def test_with_prefix(act: Action, gstat_helpers):
    # Insert each records twice to get the same values of average prefix and average data length
    act.isql(switches=[], input=(init_script*2+create_index))
    act.reset()
    # Only one byte for prefix length must be added.
    # So average length of additional bytes for prefix and data is (2+1)/2=1.5.
    act.gstat(switches=['-i'])
    length = gstat_helpers.get_stat(act.stdout, 'TEST', METRIC)
    assert length == 46.5
