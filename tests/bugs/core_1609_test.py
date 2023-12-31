#coding:utf-8

"""
ID:          issue-2030
ISSUE:       2030
TITLE:       PSQL output parameter size limited
DESCRIPTION:
JIRA:        CORE-1609
FBTEST:      bugs.core_1609
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    set bail on;
    set term ^;

    create or alter procedure spro$parse_tag1 as begin end
    ^
    create or alter procedure spro$parse_tag2 as begin end
    ^
    create or alter procedure spro$parse_tag3 as begin end
    ^
    commit
    ^

    execute block as
    begin
        execute statement 'drop domain spro$long_string';
        when any do begin end
    end
    ^
    commit
    ^

    create domain spro$long_string as varchar(32765) character set none collate none
    ^
    commit
    ^

    create or alter procedure spro$parse_tag1(
        str_in type of spro$long_string,
        delimeter varchar(10))
    returns (
        str_out1 type of spro$long_string,
        str_out2 type of spro$long_string)
    as begin
        suspend;
    end
    ^

    create or alter procedure spro$parse_tag2(
        str_in type of spro$long_string,
        delimeter varchar(10))
    returns (
        str_out1 type of spro$long_string,
        str_out2 varchar(32759))
    as begin
        suspend;
    end
    ^

    create or alter procedure spro$parse_tag3(
        str_in type of spro$long_string,
        delimeter varchar(10))
    returns (
         str_out01 varchar(32765)
        ,str_out02 varchar(32765)
        ,str_out03 varchar(32765)
        ,str_out04 varchar(32765)
        ,str_out05 varchar(32765)
        ,str_out06 varchar(32765)
        ,str_out07 varchar(32765)
        ,str_out08 varchar(32765)
        ,str_out09 varchar(32765)
        ,str_out10 varchar(32765)
        ,str_out11 varchar(32765)
        ,str_out12 varchar(32765)
        ,str_out13 varchar(32765)
        ,str_out14 varchar(32765)
        ,str_out15 varchar(32765)
        ,str_out16 varchar(32765)
        ,str_out17 varchar(32765)
        ,str_out18 varchar(32765)
        ,str_out19 varchar(32765)
        ,str_out20 varchar(32765)
        ,str_out21 varchar(32765)
        ,str_out22 varchar(32765)
        ,str_out23 varchar(32765)
        ,str_out24 varchar(32765)
        ,str_out25 varchar(32765)
        ,str_out26 varchar(32765)
        ,str_out27 varchar(32765)
        ,str_out28 varchar(32765)
        ,str_out29 varchar(32765)
        ,str_out30 varchar(32765)
        ,str_out31 varchar(32765)
        ,str_out32 varchar(32765)
        ,str_out33 varchar(32765)
        ,str_out34 varchar(32765)
        ,str_out35 varchar(32765)
        ,str_out36 varchar(32765)
        ,str_out37 varchar(32765)
        ,str_out38 varchar(32765)
        ,str_out39 varchar(32765)
        ,str_out40 varchar(32765)
        ,str_out41 varchar(32765)
        ,str_out42 varchar(32765)
        ,str_out43 varchar(32765)
        ,str_out44 varchar(32765)
        ,str_out45 varchar(32765)
        ,str_out46 varchar(32765)
        ,str_out47 varchar(32765)
        ,str_out48 varchar(32765)
        ,str_out49 varchar(32765)
        ,str_out50 varchar(32765)
    ) as
    begin
        suspend;
    end
    ^
    set term ;^
    commit;
"""

act = isql_act('db', test_script)

@pytest.mark.version('>=3.0.1')
def test_1(act: Action):
    act.execute()
