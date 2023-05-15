#coding:utf-8

"""
ID:          issue-7218
ISSUE:       https://github.com/FirebirdSQL/firebird/issues/7218
TITLE:       Let ISQL show per-table run-time statistics.
NOTES:
    [23.02.2023] pzotov
    Checked on 5.0.0.958.
"""

import pytest
from firebird.qa import *
from pathlib import Path

db = db_factory(charset = 'utf8')

act = python_act('db', substitutions=[('in file .*', 'in file XXX')])

non_ascii_ddl='''
     set bail on;
     recreate table "склад" (
          id int
         ,amt numeric(12,2)
         ,grp_id int
         ,constraint "склад_ПК" primary key (id)
     );

     recreate table "справочник групп изделий используемых в ремонте спецавтомобилей" (
          id int
         ,grp varchar(155)
         ,constraint "справочник групп изделий используемых в ремонте спецавтомоб__ПК" primary key (id)
     );

     recreate view "группы_изд" as select * from "справочник групп изделий используемых в ремонте спецавтомобилей";

     recreate view "Электрика" ("ид изделия", "Запас") as
     select
          s.id
         ,s.amt
     from "склад" s
     join "группы_изд" g on s.grp_id = g.id
     where g.grp = 'Электрика'
     ;
     commit;

     -------------------------------------------------
     insert into "группы_изд" values(1, 'Метизы');
     insert into "группы_изд" values(2, 'ГСМ');
     insert into "группы_изд" values(3, 'Электрика');
     insert into "группы_изд" values(4, 'Лако-красочные материалы');
     -------------------------------------------------
     insert into "склад"(id, amt, grp_id) values (1, 111, 1);
     insert into "склад"(id, amt, grp_id) values (2, 222, 3);
     insert into "склад"(id, amt, grp_id) values (3, 333, 1);
     insert into "склад"(id, amt, grp_id) values (4, 444, 3);
     insert into "склад"(id, amt, grp_id) values (5, 555, 3);
     insert into "склад"(id, amt, grp_id) values (7, 777, 1);
     commit;

     SET PER_TABLE_STATS ON;
     set list on;
     select count(*) as "Всего номенклатура электрики, шт." from "Электрика";
'''

tmp_file = temp_file('non_ascii_ddl.sql')

expected_stdout = """
    Всего номенклатура электрики, шт. 3
    Per table statistics:
    ----------------------------------------------------------------+---------+---------+---------+---------+---------+---------+---------+---------+
    Table name                                                     | Natural | Index   | Insert  | Update  | Delete  | Backout | Purge   | Expunge |
    ----------------------------------------------------------------+---------+---------+---------+---------+---------+---------+---------+---------+
    RDB$FIELDS                                                      |         |        2|         |         |         |         |         |         |
    RDB$RELATION_FIELDS                                             |         |        4|         |         |         |         |         |         |
    RDB$RELATIONS                                                   |         |        3|         |         |         |         |         |         |
    RDB$SECURITY_CLASSES                                            |         |        1|         |         |         |         |         |         |
    склад                                                           |        6|         |         |         |         |         |         |         |
    справочник групп изделий используемых в ремонте спецавтомобилей |        4|         |         |         |         |         |         |         |
    ----------------------------------------------------------------+---------+---------+---------+---------+---------+---------+---------+---------+
"""

@pytest.mark.version('>=5.0')
def test_1(act: Action, tmp_file: Path):
    tmp_file.write_bytes(non_ascii_ddl.encode('cp1251'))

    act.expected_stdout = expected_stdout
    # !NB! run with charset:
    act.isql(switches=['-q'], combine_output = True, input_file = tmp_file, charset = 'win1251', io_enc = 'cp1251')
    assert act.clean_stdout == act.clean_expected_stdout
