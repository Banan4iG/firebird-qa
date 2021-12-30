#coding:utf-8
#
# id:           bugs.gh_7018
# title:        Problems with windows frames
# decription:   
#                   https://github.com/FirebirdSQL/firebird/issues/7018
#               
#                   Confirmed bug on 5.0.0.259
#                   Checked on 5.0.0.263, 4.0.1.2642 -- all fine.
#                
# tracker_id:   
# min_versions: ['4.0.1']
# versions:     4.0.1
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 4.0.1
# resources: None

substitutions_1 = [('LIST\\s+\\d+:\\d+', '')]

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """
    recreate table t1 (id integer, f01 integer);
    recreate table entries(id int, f01 int);

    insert into t1(id,f01) select row_number()over(), -row_number()over() from rdb$types rows 5;
    insert into entries(id, f01) select id, 100 from t1;
    commit;
    set list on;
    -----------------
    select 'sttm-1' as msg, id, f01, first_value(id) over (range current row) from t1 order by id;
    select 'sttm-2' as msg, id, f01, first_value(id) over (rows 2 preceding) from t1;
    select 'sttm-3' as msg, id, f01, first_value(id) over (range between unbounded preceding and unbounded following) from t1 order by id;
    select 'sttm-4' as msg, id, sum(id) over (rows between current row and current row) from t1 where id is not null order by id;
    select 'sttm-5' as msg, id, f01, list(distinct f01) over (rows between unbounded preceding and current row) from t1 order by id, f01;
    select 'sttm-6' as msg, id, f01, list(f01) over (rows between unbounded preceding and current row) from t1 order by id, f01;
    -----------------
    select 'sttm-7' as msg, id, f01, lag(id) over (range 2 preceding) from t1;
    -----------------
    select 'sttm-8' as msg, count(distinct f01) over (rows between unbounded preceding and current row) id from entries where id <= 2 order by id;
    select 'sttm-9' as msg, count(distinct f01) over (rows between unbounded preceding and unbounded following) id from entries where id <= 2 order by id;
"""

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    MSG                             sttm-1
    ID                              1
    F01                             -1
    FIRST_VALUE                     1
    MSG                             sttm-1
    ID                              2
    F01                             -2
    FIRST_VALUE                     1
    MSG                             sttm-1
    ID                              3
    F01                             -3
    FIRST_VALUE                     1
    MSG                             sttm-1
    ID                              4
    F01                             -4
    FIRST_VALUE                     1
    MSG                             sttm-1
    ID                              5
    F01                             -5
    FIRST_VALUE                     1

    MSG                             sttm-2
    ID                              1
    F01                             -1
    FIRST_VALUE                     1
    MSG                             sttm-2
    ID                              2
    F01                             -2
    FIRST_VALUE                     1
    MSG                             sttm-2
    ID                              3
    F01                             -3
    FIRST_VALUE                     1
    MSG                             sttm-2
    ID                              4
    F01                             -4
    FIRST_VALUE                     2
    MSG                             sttm-2
    ID                              5
    F01                             -5
    FIRST_VALUE                     3

    MSG                             sttm-3
    ID                              1
    F01                             -1
    FIRST_VALUE                     1
    MSG                             sttm-3
    ID                              2
    F01                             -2
    FIRST_VALUE                     1
    MSG                             sttm-3
    ID                              3
    F01                             -3
    FIRST_VALUE                     1
    MSG                             sttm-3
    ID                              4
    F01                             -4
    FIRST_VALUE                     1
    MSG                             sttm-3
    ID                              5
    F01                             -5
    FIRST_VALUE                     1

    MSG                             sttm-4
    ID                              1
    SUM                             1
    MSG                             sttm-4
    ID                              2
    SUM                             2
    MSG                             sttm-4
    ID                              3
    SUM                             3
    MSG                             sttm-4
    ID                              4
    SUM                             4
    MSG                             sttm-4
    ID                              5
    SUM                             5

    
    MSG                             sttm-5
    ID                              1
    F01                             -1
    LIST                            0:1
    -5,-4,-3,-2,-1
    MSG                             sttm-5
    ID                              2
    F01                             -2
    LIST                            0:1
    -5,-4,-3,-2,-1
    MSG                             sttm-5
    ID                              3
    F01                             -3
    LIST                            0:1
    -5,-4,-3,-2,-1
    MSG                             sttm-5
    ID                              4
    F01                             -4
    LIST                            0:1
    -5,-4,-3,-2,-1
    MSG                             sttm-5
    ID                              5
    F01                             -5
    LIST                            0:1
    -5,-4,-3,-2,-1
    
    
    MSG                             sttm-6
    ID                              1
    F01                             -1
    LIST                            0:7
    -1,-2,-3,-4,-5
    MSG                             sttm-6
    ID                              2
    F01                             -2
    LIST                            0:7
    -1,-2,-3,-4,-5
    MSG                             sttm-6
    ID                              3
    F01                             -3
    LIST                            0:7
    -1,-2,-3,-4,-5
    MSG                             sttm-6
    ID                              4
    F01                             -4
    LIST                            0:7
    -1,-2,-3,-4,-5
    MSG                             sttm-6
    ID                              5
    F01                             -5
    LIST                            1:7
    -1,-2,-3,-4,-5
"""

expected_stderr_1 = """
    Statement failed, SQLSTATE = 42000
    RANGE based window with <offset> PRECEDING/FOLLOWING must have a single ORDER BY key of numerical, date, time or timestamp types

    Statement failed, SQLSTATE = 0A000
    feature is not supported
    -DISTINCT is not supported in windows with ORDER BY or frame by ROWS clauses

    Statement failed, SQLSTATE = 0A000
    feature is not supported
    -DISTINCT is not supported in windows with ORDER BY or frame by ROWS clauses
"""

@pytest.mark.version('>=4.0.1')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.expected_stderr = expected_stderr_1
    act_1.execute()
    assert act_1.clean_stderr == act_1.clean_expected_stderr
    assert act_1.clean_stdout == act_1.clean_expected_stdout
