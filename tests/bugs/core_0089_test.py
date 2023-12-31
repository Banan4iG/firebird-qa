#coding:utf-8

"""
ID:          issue-414
ISSUE:       414
TITLE:       Wrong return from simple SQL
DESCRIPTION:
JIRA:        CORE-89
FBTEST:      bugs.core_0089
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    -- DDL and data are based on text file (report) that is attached to ticket.
    -- No difference between FB 1.5.6 and 4.0.0 found.
    -- Added PK on table categorygroup and index "schemacategories(typecol)"
    -- after analyzing text of queries - it seems to me that such indices
    -- does exist on real schema.

    recreate table schemacategories(
        schemanr int
        ,catnr int
        ,typecol int
        ,depnr int
        ,ownedby int
        ,heritage char(4)
    );
    commit;
    create index sch_cat_typecol on schemacategories(typecol);

    recreate table categorygroup(
        id int primary key
        ,parent int
        ,depnr int
        ,heritage char(4)
        ,activecol int
        ,displaytype int
    );
    commit;

    insert into schemacategories values(11, 472, 10, 1, 10000175, 'TRUE');
    insert into schemacategories values(11, 463, 10, 1, 10000175, 'TRUE');
    insert into schemacategories values(11, 464, 10, 1, 10000175, 'TRUE');
    insert into schemacategories values(11, 497, 4, 1, 10000175, 'TRUE');
    insert into schemacategories values(11, 501, 4, 1, 10000175, 'TRUE');
    insert into schemacategories values(11, 296, 4, 1, 10000175, 'TRUE');
    insert into schemacategories values(11, 265, 4, 1, 10000175, 'TRUE');
    insert into schemacategories values(11, 496, 4, 1, 10000175, 'TRUE');
    insert into schemacategories values(11, 500, 4, 1, 10000175, 'TRUE');
    insert into schemacategories values(11, 498, 4, 1, 10000175, 'TRUE');
    insert into schemacategories values(11, 499, 4, 1, 10000175, 'TRUE');
    insert into schemacategories values(11, 494, 4, 1, 10000175, 'TRUE');
    insert into schemacategories values(11, 261, 4, 1, 10000175, 'TRUE');
    insert into schemacategories values(11, 495, 4, 1, 10000175, 'TRUE');
    insert into schemacategories values(11, 413, 5, 1, 10000175, 'TRUE');
    insert into schemacategories values(11, 244, 5, 1, 10000175, 'TRUE');
    insert into schemacategories values(11, 488, 5, 1, 10000175, 'TRUE');
    insert into schemacategories values(11, 492, 5, 1, 10000175, 'TRUE');
    insert into schemacategories values(11, 249, 5, 1, 10000175, 'TRUE');
    insert into schemacategories values(11, 493, 5, 1, 10000175, 'TRUE');
    insert into schemacategories values(11, 247, 5, 1, 10000175, 'TRUE');
    insert into schemacategories values(11, 502, 6, 1, 10000175, 'TRUE');
    insert into schemacategories values(11, 251, 6, 1, 10000175, 'TRUE');
    insert into schemacategories values(11, 490, 6, 1, 10000175, 'TRUE');
    insert into schemacategories values(11, 367, 6, 1, 10000175, 'TRUE');
    insert into schemacategories values(11, 489, 6, 1, 10000175, 'TRUE');
    insert into schemacategories values(11, 505, 5, 1, 10000175, 'TRUE');
    insert into schemacategories values(11, 506, 4, 1, 10000175, 'TRUE');
    insert into schemacategories values(11, 507, 5, 1, 10000175, 'TRUE');
    insert into schemacategories values(11, 508, 5, 1, 10000175, 'TRUE');
    insert into schemacategories values(11, 509, 5, 1, 10000175, 'TRUE');
    insert into schemacategories values(11, 491, 6, 1, 10000175, 'TRUE');
    insert into schemacategories values(11, 450, 1, 1, 10000090, 'TRUE');
    insert into schemacategories values(11, 485, 1, 1, 10000090, 'TRUE');
    insert into schemacategories values(11, 486, 1, 1, 10000090, 'TRUE');
    insert into schemacategories values(11, 451, 1, 1, 10000090, 'TRUE');
    insert into schemacategories values(11, 452, 1, 1, 10000090, 'TRUE');
    insert into schemacategories values(11, 453, 1, 1, 10000090, 'TRUE');
    insert into schemacategories values(11, 454, 1, 1, 10000090, 'TRUE');
    insert into schemacategories values(11, 455, 1, 1, 10000090, 'TRUE');
    insert into schemacategories values(11, 456, 1, 1, 10000090, 'TRUE');
    commit;


    insert into categorygroup  values(1,0,1,'TRUE',1,1);
    insert into categorygroup  values(2,0,1,'TRUE',1,2);
    insert into categorygroup  values(3,0,1,'TRUE',1,2);
    insert into categorygroup  values(4,0,1,'TRUE',1,3);
    insert into categorygroup  values(5,0,1,'TRUE',1,3);
    insert into categorygroup  values(6,0,1,'TRUE',1,3);
    insert into categorygroup  values(7,0,1,'TRUE',1,2);
    insert into categorygroup  values(8,5,1,'TRUE',0,3);
    insert into categorygroup  values(9,0,1,'TRUE',1,2);
    insert into categorygroup  values(10,0,1,'TRUE',1,2);
    commit;

    set list on;
    select sc.schemanr,sc.catnr,sc.typecol,cg.id
    from schemacategories sc, categorygroup cg
    where sc.schemanr = 11 and sc.typecol = cg.id
    order by sc.catnr;
"""

act = isql_act('db', test_script)

expected_stdout = """
    SCHEMANR                        11
    CATNR                           244
    TYPECOL                         5
    ID                              5

    SCHEMANR                        11
    CATNR                           247
    TYPECOL                         5
    ID                              5

    SCHEMANR                        11
    CATNR                           249
    TYPECOL                         5
    ID                              5

    SCHEMANR                        11
    CATNR                           251
    TYPECOL                         6
    ID                              6

    SCHEMANR                        11
    CATNR                           261
    TYPECOL                         4
    ID                              4

    SCHEMANR                        11
    CATNR                           265
    TYPECOL                         4
    ID                              4

    SCHEMANR                        11
    CATNR                           296
    TYPECOL                         4
    ID                              4

    SCHEMANR                        11
    CATNR                           367
    TYPECOL                         6
    ID                              6

    SCHEMANR                        11
    CATNR                           413
    TYPECOL                         5
    ID                              5

    SCHEMANR                        11
    CATNR                           450
    TYPECOL                         1
    ID                              1

    SCHEMANR                        11
    CATNR                           451
    TYPECOL                         1
    ID                              1

    SCHEMANR                        11
    CATNR                           452
    TYPECOL                         1
    ID                              1

    SCHEMANR                        11
    CATNR                           453
    TYPECOL                         1
    ID                              1

    SCHEMANR                        11
    CATNR                           454
    TYPECOL                         1
    ID                              1

    SCHEMANR                        11
    CATNR                           455
    TYPECOL                         1
    ID                              1

    SCHEMANR                        11
    CATNR                           456
    TYPECOL                         1
    ID                              1

    SCHEMANR                        11
    CATNR                           463
    TYPECOL                         10
    ID                              10

    SCHEMANR                        11
    CATNR                           464
    TYPECOL                         10
    ID                              10

    SCHEMANR                        11
    CATNR                           472
    TYPECOL                         10
    ID                              10

    SCHEMANR                        11
    CATNR                           485
    TYPECOL                         1
    ID                              1

    SCHEMANR                        11
    CATNR                           486
    TYPECOL                         1
    ID                              1

    SCHEMANR                        11
    CATNR                           488
    TYPECOL                         5
    ID                              5

    SCHEMANR                        11
    CATNR                           489
    TYPECOL                         6
    ID                              6

    SCHEMANR                        11
    CATNR                           490
    TYPECOL                         6
    ID                              6

    SCHEMANR                        11
    CATNR                           491
    TYPECOL                         6
    ID                              6

    SCHEMANR                        11
    CATNR                           492
    TYPECOL                         5
    ID                              5

    SCHEMANR                        11
    CATNR                           493
    TYPECOL                         5
    ID                              5

    SCHEMANR                        11
    CATNR                           494
    TYPECOL                         4
    ID                              4

    SCHEMANR                        11
    CATNR                           495
    TYPECOL                         4
    ID                              4

    SCHEMANR                        11
    CATNR                           496
    TYPECOL                         4
    ID                              4

    SCHEMANR                        11
    CATNR                           497
    TYPECOL                         4
    ID                              4

    SCHEMANR                        11
    CATNR                           498
    TYPECOL                         4
    ID                              4

    SCHEMANR                        11
    CATNR                           499
    TYPECOL                         4
    ID                              4

    SCHEMANR                        11
    CATNR                           500
    TYPECOL                         4
    ID                              4

    SCHEMANR                        11
    CATNR                           501
    TYPECOL                         4
    ID                              4

    SCHEMANR                        11
    CATNR                           502
    TYPECOL                         6
    ID                              6

    SCHEMANR                        11
    CATNR                           505
    TYPECOL                         5
    ID                              5

    SCHEMANR                        11
    CATNR                           506
    TYPECOL                         4
    ID                              4

    SCHEMANR                        11
    CATNR                           507
    TYPECOL                         5
    ID                              5

    SCHEMANR                        11
    CATNR                           508
    TYPECOL                         5
    ID                              5

    SCHEMANR                        11
    CATNR                           509
    TYPECOL                         5
    ID                              5
"""

@pytest.mark.version('>=3')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

