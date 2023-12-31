#coding:utf-8

"""
ID:          issue-1510
ISSUE:       1510
TITLE:       Wrong ordering with views, distinct, left join and order by
DESCRIPTION:
JIRA:        CORE-1089
FBTEST:      bugs.core_1089
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    create table fat(
        idxxfat varchar(26) not null,
        progfat int,
        idxxccb varchar(20),
        ndonfat int,
        constraint pk$_fat primary key (idxxfat)
    );
    create table sca(
        idxxsca varchar(16) not null,
        progsca int,
        idxxfat varchar(26),
        constraint pk$_sca primary key (idxxsca)
    );
    commit;

    create view vw$_sca as
    select distinct
        sca.idxxsca,
        sca.progsca,
        sca.idxxfat,
        fat.idxxccb,
        fat.ndonfat
    from sca
    left join fat on sca.idxxfat=fat.idxxfat;


    insert into fat (idxxfat,progfat,idxxccb,ndonfat) values('2007.1',1,'y',1002);
    insert into fat (idxxfat,progfat,idxxccb,ndonfat) values('2007.2',2,'x',1001);
    commit;

    insert into sca (idxxsca,progsca,idxxfat) values ('2007.4',4,'2007.1');
    insert into sca (idxxsca,progsca,idxxfat) values ('2007.3',3,'2007.1');
    insert into sca (idxxsca,progsca,idxxfat) values ('2007.2',2,'2007.2');
    insert into sca (idxxsca,progsca,idxxfat) values ('2007.1',1,'2007.2');
    commit;

    -- test-1:
    set list on;
    select 'test-1' as msg, v.*
    from vw$_sca v
    order by 2 desc;
    commit;

    ------------------------------------
    -- Sample from core-2863 (wrong output confirmed on 2.1.0.17798):

    recreate view test_view as select 1 i from rdb$database;
    commit;

    recreate table test_table(myfield integer);

    recreate view test_view(myfield1, myfield2) as
    select distinct m.myfield, s.myfield
    from test_table m
    left join test_table s on m.myfield = s.myfield;
    commit;

    insert into test_table values (1);
    insert into test_table values (2);

    commit;

    set list on;

    select 'test-2' as msg, v.*
    from test_view v
    order by myfield1 desc;
    commit;

"""

act = isql_act('db', test_script)

expected_stdout = """
    MSG                             test-1
    IDXXSCA                         2007.4
    PROGSCA                         4
    IDXXFAT                         2007.1
    IDXXCCB                         y
    NDONFAT                         1002

    MSG                             test-1
    IDXXSCA                         2007.3
    PROGSCA                         3
    IDXXFAT                         2007.1
    IDXXCCB                         y
    NDONFAT                         1002

    MSG                             test-1
    IDXXSCA                         2007.2
    PROGSCA                         2
    IDXXFAT                         2007.2
    IDXXCCB                         x
    NDONFAT                         1001

    MSG                             test-1
    IDXXSCA                         2007.1
    PROGSCA                         1
    IDXXFAT                         2007.2
    IDXXCCB                         x
    NDONFAT                         1001


    MSG                             test-2
    MYFIELD1                        2
    MYFIELD2                        2

    MSG                             test-2
    MYFIELD1                        1
    MYFIELD2                        1
"""

@pytest.mark.version('>=3')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

