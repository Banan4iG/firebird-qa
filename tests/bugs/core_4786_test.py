#coding:utf-8

"""
ID:          issue-5085
ISSUE:       5085
TITLE:       Problematic key value (when attempt to insert duplicate in PK/UK) is not shown
  where length of key >= 127 characters
DESCRIPTION:
JIRA:        CORE-4786
FBTEST:      bugs.core_4786
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    recreate table test_none(s varchar(250) character set none constraint test_cset_none_unq unique using index test_cset_none_unq);
    commit;
    insert into test_none values( rpad('', 245, '0123456789') || 'ABCDE' );
    insert into test_none values( rpad('', 245, '0123456789') || 'ABCDE');
    commit;

    recreate table test_utf8(s varchar(169) character set utf8 constraint test_cset_utf8_unq unique using index test_cset_utf8_unq);
    commit;

    -- One byte per character (not so interesting, but error message should display ALL of them, from 1st to last):
    insert into test_utf8 values( rpad('', 164, 'A')||'BCDEF' );
    insert into test_utf8 values( rpad('', 164, 'A')||'BCDEF' );

    -- Two bytes per character: character from latin-1 and letter from Serbian alphabet:
    insert into test_utf8 values( rpad('', 169, 'Á') );
    insert into test_utf8 values( rpad('', 169, 'Á') );
    insert into test_utf8 values( rpad('', 169, 'Њ') );
    insert into test_utf8 values( rpad('', 169, 'Њ') );

    -- Three bytes per character: 'euro' currency sign and mathematical 'Sigma' sign (SUM):
    insert into test_utf8 values( rpad('', 169, '€') );
    insert into test_utf8 values( rpad('', 169, '€') );
    insert into test_utf8 values( rpad('', 169, '∑') );
    insert into test_utf8 values( rpad('', 169, '∑') );

    -- Two-Three bytes_per-character combinations:
    insert into test_utf8 values( rpad('', 169, 'Á∑') );
    insert into test_utf8 values( rpad('', 169, 'ÁÁ∑') );
    insert into test_utf8 values( rpad('', 169, 'ÁÁÁ∑') );
    insert into test_utf8 values( rpad('', 169, 'ÁÁÁ∑∑') );
    insert into test_utf8 values( rpad('', 169, 'ÁÁÁÁ∑') );
    insert into test_utf8 values( rpad('', 169, 'Á∑∑') );
    insert into test_utf8 values( rpad('', 169, 'Á∑∑∑') );
    insert into test_utf8 values( rpad('', 169, 'ÁÁ∑∑∑') );
    insert into test_utf8 values( rpad('', 169, 'Á∑∑∑∑') );

    insert into test_utf8 values( rpad('', 169, 'Á∑') );
    insert into test_utf8 values( rpad('', 169, 'ÁÁ∑') );
    insert into test_utf8 values( rpad('', 169, 'ÁÁÁ∑') );
    insert into test_utf8 values( rpad('', 169, 'ÁÁÁ∑∑') );
    insert into test_utf8 values( rpad('', 169, 'ÁÁÁÁ∑') );
    insert into test_utf8 values( rpad('', 169, 'Á∑∑') );
    insert into test_utf8 values( rpad('', 169, 'Á∑∑∑') );
    insert into test_utf8 values( rpad('', 169, 'ÁÁ∑∑∑') );
    insert into test_utf8 values( rpad('', 169, 'Á∑∑∑∑') );

    -- NB: textual key representation has a limit of 249 _bytes_, so full key can be seen only for single-byte characters.
    -- Multi-byte values will be printed shorter.
"""

act = isql_act('db', test_script)

expected_stderr = """
    Statement failed, SQLSTATE = 23000
    violation of PRIMARY or UNIQUE KEY constraint "TEST_CSET_NONE_UNQ" on table "TEST_NONE"
    -Problematic key value is ("S" = '01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234ABCD...)

    Statement failed, SQLSTATE = 23000
    violation of PRIMARY or UNIQUE KEY constraint "TEST_CSET_UTF8_UNQ" on table "TEST_UTF8"
    -Problematic key value is ("S" = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABCDEF')

    Statement failed, SQLSTATE = 23000
    violation of PRIMARY or UNIQUE KEY constraint "TEST_CSET_UTF8_UNQ" on table "TEST_UTF8"
    -Problematic key value is ("S" = 'ÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁ...)

    Statement failed, SQLSTATE = 23000
    violation of PRIMARY or UNIQUE KEY constraint "TEST_CSET_UTF8_UNQ" on table "TEST_UTF8"
    -Problematic key value is ("S" = 'ЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊЊ...)

    Statement failed, SQLSTATE = 23000
    violation of PRIMARY or UNIQUE KEY constraint "TEST_CSET_UTF8_UNQ" on table "TEST_UTF8"
    -Problematic key value is ("S" = '€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€...)

    Statement failed, SQLSTATE = 23000
    violation of PRIMARY or UNIQUE KEY constraint "TEST_CSET_UTF8_UNQ" on table "TEST_UTF8"
    -Problematic key value is ("S" = '∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑∑...)

    Statement failed, SQLSTATE = 23000
    violation of PRIMARY or UNIQUE KEY constraint "TEST_CSET_UTF8_UNQ" on table "TEST_UTF8"
    -Problematic key value is ("S" = 'Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á∑Á...)

    Statement failed, SQLSTATE = 23000
    violation of PRIMARY or UNIQUE KEY constraint "TEST_CSET_UTF8_UNQ" on table "TEST_UTF8"
    -Problematic key value is ("S" = 'ÁÁ∑ÁÁ∑ÁÁ∑ÁÁ∑ÁÁ∑ÁÁ∑ÁÁ∑ÁÁ∑ÁÁ∑ÁÁ∑ÁÁ∑ÁÁ∑ÁÁ∑ÁÁ∑ÁÁ∑ÁÁ∑ÁÁ∑ÁÁ∑ÁÁ∑ÁÁ∑ÁÁ∑ÁÁ∑ÁÁ∑ÁÁ∑ÁÁ∑ÁÁ∑ÁÁ∑ÁÁ∑ÁÁ∑ÁÁ∑ÁÁ∑ÁÁ∑ÁÁ∑ÁÁ∑ÁÁ∑ÁÁ...)

    Statement failed, SQLSTATE = 23000
    violation of PRIMARY or UNIQUE KEY constraint "TEST_CSET_UTF8_UNQ" on table "TEST_UTF8"
    -Problematic key value is ("S" = 'ÁÁÁ∑ÁÁÁ∑ÁÁÁ∑ÁÁÁ∑ÁÁÁ∑ÁÁÁ∑ÁÁÁ∑ÁÁÁ∑ÁÁÁ∑ÁÁÁ∑ÁÁÁ∑ÁÁÁ∑ÁÁÁ∑ÁÁÁ∑ÁÁÁ∑ÁÁÁ∑ÁÁÁ∑ÁÁÁ∑ÁÁÁ∑ÁÁÁ∑ÁÁÁ∑ÁÁÁ∑ÁÁÁ∑ÁÁÁ∑ÁÁÁ∑ÁÁÁ∑ÁÁÁ∑ÁÁÁ...)

    Statement failed, SQLSTATE = 23000
    violation of PRIMARY or UNIQUE KEY constraint "TEST_CSET_UTF8_UNQ" on table "TEST_UTF8"
    -Problematic key value is ("S" = 'ÁÁÁ∑∑ÁÁÁ∑∑ÁÁÁ∑∑ÁÁÁ∑∑ÁÁÁ∑∑ÁÁÁ∑∑ÁÁÁ∑∑ÁÁÁ∑∑ÁÁÁ∑∑ÁÁÁ∑∑ÁÁÁ∑∑ÁÁÁ∑∑ÁÁÁ∑∑ÁÁÁ∑∑ÁÁÁ∑∑ÁÁÁ∑∑ÁÁÁ∑∑ÁÁÁ∑∑ÁÁÁ∑∑ÁÁÁ∑∑ÁÁÁ∑...)

    Statement failed, SQLSTATE = 23000
    violation of PRIMARY or UNIQUE KEY constraint "TEST_CSET_UTF8_UNQ" on table "TEST_UTF8"
    -Problematic key value is ("S" = 'ÁÁÁÁ∑ÁÁÁÁ∑ÁÁÁÁ∑ÁÁÁÁ∑ÁÁÁÁ∑ÁÁÁÁ∑ÁÁÁÁ∑ÁÁÁÁ∑ÁÁÁÁ∑ÁÁÁÁ∑ÁÁÁÁ∑ÁÁÁÁ∑ÁÁÁÁ∑ÁÁÁÁ∑ÁÁÁÁ∑ÁÁÁÁ∑ÁÁÁÁ∑ÁÁÁÁ∑ÁÁÁÁ∑ÁÁÁÁ∑ÁÁÁÁ∑ÁÁÁÁ∑ÁÁÁ...)

    Statement failed, SQLSTATE = 23000
    violation of PRIMARY or UNIQUE KEY constraint "TEST_CSET_UTF8_UNQ" on table "TEST_UTF8"
    -Problematic key value is ("S" = 'Á∑∑Á∑∑Á∑∑Á∑∑Á∑∑Á∑∑Á∑∑Á∑∑Á∑∑Á∑∑Á∑∑Á∑∑Á∑∑Á∑∑Á∑∑Á∑∑Á∑∑Á∑∑Á∑∑Á∑∑Á∑∑Á∑∑Á∑∑Á∑∑Á∑∑Á∑∑Á∑∑Á∑∑Á∑∑Á∑∑Á∑∑...)

    Statement failed, SQLSTATE = 23000
    violation of PRIMARY or UNIQUE KEY constraint "TEST_CSET_UTF8_UNQ" on table "TEST_UTF8"
    -Problematic key value is ("S" = 'Á∑∑∑Á∑∑∑Á∑∑∑Á∑∑∑Á∑∑∑Á∑∑∑Á∑∑∑Á∑∑∑Á∑∑∑Á∑∑∑Á∑∑∑Á∑∑∑Á∑∑∑Á∑∑∑Á∑∑∑Á∑∑∑Á∑∑∑Á∑∑∑Á∑∑∑Á∑∑∑Á∑∑∑Á∑∑∑Á∑...)

    Statement failed, SQLSTATE = 23000
    violation of PRIMARY or UNIQUE KEY constraint "TEST_CSET_UTF8_UNQ" on table "TEST_UTF8"
    -Problematic key value is ("S" = 'ÁÁ∑∑∑ÁÁ∑∑∑ÁÁ∑∑∑ÁÁ∑∑∑ÁÁ∑∑∑ÁÁ∑∑∑ÁÁ∑∑∑ÁÁ∑∑∑ÁÁ∑∑∑ÁÁ∑∑∑ÁÁ∑∑∑ÁÁ∑∑∑ÁÁ∑∑∑ÁÁ∑∑∑ÁÁ∑∑∑ÁÁ∑∑∑ÁÁ∑∑∑ÁÁ∑∑∑ÁÁ∑∑∑Á...)

    Statement failed, SQLSTATE = 23000
    violation of PRIMARY or UNIQUE KEY constraint "TEST_CSET_UTF8_UNQ" on table "TEST_UTF8"
    -Problematic key value is ("S" = 'Á∑∑∑∑Á∑∑∑∑Á∑∑∑∑Á∑∑∑∑Á∑∑∑∑Á∑∑∑∑Á∑∑∑∑Á∑∑∑∑Á∑∑∑∑Á∑∑∑∑Á∑∑∑∑Á∑∑∑∑Á∑∑∑∑Á∑∑∑∑Á∑∑∑∑Á∑∑∑∑Á∑∑∑∑Á∑∑∑...)
"""

@pytest.mark.version('>=3')
def test_1(act: Action):
    act.expected_stderr = expected_stderr
    act.execute(charset='utf8')
    assert act.clean_stderr == act.clean_expected_stderr

