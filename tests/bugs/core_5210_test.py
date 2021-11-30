#coding:utf-8
#
# id:           bugs.core_5210
# title:        Firebird 3.0 + fbclient 3.0 - POST_EVENT won't work
# decription:
#                   We create database-level trigger which sends event with name 'dml_event' on COMMIT.
#                   Then we do new connect and run thread with INSERT statement (with delay = 1.0 second), and wait
#                   NO MORE than <max4delivering> sec.
#                   We should receive event during ~ 1.0 second.
#                   We have to consider result as FAIL if we do not receive event in <max4delivering> seconds.
#                   Result of "events.wait(max4delivering)" will be non-empty dictionary with following key-value:
#                     {'dml_event': 1} - when all fine and client got event;
#                     {'dml_event': 0} - when NO event was delivered
#                   All such actions are repeated several times in order to increase probability of failure if something
#                   in FB will be broken.
#
#                   Confirmed wrong result on: 4.0.0.145, V3.0.0.32493 - with probability approx 60%.
#                   All fine on: T4.0.0.150, WI-V3.0.0.32496 (SS/SC/CS).
#
#                   PS. Event handling code in this text was adapted from fdb manual:
#                   http://pythonhosted.org/fdb/usage-guide.html#database-events
#
# tracker_id:   CORE-5210
# min_versions: ['2.5.6']
# versions:     2.5.6
# qmid:         None

import pytest
from time import time
from threading import Timer
from firebird.qa import db_factory, python_act, Action

# version: 2.5.6
# resources: None

substitutions_1 = []

init_script_1 = """
    set term ^;
    create or alter trigger trg_commit on transaction commit as
    begin
        post_event 'dml_event';
    end ^
    set term ;^
    commit;

    recreate table test(id int);
    commit;
"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

# test_script_1
#---
#
#  def check_events(seqno):
#      import fdb
#      import threading
#      import datetime
#      import time
#      from time import time
#      import os
#
#      os.environ["ISC_USER"] = user_name
#      os.environ["ISC_PASSWORD"] = user_password
#
#      # Utility function
#      def send_events(command_list):
#         cur=db_conn.cursor()
#         for cmd in command_list:
#            cur.execute(cmd)
#         db_conn.commit()
#
#      timed_event = threading.Timer(1.0, send_events, args=[["insert into test(id) values ( rand()*1000 )",]])
#
#      # Connection.event_conduit() takes a sequence of string event names as parameter, and returns
#      # EventConduit instance.
#      events = db_conn.event_conduit(['dml_event'])
#
#      # To start listening for events it's necessary (starting from FDB version 1.4.2)
#      # to call EventConduit.begin() method or use EventConduit's context manager interface
#      # Immediately when begin() method is called, EventConduit starts to accumulate notifications
#      # of any events that occur within the conduit's internal queue until the conduit is closed
#      # (via the close() method)
#
#      #print("Start listening for event")
#
#      events.begin()
#
#      timed_event.start()
#
#
#      # Notifications about events are aquired through call to wait() method, that blocks the calling
#      # thread until at least one of the events occurs, or the specified timeout (if any) expires,
#      # and returns None if the wait timed out, or a dictionary that maps event_name -> event_occurrence_count.
#      #t1 = datetime.datetime.now()
#      t1 = time()
#      max4delivering = 3
#      e = events.wait(max4delivering)
#      t2 = time()
#      #t2 = datetime.datetime.now()
#
#
#      events.close()
#
#      print(e)
#      print( str(seqno)+': event was SUCCESSFULLY delivered.' if t2-t1 < max4delivering else str(seqno)+': event was NOT delivered for %.2f s (threshold is %.2f s)' % ( (t2-t1), max4delivering ) )
#
#  check_events(1)
#  check_events(2)
#  check_events(3)
#  check_events(4)
#  check_events(5)
#
#---

act_1 = python_act('db_1', substitutions=substitutions_1)

expected_stdout_1 = """
    {'dml_event': 1}
    1: event was SUCCESSFULLY delivered.

    {'dml_event': 1}
    2: event was SUCCESSFULLY delivered.

    {'dml_event': 1}
    3: event was SUCCESSFULLY delivered.

    {'dml_event': 1}
    4: event was SUCCESSFULLY delivered.

    {'dml_event': 1}
    5: event was SUCCESSFULLY delivered.
"""

def send_events(con, command_list):
   cur = con.cursor()
   for cmd in command_list:
      cur.execute(cmd)
   con.commit()

@pytest.mark.version('>=2.5.6')
def test_1(act_1: Action, capsys):
   def check_events(seqno: int):
      with act_1.db.connect() as con:
         timed_event = Timer(1.0, send_events, args=[con, ["insert into test(id) values (rand()*1000)",]])
         with con.event_collector(['dml_event']) as events:
            timed_event.start()
            t1 = time()
            max4delivering = 3
            e = events.wait(max4delivering)
            t2 = time()
         print(e)
         print(f'{seqno}: event was SUCCESSFULLY delivered.' if t2-t1 < max4delivering
               else f'{seqno}: event was NOT delivered for {t2-t1}s (threshold is {max4delivering}s)')

   #
   check_events(1)
   check_events(2)
   check_events(3)
   check_events(4)
   check_events(5)
   # Check
   act_1.expected_stdout = expected_stdout_1
   act_1.stdout = capsys.readouterr().out
   assert act_1.clean_stdout == act_1.clean_expected_stdout
