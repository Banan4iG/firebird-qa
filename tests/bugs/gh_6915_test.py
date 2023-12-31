#coding:utf-8

"""
ID:          issue-6915
ISSUE:       6915
TITLE:       Allow attribute DISABLE-COMPRESSIONS in UNICODE collations
DESCRIPTION:
  Only ability to use 'DISABLE-COMPRESSION' in attributes list is checked here.
  Performance comparison with and without this attribute will be checked in separate test.
FBTEST:      bugs.gh_6915
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    create collation coll_cs_dc
       for UTF8
       from UNICODE
       case sensitive
       'LOCALE=cs_CZ;DISABLE-COMPRESSIONS=1'
    ;

    create collation coll_ci_dc
       for UTF8
       from UNICODE
       case insensitive
       'LOCALE=cs_CZ;DISABLE-COMPRESSIONS=1'
    ;

    create collation coll_cs_dc_ns
       for UTF8
       from UNICODE
       case sensitive
       'LOCALE=cs_CZ;DISABLE-COMPRESSIONS=1;NUMERIC-SORT=1'
    ;

    create collation coll_ci_dc_ns
       for UTF8
       from UNICODE
       case insensitive
       'LOCALE=cs_CZ;DISABLE-COMPRESSIONS=1;NUMERIC-SORT=1'
    ;
"""

act = isql_act('db', test_script, substitutions=[('[ \t]+', ' ')])

@pytest.mark.version('>=4.0.1')
def test_1(act: Action):
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
