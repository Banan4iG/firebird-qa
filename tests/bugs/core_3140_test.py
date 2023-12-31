#coding:utf-8

"""
ID:          issue-3517
ISSUE:       3517
TITLE:       Preserve comments for parameters after altering procedures
DESCRIPTION:
JIRA:        CORE-3140
FBTEST:      bugs.core_3140
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    create or alter procedure sp_01 as begin end;
    commit;
    set term ^;
    execute block as
    begin
      begin execute statement 'drop domain dm_i'; when any do begin end end
      begin execute statement 'drop domain dm_s'; when any do begin end end
      begin execute statement 'drop domain dm_t'; when any do begin end end
      begin execute statement 'drop domain dm_b'; when any do begin end end
    end^
    set term ;^
    commit;

    create domain dm_i int;
    create domain dm_s varchar(10);
    create domain dm_t timestamp;
    create domain dm_b blob;

    recreate table t_01(id int, s varchar(10), dts timestamp, b blob);
    commit;

    set term ^;
    create or alter procedure sp_01(
       a_01 int
      ,a_02 varchar(10)
      ,a_03 timestamp
      ,a_04 blob
    ) returns (
       o_01 int
      ,o_02 varchar(10)
      ,o_03 timestamp
      ,o_04 blob
    ) as
    begin
      suspend;
    end
    ^
    set term ;^
    commit;
    comment on parameter sp_01.a_01 is 'INPUT par. ''a_01'', mech = 0';
    comment on parameter sp_01.a_02 is 'INPUT par. ''a_02'', mech = 0';
    comment on parameter sp_01.a_03 is 'INPUT par. ''a_03'', mech = 0';
    comment on parameter sp_01.a_04 is 'INPUT par. ''a_04'', mech = 0';
    comment on parameter sp_01.o_01 is 'OUTPUT par. ''o_01'', mech = 0';
    comment on parameter sp_01.o_02 is 'OUTPUT par. ''o_02'', mech = 0';
    comment on parameter sp_01.o_03 is 'OUTPUT par. ''o_03'', mech = 0';
    comment on parameter sp_01.o_04 is 'OUTPUT par. ''o_04'', mech = 0';
    commit;

    set term ^;
    alter procedure sp_01(
       a_01 int
      ,a_02 varchar(10)
      ,a_03 timestamp
      ,a_04 blob
      ,a_05 type of dm_i
      ,a_06 type of dm_s
      ,a_07 type of dm_t
      ,a_08 type of dm_b
    ) returns (
       o_01 int
      ,o_02 varchar(10)
      ,o_03 timestamp
      ,o_04 blob
      ,o_05 type of column t_01.id
      ,o_06 type of column t_01.id
      ,o_07 type of column t_01.id
      ,o_08 type of column t_01.id
    ) as
    begin
      suspend;
    end
    ^
    set term ;^
    commit;

    comment on parameter sp_01.a_05 is 'added INPUT par ''a_05'', mech = 1';
    comment on parameter sp_01.a_06 is 'added INPUT par ''a_06'', mech = 1';
    comment on parameter sp_01.a_07 is 'added INPUT par ''a_07'', mech = 1';
    comment on parameter sp_01.a_08 is 'added INPUT par ''a_08'', mech = 1';

    comment on parameter sp_01.o_05 is 'added OUTPUT par ''o_05'', mech = 1';
    comment on parameter sp_01.o_06 is 'added OUTPUT par ''o_06'', mech = 1';
    comment on parameter sp_01.o_07 is 'added OUTPUT par ''o_07'', mech = 1';
    comment on parameter sp_01.o_08 is 'added OUTPUT par ''o_08'', mech = 1';
    commit;

    set width par_name 31;
    set width par_desc 50;
    set list on;
    select
      cast(rdb$parameter_name as varchar(31)) par_name,
      cast(rdb$description as varchar(50)) par_desc,
      coalesce(rdb$parameter_mechanism, 0 ) par_mech
    from rdb$procedure_parameters
    where rdb$procedure_name='SP_01'
    order by par_name;
"""

act = isql_act('db', test_script)

expected_stdout = """
    PAR_NAME                        A_01
    PAR_DESC                        INPUT par. 'a_01', mech = 0
    PAR_MECH                        0
    PAR_NAME                        A_02
    PAR_DESC                        INPUT par. 'a_02', mech = 0
    PAR_MECH                        0
    PAR_NAME                        A_03
    PAR_DESC                        INPUT par. 'a_03', mech = 0
    PAR_MECH                        0
    PAR_NAME                        A_04
    PAR_DESC                        INPUT par. 'a_04', mech = 0
    PAR_MECH                        0
    PAR_NAME                        A_05
    PAR_DESC                        added INPUT par 'a_05', mech = 1
    PAR_MECH                        1
    PAR_NAME                        A_06
    PAR_DESC                        added INPUT par 'a_06', mech = 1
    PAR_MECH                        1
    PAR_NAME                        A_07
    PAR_DESC                        added INPUT par 'a_07', mech = 1
    PAR_MECH                        1
    PAR_NAME                        A_08
    PAR_DESC                        added INPUT par 'a_08', mech = 1
    PAR_MECH                        1
    PAR_NAME                        O_01
    PAR_DESC                        OUTPUT par. 'o_01', mech = 0
    PAR_MECH                        0
    PAR_NAME                        O_02
    PAR_DESC                        OUTPUT par. 'o_02', mech = 0
    PAR_MECH                        0
    PAR_NAME                        O_03
    PAR_DESC                        OUTPUT par. 'o_03', mech = 0
    PAR_MECH                        0
    PAR_NAME                        O_04
    PAR_DESC                        OUTPUT par. 'o_04', mech = 0
    PAR_MECH                        0
    PAR_NAME                        O_05
    PAR_DESC                        added OUTPUT par 'o_05', mech = 1
    PAR_MECH                        1
    PAR_NAME                        O_06
    PAR_DESC                        added OUTPUT par 'o_06', mech = 1
    PAR_MECH                        1
    PAR_NAME                        O_07
    PAR_DESC                        added OUTPUT par 'o_07', mech = 1
    PAR_MECH                        1
    PAR_NAME                        O_08
    PAR_DESC                        added OUTPUT par 'o_08', mech = 1
    PAR_MECH                        1
"""

@pytest.mark.version('>=2.5.1')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

