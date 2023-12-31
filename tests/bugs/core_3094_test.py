#coding:utf-8

"""
ID:          issue-3473
ISSUE:       3473
TITLE:       Parameters doesn't work with NOT IN from a selectable procedure
DESCRIPTION:
JIRA:        CORE-3094
FBTEST:      bugs.core_3094
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    create or alter procedure sp_test as begin end;
    recreate table con_miem (
        fgrupo   int,
        fmiembr  int,
        constraint con_miem_pk primary key (fgrupo, fmiembr)
    );
    recreate table con_cuen (
        fcuenta  int,
        fnombre  varchar(30),
        constraint con_cuen_pk primary key (fcuenta)
    );
    set term ^;
    create or alter procedure sp_test (grupo integer) returns (fcuenta type of column con_miem.fmiembr) as
    begin
      for select fmiembr from con_miem where fgrupo=:grupo into :fcuenta do suspend;
    end
    ^ set term ;^
    commit;

    insert into con_cuen (fcuenta, fnombre) values (5000, 'cuenta 5000');
    insert into con_cuen (fcuenta, fnombre) values (6000, 'cuenta 6000');
    insert into con_cuen (fcuenta, fnombre) values (7101, 'cuenta 7101');
    insert into con_cuen (fcuenta, fnombre) values (7102, 'cuenta 7102');
    insert into con_cuen (fcuenta, fnombre) values (7103, 'cuenta 7103');
    insert into con_cuen (fcuenta, fnombre) values (7104, 'cuenta 7104');
    insert into con_cuen (fcuenta, fnombre) values (7105, 'cuenta 7105');
    insert into con_cuen (fcuenta, fnombre) values (7106, 'cuenta 7106');
    insert into con_cuen (fcuenta, fnombre) values (7108, 'cuenta 7108');
    insert into con_cuen (fcuenta, fnombre) values (7109, 'cuenta 7109');
    insert into con_cuen (fcuenta, fnombre) values (7110, 'cuenta 7110');
    insert into con_cuen (fcuenta, fnombre) values (7111, 'cuenta 7111');
    insert into con_cuen (fcuenta, fnombre) values (7112, 'cuenta 7112');
    insert into con_cuen (fcuenta, fnombre) values (7113, 'cuenta 7113');
    insert into con_cuen (fcuenta, fnombre) values (7114, 'cuenta 7114');
    insert into con_cuen (fcuenta, fnombre) values (7115, 'cuenta 7115');
    insert into con_cuen (fcuenta, fnombre) values (7116, 'cuenta 7116');
    insert into con_cuen (fcuenta, fnombre) values (7117, 'cuenta 7117');
    insert into con_cuen (fcuenta, fnombre) values (7118, 'cuenta 7118');
    insert into con_cuen (fcuenta, fnombre) values (7119, 'cuenta 7119');


    insert into con_miem (fgrupo, fmiembr) values (100, 5000);
    insert into con_miem (fgrupo, fmiembr) values (100, 6000);
    insert into con_miem (fgrupo, fmiembr) values (100, 7101);
    insert into con_miem (fgrupo, fmiembr) values (100, 7102);
    insert into con_miem (fgrupo, fmiembr) values (100, 7103);
    insert into con_miem (fgrupo, fmiembr) values (100, 7104);
    insert into con_miem (fgrupo, fmiembr) values (100, 7105);
    insert into con_miem (fgrupo, fmiembr) values (100, 7106);
    insert into con_miem (fgrupo, fmiembr) values (100, 7108);
    insert into con_miem (fgrupo, fmiembr) values (100, 7109);
    insert into con_miem (fgrupo, fmiembr) values (100, 7110);
    insert into con_miem (fgrupo, fmiembr) values (100, 7111);
    insert into con_miem (fgrupo, fmiembr) values (100, 7112);
    insert into con_miem (fgrupo, fmiembr) values (100, 7113);
    insert into con_miem (fgrupo, fmiembr) values (100, 7114);
    insert into con_miem (fgrupo, fmiembr) values (100, 7115);
    insert into con_miem (fgrupo, fmiembr) values (100, 7116);
    insert into con_miem (fgrupo, fmiembr) values (100, 7117);
    insert into con_miem (fgrupo, fmiembr) values (100, 7118);
    insert into con_miem (fgrupo, fmiembr) values (100, 7119);
    commit;

    set list on;
    set term ^;
    execute block returns (fcuenta type of column con_miem.fmiembr, fnombre type of column con_cuen.fnombre)
    as
      declare gro integer = 100;
    begin
      for
          select fcuenta, fnombre
          from con_cuen
          where fcuenta not in ( select p.fcuenta from sp_test(:gro) p )
          into fcuenta, fnombre
      do
      begin
          suspend;
      end
    end
    ^
    set term ;^
"""

act = isql_act('db', test_script)

@pytest.mark.version('>=3')
def test_1(act: Action):
    act.execute()
