#coding:utf-8

"""
ID:          exception.create-03
FBTEST:      functional.exception.create.03
TITLE:       CREATE EXCEPTION - too long message
DESCRIPTION:
NOTES:
[23.10.2015]
  try to create in the SAME transaction exceptions with too long message and correct message (reduce its length with 1)
  after statement fails. Do that using both ascii and non-ascii characters in these exceptions messages.
  Expected result: no errors should occur on commit, exceptions should work fine. Taken from eqc ticket #12062.
[13.06.2016]
  replaced 'show exception' with regular select from rdb$exception: output of SHOW commands
 is volatile in unstable FB versions.
"""

import pytest
from firebird.qa import *

db = db_factory(charset='UTF8')

test_script = """
    set autoddl off;
    commit;

    create exception boo_ascii
    'FOO!BAR!abcdefghijklmnoprstu012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345'
    ;

    create exception boo_ascii
    'FOOBAR!abcdefghijklmnoprstu012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345'
    ;


    create exception boo_utf8
    '32ηΣημείωσηΣημείωσηΣημεσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωση'
    ;

    create exception boo_utf8
    '3ηΣημείωσηΣημείωσηΣημεσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωση'
    ;

    commit;

    set list on;
    select rdb$exception_name, rdb$message from rdb$exceptions;

    set term ^;
    execute block as
    begin
      exception boo_ascii;
    end
    ^

    execute block as
    begin
      exception boo_utf8;
    end
    ^
    set term ;^
"""

act = isql_act('db', test_script, substitutions=[('-At block line: [\\d]+, col: [\\d]+', '-At block line')])

expected_stdout = """
    RDB$EXCEPTION_NAME              BOO_ASCII
    RDB$MESSAGE                     FOOBAR!abcdefghijklmnoprstu012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345

    RDB$EXCEPTION_NAME              BOO_UTF8
    RDB$MESSAGE                     3ηΣημείωσηΣημείωσηΣημεσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωση
"""

expected_stderr = """
    Statement failed, SQLSTATE = 42000
    unsuccessful metadata update
    -CREATE EXCEPTION BOO_ASCII failed
    -Name longer than database column size

    Statement failed, SQLSTATE = 42000
    unsuccessful metadata update
    -CREATE EXCEPTION BOO_UTF8 failed
    -Name longer than database column size

    Statement failed, SQLSTATE = HY000
    exception 1
    -BOO_ASCII
    -FOOBAR!abcdefghijklmnoprstu012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345
    -At block line: 3, col: 7

    Statement failed, SQLSTATE = HY000
    exception 2
    -BOO_UTF8
    -3ηΣημείωσηΣημείωσηΣημεσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωση
    -At block line: 3, col: 7
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.expected_stderr = expected_stderr
    act.execute()
    assert (act.clean_stderr == act.clean_expected_stderr and
            act.clean_stdout == act.clean_expected_stdout)
