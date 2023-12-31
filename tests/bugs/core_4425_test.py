#coding:utf-8

"""
ID:          issue-1551
ISSUE:       1551
TITLE:       User-collations based on UNICODE are not upgrade to newer ICU version on restore
DESCRIPTION:
  Test uses .fbk which was created on linux host and has collation with following DDL:
  create collation nums_coll for utf8 from unicode case insensitive 'NUMERIC-SORT=1';

  SHOW COLLATION on linux host did show: COLL-VERSION=49.192.5.41.

  We restore this database and try to use existing collation again.
JIRA:        CORE-4425
FBTEST:      bugs.core_4425
"""

import pytest
from firebird.qa import *

db = db_factory(from_backup='core4425.fbk')

test_script = """
    create domain dm_nums2 as varchar(20) character set utf8 collate nums_coll;
    commit;
    create table test2(s1 dm_nums2, s2 dm_nums2);
    commit;

    insert into test2 values('123qWe', '123QwE');
    insert into test2 values('1zXcvU', '1ZXcvu');
    insert into test2 values('12XcvU', '12xCVu');

    commit;
    set list on;
    select 'old table:' as msg, s1,s2,s1=s2 from test order by s1;
    select 'new table:' as msg, s1,s2,s1=s2 from test2 order by s2;
    commit;
"""

act = isql_act('db', test_script)

expected_stdout = """
    MSG                             old table:
    S1                              1zXcvU
    S2                              1ZXcvu
    <true>
    MSG                             old table:
    S1                              12XcvU
    S2                              12xCVu
    <true>
    MSG                             old table:
    S1                              123qWe
    S2                              123QwE
    <true>

    MSG                             new table:
    S1                              1zXcvU
    S2                              1ZXcvu
    <true>
    MSG                             new table:
    S1                              12XcvU
    S2                              12xCVu
    <true>
    MSG                             new table:
    S1                              123qWe
    S2                              123QwE
    <true>
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

