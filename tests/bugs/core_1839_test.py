#coding:utf-8

"""
ID:          issue-2268
ISSUE:       2268
TITLE:       AV when sorting by field, calculated using recursive CTE
DESCRIPTION:
  Bug happens only when table used in CTE contains records with different formats
JIRA:        CORE-1839
FBTEST:      bugs.core_1839
"""

import pytest
from firebird.qa import *

db = db_factory(charset='UTF8')

test_script = """
    recreate table test(id int, pid int, name varchar(20));
    commit;
    insert into test values(1, null, 'earth');
        insert into test values(2, 1, 'europe');
            insert into test values(3, 2, 'Sverige');
            insert into test values(4, 2, 'Norge');
            insert into test values(5, 2, 'Dänemarks');
        insert into test values(6, 1, 'africa');
            insert into test values(7, 6, 'kenya');
            insert into test values(8, 6, 'egypt');
    commit;

    alter table test add geo char(48); ------ change records format
    commit;

        insert into test values(9, 1, 'asia', null);
            insert into test values(10, 9, 'iran', null);
            insert into test values(11, 9, 'turkey', null);
                insert into test values(12, 10, 'tehran', '35°41''46"N 51°25''23"E');
                insert into test values(13, 11, 'istanbul', '41°00''49"N 28°57''18"E');

                -- pid = 7 - kenya, 8= egypt
                insert into test values(14, 7, 'nairobi', '1°17''S 36°49"E');
                insert into test values(15, 8, 'al-qāhirah',   '30°3''0"N 31°14''0"E');

    commit;

    alter table test add full_caption computed by (
        (
            with recursive
            r as(
                select a.id, a.pid, cast(a.name as varchar(8000)) caption, a.geo, 0 as rlevel
                from test a
                where a.pid is null
                union all
                select b.id, b.pid, r.caption ||':' || b.name,  b.geo, r.rlevel+1
                --select b.id, b.pid, b.name,  b.geo, r.rlevel+1
                from test b
                join r on b.pid=r.id
            )
            ,c as(
                select id,caption||':'||geo full_name from r where geo is not null order by id desc
            )
            select full_name
            from c
            where id = test.id
        )
    );
    commit;

    alter table test ------ change records format
        add year_found smallint,
        alter geo type varchar(50),
        alter full_caption position 1,
        alter pid type bigint,
        alter id type bigint
        ;
    commit;
                -- pid=3 = sweden, 4 = norway, 5 = denmark
                insert into test values(16, 3, 'stockholm',  '59°19''46"N 18°4''7"E', 1252);
                insert into test values(17, 4, 'oslo',       '59°57"N 10°45"E', 1000);
                insert into test values(18, 5, 'København', '55°40''34"N 12°34''6"E', 1167);

    commit;

    set list on;
    select list(x.full_caption, ';') all_captions
    from (
        select trim(x.full_caption) full_caption
        from test x
        where x.full_caption is not null
        order by cast( x.full_caption as varchar(8000) )
    ) x;
    commit;
"""

act = isql_act('db', test_script, substitutions=[('ALL_CAPTIONS.*', '')])

expected_stdout = """
    ALL_CAPTIONS                    0:1
    earth:africa:egypt:al-qāhirah:30°3'0"N 31°14'0"E;earth:africa:kenya:nairobi:1°17'S 36°49"E;earth:asia:iran:tehran:35°41'46"N 51°25'23"E;earth:asia:turkey:istanbul:41°00'49"N 28°57'18"E;earth:europe:Dänemarks:København:55°40'34"N 12°34'6"E;earth:europe:Norge:oslo:59°57"N 10°45"E;earth:europe:Sverige:stockholm:59°19'46"N 18°4'7"E
"""

@pytest.mark.version('>=2.5')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

