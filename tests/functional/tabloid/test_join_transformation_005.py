#coding:utf-8
#
# id:           functional.tabloid.join_transformation_005
# title:        Check ability of outer join simplification.
# decription:   
#                  Query like this: 
#                     A inner join B left join C can be simplified to:
#                     A inner join B inner join C
#                  -- if join-expression of 'B left join C' is null-rejecting.
#                
# tracker_id:   
# min_versions: ['3.0']
# versions:     3.0
# qmid:         

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 3.0
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(from_backup='join-transformations.fbk', init=init_script_1)

test_script_1 = """
    execute procedure sp_fill( 35, 30 );
    --                         ^    ^- probability of assign each field on each row to NULL (percent).
    --                         +- number of rows in each of tables t1...t6

    commit;
    execute procedure sp_recalc_idx_stat;
    commit;
    
    set list on;
    set term ^;
    execute block returns(result varchar(50)) as
    begin
        select result
        from sp_run(
            ---------------------- Query-1 (not simplified)
            -- NB: we have to make "padding" of null literals up to 6 fields
            -- if query returns less columns:
            'select a.id, b.id, c.id, null, null, null
            from t1 a
            left  ---------------------------- [1]: this can be replaced with INNER.
            join t2 b on a.x = b.y
            join t3 c on b.y = c.z'
            --           ^^^^^^^^^------------ this is null-rejected expression
          ,
            ---------------------- Query-2 (simplified and we assume that it ALWAYS produces the same result as Q1)
            'select a.id, b.id, c.id, null, null, null
            from t1 a
            inner 
            join t2 b on a.x = b.y
            join t3 c on b.y = c.z'
          , 0 ------------------------------------ nr_total: when 0 then do NOT run sp_fill because we already do have data for checking
        ) into result;

        suspend;

        if ( result not containing 'Passed' ) then
            -- this context variable serves as 'flag' to show 
            -- problematic data (see following EB):
            rdb$set_context('USER_SESSION', 'FAULT', '1'); 
    end
    ^
    execute block returns( failed_on varchar(255) ) as
    begin
        -- When queries are NOT equal on some data then we have to output
        -- rows from all tables in order to reproduce this trouble later:
        if ( rdb$get_context('USER_SESSION', 'FAULT') = '1' ) then
        begin
          for 
              select dml from sp_show_data 
              into failed_on
          do
              suspend;
        end
    end
    ^
    set term ^;


  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    RESULT                          Passed.
  """

@pytest.mark.version('>=3.0')
def test_join_transformation_005_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout

