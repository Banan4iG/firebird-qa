#coding:utf-8

"""
ID:          fkey.primary.insert-07
FBTEST:      functional.fkey.primary.insert_pk_07
ISSUE:       2027
JIRA:        CORE-1606
TITLE:       Check correct work fix with foreign key
DESCRIPTION:
  Check foreign key work.
  Master table has primary key consisting of several fields.
  Master transaction modifies non key fields.
  Detail transaction inserts record in detail_table.
  Expected: no errors.
  Related to #2027. Ability to insert child record if parent record is locked but foreign key target unchanged.
"""

import pytest
from firebird.qa import *
from firebird.driver import tpb, Isolation

init_script = """CREATE TABLE MASTER_TABLE (
    ID_1 INTEGER NOT NULL,
    ID_2 VARCHAR(20) NOT NULL,
    INT_F  INTEGER,
    PRIMARY KEY (ID_1, ID_2)
);

CREATE TABLE DETAIL_TABLE (
    ID    INTEGER PRIMARY KEY,
    FKEY_1  INTEGER,
    FKEY_2  VARCHAR(20)
);

ALTER TABLE DETAIL_TABLE ADD CONSTRAINT FK_DETAIL_TABLE FOREIGN KEY (FKEY_1, FKEY_2) REFERENCES MASTER_TABLE (ID_1, ID_2);
COMMIT;
INSERT INTO MASTER_TABLE (ID_1, ID_2, INT_F) VALUES (1, 'one', 10);
COMMIT;"""

db = db_factory(init=init_script)

act = python_act('db')

@pytest.mark.version('>=3')
def test_1(act: Action):
    with act.db.connect() as con:
        cust_tpb = tpb(isolation=Isolation.READ_COMMITTED_RECORD_VERSION, lock_timeout=0)
        con.begin(cust_tpb)
        with con.cursor() as c:
            c.execute('UPDATE MASTER_TABLE SET INT_F=2')
            #Create second connection for change detail table
            with act.db.connect() as con_detail:
                con_detail.begin(cust_tpb)
                with con_detail.cursor() as cd:
                    cd.execute("INSERT INTO DETAIL_TABLE (ID, FKEY_1, FKEY_2) VALUES (1, 1, 'one')")
                con_detail.commit()
    # Passed.
