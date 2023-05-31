#coding:utf-8
"""
ID:          utilites.gstat.index.leaf_buckets
TITLE:       Check number of the index leaf pages. 
DESCRIPTION: 
NOTES:
"""

import pytest
from firebird.qa import *
import string

METRIC = 'leaf buckets'

PAGE_SIZE = 4096
FIELD_WIDTH = 100

db = db_factory(page_size=PAGE_SIZE)

act = python_act('db')

@pytest.mark.version('>=3.0')
def test_no_records(act: Action, gstat_helpers):   
    with act.db.connect() as con:
        con.execute_immediate(f"create TABLE TEST(STR CHAR({FIELD_WIDTH}));")
        con.commit()
        con.execute_immediate(f"create INDEX IDX_TEST on TEST(STR);")
        con.commit()

    act.gstat(switches=['-i'])
    leafs = gstat_helpers.get_stat(act.stdout, 'TEST', METRIC)
    assert leafs == 1

@pytest.mark.version('>=3.0')
def test_with_records(act: Action, gstat_helpers):   
    init_script = f"""
        create table TEST (str char({FIELD_WIDTH}));
        commit;
    """

    for lower in string.ascii_lowercase:
        for upper in string.ascii_lowercase:
            for digit in string.digits:
                temp_string = (lower + upper + digit)*30
                temp_script = f"""
                    insert into TEST values('{temp_string}');
                """
                init_script += temp_script
    init_script += """
        commit;
        create INDEX IDX_TEST on TEST(STR);
        commit;
    """
    
    act.isql(switches=[], input=init_script)
    act.reset()

    act.gstat(switches=['-i'])
    leafs = gstat_helpers.get_stat(act.stdout, 'TEST', METRIC)
    assert leafs == 161
