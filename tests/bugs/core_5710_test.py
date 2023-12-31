#coding:utf-8

"""
ID:          issue-5976
ISSUE:       5976
TITLE:       Datatype declaration DECFLOAT without precision should use a default precision
DESCRIPTION:
JIRA:        CORE-5710
FBTEST:      bugs.core_5710
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    set list on;
    recreate table test( distance_small decfloat(16), distance_huge decfloat(34), distance_default decfloat );
    commit;

    select
         r.rdb$field_name
        ,f.rdb$field_length
        ,f.rdb$field_scale
        ,f.rdb$field_type
        ,f.rdb$field_precision
    from rdb$fields f
    join rdb$relation_fields r on f.rdb$field_name = r.rdb$field_source
    where
        r.rdb$relation_name = upper('test')
        and r.rdb$field_name starting with upper('distance')
    order by r.rdb$field_position
    ;
"""

act = isql_act('db', test_script)

expected_stdout = """
    RDB$FIELD_NAME                  DISTANCE_SMALL
    RDB$FIELD_LENGTH                8
    RDB$FIELD_SCALE                 0
    RDB$FIELD_TYPE                  24
    RDB$FIELD_PRECISION             16

    RDB$FIELD_NAME                  DISTANCE_HUGE
    RDB$FIELD_LENGTH                16
    RDB$FIELD_SCALE                 0
    RDB$FIELD_TYPE                  25
    RDB$FIELD_PRECISION             34

    RDB$FIELD_NAME                  DISTANCE_DEFAULT
    RDB$FIELD_LENGTH                16
    RDB$FIELD_SCALE                 0
    RDB$FIELD_TYPE                  25
    RDB$FIELD_PRECISION             34
"""

@pytest.mark.version('>=4.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
