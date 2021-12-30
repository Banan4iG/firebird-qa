#coding:utf-8
#
# id:           bugs.core_1018
# title:        Provide mechanism to get engine version without needing to call API function
# decription:   
# tracker_id:   CORE-1018
# min_versions: []
# versions:     3.0, 4.0, 5.0
# qmid:         bugs.core_1018-211

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 3.0
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """
    set list on;
    -- Engine version could contain more than one digit in any section or more sections.
    -- Changed pattern for matching such cases of engine version as:
    -- '3.2.23' or '3.3.2.1.0.1.2.3.4.5.7' etc
    select iif( t.ev similar to '[0-9]+.[0-9]+.[0-9]+((.?[0-9]+)*)', substring(ev from 1 for 3), null) as version
    from (
        select rdb$get_context('SYSTEM', 'ENGINE_VERSION') ev
        from rdb$database
    )t;
"""

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    VERSION                         3.0
"""

@pytest.mark.version('>=3.0,<4.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_stdout == act_1.clean_expected_stdout

# version: 4.0
# resources: None

substitutions_2 = [('4\\.\\d+', '4\\.')]

init_script_2 = """"""

db_2 = db_factory(sql_dialect=3, init=init_script_2)

test_script_2 = """
    set list on;
    -- Engine version could contain more than one digit in any section or more sections.
    -- Changed pattern for matching such cases of engine version as:
    -- '3.2.23' or '3.3.2.1.0.1.2.3.4.5.7' etc
    select iif( t.ev similar to '[0-9]+.[0-9]+.[0-9]+((.?[0-9]+)*)', substring(ev from 1 for 3), null) as version
    from (
        select rdb$get_context('SYSTEM', 'ENGINE_VERSION') ev
        from rdb$database
    )t;
"""

act_2 = isql_act('db_2', test_script_2, substitutions=substitutions_2)

expected_stdout_2 = """
    VERSION                         4.0
"""

@pytest.mark.version('>=4.0,<5.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout

# version: 5.0
# resources: None

substitutions_3 = [('5\\.\\d+', '5\\.')]

init_script_3 = """"""

db_3 = db_factory(sql_dialect=3, init=init_script_3)

test_script_3 = """
    set list on;
    -- Engine version could contain more than one digit in any section or more sections.
    -- Changed pattern for matching such cases of engine version as:
    -- '3.2.23' or '3.3.2.1.0.1.2.3.4.5.7' etc
    select iif( t.ev similar to '[0-9]+.[0-9]+.[0-9]+((.?[0-9]+)*)', substring(ev from 1 for 3), null) as version
    from (
        select rdb$get_context('SYSTEM', 'ENGINE_VERSION') ev
        from rdb$database
    )t;
"""

act_3 = isql_act('db_3', test_script_3, substitutions=substitutions_3)

expected_stdout_3 = """
    VERSION                         5.0
"""

@pytest.mark.version('>=5.0')
def test_3(act_3: Action):
    act_3.expected_stdout = expected_stdout_3
    act_3.execute()
    assert act_3.clean_stdout == act_3.clean_expected_stdout

