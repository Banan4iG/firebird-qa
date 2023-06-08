#coding:utf-8
"""
ID:          utilites.gstat.all_stats
TITLE:       Check gstat -a key.
DESCRIPTION: Compare gstat output with -a key and without it. Outputs must be equal. 
			 Also using keys -d and -i together should give the same output.
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
act = python_act('db', substitutions=[('TEST \\(.*','TEST')])

@pytest.mark.version('>=3.0')
def test_1(act: Action, gstat_helpers):
    act.gstat(switches=[])
    without_keys = gstat_helpers.get_full_stat(act.stdout, 'Analyzing database pages')
    act.gstat(switches=['-a'])
    all_key = gstat_helpers.get_full_stat(act.stdout, 'Analyzing database pages')
    assert without_keys == all_key
    act.gstat(switches=['-d', '-i'])
    data_index_keys = gstat_helpers.get_full_stat(act.stdout, 'Analyzing database pages')
    assert all_key == data_index_keys
    