#coding:utf-8

"""
ID:          issue-2970
ISSUE:       2970
TITLE:       Maximum and minimum identifier length should be enforced by DSQL
DESCRIPTION:
JIRA:        CORE-2560
FBTEST:      bugs.core_2560
"""

import pytest
from firebird.qa import *

db = db_factory()

# version: 3.0

test_script_1 = """
    --set echo on;
    select 1 as cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
    from rdb$database order by cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc;

    select 1 from rdb$database dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
    where dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd.rdb$relation_id > 10;

    savepoint zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz;

    create role rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr;
    create sequence gggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg;

    create collation uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu for iso8859_1;

    create user zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz password 'q';

    savepoint "";
    rollback to "";

    create role "";
    grant select on t1 to role "";
    grant "" to public;
    drop role "";

    create user "" password 'q';
    create user tmp$c2560 password '';

    create sequence "";
    create domain "" int;
    create exception "" as '@1';
    create view "" as select 1 from rdb$database;
    create table ""(x int);
    create table tx("" int);
    create procedure "" as begin end;
    create procedure p("" int) as begin end;
    set term ^;
    create function "" returns int as begin return 1; end
    ^
    recreate package "" as
    begin
    function pg_func(a int) returns bigint;
    end
    ^
    create package body "" as
    begin
    function pg_func(a int) returns bigint as
    begin
    return a * a;
    end
    end
    recreate package pg_test as
    begin
    function ""(a int) returns bigint;
    end
    ^
    create package body pg_test as
    begin
    function ""(a int) returns bigint as
    begin
    return a * a;
    end
    end
    ^
    execute block returns("" int) as
    begin
    "" = 1;
    suspend;
    end
    ^
    set term ^;

"""

act_1 = isql_act('db', test_script_1)

expected_stderr_1 = """
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Name longer than database column size
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Name longer than database column size
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Name longer than database column size
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Name longer than database column size
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Name longer than database column size
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Name longer than database column size
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Name longer than database column size
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Zero length identifiers are not allowed
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Zero length identifiers are not allowed
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Zero length identifiers are not allowed
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Zero length identifiers are not allowed
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Zero length identifiers are not allowed
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Zero length identifiers are not allowed
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Zero length identifiers are not allowed
    Statement failed, SQLSTATE = 42000
    unsuccessful metadata update
    -CREATE USER TMP$C2560 failed
    -Password should not be empty string
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Zero length identifiers are not allowed
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Zero length identifiers are not allowed
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Zero length identifiers are not allowed
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Zero length identifiers are not allowed
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Zero length identifiers are not allowed
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Zero length identifiers are not allowed
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Zero length identifiers are not allowed
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Zero length identifiers are not allowed
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Zero length identifiers are not allowed
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Zero length identifiers are not allowed
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Zero length identifiers are not allowed
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Zero length identifiers are not allowed
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Zero length identifiers are not allowed
"""

@pytest.mark.version('>=3.0,<4.0')
def test_1(act_1: Action):
    act_1.expected_stderr = expected_stderr_1
    act_1.execute()
    assert act_1.clean_stderr == act_1.clean_expected_stderr

# version: 4.0

test_script_2 = """
    --set echo on;
    --set list on;

    create role
r2345678901234567890123456789012345678901234567890123456789012345;

    create sequence
g2345678901234567890123456789012345678901234567890123456789012345;

    create exception
e2345678901234567890123456789012345678901234567890123456789012345 'foo!..';

    create collation
c2345678901234567890123456789012345678901234567890123456789012345 for utf8 from unicode;

    create domain
d2345678901234567890123456789012345678901234567890123456789012345 int;

    create table
t2345678901234567890123456789012345678901234567890123456789012345 (x int);

    create table
x(
t2345678901234567890123456789012345678901234567890123456789012345 int);

    create or alter procedure
p2345678901234567890123456789012345678901234567890123456789012345 as begin end;

    set term ^;
    create or alter procedure p1 returns(
o2345678901234567890123456789012345678901234567890123456789012345 int
) as
begin
    suspend;
end^

create or alter procedure p2 returns(o2 double precision) as
    declare
v2345678901234567890123456789012345678901234567890123456789012345
    int;
begin
    select rand()*1000 as
a2345678901234567890123456789012345678901234567890123456789012345
    from rdb$database
    into
v2345678901234567890123456789012345678901234567890123456789012345
    o2 = sqrt(
v2345678901234567890123456789012345678901234567890123456789012345
);
    suspend;
end^


    create or alter function
f2345678901234567890123456789012345678901234567890123456789012345 returns int as
begin
    return 1;
end^

    create or alter function
f(
a2345678901234567890123456789012345678901234567890123456789012345 int ) returns int as
begin
    return 1;
end^

    recreate package
p2345678901234567890123456789012345678901234567890123456789012345
    as begin
        function f(a int) returns bigint;
    end
    ^

    recreate package p1 as
    begin
        function
f2345678901234567890123456789012345678901234567890123456789012345( a int) returns bigint;
    end
    ^

    recreate package p2 as
    begin
        function g(
a2345678901234567890123456789012345678901234567890123456789012345 int) returns bigint;
    end
    ^

    set term ;^
commit;

    -- deferred, see CORE-5277:
    create or alter user
u2345678901234567890123456789012345678901234567890123456789012345 password 'q';
    commit;

    -- ############  check that empty names are forbidden  ###############

    create role "";

    create sequence "";

    create domain "" int;

    create exception "" as '@1';

    create view "" as select 1 from rdb$database;

    create table ""(x int);

    create table tx("" int);

    create procedure "" as begin end;

    create procedure p("" int) as begin end;

    set term ^;
    create function "" returns int as begin return 1; end
    ^
    recreate package "" as
    begin
    function pg_func(a int) returns bigint;
    end
    ^
    create package body "" as
    begin
        function pg_func(a int) returns bigint as
        begin
            return a * a;
        end
    end

    recreate package pg_test as
    begin
        function ""(a int) returns bigint;
    end
    ^
    create package body pg_test as
    begin
        function ""(a int) returns bigint as
        begin
            return a * a;
        end
    end
    ^
    execute block returns("" int) as
    begin
    "" = 1;
    suspend;
    end
    ^
    set term ^;

"""

act_2 = isql_act('db', test_script_2,
                 substitutions=[('After line.*', ''),
                                ('-At line[:]{0,1}[\\s]+[\\d]+,[\\s]+column[:]{0,1}[\\s]+[\\d]+', '')])

expected_stderr_2 = """
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Name longer than database column size
    After line 0 in file c2560-x.sql
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Name longer than database column size
    After line 5 in file c2560-x.sql
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Name longer than database column size
    After line 8 in file c2560-x.sql
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Name longer than database column size
    After line 11 in file c2560-x.sql
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Name longer than database column size
    After line 14 in file c2560-x.sql
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Name longer than database column size
    After line 17 in file c2560-x.sql
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Name longer than database column size
    After line 20 in file c2560-x.sql
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Name longer than database column size
    After line 24 in file c2560-x.sql
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Name longer than database column size
    After line 29 in file c2560-x.sql
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Name longer than database column size
    After line 35 in file c2560-x.sql
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Name longer than database column size
    After line 51 in file c2560-x.sql
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Name longer than database column size
    After line 58 in file c2560-x.sql
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Name longer than database column size
    After line 65 in file c2560-x.sql
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Name longer than database column size
    After line 72 in file c2560-x.sql
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Name longer than database column size
    After line 79 in file c2560-x.sql
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Name longer than database column size
    After line 89 in file c2560-x.sql
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Zero length identifiers are not allowed
    After line 94 in file c2560-x.sql
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Zero length identifiers are not allowed
    After line 98 in file c2560-x.sql
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Zero length identifiers are not allowed
    After line 100 in file c2560-x.sql
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Zero length identifiers are not allowed
    After line 102 in file c2560-x.sql
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Zero length identifiers are not allowed
    After line 104 in file c2560-x.sql
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Zero length identifiers are not allowed
    After line 106 in file c2560-x.sql
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Zero length identifiers are not allowed
    After line 108 in file c2560-x.sql
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Zero length identifiers are not allowed
    After line 110 in file c2560-x.sql
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Zero length identifiers are not allowed
    After line 112 in file c2560-x.sql
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Zero length identifiers are not allowed
    After line 116 in file c2560-x.sql
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Zero length identifiers are not allowed
    After line 118 in file c2560-x.sql
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Zero length identifiers are not allowed
    After line 123 in file c2560-x.sql
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Zero length identifiers are not allowed
    After line 136 in file c2560-x.sql
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Zero length identifiers are not allowed
    After line 144 in file c2560-x.sql
"""

@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stderr = expected_stderr_2
    act_2.execute()
    assert act_2.clean_stderr == act_2.clean_expected_stderr

