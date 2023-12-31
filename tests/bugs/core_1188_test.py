#coding:utf-8

"""
ID:          issue-1613
ISSUE:       1613
TITLE:       Select Starting with :Param (Empty string) doesn't work if using index with many fields
DESCRIPTION:
JIRA:        CORE-1188
FBTEST:      bugs.core_1188
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    -- NB! As of 17.04.2015 this ticket resolves trouble only for FB-3.0.
    -- Build WI-V2.5.4.26857 returns NO rows!
    -- 23.10.2016: WI-V2.5.7.27026 - result the same (bad).

    set list on;

    -- from core-1188:
    recreate table test_1(
        f01 varchar(10),
        f02 varchar(10)
    );
    commit;
    insert into test_1 values('a','b');
    commit;
    create index test_1_idx on test_1(f01,f02);
    commit;


    set term ^;
    execute block returns(
        msg varchar(10),
        f01 type of column test_1.f01,
        f02 type of column test_1.f02
        ) as
        declare v_stt1 varchar(255);
    begin
        msg='test_1';
        v_stt1 = 'select f01, f02 from test_1 where f01=''a'' and f02 starting with ?';
        for
            execute statement(v_stt1) ('')
            into f01, f02
        do
            suspend;
    end
    ^
    set term ;^


    -- from core-3971:
    recreate table test_2 (
        field_id integer not null,
        field_desc varchar(10) not null,
        field_sel smallint not null
    );

    create index test_2_idx1 on test_2 (field_id, field_desc);
    create index test_2_idx2 on test_2 (field_sel, field_desc);
    commit;

    insert into test_2 (field_id, field_desc, field_sel)
                   values (1, '', 1);
    insert into test_2 (field_id, field_desc, field_sel)
                   values (2, '', 1);
    insert into test_2 (field_id, field_desc, field_sel)
                   values (3, 'b', 1);

    set term ^;
    execute block returns(
        msg varchar(10),
        f01 type of column test_2.field_id,
        f02 type of column test_2.field_desc,
        f03 type of column test_2.field_sel
        ) as
        declare v_stt varchar(255);
    begin
        msg = 'test_2';
        v_stt = 'select field_id, ''>''||field_desc||''<'', field_sel'
                ||' from test_2'
                || ' where field_sel = 1 and field_desc starting with ? ';

        for
            execute statement(v_stt) ('')
            into f01, f02, f03
        do
            suspend;
    end
    ^
    set term ;^
"""

act = isql_act('db', test_script)

expected_stdout = """
    MSG                             test_1
    F01                             a
    F02                             b

    MSG                             test_2
    F01                             1
    F02                             ><
    F03                             1

    MSG                             test_2
    F01                             2
    F02                             ><
    F03                             1

    MSG                             test_2
    F01                             3
    F02                             >b<
    F03                             1
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

