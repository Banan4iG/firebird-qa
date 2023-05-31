#coding:utf-8
"""
ID:          utilites.gstat.index.max_duplicates
TITLE:       Check max number of the index key duplicates. 
DESCRIPTION: 
NOTES:
"""

import pytest
from firebird.qa import *
from pathlib import Path
import string

METRIC = 'max dup'

PAGE_SIZE = 4096
init_table = """
    create table TEST (id int, str char(100));
    commit;
"""

init_script = ""
id = 0
for upper in string.ascii_uppercase:
    for lower in string.ascii_lowercase:
        for digit in string.digits: 
            temp_string = (upper + lower + digit)*30
            temp_script = f"""
                insert into TEST values({id}, '{temp_string}');
            """
            init_script += temp_script
            id += 1
init_script += "commit;"

db = db_factory(page_size=PAGE_SIZE, init=(init_table + init_script))
act = python_act('db')

create_index = "create INDEX IDX_TEST on TEST(STR); commit;"

@pytest.mark.version('>=3.0')
def test_no_duplicates(act: Action, gstat_helpers): 
    act.isql(switches=[], input=create_index)
    act.reset()

    act.gstat(switches=['-i'])
    duplicates = gstat_helpers.get_stat(act.stdout, 'TEST', METRIC)
    assert duplicates == 0

@pytest.mark.version('>=3.0')
def test_one_duplicate(act: Action, gstat_helpers):   
    act.isql(switches=[], input=(init_script+create_index))
    act.reset()

    act.gstat(switches=['-i'])
    duplicates = gstat_helpers.get_stat(act.stdout, 'TEST', METRIC)
    assert duplicates == 1

@pytest.mark.version('>=3.0')
def test_several_duplicates(act: Action, gstat_helpers):   
    # Add records with duplicate STR column values
    test_script = ""
    upper = 'A'
    lower = 'a'
    for digit in string.digits: 
        for cycles in range(int(digit)):
            temp_string = (upper + lower + digit)*30
            temp_script = f"""
                insert into TEST(STR) values('{temp_string}');
            """
            test_script += temp_script
    test_script += "commit;"
    
    act.isql(switches=[], input=(test_script+create_index))
    act.reset()

    act.gstat(switches=['-i'])
    duplicates = gstat_helpers.get_stat(act.stdout, 'TEST', METRIC)
    assert duplicates == 9
