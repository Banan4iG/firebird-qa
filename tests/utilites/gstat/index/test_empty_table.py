#coding:utf-8
"""
ID:          utilites.gstat.index.empty_table
TITLE:       Check statistics for an empty table
DESCRIPTION: 
NOTES:
"""

import pytest
from firebird.qa import *

init_script = """
    create table TEST(STR CHAR(1500));
    commit;
    create INDEX IDX_TEST on TEST(STR);
    commit;
"""

db = db_factory(init = init_script)
# Dont check different page numbers to get RDB version compatibility
act = python_act('db', substitutions=[('TEST \\(.*','TEST'), ('page: \\d+', 'page:')])

expected_stdout = """
    Index IDX_TEST (0)
	Root page: 232, depth: 1, leaf buckets: 1, nodes: 0
	Average node length: 0.00, total dup: 0, max dup: 0
	Average key length: 0.00, compression ratio: 0.00
	Average prefix length: 0.00, average data length: 0.00
	Clustering factor: 0, ratio: 0.00
	Fill distribution:
	     0 - 19% = 1
	    20 - 39% = 0
	    40 - 59% = 0
	    60 - 79% = 0
	    80 - 99% = 0
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action, gstat_helpers):
    act.expected_stdout = expected_stdout
    act.gstat(switches=['-i'])
    stats = gstat_helpers.get_full_stat(act.stdout, 'TEST')
    act.stdout = stats
    assert act.clean_stdout == act.clean_expected_stdout
