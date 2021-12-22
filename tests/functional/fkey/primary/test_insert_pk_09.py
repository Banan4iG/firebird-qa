#coding:utf-8
#
# id:           functional.fkey.primary.insert_pk_09
# title:        Check correct work fix with foreign key
# decription:   Check foreign key work.
#               Master table has primary key consisting of several fields.
#               Master transaction modifies all primary key fields.
#               Detail transaction inserts record in detail_table.
#               Expected: error - primary in master_table has been changed.
# tracker_id:
# min_versions: []
# versions:     2.5.3
# qmid:         functional.fkey.primary.ins_09

import pytest
from firebird.qa import db_factory, python_act, Action
from firebird.driver import DatabaseError, tpb, Isolation

# version: 2.5.3
# resources: None

substitutions_1 = []

init_script_1 = """CREATE TABLE MASTER_TABLE (
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

db_1 = db_factory(sql_dialect=3, init=init_script_1)

# test_script_1
#---
# TPB_master = (
#        chr(kdb.isc_tpb_write)
#      + chr(kdb.isc_tpb_read_committed) + chr(kdb.isc_tpb_rec_version)
#      + chr(kdb.isc_tpb_nowait)
#                    )
#  TPB_detail = (
#        chr(kdb.isc_tpb_write)
#      + chr(kdb.isc_tpb_read_committed) + chr(kdb.isc_tpb_rec_version)
#      + chr(kdb.isc_tpb_nowait)
#                    )
#  db_conn.begin(tpb=TPB_master)
#  cm_1 = db_conn.cursor()
#  cm_1.execute("UPDATE MASTER_TABLE SET ID_1=2 WHERE ID_1=1")
#  cm_1.execute("UPDATE MASTER_TABLE SET ID_2='two' WHERE ID_2='one'")
#
#  #Create second connection for change detail table
#  con_detail = kdb.connect(
#       dsn=dsn.encode(),
#       user=user_name.encode(),
#       password=user_password.encode()
#  )
#
#  try:
#     con_detail.begin(tpb=TPB_detail)
#     cd = con_detail.cursor()
#     cd.execute("INSERT INTO DETAIL_TABLE (ID, FKEY_1, FKEY_2) VALUES (1, 1, 'one')")
#     con_detail.commit()
#  except Exception, e:
#  print (e[0])
#---

act_1 = python_act('db_1', substitutions=substitutions_1)

@pytest.mark.version('>=2.5.3')
def test_1(act_1: Action):
    with act_1.db.connect() as con:
        cust_tpb = tpb(isolation=Isolation.READ_COMMITTED_RECORD_VERSION, lock_timeout=0)
        con.begin(cust_tpb)
        with con.cursor() as c:
            c.execute("UPDATE MASTER_TABLE SET ID_1=2 WHERE ID_1=1")
            c.execute("UPDATE MASTER_TABLE SET ID_2='two' WHERE ID_2='one'")
            #Create second connection for change detail table
            with act_1.db.connect() as con_detail:
                con_detail.begin(cust_tpb)
                with con_detail.cursor() as cd:
                    with pytest.raises(DatabaseError,
                                       match='.*violation of FOREIGN KEY constraint "FK_DETAIL_TABLE" on table "DETAIL_TABLE".*'):
                        cd.execute("INSERT INTO DETAIL_TABLE (ID, FKEY_1, FKEY_2) VALUES (1, 1, 'one')")
                con_detail.commit()
    # Passed.
