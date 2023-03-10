#coding:utf-8

"""
ID:          domain.alter-06
FBTEST:      functional.domain.alter.06
TITLE:       Changing COLLATE with ALTER DOMAIN
DESCRIPTION: Checks the normal operation of the COLLATE changing with ALTER DOMAIN
"""

import pytest
from firebird.qa import *

init_script = """
create domain d1 varchar(30) character set UTF8 collate UNICODE;

CREATE TABLE test(
data1 d1
);

insert into test values('A');
insert into test values('a');
"""

db = db_factory(init=init_script)

test_script = """
select data1 from test where data1 = 'a';
alter domain d1 type varchar(30) character set UTF8 collate UNICODE_CI;
select data1 from test where data1 = 'a';
"""

act = isql_act('db', test_script)

expected_stdout = """
DATA1
==============================
a

DATA1
==============================
A
a
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
