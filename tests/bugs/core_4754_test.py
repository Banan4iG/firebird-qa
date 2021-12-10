#coding:utf-8
#
# id:           bugs.core_4754
# title:        Bugcheck 167 (invalid SEND request) while working with GTT from several attachments (using EXECUTE STATEMENT ... ON EXTERNAL and different roles)
# decription:
#                  We start two transactions and do DML ('insert ...') in 1st and DDL ('create index ...') in second.
#                  Then we issue COMMIT in DDL transaction. This should raise 'lock conflict ... table "<name>" is in use'.
#                  On 2.5.4 this COMMIT in DDL did NOT raise any error and subsequent reconnect and DML raised bugcheck.
#
#                  Checked on 2.5.6.27013, 3.0.1.32524 - works OK.
#                  Bugcheck can be reproduced on 2.5.4.26856.
#
#                  PS. Old ticket name:
#                      Manipulations with GTT from several attachments (using ES/EDS and different roles) leads to:
#                      "internal Firebird consistency check (invalid SEND request (167), file: JrdStatement.cpp line: 325)"
#
# tracker_id:   CORE-4754
# min_versions: ['2.5.5']
# versions:     2.5.5
# qmid:

import pytest
from firebird.qa import db_factory, python_act, Action
from firebird.driver import tpb, Isolation, TraAccessMode, DatabaseError

# version: 2.5.5
# resources: None

substitutions_1 = []

init_script_1 = """
    recreate global temporary table gtt_session(x int, y int) on commit preserve rows;
    commit;
"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

# test_script_1
#---
#
#  import os
#  import subprocess
#  import fdb
#
#  db_conn.close()
#  os.environ["ISC_USER"] = user_name
#  os.environ["ISC_PASSWORD"] = user_password
#  #db_file="$(DATABASE_LOCATION)bugs.core_4754.fdb"
#
#  customTPB = ( [ fdb.isc_tpb_read_committed, fdb.isc_tpb_rec_version, fdb.isc_tpb_nowait ] )
#  con1 = fdb.connect(dsn=dsn)
#  #print(con1.firebird_version)
#
#  tx1a=con1.trans( default_tpb = customTPB )
#  tx1b=con1.trans( default_tpb = customTPB )
#  cur1a = tx1a.cursor()
#  cur1b = tx1b.cursor()
#  msg=''
#  try:
#      cur1a.execute( "insert into gtt_session select rand()*10, rand()*10 from rdb$types" )
#      cur1b.execute( "create index gtt_session_x_y on gtt_session computed by ( x+y )" )
#      tx1b.commit() # WI-V2.5.6.27013 issues here: lock conflict on no wait transaction unsuccessful metadata update object TABLE "GTT_SESSION" is in use -901 335544345
#      tx1a.commit()
#  except Exception as e:
#      print('Error-1:')
#      msg = e[0]
#      print(msg)
#
#  con1.close()
#
#
#  # ---------------------------------------------------------------
#
#  if not msg.split():
#      # 2.5.5: control should NOT pass here at all!
#      con2 = fdb.connect(dsn=dsn)
#      try:
#          tx2a = con2.trans()
#          cur2a = tx2a.cursor()
#          '''
#          Following INSERT statement will raise on WI-V2.5.4.26856:
#             fdb.fbcore.DatabaseError: ('Error while executing SQL statement:
#  - SQLCODE: -902
#  - internal Firebird consistency
#             check (invalid SEND request (167), file: exe.cpp line: 614)', -902, 335544333)
#             Exception fdb.fbcore.DatabaseError: DatabaseError("Error while rolling back transaction:
#  - SQLCODE: -902
#  - intern
#             al Firebird consistency check (can't continue after bugcheck)", -902, 335544333) in <bound method Connection.__del_
#             _ of <fdb.fbcore.Connection object at 0x00E40790>> ignored
#          '''
#          cur2a.execute( "insert into gtt_session select rand()*11, rand()*11 from rdb$types" )
#      except Exception as e:
#          print('Error-2:')
#          print(e[0])
#      con2.close()
#
#---

act_1 = python_act('db_1', substitutions=substitutions_1)

expected_stdout_1 = """
Error-1:
lock conflict on no wait transaction
-unsuccessful metadata update
-object TABLE "GTT_SESSION" is in use
"""

@pytest.mark.version('>=2.5.5')
def test_1(act_1: Action, capsys):
    custom_tpb = tpb(isolation=Isolation.READ_COMMITTED_RECORD_VERSION,
                     access_mode=TraAccessMode.WRITE, lock_timeout=0)
    with act_1.db.connect() as con1:
        tx1a = con1.transaction_manager(custom_tpb)
        cur1a = tx1a.cursor()
        tx1b = con1.transaction_manager(custom_tpb)
        cur1b = tx1b.cursor()
        try:
            cur1a.execute("insert into gtt_session select rand()*10, rand()*10 from rdb$types")
            cur1b.execute("create index gtt_session_x_y on gtt_session computed by (x+y)")
            tx1b.commit() # WI-V2.5.6.27013 issues here: lock conflict on no wait transaction unsuccessful metadata update object TABLE "GTT_SESSION" is in use -901 335544345
            tx1a.commit()
        except DatabaseError as e:
            print('Error-1:')
            msg = e.args[0]
            print(msg)
    #
    if not msg.split():
        # 2.5.5: control should NOT pass here at all!
        with act_1.db.connect() as con2:
            try:
                tx2a = con2.transaction_manager()
                cur2a = tx2a.cursor()
                cur2a.execute("insert into gtt_session select rand()*11, rand()*11 from rdb$types")
            except DatabaseError as e:
                print('Error-2:')
                print(e.args[0])
    #
    act_1.expected_stdout = expected_stdout_1
    act_1.stdout = capsys.readouterr().out
    assert act_1.clean_stdout == act_1.clean_expected_stdout
