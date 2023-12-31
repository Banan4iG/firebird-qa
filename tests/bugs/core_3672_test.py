#coding:utf-8

"""
ID:          issue-4022
ISSUE:       4022
TITLE:       computed index by substring function for long columns
DESCRIPTION:
JIRA:        CORE-3672
FBTEST:      bugs.core_3672
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    recreate table test(
         col1 varchar(8190) character set utf8 collate unicode_ci_ai
        ,col2 computed by ( substring(col1 from 1 for 169) )
        ,col3 computed by ( substring(trim( col2 from col1 ) from 1 for 169) )
    );
    commit;

    -- Index on UTF8-field which should be collate in CI_AI manner, will contain 6 bytes per one character (hereafter this is 'N').
    -- This mean that maximum length of key for default page_size = 4096 is:
    -- max_key_length = floor( (page_size / 4 - 9) / N ) = 169 characters.

    -- Verify that we CAN do that w/o error:
    create index test_col1_idx_a on test computed by ( substring(col1 from 1 for 169) );
    create index test_col1_idx_b on test computed by ( substring(trim( col2 from col1 ) from 1 for 169) );
    create index test_col2_idx_a on test computed by ( col2 );
    create index test_col2_idx_b on test computed by ( substring(col2 from 1 for 169) );
    create index test_col3_idx_a on test computed by ( col3 );
    create index test_col3_idx_b on test computed by ( substring(col3 from 1 for 169) );
    commit;
    -- Confirmed for 2.5.5: "-key size exceeds implementation restriction"

    show index test_col1_idx_a;
    show index test_col1_idx_b;
    show index test_col2_idx_a;
    show index test_col2_idx_b;
    show index test_col3_idx_a;
    show index test_col3_idx_b;
"""

act = isql_act('db', test_script)

expected_stdout = """
    TEST_COL1_IDX_A INDEX ON TEST COMPUTED BY ( substring(col1 from 1 for 169) )
    TEST_COL1_IDX_B INDEX ON TEST COMPUTED BY ( substring(trim( col2 from col1 ) from 1 for 169) )
    TEST_COL2_IDX_A INDEX ON TEST COMPUTED BY ( col2 )
    TEST_COL2_IDX_B INDEX ON TEST COMPUTED BY ( substring(col2 from 1 for 169) )
    TEST_COL3_IDX_A INDEX ON TEST COMPUTED BY ( col3 )
    TEST_COL3_IDX_B INDEX ON TEST COMPUTED BY ( substring(col3 from 1 for 169) )
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

