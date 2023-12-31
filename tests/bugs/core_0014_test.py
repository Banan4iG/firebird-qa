#coding:utf-8

"""
ID:          issue-333
ISSUE:       333
JIRA:        CORE-14
TITLE:       Trigger do it wrong
DESCRIPTION: Computed by columns inside triggers always=NULL
FBTEST:      bugs.core_0014
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    -- Works OK on 1.5.6 and up to 4.0.0.
    create domain dom_datum_vreme as timestamp not null;
    create domain dom_dokid as varchar(20) not null;
    create domain dom_jid as integer;
    create domain dom_kolicina as integer default 0;
    create domain dom_naziv as varchar(100) not null;
    create domain dom_novac as double precision  default 0;
    create domain dom_rabat as float  default 0;
    create domain dom_status as integer default 0;
    commit;

    create table ulaz_master
    (
      ulzid dom_jid not null,
      datum dom_datum_vreme not null,
      broj_racuna dom_dokid not null,
      dobid dom_jid not null,
      dobavljac dom_naziv not null,
      napid dom_jid not null,
      nacin_placanja dom_naziv not null,
      datumprispeca timestamp, -- dom_datum_vreme null ,
      vrednost dom_novac default 0,
      rvrednost dom_novac default 0,
      status dom_status default 0,
      constraint pk_ulaz_master primary key (ulzid)
    );

    create table ulaz_detalji
    (
      ulzid dom_jid not null,
      artid dom_jid not null,
      artikal dom_naziv not null,
      kolicina dom_kolicina default 0 not null,
      cena dom_novac default 0 not null,
      rabat dom_rabat default 0 not null,
      ukupno computed by (kolicina * cena),
      vratio dom_kolicina default 0,
      constraint pk_ulaz_detalji primary key (ulzid, artid)
    );


    set term ^;
    create trigger trig_ulaz_detalji_ai for ulaz_detalji
    active after insert position 0
    as
    begin

        update ulaz_master u set u.vrednost = u.vrednost + new.ukupno
        where u.ulzid = new.ulzid;

        update ulaz_master u set u.rvrednost = u.rvrednost + (1 - new.rabat/100) * new.ukupno
        where u.ulzid = new.ulzid;

    end
    ^
    set term ;^
    commit;

    -- this trigger sets fiedls to null on rc8.
    -- on rc6 it works as it should.

    insert into ulaz_master(ulzid, datum, broj_racuna, dobid, dobavljac, napid, nacin_placanja)
                     values(1000,  '19.03.2016 12:01:03', 'qwerty123', 78966, 'foo-bar', 32101, 'asd-fgh-jkl'  );
    /*
    create domain dom_datum_vreme as timestamp not null;
    create domain dom_dokid as varchar(20) not null;
    create domain dom_jid as integer;
    create domain dom_kolicina as integer default 0;
    create domain dom_naziv as varchar(100) not null;
    create domain dom_novac as double precision  default 0;
    create domain dom_rabat as float  default 0;
    create domain dom_status as integer default 0;

      datum dom_datum_vreme not null,
      broj_racuna dom_dokid not null,
      dobid dom_jid not null,
      dobavljac dom_naziv not null,
      napid dom_jid not null,
      nacin_placanja dom_naziv not null,
    */

    set list on;
    set count on;

    select
         ulzid, datum, broj_racuna, dobid, dobavljac, napid, nacin_placanja, datumprispeca
        ,cast(vrednost as numeric(10,2)) as vrednost
        ,cast(rvrednost as numeric(10,2)) as rvrednost
        ,status
    from ulaz_master;

    insert into
        ulaz_detalji(ulzid, artid, artikal, kolicina, cena, rabat, vratio)
              values(1000,  1000,  'liste',   19,        7,    30,    0);

    select
         ulzid, artid, artikal, kolicina,
         cast(cena as numeric(12,2)) as cena,
         rabat,
         cast(ukupno as numeric(12,2)) as ukupno,
         vratio
    from ulaz_detalji;

    select
         ulzid, datum, broj_racuna, dobid, dobavljac, napid, nacin_placanja, datumprispeca
        ,cast(vrednost as numeric(10,2)) as vrednost
        ,cast(rvrednost as numeric(10,2)) as rvrednost
        ,status
    from ulaz_master;

"""

act = isql_act('db', test_script)

expected_stdout = """
    ULZID                           1000
    DATUM                           2016-03-19 12:01:03.0000
    BROJ_RACUNA                     qwerty123
    DOBID                           78966
    DOBAVLJAC                       foo-bar
    NAPID                           32101
    NACIN_PLACANJA                  asd-fgh-jkl
    DATUMPRISPECA                   <null>
    VREDNOST                        0.00
    RVREDNOST                       0.00
    STATUS                          0


    Records affected: 1
    Records affected: 1

    ULZID                           1000
    ARTID                           1000
    ARTIKAL                         liste
    KOLICINA                        19
    CENA                            7.00
    RABAT                           30
    UKUPNO                          133.00
    VRATIO                          0


    Records affected: 1

    ULZID                           1000
    DATUM                           2016-03-19 12:01:03.0000
    BROJ_RACUNA                     qwerty123
    DOBID                           78966
    DOBAVLJAC                       foo-bar
    NAPID                           32101
    NACIN_PLACANJA                  asd-fgh-jkl
    DATUMPRISPECA                   <null>
    VREDNOST                        133.00
    RVREDNOST                       93.10
    STATUS                          0

    Records affected: 1
"""

@pytest.mark.version('>=3')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

