#coding:utf-8
#
# id:           functional.fkey.unique.select_uf_02
# title:        Check correct work fix with foreign key
# decription:   Check foreign key work.
#               Master transaction is perform select with lock but not perform fetch.
#               Detail transaction inserts record in detail_table and commit;
#               Master transaction fetched record and trying update it;
# tracker_id:   
# min_versions: []
# versions:     2.1
# qmid:         functional.fkey.unique.select_02

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 2.1
# resources: None

substitutions_1 = []

init_script_1 = """CREATE TABLE MASTER_TABLE (
    ID     INTEGER PRIMARY KEY,
    UF     INTEGER UNIQUE,
    INT_F  INTEGER
);

CREATE TABLE DETAIL_TABLE (
    ID    INTEGER PRIMARY KEY,
    FKEY  INTEGER
);

ALTER TABLE DETAIL_TABLE ADD CONSTRAINT FK_DETAIL_TABLE FOREIGN KEY (FKEY) REFERENCES MASTER_TABLE (UF);
COMMIT;
INSERT INTO MASTER_TABLE (ID, UF, INT_F) VALUES (1, 1, 10);
commit;"""

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
#  
#  db_conn.begin(tpb=TPB_master)
#  c = db_conn.cursor()
#  c.execute("SELECT UF, INT_F FROM MASTER_TABLE WHERE ID=1 WITH LOCK")
#  
#  #Create second connection for change detail table
#  con_detail = kdb.connect(
#       dsn=dsn.encode(),
#       user=user_name.encode(),
#       password=user_password.encode()
#  )
#  
#  try:
#    con_detail.begin(tpb=TPB_detail)
#    cd = con_detail.cursor()
#    cd.execute("INSERT INTO DETAIL_TABLE (ID, FKEY) VALUES (1,1)")
#    con_detail.commit()
#  except Exception, e:
#    print (e[1])
#  try:
#    c.fetchall()
#    c.execute("UPDATE MASTER_TABLE SET UF=2")
#    db_conn.commit()
#  except Exception, e:
#    print (e[0])
#---
#act_1 = python_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """Error while executing SQL statement:
- SQLCODE: -530
- violation of FOREIGN KEY constraint "FK_DETAIL_TABLE" on table "DETAIL_TABLE"
- Foreign key references are present for the record
- Problematic key value is ("UF" = 1)
"""

@pytest.mark.version('>=2.1')
@pytest.mark.xfail
def test_select_uf_02_1(db_1):
    pytest.fail("Test not IMPLEMENTED")


