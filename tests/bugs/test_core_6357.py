#coding:utf-8
#
# id:           bugs.core_6357
# title:        LEAD() and LAG() do not allow to specify 3rd argument ("DEFAULT" value when pointer is out of scope) of INT128 datatype.
# decription:   
#                   Checked on 4.0.0.2091 - all OK.
#                   (intermediate snapshot with timestamp: 08.07.20 15:10)
#                
# tracker_id:   CORE-6357
# min_versions: ['4.0']
# versions:     4.0
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 4.0
# resources: None

substitutions_1 = [('^((?!sqltype|FIELD_A|LAG_FOR|LEAD_FOR).)*$', ''), ('[ \t]+', ' ')]

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """
    set heading off;
    recreate table test1 (a smallint);
    recreate table test2 (a bigint);
    recreate table test3 (a int128);
    recreate table test4 (a decfloat);
     
    insert into test1 values (1);
    insert into test1 values (2);
     
    insert into test2 select * from test1;
    insert into test3 select * from test1;
    insert into test4 select * from test1;
     
    set list on;
    set sqlda_display on;
     
    select a as field_a, lead(a, 1, 32767)over(order by a) lead_for_smallint from test1;
    select a as field_a, lag(a, 1, -32768)over(order by a) lag_for_smallint from test1;
     
    select a as field_a, lead(a, 1, 9223372036854775807)over(order by a) lead_for_bigint from test2;
    select a as field_a, lag(a, 1, -9223372036854775808)over(order by a) lag_for_bigint from test2;
     
    select a as field_a, lead(a, 1, 170141183460469231731687303715884105727)over(order by a) lead_for_int128 from test3;
    select a as field_a, lag(a, 1, -170141183460469231731687303715884105728)over(order by a) lag_for_int128 from test3;
     
    select a as field_a, lag(a, 1, -9.999999999999999999999999999999999e6144) over (order by a) lag_for_decfloat_1 from test4;
    select a as field_a, lag(a, 1, -1.0e-6143)over(order by a) lag_for_decfloat_2 from test4;
    select a as field_a, lag(a, 1, 1.0e-6143)over(order by a) lag_for_decfloat_3 from test4;
    select a as field_a, lag(a, 1, 9.999999999999999999999999999999999e6144)over(order by a) lag_for_decfloat_4 from test4;
  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    01: sqltype: 500 SHORT Nullable scale: 0 subtype: 0 len: 2
    :  name: A  alias: FIELD_A
    02: sqltype: 500 SHORT Nullable scale: 0 subtype: 0 len: 2
    :  name: LEAD  alias: LEAD_FOR_SMALLINT
    FIELD_A                         1
    LEAD_FOR_SMALLINT               2
    FIELD_A                         2
    LEAD_FOR_SMALLINT               32767
    01: sqltype: 500 SHORT Nullable scale: 0 subtype: 0 len: 2
    :  name: A  alias: FIELD_A
    02: sqltype: 500 SHORT Nullable scale: 0 subtype: 0 len: 2
    :  name: LAG  alias: LAG_FOR_SMALLINT
    FIELD_A                         1
    LAG_FOR_SMALLINT                -32768
    FIELD_A                         2
    LAG_FOR_SMALLINT                1
    01: sqltype: 580 INT64 Nullable scale: 0 subtype: 0 len: 8
    :  name: A  alias: FIELD_A
    02: sqltype: 580 INT64 Nullable scale: 0 subtype: 0 len: 8
    :  name: LEAD  alias: LEAD_FOR_BIGINT
    FIELD_A                         1
    LEAD_FOR_BIGINT                 2
    FIELD_A                         2
    LEAD_FOR_BIGINT                 9223372036854775807
    01: sqltype: 580 INT64 Nullable scale: 0 subtype: 0 len: 8
    :  name: A  alias: FIELD_A
    02: sqltype: 580 INT64 Nullable scale: 0 subtype: 0 len: 8
    :  name: LAG  alias: LAG_FOR_BIGINT
    FIELD_A                         1
    LAG_FOR_BIGINT                  -9223372036854775808
    FIELD_A                         2
    LAG_FOR_BIGINT                  1
    01: sqltype: 32752 INT128 Nullable scale: 0 subtype: 0 len: 16
    :  name: A  alias: FIELD_A
    02: sqltype: 32752 INT128 Nullable scale: 0 subtype: 0 len: 16
    :  name: LEAD  alias: LEAD_FOR_INT128
    FIELD_A                                                                     1
    LEAD_FOR_INT128                                                             2
    FIELD_A                                                                     2
    LEAD_FOR_INT128                       170141183460469231731687303715884105727
    01: sqltype: 32752 INT128 Nullable scale: 0 subtype: 0 len: 16
    :  name: A  alias: FIELD_A
    02: sqltype: 32752 INT128 Nullable scale: 0 subtype: 0 len: 16
    :  name: LAG  alias: LAG_FOR_INT128
    FIELD_A                                                                     1
    LAG_FOR_INT128                       -170141183460469231731687303715884105728
    FIELD_A                                                                     2
    LAG_FOR_INT128                                                              1
    01: sqltype: 32762 DECFLOAT(34) Nullable scale: 0 subtype: 0 len: 16
    :  name: A  alias: FIELD_A
    02: sqltype: 32762 DECFLOAT(34) Nullable scale: 0 subtype: 0 len: 16
    :  name: LAG  alias: LAG_FOR_DECFLOAT_1
    FIELD_A                                                                  1
    LAG_FOR_DECFLOAT_1              -9.999999999999999999999999999999999E+6144
    FIELD_A                                                                  2
    LAG_FOR_DECFLOAT_1                                                       1
    01: sqltype: 32762 DECFLOAT(34) Nullable scale: 0 subtype: 0 len: 16
    :  name: A  alias: FIELD_A
    02: sqltype: 32762 DECFLOAT(34) Nullable scale: 0 subtype: 0 len: 16
    :  name: LAG  alias: LAG_FOR_DECFLOAT_2
    FIELD_A                                                                  1
    LAG_FOR_DECFLOAT_2                                              -1.0E-6143
    FIELD_A                                                                  2
    LAG_FOR_DECFLOAT_2                                                       1
    01: sqltype: 32762 DECFLOAT(34) Nullable scale: 0 subtype: 0 len: 16
    :  name: A  alias: FIELD_A
    02: sqltype: 32762 DECFLOAT(34) Nullable scale: 0 subtype: 0 len: 16
    :  name: LAG  alias: LAG_FOR_DECFLOAT_3
    FIELD_A                                                                  1
    LAG_FOR_DECFLOAT_3                                               1.0E-6143
    FIELD_A                                                                  2
    LAG_FOR_DECFLOAT_3                                                       1
    01: sqltype: 32762 DECFLOAT(34) Nullable scale: 0 subtype: 0 len: 16
    :  name: A  alias: FIELD_A
    02: sqltype: 32762 DECFLOAT(34) Nullable scale: 0 subtype: 0 len: 16
    :  name: LAG  alias: LAG_FOR_DECFLOAT_4
    FIELD_A                                                                  1
    LAG_FOR_DECFLOAT_4               9.999999999999999999999999999999999E+6144
    FIELD_A                                                                  2
    LAG_FOR_DECFLOAT_4                                                       1
  """

@pytest.mark.version('>=4.0')
def test_core_6357_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout

