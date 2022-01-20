#coding:utf-8

"""
ID:          issue-1595
ISSUE:       1595
TITLE:       Expression index based on computed fields
DESCRIPTION: Index based on COMPUTED-BY column must be taken in account by optimizer.
JIRA:        CORE-1173
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    create sequence g;
    recreate table test (
      fcode integer not null,
      fdate date not null,
      ftime time not null,
      fcomp computed by (fdate+ftime),
      constraint test_pk primary key (fcode)
    );

    insert into test(fcode, fdate, ftime)
    select gen_id(g,1), dateadd( gen_id(g,1) day to cast('01.01.2010' as date) ), dateadd( gen_id(g,1) second to cast('00:00:00' as time) ) from rdb$types rows 200;
    commit;

    -- #########################################################################

    -- Index on COMPUTED BY field, ascending:
    create index test_on_computed_field_asc on test computed by (fcomp);
    commit;

    set plan on;

    select * from test where fcomp>'now' rows 0;
    commit;

    drop index test_on_computed_field_asc;
    commit;

    -- COMPUTED-BY index with expression equal to computed-by column, ascending:
    create index test_fdate_ftime_asc on test computed by (fdate+ftime);
    select * from test where fcomp>'now' rows 0;
    commit;

    drop index test_fdate_ftime_asc;
    commit;

    -- #########################################################################

    -- Index on COMPUTED BY field, descending:
    create descending index test_on_computed_field_dec on test computed by (fcomp);
    commit;

    set plan on;

    select * from test where fcomp>'now' rows 0;
    commit;

    drop index test_on_computed_field_dec;
    commit;

    -- COMPUTED-BY index with expression equal to computed-by column, decending:
    create descending index test_fdate_ftime_dec on test computed by (fdate+ftime);
    select * from test where fcomp>'now' rows 0;
    commit;

    drop index test_fdate_ftime_dec;
    commit;

    set plan off;
"""

act = isql_act('db', test_script)

expected_stdout = """
    PLAN (TEST INDEX (TEST_ON_COMPUTED_FIELD_ASC))
    PLAN (TEST INDEX (TEST_FDATE_FTIME_ASC))
    PLAN (TEST INDEX (TEST_ON_COMPUTED_FIELD_DEC))
    PLAN (TEST INDEX (TEST_FDATE_FTIME_DEC))
"""

@pytest.mark.version('>=3')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

