#coding:utf-8
#
# id:           bugs.core_6084
# title:        CREATE SEQUENCE START WITH has wrong initial value
# decription:   
#                  Behaviour of 'next value for <sequence>' and gen_id(<sequence>, N) has been changed:
#                  1) first, it returns to caller value that was NOT YET changed (i.e. 'current'), and
#                  2) only after this it increments sequence.
#                  When clause 'START WITH' absent then initial value of sequence must be 1.
#               
#                  Test verifies several possible cases for this by making different START/INCREMENT clauses combination.
#                  See also: doc/README.incompatibilities.3to4.txt
#                  See also: tests
#               unctional\\generatorlter_01.fbt
#               
#                  Checked on 4.0.0.2131.
#                
# tracker_id:   CORE-6084
# min_versions: ['4.0']
# versions:     4.0
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 4.0
# resources: None

substitutions_1 = [('[ \t]+', ' ')]

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """
    set heading off;
    --set echo on;

    recreate sequence gen_nxtval; recreate sequence gen_common;
    select 'case-00' as msg, (next value for gen_nxtval) as gen_nxtval, gen_id(gen_common,1) as gen_common_gen_id from rdb$database;

    recreate sequence gen_nxtval start with 1; recreate sequence gen_common start with 1;
    select 'case-01' as msg, (next value for gen_nxtval) as gen_nxtval, gen_id(gen_common,1) as gen_common_gen_id from rdb$database;

    recreate sequence gen_nxtval start with 1 increment by 2; recreate sequence gen_common start with 1 increment by 2;
    select 'case-02' as msg, (next value for gen_nxtval) as gen_nxtval, gen_id(gen_common,2) as gen_common_gen_id from rdb$database;

    recreate sequence gen_nxtval start with 1 increment by -1; recreate sequence gen_common start with 1 increment by -1;
    select 'case-03' as msg, (next value for gen_nxtval) as gen_nxtval, gen_id(gen_common,-1) as gen_common_gen_id from rdb$database;

    recreate sequence gen_nxtval start with 1 increment by -2; recreate sequence gen_common start with 1 increment by -2;
    select 'case-04' as msg, (next value for gen_nxtval) as gen_nxtval, gen_id(gen_common,-2) as gen_common_gen_id from rdb$database;

    recreate sequence gen_nxtval increment by 2; recreate sequence gen_common increment by 2;
    select 'case-05' as msg, (next value for gen_nxtval) as gen_nxtval, gen_id(gen_common,2) as gen_common_gen_id from rdb$database;

    recreate sequence gen_nxtval increment by -1; recreate sequence gen_common increment by -1;
    select 'case-06' as msg, (next value for gen_nxtval) as gen_nxtval, gen_id(gen_common,-1) as gen_common_gen_id from rdb$database;

    recreate sequence gen_nxtval increment by -2; recreate sequence gen_common increment by -2;
    select 'case-07' as msg, (next value for gen_nxtval) as gen_nxtval, gen_id(gen_common,-2) as gen_common_gen_id from rdb$database;

    recreate sequence gen_nxtval increment by 1000000000; recreate sequence gen_common increment by 1000000000;
    select 'case-08' as msg, (next value for gen_nxtval) as gen_nxtval, gen_id(gen_common, 1000000000) as gen_common_gen_id from rdb$database;

    recreate sequence gen_nxtval increment by -1000000000; recreate sequence gen_common increment by -1000000000;
    select 'case-09' as msg, (next value for gen_nxtval) as gen_nxtval, gen_id(gen_common, -1000000000) as gen_common_gen_id from rdb$database;

    recreate sequence gen_nxtval start with 9223372036854775807 increment by -1; recreate sequence gen_common start with 9223372036854775807 increment by -1;
    select 'case-10' as msg, (next value for gen_nxtval) as gen_nxtval, gen_id(gen_common,-1) as gen_common_gen_id from rdb$database;

    recreate sequence gen_nxtval start with 9223372036854775807 increment by -2147483647; recreate sequence gen_common start with 9223372036854775807 increment by -2147483647;
    select 'case-11' as msg, (next value for gen_nxtval) as gen_nxtval, gen_id(gen_common,-2147483647) as gen_common_gen_id from rdb$database;

    recreate sequence gen_nxtval start with -9223372036854775808 increment by 2147483647; recreate sequence gen_common start with -9223372036854775808 increment by 2147483647;
    select 'case-12' as msg, (next value for gen_nxtval) as gen_nxtval, gen_id(gen_common,2147483647) as gen_common_gen_id from rdb$database;

    recreate table test(id int generated always as identity);
    insert into test default values;
    insert into test default values;
    select 'case-13' as msg, id from test;
    commit;

    recreate table test(id bigint generated always as identity);
    insert into test default values;
    insert into test default values;
    select 'case-14' as msg, id from test;
    commit;

    recreate table test(id bigint generated always as identity (start with -9223372036854775808) );
    insert into test default values;
    insert into test default values;
    select 'case-15' as msg, id from test;
    commit;

    recreate table test(id bigint generated always as identity (start with -9223372036854775808 increment by 2147483647) );
    insert into test default values;
    insert into test default values;
    select 'case-16' as msg, id from test;
    commit;

    recreate table test(id bigint generated always as identity (increment by 2147483647) );
    insert into test default values;
    insert into test default values;
    select 'case-17' as msg, id from test;
    commit;

    recreate table test(id bigint generated always as identity (start with 9223372036854775807 increment by -2147483647) );
    insert into test default values;
    insert into test default values;
    select 'case-18' as msg, id from test;
    commit;

    recreate table test(id bigint generated always as identity (increment by -2147483647) );
    insert into test default values;
    insert into test default values;
    select 'case-19' as msg, id from test;
    commit;
  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    case-00                     1                     1
    case-01                     1                     1
    case-02                     1                     1
    case-03                     1                     1
    case-04                     1                     1
    case-05                     1                     1
    case-06                     1                     1
    case-07                     1                     1
    case-08                     1                     1
    case-09                     1                     1
    case-10   9223372036854775807   9223372036854775807
    case-11   9223372036854775807   9223372036854775807
    case-12  -9223372036854775808  -9223372036854775808
    case-13            1
    case-13            2
    case-14                     1
    case-14                     2
    case-15  -9223372036854775808
    case-15  -9223372036854775807
    case-16  -9223372036854775808
    case-16  -9223372034707292161
    case-17                     1
    case-17            2147483648
    case-18   9223372036854775807
    case-18   9223372034707292160
    case-19                     1
    case-19           -2147483646
   """

@pytest.mark.version('>=4.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout

