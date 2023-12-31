#coding:utf-8

"""
ID:          issue-807
ISSUE:       807
TITLE:       JOIN including a complex view kills the server
DESCRIPTION:
  NB: all versions of 2.1 and 2.5 fail on 2nd query (issue 2002-jul-12) with message about
  "too many contexts, max = 256" so this test checks only FB 3.0 and above.
JIRA:        CORE-461
FBTEST:      bugs.core_0461
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    set bail on;

    create domain d_global_id as varchar(15) not null ;
    create domain d_long_desc as varchar(200);
    create domain d_group as integer default 0 check ((value is not null));

    create domain d_global_ref as varchar(15);
    create domain d_icon as smallint check (((value is null) or (value between 0 and 8)));

    recreate table knowledgestreams (
            stream_id d_global_id not null,
            name d_long_desc,
            content_groups d_group,
            constraint pk_knowledgestreams primary key (stream_id)
    );

    recreate table mainmenu (
            menu_id d_global_id not null,
            parent_id d_global_ref,
            description d_long_desc,
            content_group d_group not null,
            icon d_icon,
            constraint pk_mainmenu primary key (menu_id)
    );

    alter table mainmenu add constraint fk_mainmenu foreign key (parent_id)
    references mainmenu(menu_id) on delete cascade on update cascade;

    recreate table menu_groups (
            menu_id d_global_id not null,
            content_id d_global_id not null
    );

    create index menu_groups_idx1 on menu_groups (menu_id);
    create index menu_groups_idx2 on menu_groups (content_id);

    recreate table streammenu (
            stream_id d_global_id not null,
            parent d_global_id not null,
            constraint pk_streammenu primary key (parent, stream_id)
    );

    alter table streammenu add constraint fk_streammenu_parent foreign key
    (parent) references mainmenu(menu_id) on delete cascade;

    alter table streammenu add constraint fk_streammenu_stream_id foreign
    key (stream_id) references knowledgestreams(stream_id) on delete
    cascade;

    create view fullmenu (
        code,
        parent,
        description,
        link,
        content_group
    ) as
    select menu_id,parent_id,description,cast(null as
    varchar(100)),content_group from mainmenu
    union all
    select m.stream_id, m.parent, s.name
    ,cast('/servlets/uk.co.wmeng.intelus.knowledgestream?action=display&amp;id='
    || s.stream_id as varchar(100)),content_groups from streammenu m join
    knowledgestreams s on s.stream_id = m.stream_id
    ;

    -------------------------------------------------

    create table drzava
    (
        pozivnibrojdrzave varchar(4) not null,
        nazivdrzave varchar(20),
        grupa integer not null,
        primary key (pozivnibrojdrzave)
    );

    create table log
    (
        broj varchar(25) not null,
        pocetak timestamp not null,
        trajanje integer not null,
        lokal integer,
        linija integer,
        cena numeric(8,2) not null
    );

    create table lokal
    (
        brojlokala integer not null,
        nazivlokala varchar(25) not null,
        primary key (brojlokala)
    );

    create table mesni
    (
        ptt char(5) not null,
        lokalniprefix varchar(5) not null,
        primary key (ptt, lokalniprefix)
    );

    create table mreza
    (
        brojmreze varchar(4) not null,
        pozivnibroj varchar(4) not null,
        zona integer not null,
        primary key (brojmreze, pozivnibroj)
    );

    create table vrstart
    (
    sifravrt char(7) not null,
    nazivvrt varchar(30) not null,
    jm varchar(6),
    primary key (sifravrt)
    );

    create table poslovnica
    (
    sifraposlovnice char(2) not null,
    nazivposlovnice varchar(18) not null,
    primary key (sifraposlovnice)
    );

    create table rezijskitrosak
    (
    rednibroj integer not null,
    datumtroska timestamp not null,
    sifraposlovnice char(2) not null references
    poslovnica (sifraposlovnice) on update cascade,
    sifravrt char(7) not null references vrstart
    (sifravrt) on update cascade,
    kolicina decimal(8,2),
    iznos decimal(8,2) not null,
    primary key (rednibroj)
    );

    create generator gen_rt_id;
    set generator gen_rt_id to 0;

    create table vrstamt
    (
    sifravmt char(7) not null,
    nazivvmt varchar(30) not null,
    defaultjm varchar(6),
    primary key (sifravmt)
    );

    create table roba
    (
    sifrarobe char(6) not null,
    vrstarobe char(7) not null references vrstamt
    (sifravmt) on update cascade,
    nazivrobe varchar(30) not null,
    jm varchar(6) not null,
    barcode varchar(50),
    pakovanje integer,
    napomena varchar(100),
    primary key (sifrarobe)
    );

    create table mesto
    (
    ptt char(5) not null,
    nazivmesta varchar(40) not null,
    pozivnibroj char(4),
    primary key (ptt)
    );

    create table komitent
    (
    sifrakomitenta integer not null,
    naziv varchar(25) not null ,
    ptt char(5) not null references mesto
    (ptt) on update cascade,
    napomena varchar(100),
    owner char(8),
    primary key (sifrakomitenta)
    );

    create generator gen_komitent_id;
    set generator gen_komitent_id to 0;

    create table vrstadetalja
    (
    sifravd integer not null,
    opisvd varchar(15),
    telefon char(1),
    check (telefon is null or telefon = 'd' or telefon = 'z'),
    primary key(sifravd)
    );

    create generator gen_vrstadetalja_id;
    set generator gen_vrstadetalja_id to 0;

    create table komitentdetaljno
    (
    sifrakd integer not null,
    sifrakomitenta integer not null references komitent
    (sifrakomitenta) on update cascade on delete
    cascade,
    sifravd integer not null references
    vrstadetalja (sifravd) on update cascade,
    podatak varchar(40) not null,
    cistbroj varchar(25),
    primary key(sifrakd)
    );

    create generator gen_komitentdetaljno_id;
    set generator gen_komitentdetaljno_id to 0;

    create table prijem
    (
    brdok integer not null,
    datumulaza timestamp not null,
    sifrakomitenta integer references komitent
    (sifrakomitenta) on update cascade,
    primary key (brdok)
    );

    create generator gen_prij_id;
    set generator gen_prij_id to 0;

    create table prijemst
    (
    brdok integer not null references prijem
    (brdok) on update cascade on delete cascade,
    sifrarobe char(6) not null references roba
    (sifrarobe) on update cascade,
    kolicina decimal(8,2) not null,
    cena decimal(8,2) not null,
    primary key (brdok, sifrarobe)
    );

    create table alokacija
    (
    brdok integer not null,
    datum timestamp not null,
    sifraposlovnice char(2) not null references poslovnica
    (sifraposlovnice) on update cascade,
    primary key (brdok)
    );

    create generator gen_alok_id;
    set generator gen_alok_id to 1;

    create table alokacijast
    (
    brdok integer not null references alokacija
    (brdok) on update cascade on delete cascade,
    sifrarobe char(6) not null references roba
    (sifrarobe) on update cascade,
    kolicina decimal(8,2) not null,
    cena decimal(8,2) not null,
    primary key (brdok, sifrarobe)
    );

    create table vrstagoriva
    (
        sifravrstegoriva integer not null,
        nazivvrstegoriva varchar(10) not null,
        primary key (sifravrstegoriva)
    );


    create table vrstavozila
    (
        sifravrste char(2) not null,
        nazivvrste varchar(18) not null,
        primary key (sifravrste)
    );

    create table vozilo
    (
        sifravozila char(12) not null,
        sifravrste char(2) not null references
    vrstavozila (sifravrste) on update cascade,
        regbroj char(10),
        marka char(10),
        tip char(20),
        brojsasije char(25),
        brojmotora char(25),
        prvaregistracija timestamp,
        snagamotora decimal(10,2),
        zapremina integer,
        nosivost integer,
        mestazasedenje char(4),
        karoserija char(25),
        boja char(20),
        brojosovina char(1),
        rokppaparata timestamp,

        primary key (sifravozila)
    );

    create table vozac
    (
        sifravozaca integer not null,
        ime char(25) not null,
        kategorije char(5) not null,
        datumvazenjadozvole timestamp,

        primary key (sifravozaca)
    );


    create table sipanjegoriva
    (
        sifrasg integer not null,
        datum timestamp not null,
        sifravozila char(12) not null references vozilo
    (sifravozila) on update cascade,
        sifravozaca integer not null references vozac
    (sifravozaca) on update cascade,
        sifravrstegoriva integer not null references
    vrstagoriva (sifravrstegoriva) on update cascade,
        sifraposlovnice char(2) not null references
    poslovnica (sifraposlovnice) on update cascade,
        kmsat decimal(9,1),
        kolicina decimal(10, 2) not null,
        cena decimal(8,2) not null,
        pundocepa char(1),
        check (pundocepa = 'n' or pundocepa = 'd'),

        primary key (sifrasg)
    );

    create generator gen_gorivo_id;
    set generator gen_gorivo_id to 1;

    create table popravka
    (
        datum timestamp not null,
        sifravozila char(12) not null references vozilo
    (sifravozila) on update cascade,
        sifravozaca integer not null references vozac
    (sifravozaca) on update cascade,
        sifraposlovnice char(2) not null references
    poslovnica (sifraposlovnice) on update cascade,
        iznos decimal(12,2) not null,
        opis varchar(200),

        primary key (datum,sifravozila)
    );


    create table registracija
    (
        datum timestamp not null,
        sifravozila char(12) not null references vozilo
    (sifravozila) on update cascade,
        cenatehnickog decimal(12,2),
        cenaosiguranja decimal(12,2),
        ostalitroskovi decimal(12,2),
        sifraposlovnice char(2) not null references
    poslovnica (sifraposlovnice) on update cascade,

        primary key (datum,sifravozila)
    );

    create table dummy
    (
        foobar integer not null primary key,
        check (foobar = 1)
    );

    insert into dummy values (1);


    /* then, i create few views to make summary report */

    create view apromet(datum, so, vrsta, iznos)
    as

    select rt.datumtroska, sifraposlovnice, cast
    (vrt.nazivvrt as varchar
    (30)), cast (rt.iznos as numeric(18, 2))
    from rezijskitrosak rt
    left join vrstart vrt on rt.sifravrt = vrt.sifravrt

    union all

    select al.datum, sifraposlovnice, cast ('kancmat'
    as varchar(30)),
    cast(sum(alst.kolicina * alst.cena) as numeric(18, 2))
    from alokacijast alst
    left join alokacija al on alst.brdok=al.brdok
    left join roba r on alst.sifrarobe = r.sifrarobe
    where r.vrstarobe = 'km'
    group by al.datum, sifraposlovnice

    union all

    select al.datum, sifraposlovnice, cast ('hemikalije'
    as varchar(30)),
    cast(sum(alst.kolicina * alst.cena) as numeric(18, 2))
    from alokacijast alst
    left join alokacija al on alst.brdok=al.brdok
    left join roba r on alst.sifrarobe = r.sifrarobe
    where r.vrstarobe = 'he'
    group by al.datum, sifraposlovnice

    union all

    select al.datum, sifraposlovnice, cast ('prehrana'
    as varchar(30)),
    cast(sum(alst.kolicina * alst.cena) as numeric(18, 2))
    from alokacijast alst
    left join alokacija al on alst.brdok=al.brdok
    left join roba r on alst.sifrarobe = r.sifrarobe
    where r.vrstarobe = 'hr'
    group by al.datum, sifraposlovnice
    union all

    select pp.datum, sifraposlovnice, cast ('popravke'
    as varchar(30)),
    cast(sum(iznos) as numeric(18,2))
    from popravka pp
    group by pp.datum, sifraposlovnice

    union all

    select rg.datum, sifraposlovnice, cast ('registracije'
    as varchar
    (30)), cast(sum(cenatehnickog + cenaosiguranja +
    ostalitroskovi) as
    numeric(18,2))
    from registracija rg
    group by rg.datum, sifraposlovnice

    union all

    select sg.datum, sifraposlovnice, cast ('gorivo' as
    varchar(30)), cast
    (sum(kolicina * cena) as numeric(18,2))
    from sipanjegoriva sg
    group by sg.datum, sifraposlovnice
    ;


    create view vv(vrsta)
    as
    select distinct vrsta
    from apromet a
    ;

    -------------------------------------------------

    set list on;

    select distinct fm.code, fm.description, fm.link
    from fullmenu fm
    join menu_groups mg on fm.code = mg.menu_id
    ;

    select 'Query from issue 2000-oct-18 passed OK' as msg from rdb$database;

    -------------------------------------------------

    select
        vv.vrsta,
        (select sum(ap.iznos) from apromet ap where ap.vrsta =
        vv.vrsta and
        extract(month from ap.datum)=1),
        (select sum(ap.iznos) from apromet ap where ap.vrsta =
        vv.vrsta and
        extract(month from ap.datum)=2),
        (select sum(ap.iznos) from apromet ap where ap.vrsta =
        vv.vrsta and
        extract(month from ap.datum)=3),
        (select sum(ap.iznos) from apromet ap where ap.vrsta =
        vv.vrsta and
        extract(month from ap.datum)=4),
        (select sum(ap.iznos) from apromet ap where ap.vrsta =
        vv.vrsta and
        extract(month from ap.datum)=5),
        (select sum(ap.iznos) from apromet ap where ap.vrsta =
        vv.vrsta and
        extract(month from ap.datum)=6),
        (select sum(ap.iznos) from apromet ap where ap.vrsta =
        vv.vrsta and
        extract(month from ap.datum)=7),
        (select sum(ap.iznos) from apromet ap where ap.vrsta =
        vv.vrsta and
        extract(month from ap.datum)=8),
        (select sum(ap.iznos) from apromet ap where ap.vrsta =
        vv.vrsta and
        extract(month from ap.datum)=9),
        (select sum(ap.iznos) from apromet ap where ap.vrsta =
        vv.vrsta and
        extract(month from ap.datum)=10),
        (select sum(ap.iznos) from apromet ap where ap.vrsta =
        vv.vrsta and
        extract(month from ap.datum)=11),
        (select sum(ap.iznos) from apromet ap where ap.vrsta =
        vv.vrsta and
        extract(month from ap.datum)=12),
        (select sum(ap.iznos) from apromet ap where ap.vrsta = vv.vrsta)
    from vv
    ;

    select 'Query from issue 2002-jul-12 passed OK' as msg from rdb$database;
"""

act = isql_act('db', test_script)

expected_stdout = """
    MSG                             Query from issue 2000-oct-18 passed OK
    MSG                             Query from issue 2002-jul-12 passed OK
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

