#coding:utf-8
"""
ID:          utilites.gstat.parallel.index
TITLE:       Check metrics for index nodes with parallel key. 
DESCRIPTION:
NOTES:
"""

import pytest
from firebird.qa import *
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

db = db_factory(filename='par_index.fdb', page_size=PAGE_SIZE, init=init_script)
act = python_act('db', substitutions=[('TEST \\(.*','TEST'), ('File.*par_index.fdb', 'File par_index.fdb'), ('Root page: \\d+', 'Root page: ')])

expected_output = """
File par_index.fdb is the only file
TEST (128)

    Index IDX_TEST (0)
	Root page: 589, depth: 3, leaf buckets: 161, nodes: 6760
	Average node length: 93.07, total dup: 0, max dup: 0
	Average key length: 91.12, compression ratio: 0.99
	Average prefix length: 1.85, average data length: 88.15
	Clustering factor: 251, ratio: 0.04
	Fill distribution:
	     0 - 19% = 0
	    20 - 39% = 0
	    40 - 59% = 0
	    60 - 79% = 0
	    80 - 99% = 161
"""

@pytest.mark.version('>=5.0')
def test_1(act: Action, gstat_helpers):
    act.expected_stdout = expected_output
    act.gstat(switches=['-i', '-par', '4'])
    stats = gstat_helpers.get_full_stat(act.stdout, 'Database file sequence')
    act.stdout = stats
    assert act.clean_stdout == act.clean_expected_stdout
