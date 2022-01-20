#coding:utf-8

"""
ID:          issue-789
ISSUE:       789
TITLE:       Adding a non-null restricted column to a populated table renders the table inconsistent
DESCRIPTION:
JIRA:        CORE-1518
"""

import pytest
from firebird.qa import *

init_script = """
    -- Tests that manipulates with NULL fields/domains and check results:
    -- CORE-1518 Adding a non-null restricted column to a populated table renders the table inconsistent
    -- CORE-4453 (Regression: NOT NULL constraint, declared in domain, does not work)
    -- CORE-4725 (Inconsistencies with ALTER DOMAIN and ALTER TABLE with DROP NOT NULL and PRIMARY KEYs)
    -- CORE-4733 (Command "Alter table <T> alter TYPE <C> <DOMAIN_WITH_NOT_NULL" does not verifies data in column <C> and makes incorrect assignments in <C> to ZERO / JULIAN_DATE / ASCII(0) for types INT, TIMESTAMP and VARCHAR)
    create domain dm_nn int not null;
    create table test(c1 int);
    commit;
    insert into test(c1) values (null);
    commit;
"""

db = db_factory(init=init_script)

test_script = """
    -- Source sample in the ticket:
    -- create table dyd(c1 integer), insert one record with value = 1.
    -- alter table dyd add c2 integer not null ==> did not raise exception but should.


    -- All these statements should produce exception in 3.0:
    alter table test alter c1 set not null;
    alter table test alter c1 type dm_nn;
    alter table test add c2 int not null; -- this also check for core-2696 ("alter table" command can add a field which has "not null" definition)
    alter table test add c3 dm_nn;

    -- still passed on 3.0 (does not verifies old data on new check condition):
    -- alter table test add constraint test_nn check(c1 is not null); -- :(((
"""

act = isql_act('db', test_script)

expected_stderr = """
    Statement failed, SQLSTATE = 22006
    unsuccessful metadata update
    -Cannot make field C1 of table TEST NOT NULL because there are NULLs present

    Statement failed, SQLSTATE = 22006
    unsuccessful metadata update
    -Cannot make field C1 of table TEST NOT NULL because there are NULLs present

    Statement failed, SQLSTATE = 22006
    unsuccessful metadata update
    -Cannot make field C2 of table TEST NOT NULL because there are NULLs present

    Statement failed, SQLSTATE = 22006
    unsuccessful metadata update
    -Cannot make field C3 of table TEST NOT NULL because there are NULLs present
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stderr = expected_stderr
    act.execute()
    assert act.clean_stderr == act.clean_expected_stderr

