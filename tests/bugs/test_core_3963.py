#coding:utf-8
#
# id:           bugs.core_3963
# title:        isql doesn't know the difference between UDF's and psql-functions 
# decription:   
#                    *** FOR FB 3.X ONLY ***
#                       Test uses UDF 'strlen' declared in ib_udf.sql script which for sure present in every FB snapshot.
#                       After this, we try to create PSQL function with the same signature but evaluate its returning value
#                       as double size of input argument (in order to distinguish these functions by their results).
#               
#                   *** FOR FB 4.X AND ABOVE  ***
#                       Added separate code for running on FB 4.0.x.
#                       UDF usage is deprecated in FB 4+, see: ".../doc/README.incompatibilities.3to4.txt".
#                       Functions div, frac, dow, sdow, getExactTimestampUTC and isLeapYear got safe replacement 
#                       in UDR library "udf_compat", see it in folder: ../plugins/udr/
#                   Checked on:
#                       3.0.5.33086: OK, 1.454s.
#                       4.0.0.1172: OK, 7.781s.
#                       4.0.0.1340: OK, 3.844s.
#                       4.0.0.1378: OK, 3.485s.   
#                
# tracker_id:   CORE-3963
# min_versions: ['3.0']
# versions:     3.0, 4.0
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 3.0
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """
    set list on;
    --set echo on;

    -- Should PASS:
    set term ^; 
    create function strlen(s varchar(32765)) returns int as begin return 2 * char_length(s); end
    ^ 
    set term ;^
    select strlen('tratata') from rdb$database;
    commit;

    -- Should FAIL:
    DECLARE EXTERNAL FUNCTION strlen CSTRING(32767) RETURNS INTEGER BY VALUE ENTRY_POINT 'IB_UDF_strlen' MODULE_NAME 'ib_udf';

    drop function strlen; -- kill PSQL function 
    commit;


    -- Should PASS:
    DECLARE EXTERNAL FUNCTION strlen CSTRING(32767) RETURNS INTEGER BY VALUE ENTRY_POINT 'IB_UDF_strlen' MODULE_NAME 'ib_udf';

    select strlen('tratata') from rdb$database;
    commit;

    -- Should FAIL:
    set term ^; 
    create function strlen(s varchar(32765)) returns int as begin return 2 * char_length(s); end
    ^ 
    set term ;^

    select strlen('tratata') from rdb$database;
    commit;

    drop function strlen; -- kill UDF function
    commit;


    -- Should PASS:
    set term ^; 
    create function strlen(s varchar(32765)) returns int as begin return 2 * char_length(s); end
    ^ 
    set term ;^
    select strlen('tratata') from rdb$database;
    commit;

    drop function strlen;
    commit;

  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    STRLEN                          14
    STRLEN                          7
    STRLEN                          7
    STRLEN                          14
  """
expected_stderr_1 = """
    Statement failed, SQLSTATE = 42000
    unsuccessful metadata update
    -CREATE FUNCTION STRLEN failed
    -Function STRLEN already exists

    Statement failed, SQLSTATE = 42000
    unsuccessful metadata update
    -CREATE FUNCTION STRLEN failed
    -Function STRLEN already exists
  """

@pytest.mark.version('>=3.0,<4.0')
def test_core_3963_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.expected_stderr = expected_stderr_1
    act_1.execute()
    assert act_1.clean_expected_stderr == act_1.clean_stderr
    assert act_1.clean_expected_stdout == act_1.clean_stdout

# version: 4.0
# resources: None

substitutions_2 = []

init_script_2 = """"""

db_2 = db_factory(sql_dialect=3, init=init_script_2)

test_script_2 = """
    set list on;

    -- See declaration sample in plugins\\udr\\UdfBackwardCompatibility.sql:

    create function the_frac(
        val double precision
    ) returns double precision
        external name 'udf_compat!UC_frac'
        engine udr;
    commit;

    set sqlda_display on;

    select the_frac( -pi() ) from rdb$database;
    commit;

    -- should FAIL:
    set term ^; 
    create function the_frac( val double precision ) returns double precision as 
    begin 
        return val - cast(val as int); 
    end
    ^ 
    set term ;^
    commit;

    -- should PASS:
    drop function the_frac;
    commit;

    -- should FAIL:
    select the_frac( -pi() ) from rdb$database;
    commit;


    -- should PASS:
    set term ^; 
    create function the_frac( val double precision ) returns double precision as 
    begin 
        return val - cast(val as int); 
    end
    ^ 
    set term ;^
    commit;

    -- should PASS:
    select the_frac( -pi() ) from rdb$database;
    commit;

    -- should FAIL:
    create function the_frac(
        val double precision
    ) returns double precision
        external name 'udf_compat!UC_frac'
        engine udr;
    commit;

  """

act_2 = isql_act('db_2', test_script_2, substitutions=substitutions_2)

expected_stdout_2 = """

    INPUT message field count: 0

    OUTPUT message field count: 1
    01: sqltype: 480 DOUBLE Nullable scale: 0 subtype: 0 len: 8
      :  name: THE_FRAC  alias: THE_FRAC
      : table:   owner: 

    THE_FRAC                        -0.1415926535897931



    INPUT message field count: 0

    OUTPUT message field count: 1
    01: sqltype: 480 DOUBLE Nullable scale: 0 subtype: 0 len: 8
      :  name: THE_FRAC  alias: THE_FRAC
      : table:   owner: 

    THE_FRAC                        -0.1415926535897931

  """
expected_stderr_2 = """
    Statement failed, SQLSTATE = 42000
    unsuccessful metadata update
    -CREATE FUNCTION THE_FRAC failed
    -Function THE_FRAC already exists

    Statement failed, SQLSTATE = 39000
    Dynamic SQL Error
    -SQL error code = -804
    -Function unknown
    -THE_FRAC

    Statement failed, SQLSTATE = 42000
    unsuccessful metadata update
    -CREATE FUNCTION THE_FRAC failed
    -Function THE_FRAC already exists
  """

@pytest.mark.version('>=4.0')
def test_core_3963_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.expected_stderr = expected_stderr_2
    act_2.execute()
    assert act_2.clean_expected_stderr == act_2.clean_stderr
    assert act_2.clean_expected_stdout == act_2.clean_stdout

