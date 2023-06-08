#coding:utf-8
"""
ID:          utilites.gstat.encryption
TITLE:       Check encryption status of user tables pages. 
DESCRIPTION:
NOTES:
"""

import pytest
from math import floor
from firebird.qa import *
import re

PAGE_SIZE = 8192

# Empty db without encryption
expected_stdout_rdb3 = """
Data pages: total 47, encrypted 0, non-crypted 47
Index pages: total 57, encrypted 0, non-crypted 57
Blob pages: total 0, encrypted 0, non-crypted 0
Generator pages: total 1, encrypted 0, non-crypted 1
"""

expected_stdout_rdb5 = """
Data pages: total 82, encrypted 0, non-crypted 82
Index pages: total 63, encrypted 0, non-crypted 63
Blob pages: total 0, encrypted 0, non-crypted 0
Generator pages: total 1, encrypted 0, non-crypted 1
"""

db = db_factory(page_size=PAGE_SIZE)
act = python_act('db')

@pytest.mark.version('>=3.0')
def test_without_encryption(act: Action, gstat_helpers):
    if act.is_version('>=5.0'):
        act.expected_stdout = expected_stdout_rdb5
    else:
        act.expected_stdout = expected_stdout_rdb3
    act.gstat(switches=['-e'])
    pattern = re.compile(f'^\\s+\*END.*\\n((^.*\\n)*)^Gstat completion', flags=re.M)
    result = pattern.search(act.stdout)
    if result:
        stat = result.group(1)
    else:
        raise Exception('Encryption statistics not found')
    act.stdout = stat
    assert act.clean_stdout == act.clean_expected_stdout
