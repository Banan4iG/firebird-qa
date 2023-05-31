#coding:utf-8
"""
ID:          utilites.gstat.index.compression ratio
TITLE:       Check the compression ratio of uncompressed data to compressed average key length. 
DESCRIPTION: 
NOTES:
"""

import pytest
from firebird.qa import *
from pathlib import Path
import string

METRIC = 'compression ratio'

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
    ratio = gstat_helpers.get_stat(act.stdout, 'TEST', METRIC)
    assert ratio == 0

@pytest.mark.version('>=3.0')
def test_without_prefix(act: Action, gstat_helpers):   
    act.isql(switches=[], input=(init_script+create_index))
    act.reset()
    act.gstat(switches=['-i'])
    ratio = gstat_helpers.get_stat(act.stdout, 'TEST', METRIC)
    assert ratio == 0.98

@pytest.mark.version('>=3.0')
def test_with_prefix(act: Action, gstat_helpers):
    act.isql(switches=[], input=(init_script*2+create_index))
    act.reset()
    act.gstat(switches=['-i'])
    ratio = gstat_helpers.get_stat(act.stdout, 'TEST', METRIC)
    assert ratio == 1.91
