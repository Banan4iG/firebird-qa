#coding:utf-8
#
# id:           bugs.core_1510
# title:        Bad XSQLVAR [NULL flags] for (2*COALESCE(NULL,NULL))
# decription:   
# tracker_id:   CORE-1510
# min_versions: ['2.1.7']
# versions:     3.0
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 3.0
# resources: None

substitutions_1 = [('^((?!sqltype).)*$', ''), ('[ ]+', ' '), ('[\t]*', ' '), ('charset:.*', '')]

init_script_1 = """"""

db_1 = db_factory(page_size=4096, sql_dialect=3, init=init_script_1)

test_script_1 = """
    set sqlda_display;
    select 2*COALESCE(NULL,NULL) from RDB$DATABASE;
    select 2*IIF(NULL is NULL, NULL, NULL) from RDB$DATABASE;
"""

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    01: sqltype: 580 INT64 Nullable scale: 0 subtype: 0 len: 8
    01: sqltype: 580 INT64 Nullable scale: 0 subtype: 0 len: 8
"""

@pytest.mark.version('>=3.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_stdout == act_1.clean_expected_stdout

