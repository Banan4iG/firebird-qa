#coding:utf-8
#
# id:           bugs.core_6138
# title:        Inconsistent behavior regarding visibility of master record on detail inserts
# decription:   
#                   Confirmed bug on: 3.0.5.33152 (built 14.09.19), 4.0.0.1598 (built 08.09.19):
#                   no error raised when second attach tried to insert record into child table 
#                   after first attach did commit (but main record was not visible to 2nd attach
#                   because of SNAPSHOT isolation level).
#               
#                   Works fine on:
#                       4.0.0.1639 SS: 1.745s.
#                       4.0.0.1633 CS: 2.266s.
#                       3.0.5.33183 SS: 1.265s.
#                       3.0.5.33178 CS: 1.611s.
#                
# tracker_id:   CORE-6138
# min_versions: ['3.0.5']
# versions:     3.0.5
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 3.0.5
# resources: None

substitutions_1 = [('[ \t]+', ' ')]

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

# test_script_1
#---
# 
#  import os
#  import sys
#  
#  os.environ["ISC_USER"] = user_name
#  os.environ["ISC_PASSWORD"] = user_password
#  db_conn.close()
#  
#  custom_tpb = fdb.TPB()
#  custom_tpb.isolation_level = fdb.isc_tpb_concurrency
#  custom_tpb.lock_resolution = fdb.isc_tpb_nowait
#  
#  con1=fdb.connect( dsn = dsn )
#  con2=fdb.connect( dsn = dsn )
#  con2.begin( tpb = custom_tpb )
#  
#  #print( 'FDB version: ' + fdb.__version__ )
#  #print( 'Firebird version: ' + con1.firebird_version )
#  
#  con1.execute_immediate( 'create table a (id int primary key)' )
#  con1.execute_immediate( 'create table b (id int primary key, id_a int, constraint fk_b__a foreign key(id_a) references a(id) on update cascade on delete cascade)' )
#  con1.commit()
#  
#  con1.begin( tpb = custom_tpb )
#  cur1=con1.cursor()
#  cur1.execute('insert into a(id) values( ? )', ( 1, ) )
#  
#  con2.commit()
#  con2.begin(tpb = custom_tpb )
#  cur2=con2.cursor()
#  cur2.execute('select id from a')
#  
#  con1.commit()
#  try:
#    cur2.execute( 'insert into b (id, id_a) values (?, ?)', (1, 1,) )
#    print('UNEXPECTED SUCCESS: CHILD RECORD INSERTED W/O ERROR.')
#  except Exception as e:
#      
#      print( ('EXPECTED: FK violation encountered.' if '335544466' in repr(e) else 'Unknown/unexpected exception.') )
#  
#      # print( x for x in e ) # Python 3.x:  TypeError: 'DatabaseError' object is not iterable
#      # print( e[0] ) # Python 3.x: TypeError: 'DatabaseError' object is not subscriptable
#  
#  finally:
#    cur2.close()
#  
#  con2.close()
#  
#  cur1.close()
#  con1.close()
#  
#    
#---
#act_1 = python_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    EXPECTED: FK violation encountered.
  """

@pytest.mark.version('>=3.0.5')
@pytest.mark.xfail
def test_core_6138_1(db_1):
    pytest.fail("Test not IMPLEMENTED")


