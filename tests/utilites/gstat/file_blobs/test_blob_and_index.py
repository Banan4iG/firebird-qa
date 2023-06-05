#coding:utf-8
"""
ID:          utilites.gstat.file_blobs.blob_and_index
TITLE:       Check file blobs statistics together with index key.
DESCRIPTION: We have to specify data key if we use index key together with blob key 
NOTES:
"""

import pytest
from firebird.qa import *
from pathlib import Path

init_script = f"""
    create table TEST(STR varchar(200));
    commit;
    create INDEX IDX_TEST on TEST(STR);
    commit;
"""

db = db_factory(init = init_script)
act = python_act('db', substitutions=[('TEST \\(.*','TEST')])

expected_stdout = f"""
TEST (128)
    Primary pointer page: 228, Index root page: 229
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

Analyzing file blobs ...

TEST (128)
    'FILES' field: 
        Links' count: 0
        Missing files' count: 0
        Unresolved links' count: 0
        Blob files' size: 0 bytes

Total links' count: 0
Total missing files' count: 0
Total unresolved links' count: 0
Total blob files' size: 0 bytes
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action, gstat_helpers):   
    act.expected_stdout = expected_stdout
    act.gstat(switches=['-d', '-i', '-b', 'TEST.STR'])
    stats = gstat_helpers.get_full_stat(act.stdout, 'Analyzing database pages')
    act.stdout = stats
    assert act.clean_stdout == act.clean_expected_stdout
