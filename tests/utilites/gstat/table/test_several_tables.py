#coding:utf-8
"""
ID:          utilites.gstat.table.several_tables
TITLE:       Test table key with several tables as argument
DESCRIPTION: 
NOTES:
"""

import pytest
from firebird.qa import *

PAGE_SIZE = 8192

init_script = """
    create table T1(STR CHAR(1500));
    commit;
    create INDEX IDX_T1 on T1(STR);
    commit;
    create table T2(STR CHAR(1500));
    commit;
    create INDEX IDX_T2 on T2(STR);
    commit;
    create table T3(STR CHAR(1500));
    commit;
    create INDEX IDX_T3 on T3(STR);
    commit;
"""

db = db_factory(page_size=PAGE_SIZE, init = init_script)
# Dont check different page numbers to get RDB version compatibility
act = python_act('db', substitutions=[('TEST \\(.*','TEST'), ('page: \\d+', 'page:')])

expected_stdout = """
T2 (129)
    Primary pointer page: 234, Index root page: 235
    Pointer pages: 1, data page slots: 0
    Data pages: 0, average fill: 0%
    Primary pages: 0, secondary pages: 0, swept pages: 0
    Empty pages: 0, full pages: 0
    Fill distribution:
	 0 - 19% = 0
	20 - 39% = 0
	40 - 59% = 0
	60 - 79% = 0
	80 - 99% = 0

    Index IDX_T2 (0)
	Root page: 236, depth: 1, leaf buckets: 1, nodes: 0
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

T3 (130)
    Primary pointer page: 237, Index root page: 238
    Pointer pages: 1, data page slots: 0
    Data pages: 0, average fill: 0%
    Primary pages: 0, secondary pages: 0, swept pages: 0
    Empty pages: 0, full pages: 0
    Fill distribution:
	 0 - 19% = 0
	20 - 39% = 0
	40 - 59% = 0
	60 - 79% = 0
	80 - 99% = 0

    Index IDX_T3 (0)
	Root page: 239, depth: 1, leaf buckets: 1, nodes: 0
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
    act.gstat(switches=['-t', 'T2', 'T3'])
    stats = gstat_helpers.get_full_stat(act.stdout, 'Analyzing database pages')
    act.stdout = stats
    assert act.clean_stdout == act.clean_expected_stdout