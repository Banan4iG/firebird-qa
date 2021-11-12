#coding:utf-8
#
# id:           functional.tabloid.dbp_4137_combo_full_join_and_windowed_funcs
# title:        Common SQL. Check correctness of the results
# decription:   
# tracker_id:   
# min_versions: ['3.0']
# versions:     3.0
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 3.0
# resources: None

substitutions_1 = [('=.*', '')]

init_script_1 = """"""

db_1 = db_factory(from_backup='tabloid-dbp-4137.fbk', init=init_script_1)

test_script_1 = """
    select x.ari ari_x, y.ari ari_y, z.ari ari_z
    from(
        select ari
        from (select ari, cv,
                max(ari)over(partition by tbi)-min(ari)over(partition by tbi) m
                from pdata b1
        ) q
        group by ari
        having sum(cv)=255*3 and max(m)=0
    ) x
    natural full join
    (
        select a.ari
        from (
            select a.*,max(rank)over(partition by tbi) max_rank
            from (
                select tbi,ari,cv,
                    rank()over(partition by tbi order by ari) rank
                from pdata b
            ) a
        ) a
        where max_rank=1
        group by ari
        having sum(cv)=765
    ) y
    natural full join
    (
        select ari
        from (
            select distinct
                ari,
                min(
                    (select min(ari) from pdata where ari<>s.ari and tbi=s.tbi)
                   ) over (partition by ari) st
            from pdata s
            where ari in
                (
                    select d.ari
                    from pdata d join ptube t on d.tbi=t.id
                    group by d.ari
                    having sum(d.cv)=255*3
                    and count(distinct t.tc)=3
                )
        ) z
        where st is null
    ) z
    order by 1,2
    ;
  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
       ARI_X        ARI_Y        ARI_Z 
           2            2            2 
          53           53           53 
          90           90           90 
  """

@pytest.mark.version('>=3.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout
