#coding:utf-8

"""
ID:          new-database-11
TITLE:       New DB - RDB$FUNCTION_ARGUMENTS
DESCRIPTION: Check for correct content of RDB$FUNCTION_ARGUMENTS in a new database.
FBTEST:      functional.basic.db.11
"""

import pytest
from firebird.qa import *
db = db_factory()

test_script = """
    set list on;
    set count on;
    select *
    from rdb$function_arguments fa
    order by fa.rdb$function_name, fa.rdb$argument_position;
"""

act = isql_act('db', test_script)

# version: 3.0

expected_stdout_1 = """
    Records affected: 0
"""

@pytest.mark.version('>=3.0,<4.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout_1
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

# version: 4.0

expected_stdout_2 = """
    RDB$FUNCTION_NAME               DATABASE_VERSION
    RDB$ARGUMENT_POSITION           0
    RDB$MECHANISM                   <null>
    RDB$FIELD_TYPE                  <null>
    RDB$FIELD_SCALE                 <null>
    RDB$FIELD_LENGTH                <null>
    RDB$FIELD_SUB_TYPE              <null>
    RDB$CHARACTER_SET_ID            <null>
    RDB$FIELD_PRECISION             <null>
    RDB$CHARACTER_LENGTH            <null>
    RDB$PACKAGE_NAME                RDB$TIME_ZONE_UTIL
    RDB$ARGUMENT_NAME               <null>
    RDB$FIELD_SOURCE                RDB$DBTZ_VERSION
    RDB$DEFAULT_VALUE               <null>
    RDB$DEFAULT_SOURCE              <null>
    RDB$COLLATION_ID                <null>
    RDB$NULL_FLAG                   1
    RDB$ARGUMENT_MECHANISM          <null>
    RDB$FIELD_NAME                  <null>
    RDB$RELATION_NAME               <null>
    RDB$SYSTEM_FLAG                 1
    RDB$DESCRIPTION                 <null>

    Records affected: 1
"""

@pytest.mark.version('>=4.0')
def test_2(act: Action):
    act.expected_stdout = expected_stdout_2
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
