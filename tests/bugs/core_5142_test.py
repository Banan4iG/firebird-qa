#coding:utf-8

"""
ID:          issue-5425
ISSUE:       5425
TITLE:       Error "no current record to fetch" if some record is to be deleted both by
  the statement itself and by some trigger fired during statement execution
DESCRIPTION:
JIRA:        CORE-5142
FBTEST:      bugs.core_5142
"""

import pytest
from firebird.qa import *

init_script = """
    recreate table test(id int);
    commit;

    recreate sequence test_id_gen;
    commit;

    recreate table test (
        id                 integer not null,
        ltjahr             integer,
        ltkw               integer,
        auftragsjahr       integer,
        auftragsnr         integer,
        kwtag              integer,
        stck_je_std        double precision,
        stck_je_tag        integer,
        stck_je_lkw        integer,
        palette_je_lkw     integer,
        erg_std_tag        double precision,
        status             integer,
        teilenr            varchar(16) character set iso8859_1 collate de_de,
        erg_std_datensatz  double precision,
        ap                 integer,
        arbgang            integer,
        prio               integer,
        bemerkung          varchar(200) character set iso8859_1 collate de_de,
        abgearbeitet       integer,
        menge_ist          double precision,
        ps2                integer,
        id_autoins         integer,
        schistaerke        varchar(6) character set iso8859_1 collate de_de
    );
    commit;

    alter table test add constraint pk_test primary key (id);
    create index idx_test on test(kwtag);
    create index idx_test1 on test(erg_std_datensatz);

    set term ^ ;
    create or alter trigger ai_test_id for test
    active before insert position 0
    as
    begin
      if (new.id is null) then
          new.id = gen_id(test_id_gen, 1);
    end
    ^

    create or alter trigger test_ad for test
    active after delete position 0
    as
    begin
      if(old.ap = 69) then
      begin
        delete from test where id_autoins = old.id;
      end
    end
    ^
    set term ;^
    commit;
"""

db = db_factory(charset='ISO8859_1', init=init_script)

test_script = """
    insert into test (id, ltjahr, ltkw, auftragsjahr, auftragsnr, kwtag, stck_je_std, stck_je_tag, stck_je_lkw, palette_je_lkw, erg_std_tag, status, teilenr, erg_std_datensatz, ap, arbgang, prio, bemerkung, abgearbeitet, menge_ist, ps2, id_autoins, schistaerke)
    values(1, 2016, 11, 2016, 2953, 7, 15, 2, null, null, null, null, 'must-aip-revi/1', 0.133333333333333, 15, 4, null, null, 0, null, 0, null, null);
    insert into test (id, ltjahr, ltkw, auftragsjahr, auftragsnr, kwtag, stck_je_std, stck_je_tag, stck_je_lkw, palette_je_lkw, erg_std_tag, status, teilenr, erg_std_datensatz, ap, arbgang, prio, bemerkung, abgearbeitet, menge_ist, ps2, id_autoins, schistaerke)
    values(2, 2016, 11, 2016, 2953, 7, 15, 2, null, null, null, null, 'must-aip-revi/1', 0.133333333333333, 15, 5, null, null, 0, null, 0, null, null);
    insert into test (id, ltjahr, ltkw, auftragsjahr, auftragsnr, kwtag, stck_je_std, stck_je_tag, stck_je_lkw, palette_je_lkw, erg_std_tag, status, teilenr, erg_std_datensatz, ap, arbgang, prio, bemerkung, abgearbeitet, menge_ist, ps2, id_autoins, schistaerke)
    values(3, 2016, 11, 2016, 2953, 7, 15, 2, null, null, null, null, 'must-aip-revit', 0.133333333333333, 15, 2, null, null, 0, null, 0, null, null);
    insert into test (id, ltjahr, ltkw, auftragsjahr, auftragsnr, kwtag, stck_je_std, stck_je_tag, stck_je_lkw, palette_je_lkw, erg_std_tag, status, teilenr, erg_std_datensatz, ap, arbgang, prio, bemerkung, abgearbeitet, menge_ist, ps2, id_autoins, schistaerke)
    values(4, 2016, 11, 2016, 2953, 7, 40, 2, null, null, null, null, 'must-aip-revit', 0.05, 21, 3, null, null, 0, null, 0, null, null);
    insert into test (id, ltjahr, ltkw, auftragsjahr, auftragsnr, kwtag, stck_je_std, stck_je_tag, stck_je_lkw, palette_je_lkw, erg_std_tag, status, teilenr, erg_std_datensatz, ap, arbgang, prio, bemerkung, abgearbeitet, menge_ist, ps2, id_autoins, schistaerke)
    values(5, 2016, 11, 2016, 2953, 7, 15, 2, null, null, null, null, 'must-aip-revi/1', 0.133333333333333, 23, 3, null, null, 0, null, 0, null, null);
    insert into test (id, ltjahr, ltkw, auftragsjahr, auftragsnr, kwtag, stck_je_std, stck_je_tag, stck_je_lkw, palette_je_lkw, erg_std_tag, status, teilenr, erg_std_datensatz, ap, arbgang, prio, bemerkung, abgearbeitet, menge_ist, ps2, id_autoins, schistaerke)
    values(6, 2016, 11, 2016, 2953, 7, 60, 2, null, null, null, null, 'must-aip-revi/2', 0.0333333333333333, 23, 2, null, null, 0, null, 0, null, null);
    insert into test (id, ltjahr, ltkw, auftragsjahr, auftragsnr, kwtag, stck_je_std, stck_je_tag, stck_je_lkw, palette_je_lkw, erg_std_tag, status, teilenr, erg_std_datensatz, ap, arbgang, prio, bemerkung, abgearbeitet, menge_ist, ps2, id_autoins, schistaerke)
    values(7, 2016, 11, 2016, 2953, 7, 60, 4, null, null, null, null, 'must-aip-revi/3', 0.0666666666666667, 23, 2, null, null, 0, null, 0, null, null);
    insert into test (id, ltjahr, ltkw, auftragsjahr, auftragsnr, kwtag, stck_je_std, stck_je_tag, stck_je_lkw, palette_je_lkw, erg_std_tag, status, teilenr, erg_std_datensatz, ap, arbgang, prio, bemerkung, abgearbeitet, menge_ist, ps2, id_autoins, schistaerke)
    values(8, 2016, 11, 2016, 2953, 7, 60, 4, null, null, null, null, 'must-aip-revi/4', 0.0666666666666667, 23, 2, null, null, 0, null, 0, null, null);
    insert into test (id, ltjahr, ltkw, auftragsjahr, auftragsnr, kwtag, stck_je_std, stck_je_tag, stck_je_lkw, palette_je_lkw, erg_std_tag, status, teilenr, erg_std_datensatz, ap, arbgang, prio, bemerkung, abgearbeitet, menge_ist, ps2, id_autoins, schistaerke)
    values(9, 2016, 11, 2016, 2953, 7, 60, 4, null, null, null, null, 'must-aip-revi/5', 0.0666666666666667, 23, 2, null, null, 0, null, 0, null, null);
    insert into test (id, ltjahr, ltkw, auftragsjahr, auftragsnr, kwtag, stck_je_std, stck_je_tag, stck_je_lkw, palette_je_lkw, erg_std_tag, status, teilenr, erg_std_datensatz, ap, arbgang, prio, bemerkung, abgearbeitet, menge_ist, ps2, id_autoins, schistaerke)
    values(10, 2016, 11, 2016, 2953, 7, 60, 2, null, null, null, null, 'must-aip-revi/6', 0.0333333333333333, 23, 2, null, null, 0, null, 0, null, null);
    insert into test (id, ltjahr, ltkw, auftragsjahr, auftragsnr, kwtag, stck_je_std, stck_je_tag, stck_je_lkw, palette_je_lkw, erg_std_tag, status, teilenr, erg_std_datensatz, ap, arbgang, prio, bemerkung, abgearbeitet, menge_ist, ps2, id_autoins, schistaerke)
    values(11, 2016, 11, 2016, 2953, 7, 4, 2, null, null, 35.6060832890307, null, 'must-aip-revit-p', 0.5, 69, 1, null, null, 0, null, 0, null, null);
    insert into test (id, ltjahr, ltkw, auftragsjahr, auftragsnr, kwtag, stck_je_std, stck_je_tag, stck_je_lkw, palette_je_lkw, erg_std_tag, status, teilenr, erg_std_datensatz, ap, arbgang, prio, bemerkung, abgearbeitet, menge_ist, ps2, id_autoins, schistaerke)
    values(12, 2016, 11, 2016, 2953, 7, 13.5, 2, null, null, 35.6060832890307, null, 'must-aip-revit-p', 0.148148148148148, 69, 2, null, null, 0, null, 0, null, null);
    insert into test (id, ltjahr, ltkw, auftragsjahr, auftragsnr, kwtag, stck_je_std, stck_je_tag, stck_je_lkw, palette_je_lkw, erg_std_tag, status, teilenr, erg_std_datensatz, ap, arbgang, prio, bemerkung, abgearbeitet, menge_ist, ps2, id_autoins, schistaerke)
    values(13, 2016, 11, 2016, 2953, 7, 13.5, 2, null, null, null, null, 'must-aip-revit-p', 0.148148148148148, 67, 3, null, null, 0, null, 0, 12, null);
    insert into test (id, ltjahr, ltkw, auftragsjahr, auftragsnr, kwtag, stck_je_std, stck_je_tag, stck_je_lkw, palette_je_lkw, erg_std_tag, status, teilenr, erg_std_datensatz, ap, arbgang, prio, bemerkung, abgearbeitet, menge_ist, ps2, id_autoins, schistaerke)
    values(14, 2016, 11, 2016, 2953, 7, 3, 1, null, null, null, null, 'must-aip-revi/1', 0.333333333333333, 87, 1, null, null, 0, null, 0, null, null);
    insert into test (id, ltjahr, ltkw, auftragsjahr, auftragsnr, kwtag, stck_je_std, stck_je_tag, stck_je_lkw, palette_je_lkw, erg_std_tag, status, teilenr, erg_std_datensatz, ap, arbgang, prio, bemerkung, abgearbeitet, menge_ist, ps2, id_autoins, schistaerke)
    values(15, 2016, 11, 2016, 2953, 7, 2.4, 2, null, null, null, null, 'must-aip-revi/1', 0.833333333333333, 87, 2, null, null, 0, null, 0, null, null);
    insert into test (id, ltjahr, ltkw, auftragsjahr, auftragsnr, kwtag, stck_je_std, stck_je_tag, stck_je_lkw, palette_je_lkw, erg_std_tag, status, teilenr, erg_std_datensatz, ap, arbgang, prio, bemerkung, abgearbeitet, menge_ist, ps2, id_autoins, schistaerke)
    values(16, 2016, 11, 2016, 2953, 7, 15, 2, null, null, null, null, 'must-aip-revi/2', 0.133333333333333, 87, 1, null, null, 0, null, 0, null, null);
    insert into test (id, ltjahr, ltkw, auftragsjahr, auftragsnr, kwtag, stck_je_std, stck_je_tag, stck_je_lkw, palette_je_lkw, erg_std_tag, status, teilenr, erg_std_datensatz, ap, arbgang, prio, bemerkung, abgearbeitet, menge_ist, ps2, id_autoins, schistaerke)
    values(17, 2016, 11, 2016, 2953, 7, 24, 4, null, null, null, null, 'must-aip-revi/3', 0.166666666666667, 87, 1, null, null, 0, null, 0, null, null);
    insert into test (id, ltjahr, ltkw, auftragsjahr, auftragsnr, kwtag, stck_je_std, stck_je_tag, stck_je_lkw, palette_je_lkw, erg_std_tag, status, teilenr, erg_std_datensatz, ap, arbgang, prio, bemerkung, abgearbeitet, menge_ist, ps2, id_autoins, schistaerke)
    values(18, 2016, 11, 2016, 2953, 7, 30, 4, null, null, null, null, 'must-aip-revi/4', 0.133333333333333, 87, 1, null, null, 0, null, 0, null, null);
    insert into test (id, ltjahr, ltkw, auftragsjahr, auftragsnr, kwtag, stck_je_std, stck_je_tag, stck_je_lkw, palette_je_lkw, erg_std_tag, status, teilenr, erg_std_datensatz, ap, arbgang, prio, bemerkung, abgearbeitet, menge_ist, ps2, id_autoins, schistaerke)
    values(19, 2016, 11, 2016, 2953, 7, 60, 4, null, null, null, null, 'must-aip-revi/5', 0.0666666666666667, 87, 1, null, null, 0, null, 0, null, null);
    insert into test (id, ltjahr, ltkw, auftragsjahr, auftragsnr, kwtag, stck_je_std, stck_je_tag, stck_je_lkw, palette_je_lkw, erg_std_tag, status, teilenr, erg_std_datensatz, ap, arbgang, prio, bemerkung, abgearbeitet, menge_ist, ps2, id_autoins, schistaerke)
    values(20, 2016, 11, 2016, 2953, 7, 15, 2, null, null, null, null, 'must-aip-revi/6', 0.133333333333333, 87, 1, null, null, 0, null, 0, null, null);
    insert into test (id, ltjahr, ltkw, auftragsjahr, auftragsnr, kwtag, stck_je_std, stck_je_tag, stck_je_lkw, palette_je_lkw, erg_std_tag, status, teilenr, erg_std_datensatz, ap, arbgang, prio, bemerkung, abgearbeitet, menge_ist, ps2, id_autoins, schistaerke)
    values(21, 2016, 11, 2016, 2953, 7, 4, 2, null, null, null, null, 'must-aip-revit', 0.5, 126, 1, null, null, 0, null, 0, null, null);
    commit;

    delete from test where auftragsjahr = 2016 and auftragsnr = 2953;
"""

act = isql_act('db', test_script)

@pytest.mark.version('>=3.0.1')
def test_1(act: Action):
    act.execute()

