#coding:utf-8

"""
ID:          issue-2595
ISSUE:       2595
TITLE:       error in operator "and" in as clausule where
DESCRIPTION:
JIRA:        CORE-2164
FBTEST:      bugs.core_2164
"""

import pytest
from firebird.qa import *

init_script = """
    create domain dcodempresa as integer;
    create domain dcadena30 as varchar(30) default '';
    create domain dcod_anuncio as integer;
    create domain dcodmedio as integer;
    create domain dfecha as timestamp;
    create domain dentero as integer;
    create domain dimporte as numeric(10,2);
    commit;

    create table empresas (
        cod_empresa dcodempresa not null,
        nombre dcadena30,
        provincia dcadena30,
        constraint pk_empresas primary key (cod_empresa)
    );

    create table anuncios (
        cod_anuncio dcod_anuncio not null,
        descripcion dcadena30,
        cod_empresa dcodempresa not null,
        constraint pk_anuncios primary key (cod_anuncio)
    );

    create table medios (
        cod_medio dcodmedio not null,
        nombre dcadena30,
        provincia dcadena30,
        constraint pk_medios primary key (cod_medio)
    );

    create table emisiones (
        cod_anuncio dcod_anuncio not null,
        fecha dfecha,
        veces dentero,
        importe dimporte,
        cod_medio dcodmedio not null,
        constraint pk_emisiones primary key (cod_anuncio,cod_medio)
    );


    alter table anuncios add foreign key (cod_empresa) references empresas (cod_empresa) on update cascade on delete no action ;
    alter table emisiones add foreign key (cod_anuncio) references anuncios (cod_anuncio) on update cascade on delete no action ;
    alter table emisiones add foreign key (cod_medio) references medios (cod_medio) on update cascade on delete no action ;
    commit;
"""

db = db_factory(init=init_script)

test_script = """
    --------------------- data script --------------------------------------
    delete from emisiones;
    delete from anuncios;
    delete from empresas;
    delete from medios;
    commit;


    insert into empresas (cod_empresa,nombre,provincia)
                              values (1,'puleva','granada');
    insert into empresas (cod_empresa,nombre,provincia)
                              values (2,'covap','cordoba');
    insert into empresas (cod_empresa,nombre,provincia)
                              values (3,'la vega','malaga');

    insert into medios (cod_medio,nombre,provincia)
                               values (1,'diario sur','malaga');
    insert into medios (cod_medio,nombre,provincia)
                               values (2,'40 granada','granada');
    insert into medios (cod_medio,nombre,provincia)
                               values (3,'el pais','madrid');


    insert into anuncios (cod_anuncio,descripcion,cod_empresa)
                         values (1,'la mejor leche',1);
    insert into anuncios (cod_anuncio,descripcion,cod_empresa)
                         values (2,'la dieta mediterranea ',1);
    insert into anuncios (cod_anuncio,descripcion,cod_empresa)
                         values (3,'el valle de los pedroches',2);


    insert into emisiones (cod_anuncio,fecha,veces,importe,cod_medio)
                             values (1,'10/01/2007',3,25,1);
    insert into emisiones (cod_anuncio,fecha,veces,importe,cod_medio)
                             values (1,'10/11/2007',3,25,3);
    insert into emisiones (cod_anuncio,fecha,veces,importe,cod_medio)
                             values (1,'10/01/2007',4,30,2);
    insert into emisiones (cod_anuncio,fecha,veces,importe,cod_medio)
                             values (3,'11/01/2007',1,45,3);
    commit;

    -----------------------------------------------------------------

    set list on;
    set count on;
    select e.nombre,a.cod_anuncio
            from empresas e
                 inner join anuncios a on (a.cod_empresa=e.cod_empresa)
            where a.cod_anuncio not in
                          (select em.cod_anuncio
                                        from emisiones em
                                             inner join medios m on (m.cod_medio=em.cod_medio)
                                        where m.provincia<>e.provincia
                          );

    --This statement don't return any rows
    --
    --If append other subselect, it returns one row ?why?
    --The second statement is

    select e.nombre,a.cod_anuncio
            from empresas e
                 inner join anuncios a on (a.cod_empresa=e.cod_empresa)
            where a.cod_anuncio not in
                          (select em.cod_anuncio
                                        from emisiones em
                                             inner join medios m on (m.cod_medio=em.cod_medio)
                                        where m.provincia<>e.provincia
                          )
                  and ------ fails
                  a.cod_anuncio in
                          (select em1.cod_anuncio
                                        from emisiones em1
                                             inner join medios m1 on (m1.cod_medio=em1.cod_medio)
                                        where m1.provincia=e.provincia
                          );

"""

act = isql_act('db', test_script)

expected_stdout = """
    NOMBRE                          puleva
    COD_ANUNCIO                     2
    Records affected: 1
    Records affected: 0
"""

@pytest.mark.version('>=3')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

