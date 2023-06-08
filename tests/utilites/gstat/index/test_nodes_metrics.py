#coding:utf-8
"""
ID:          utilites.gstat.index.nodes_metrics
TITLE:       Check metrics for index nodes. 
DESCRIPTION: Check following index metrics:
             - Depth
             - Leaf buckets
             - Nodes
             - Average node length
NOTES:
"""

import pytest
from firebird.qa import *
from pathlib import Path
import string

PAGE_SIZE = 4096
FIELD_WIDTH = 100

init_script = f"""
    create table TEST (id int, str char({FIELD_WIDTH}));
    commit;
"""

id = 0

for lower in string.ascii_lowercase:
    for upper in string.ascii_lowercase:
        for digit in string.digits: 
            temp_string = (lower + upper + digit)*30
            temp_script = f"""
                insert into TEST values({id}, '{temp_string}');
            """
            init_script += temp_script
            id += 1
init_script += """
    commit;
    create INDEX IDX_TEST on TEST(STR);
    commit;
"""   

db = db_factory(page_size=PAGE_SIZE, init=init_script)
act = python_act('db')

@pytest.mark.version('>=3.0')
def test_1(act: Action, gstat_helpers):
    act.gstat(switches=['-i'])
    depth = gstat_helpers.get_metric(act.stdout, 'TEST', 'depth')
    assert depth == 3
    leafs = gstat_helpers.get_metric(act.stdout, 'TEST', 'leaf buckets')
    assert leafs == 161
    nodes = gstat_helpers.get_metric(act.stdout, 'TEST', 'nodes')
    assert nodes == 6760
    length = gstat_helpers.get_metric(act.stdout, 'TEST', 'Average node length')
    assert length == 93.07
