#coding:utf-8
"""
ID:          utilites.gstat.index.with_prefix
TITLE:       Check average metrics for index keys with prefix. 
DESCRIPTION: Check following index metrics:
             - Average key length
             - Average prefox length
             - Average data length
             - Compression ratio
NOTES:
    Key length includes from 1 to 5 bytes (length of prefix or data length value) in addition to the length of data and prefix.
    Even if prefix length is zero, 1 byte is added to the average key length.
"""

import pytest
from firebird.qa import *
from pathlib import Path
import string

PAGE_SIZE = 4096
init_script = """
    create table TEST (id int, str char(100));
    commit;
"""

id = 0
# Insert each records twice to get the same values of average prefix and average data length
for letter in string.ascii_uppercase:
    temp_string = letter + 'A'*89
    temp_script = f"""
        insert into TEST values({id}, '{temp_string}');
        insert into TEST values({id}, '{temp_string}');
    """
    init_script += temp_script
    id += 1
init_script += """
    commit;
    create INDEX IDX_TEST on TEST(STR); 
    commit;
"""

expected_stdout = """

"""

db = db_factory(page_size=PAGE_SIZE, init=init_script)
act = python_act('db')

@pytest.mark.version('>=3.0')
def test_1(act: Action, gstat_helpers):   
    # Only one byte for prefix length must be added.
    # So average length of additional bytes for prefix and data is (2+1)/2=1.5.
    act.gstat(switches=['-i'])
    key_length = gstat_helpers.get_metric(act.stdout, 'TEST', 'Average key length')
    assert key_length == 92
    ratio = gstat_helpers.get_metric(act.stdout, 'TEST', 'compression ratio')
    assert ratio == 0.98
    prefix_length = gstat_helpers.get_metric(act.stdout, 'TEST', 'Average prefix length')
    assert prefix_length == 0
    data_length = gstat_helpers.get_metric(act.stdout, 'TEST', 'average data length')
    assert data_length == 90
