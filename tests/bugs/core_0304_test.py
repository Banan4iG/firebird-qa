#coding:utf-8

"""
ID:          issue-637
ISSUE:       637
TITLE:       Any user can drop procedures, generators, exceptions
DESCRIPTION:
NOTES:
[24.01.2019] Added separate code for running on FB 4.0+.
  UDF usage is deprecated in FB 4+, see: ".../doc/README.incompatibilities.3to4.txt".
  Functions div, frac, dow, sdow, getExactTimestampUTC and isLeapYear got safe replacement
  in UDR library "udf_compat", see it in folder: ../plugins/udr/
[01.06.2021] Adjusted STDERR caused by fixes
    https://github.com/FirebirdSQL/firebird/pull/6833
    https://github.com/FirebirdSQL/firebird/pull/6825
    ("Correct error message for DROP VIEW")
JIRA:        CORE-304
FBTEST:      bugs.core_0304
"""

import pytest
from firebird.qa import *

# version: 3.0

db = db_factory()
tmp_user = user_factory('db', name='tmp$c0304', password='123')

test_script_1 = """

    DECLARE EXTERNAL FUNCTION strlen CSTRING(32767) RETURNS INTEGER BY VALUE ENTRY_POINT 'IB_UDF_strlen' MODULE_NAME 'ib_udf';

    create domain dm_test int;
    create collation name_coll for utf8 from unicode case insensitive;
    create sequence g_test;
    create exception e_test 'foo';
    create or alter procedure sp_test as begin end;
    create table test(id int not null, x int);
    alter table test add constraint test_pk primary key(id) using index test_pk;
    create index test_x on test(x);
    create view v_test as select * from test;
    create role manager;
    commit;

    set term ^;
    create or alter trigger test_bi for test active
    before insert position 0
    as
    begin
       new.id = coalesce(new.id, gen_id(g_test, 1) );
    end
    ^
    set term ;^
    commit;

    connect '$(DSN)' user 'tmp$c0304' password '123';

    -- All following statements should FAIL if current user is not SYSDBA:

    execute procedure sp_test;

    show sequence g_test;

    alter domain dm_test set default 123;

    alter domain dm_test set not null;

    alter domain dm_test drop not null;

    alter trigger test_bi inactive;


    alter table test add z int;

    alter table test drop constraint test_pk;

    drop index test_x;

    drop view v_test;

    drop trigger test_bi;

    drop table test;

    drop role manager;

    drop procedure sp_test;

    drop sequence g_test;

    drop exception e_test;

    drop function strlen;


    drop collation name_coll;

    rollback;
"""

act_1 = isql_act('db', test_script_1)


expected_stderr_1 = """
    Statement failed, SQLSTATE = 28000
    no permission for EXECUTE access to PROCEDURE SP_TEST

    Statement failed, SQLSTATE = 28000
    no permission for USAGE access to GENERATOR G_TEST
    There is no generator G_TEST in this database

    Statement failed, SQLSTATE = 28000
    unsuccessful metadata update
    -ALTER DOMAIN DM_TEST failed
    -no permission for ALTER access to DOMAIN DM_TEST

    Statement failed, SQLSTATE = 28000
    unsuccessful metadata update
    -ALTER DOMAIN DM_TEST failed
    -no permission for ALTER access to DOMAIN DM_TEST

    Statement failed, SQLSTATE = 28000
    unsuccessful metadata update
    -ALTER DOMAIN DM_TEST failed
    -no permission for ALTER access to DOMAIN DM_TEST

    Statement failed, SQLSTATE = 28000
    unsuccessful metadata update
    -ALTER TRIGGER TEST_BI failed
    -no permission for ALTER access to TABLE TEST

    Statement failed, SQLSTATE = 28000
    unsuccessful metadata update
    -ALTER TABLE TEST failed
    -no permission for ALTER access to TABLE TEST

    Statement failed, SQLSTATE = 28000
    unsuccessful metadata update
    -ALTER TABLE TEST failed
    -no permission for ALTER access to TABLE TEST

    Statement failed, SQLSTATE = 28000
    unsuccessful metadata update
    -DROP INDEX TEST_X failed
    -no permission for ALTER access to TABLE TEST

    Statement failed, SQLSTATE = 28000
    unsuccessful metadata update
    -DROP VIEW V_TEST failed
    -no permission for DROP access to VIEW V_TEST

    Statement failed, SQLSTATE = 28000
    unsuccessful metadata update
    -DROP TRIGGER TEST_BI failed
    -no permission for ALTER access to TABLE TEST

    Statement failed, SQLSTATE = 28000
    unsuccessful metadata update
    -DROP TABLE TEST failed
    -no permission for DROP access to TABLE TEST

    Statement failed, SQLSTATE = 28000
    unsuccessful metadata update
    -DROP ROLE MANAGER failed
    -no permission for DROP access to ROLE MANAGER

    Statement failed, SQLSTATE = 28000
    unsuccessful metadata update
    -DROP PROCEDURE SP_TEST failed
    -no permission for DROP access to PROCEDURE SP_TEST


    Statement failed, SQLSTATE = 28000
    unsuccessful metadata update
    -DROP SEQUENCE G_TEST failed
    -no permission for DROP access to GENERATOR G_TEST


    Statement failed, SQLSTATE = 28000
    unsuccessful metadata update
    -DROP EXCEPTION E_TEST failed
    -no permission for DROP access to EXCEPTION E_TEST

    Statement failed, SQLSTATE = 28000
    unsuccessful metadata update
    -DROP FUNCTION STRLEN failed
    -no permission for DROP access to FUNCTION STRLEN

    Statement failed, SQLSTATE = 28000
    unsuccessful metadata update
    -DROP COLLATION NAME_COLL failed
    -no permission for DROP access to COLLATION NAME_COLL

"""

@pytest.mark.version('>=3.0.8,<4.0')
def test_1(act_1: Action, tmp_user: User):
    act_1.expected_stderr = expected_stderr_1
    act_1.execute()
    assert act_1.clean_stderr == act_1.clean_expected_stderr

# version: 4.0

test_script_2 = """
    -- See declaration sample in plugins\\udr\\UdfBackwardCompatibility.sql:

    create function UDR40_frac (
        val double precision
    ) returns double precision
    external name 'udf_compat!UC_frac'
    engine udr;


    create domain dm_test int;
    create collation name_coll for utf8 from unicode case insensitive;
    create sequence g_test;
    create exception e_test 'foo';
    create or alter procedure sp_test as begin end;
    create table test(id int not null, x int);
    alter table test add constraint test_pk primary key(id) using index test_pk;
    create index test_x on test(x);
    create view v_test as select * from test;
    create role manager;
    commit;

    set term ^;
    create or alter trigger test_bi for test active
    before insert position 0
    as
    begin
       new.id = coalesce(new.id, gen_id(g_test, 1) );
    end
    ^
    set term ;^
    commit;

    connect '$(DSN)' user 'tmp$c0304' password '123';

    -- All following statements should FAIL if current user is not SYSDBA:

    execute procedure sp_test;

    show sequence g_test;

    alter domain dm_test set default 123;

    alter domain dm_test set not null;

    alter domain dm_test drop not null;

    alter trigger test_bi inactive;


    alter table test add z int;

    alter table test drop constraint test_pk;

    drop index test_x;

    drop view v_test;

    drop trigger test_bi;

    drop table test;

    drop role manager;

    drop procedure sp_test;

    drop sequence g_test;

    drop exception e_test;

    drop function UDR40_frac;

    drop collation name_coll;

    rollback;
"""

act_2 = isql_act('db', test_script_2)

expected_stderr_2 = """
Statement failed, SQLSTATE = 28000
no permission for EXECUTE access to PROCEDURE SP_TEST
-Effective user is TMP$C0304

Statement failed, SQLSTATE = 28000
no permission for USAGE access to GENERATOR G_TEST
-Effective user is TMP$C0304

There is no generator G_TEST in this database
Statement failed, SQLSTATE = 28000
unsuccessful metadata update
-ALTER DOMAIN DM_TEST failed
-no permission for ALTER access to DOMAIN DM_TEST
-Effective user is TMP$C0304

Statement failed, SQLSTATE = 28000
unsuccessful metadata update
-ALTER DOMAIN DM_TEST failed
-no permission for ALTER access to DOMAIN DM_TEST
-Effective user is TMP$C0304

Statement failed, SQLSTATE = 28000
unsuccessful metadata update
-ALTER DOMAIN DM_TEST failed
-no permission for ALTER access to DOMAIN DM_TEST
-Effective user is TMP$C0304

Statement failed, SQLSTATE = 28000
unsuccessful metadata update
-ALTER TRIGGER TEST_BI failed
-no permission for ALTER access to TABLE TEST
-Effective user is TMP$C0304

Statement failed, SQLSTATE = 28000
unsuccessful metadata update
-ALTER TABLE TEST failed
-no permission for ALTER access to TABLE TEST
-Effective user is TMP$C0304

Statement failed, SQLSTATE = 28000
unsuccessful metadata update
-ALTER TABLE TEST failed
-no permission for ALTER access to TABLE TEST
-Effective user is TMP$C0304

Statement failed, SQLSTATE = 28000
unsuccessful metadata update
-DROP INDEX TEST_X failed
-no permission for ALTER access to TABLE TEST
-Effective user is TMP$C0304

Statement failed, SQLSTATE = 28000
unsuccessful metadata update
-DROP VIEW V_TEST failed
-no permission for DROP access to VIEW V_TEST
-Effective user is TMP$C0304

Statement failed, SQLSTATE = 28000
unsuccessful metadata update
-DROP TRIGGER TEST_BI failed
-no permission for ALTER access to TABLE TEST
-Effective user is TMP$C0304

Statement failed, SQLSTATE = 28000
unsuccessful metadata update
-DROP TABLE TEST failed
-no permission for DROP access to TABLE TEST
-Effective user is TMP$C0304

Statement failed, SQLSTATE = 28000
unsuccessful metadata update
-DROP ROLE MANAGER failed
-no permission for DROP access to ROLE MANAGER
-Effective user is TMP$C0304

Statement failed, SQLSTATE = 28000
unsuccessful metadata update
-DROP PROCEDURE SP_TEST failed
-no permission for DROP access to PROCEDURE SP_TEST
-Effective user is TMP$C0304

Statement failed, SQLSTATE = 28000
unsuccessful metadata update
-DROP SEQUENCE G_TEST failed
-no permission for DROP access to GENERATOR G_TEST
-Effective user is TMP$C0304

Statement failed, SQLSTATE = 28000
unsuccessful metadata update
-DROP EXCEPTION E_TEST failed
-no permission for DROP access to EXCEPTION E_TEST
-Effective user is TMP$C0304

Statement failed, SQLSTATE = 28000
unsuccessful metadata update
-DROP FUNCTION UDR40_FRAC failed
-no permission for DROP access to FUNCTION UDR40_FRAC
-Effective user is TMP$C0304

Statement failed, SQLSTATE = 28000
unsuccessful metadata update
-DROP COLLATION NAME_COLL failed
-no permission for DROP access to COLLATION NAME_COLL
-Effective user is TMP$C0304

"""

@pytest.mark.version('>=4.0')
def test_2(act_2: Action, tmp_user: User):
    act_2.expected_stderr = expected_stderr_2
    act_2.execute()
    assert act_2.clean_stderr == act_2.clean_expected_stderr

