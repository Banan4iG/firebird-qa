#coding:utf-8
"""
ID:          utilites.gstat.records.empty_table
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
TEST (128)
    Primary pointer page: 228, Index root page: 229
    Total formats: 1, used formats: 0
    Average record length: 0.00, total records: 0
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
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
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action, gstat_helpers):
    act.expected_stdout = expected_stdout
    act.gstat(switches=['-d', '-r'])
    stats = gstat_helpers.get_full_stat(act.stdout, 'Analyzing database pages')
    act.stdout = stats
    assert act.clean_stdout == act.clean_expected_stdout
