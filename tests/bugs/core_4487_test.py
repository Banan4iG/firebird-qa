#coding:utf-8
#
# id:           bugs.core_4487
# title:        Maintain package body after ALTER/RECREATE PACKAGE
# decription:   
# tracker_id:   CORE-4487
# min_versions: ['3.0']
# versions:     3.0
# qmid:         

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 3.0
# resources: None

substitutions_1 = [('HDR_SOURCE.*', ''), ('BODY_SOURCE.*', '')]

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """
    create or alter view v_pg_meta as
    select 
        rp.rdb$package_header_source hdr_source
        ,rp.rdb$package_body_source body_source
        ,rp.rdb$valid_body_flag body_valid
    from rdb$packages rp 
    where rp.rdb$package_name = upper('pg_test');
    
    set list on;
    set blob all;
    
    set term ^;
    create or alter package pg_test
    as
    begin
        function fn_test_01 returns smallint;
        function fn_test_02 returns smallint;
    end
    ^
    
    recreate package body pg_test
    as
    begin
        function fn_test_01 returns smallint as
        begin
            return 1;
        end
    
        function fn_test_02 returns smallint as
        begin
            return 2;
        end
    end
    ^
    set term ;^
    commit;
    -----------------------------------------
    select 1 as step, v.* from v_pg_meta v;
    ------------------------------------------
    
    set term ^;
    create or alter package pg_test
    as
    begin
        function fn_test_01 returns smallint;
        function fn_test_02(a_val smallint) returns smallint;
    end
    ^
    set term ;^
    commit;
    -----------------------------------------
    set term ^;
    create or alter package pg_test
    as
    begin
        function fn_test_01 returns smallint;
        -- Adding IN-argument to func must lead package body to invalid state:
        function fn_test_02(a_val smallint) returns smallint;
    end
    ^
    set term ;^
    commit;
    -----------------------------------------
    select 2 as step, v.* from v_pg_meta v;
    ------------------------------------------
    
    set term ^;
    create or alter package pg_test
    as
    begin
        function fn_test_03 returns bigint;
    end
    ^
    set term ;^
    commit;
    -----------------------------------------
    select 3 as step, v.* from v_pg_meta v;
    ------------------------------------------
    
    set term ^;
    create or alter package pg_test
    as
    begin
        -- Restoring exactly the same singnatures of both functions
        -- does NOT make package body to VALID state:
        function fn_test_01 returns smallint;
        function fn_test_02 returns smallint;
    end
    ^
    set term ;^
    commit;
    -----------------------------------------
    select 4 as step, v.* from v_pg_meta v;
    ------------------------------------------
  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    STEP                            1
    HDR_SOURCE                      2a:1
    begin
      function fn_test_01 returns smallint;
      function fn_test_02 returns smallint;
    end
    BODY_SOURCE                     2a:4
    begin
      function fn_test_01 returns smallint as
      begin
        return 1;
      end
      function fn_test_02 returns smallint as
      begin
        return 2;
      end
    end
    BODY_VALID                      1
    
    
    
    STEP                            2
    HDR_SOURCE                      2a:1
    begin
      function fn_test_01 returns smallint;
        -- Adding IN-argument to func must lead package body to invalid state:
      function fn_test_02(a_val smallint) returns smallint;
    end
    BODY_SOURCE                     2a:4
    begin
      function fn_test_01 returns smallint as
      begin
        return 1;
      end
      function fn_test_02 returns smallint as
      begin
        return 2;
      end
    end
    BODY_VALID                      0
    
    
    
    STEP                            3
    HDR_SOURCE                      2a:2
    begin
      function fn_test_03 returns bigint;
    end
    BODY_SOURCE                     2a:4
    begin
      function fn_test_01 returns smallint as
      begin
        return 1;
      end
      function fn_test_02 returns smallint as
      begin
        return 2;
      end
    end
    BODY_VALID                      0
    
    
    
    STEP                            4
    HDR_SOURCE                      2a:1
    begin
      -- Restoring exactly the same singnatures of both functions
      -- does NOT make package body to VALID state:
      function fn_test_01 returns smallint;
      function fn_test_02 returns smallint;
    end
    BODY_SOURCE                     2a:4
    begin
      function fn_test_01 returns smallint as
      begin
        return 1;
      end
      function fn_test_02 returns smallint as
      begin
        return 2;
      end
    end
    BODY_VALID                      0
  """

@pytest.mark.version('>=3.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout

