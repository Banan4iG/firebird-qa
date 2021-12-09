#coding:utf-8
#
# id:           bugs.core_5892
# title:        SQL SECURITY DEFINER context is not properly evaluated for monitoring tables
# decription:
#                   Test is based on ticket sample: we create non-privileged user and allow him to call TWO procedures.
#                   First SP is declared with DEFINER rights (i.e. with rights of SYSDBA), second - with rights of INVOKER.
#                   When first SP is called by this (non-privileged!) user then he should see two other connections:
#                   1) that was done by him (but this is other attachment)
#                   2) that was done by SYSDBA.
#                   When second SP is called then this user should see only ONE connection (first from previous list).
#                   Also this test checks ability to work with new context variable 'EFFECTIVE_USER' from 'SYSTEM' namespace.
#
#                   Checked on 4.0.0.1479: OK, 1.623s.
#
# tracker_id:   CORE-5892
# min_versions: ['4.0']
# versions:     4.0
# qmid:         None

import pytest
from firebird.qa import db_factory, python_act, Action, user_factory, User

# version: 4.0
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

# test_script_1
#---
#
#  import os
#  import fdb
#
#  os.environ["ISC_USER"] = user_name
#  os.environ["ISC_PASSWORD"] = user_password
#  db_conn.close()
#
#  con1=fdb.connect( dsn = dsn ) #, user = 'SYSDBA', password = 'masterkey' )
#  con1.execute_immediate("create or alter user TMP$C5892 password '123' using plugin Srp")
#  con1.commit()
#
#  con2=fdb.connect( dsn = dsn, user = 'TMP$C5892', password = '123' )
#  con3=fdb.connect( dsn = dsn, user = 'TMP$C5892', password = '123' )
#
#  sp_definer_ddl = '''
#      create or alter procedure sp_test_definer returns( another_name varchar(31), another_conn_id int, execution_context varchar(31) ) SQL SECURITY DEFINER
#      as
#      begin
#          execution_context = rdb$get_context('SYSTEM', 'EFFECTIVE_USER');
#          for
#              select mon$user, mon$attachment_id
#              from mon$attachments a
#              where a.mon$system_flag is distinct from 1 and a.mon$attachment_id != current_connection
#          into
#              another_name,
#              another_conn_id
#          do suspend;
#      end
#  '''
#
#  sp_invoker_ddl = '''
#      create or alter procedure sp_test_invoker returns( another_name varchar(31), another_conn_id int, execution_context varchar(31) ) SQL SECURITY INVOKER
#      as
#      begin
#          execution_context = rdb$get_context('SYSTEM', 'EFFECTIVE_USER');
#          for
#              select mon$user, mon$attachment_id
#              from mon$attachments a
#              where
#                  a.mon$system_flag is distinct from 1
#                  and a.mon$attachment_id != current_connection
#                  and a.mon$user = current_user
#          into
#              another_name,
#              another_conn_id
#          do suspend;
#      end
#  '''
#
#  con1.execute_immediate( sp_definer_ddl )
#  con1.execute_immediate( sp_invoker_ddl )
#  con1.commit()
#
#  con1.execute_immediate( 'grant execute on procedure sp_test_definer to public' )
#  con1.execute_immediate( 'grant execute on procedure sp_test_invoker to public' )
#  con1.commit()
#
#  sql_chk_definer='select current_user as "definer_-_who_am_i", d.another_name as "definer_-_who_else_here", d.execution_context as "definer_-_effective_user" from rdb$database r left join sp_test_definer d on 1=1'
#  sql_chk_invoker='select current_user as "invoker_-_who_am_i", d.another_name as "invoker_-_who_else_here", d.execution_context as "invoker_-_effective_user" from rdb$database r left join sp_test_invoker d on 1=1'
#
#
#  #---------------------------------
#  #print('=== result of call SP with DEFINER security ===')
#  cur2a=con2.cursor()
#  cur2a.execute( sql_chk_definer )
#  c2col=cur2a.description
#  for r in cur2a:
#      for i in range(0,len(c2col)):
#          print( c2col[i][0],':', r[i] )
#  cur2a.close()
#
#  #---------------------------------
#
#  #print('')
#  #print('=== result of call SP with INVOKER security ===')
#  cur2b=con2.cursor()
#  cur2b.execute( sql_chk_invoker )
#  c2col=cur2b.description
#  for r in cur2b:
#      for i in range(0,len(c2col)):
#          print( c2col[i][0],':', r[i] )
#  cur2b.close()
#
#  #---------------------------------
#
#  con2.close()
#  con3.close()
#
#  con1.execute_immediate('drop user TMP$C5892 using plugin Srp')
#  con1.close()
#
#
#---

act_1 = python_act('db_1', substitutions=substitutions_1)

expected_stdout_1 = """
    definer_-_who_am_i              TMP$C5892
    definer_-_who_else_here         SYSDBA
    definer_-_effective_user        SYSDBA

    definer_-_who_am_i              TMP$C5892
    definer_-_who_else_here         TMP$C5892
    definer_-_effective_user        SYSDBA

    invoker_-_who_am_i              TMP$C5892
    invoker_-_who_else_here         TMP$C5892
    invoker_-_effective_user        TMP$C5892
"""

sp_definer_ddl = """
    create or alter procedure sp_test_definer returns( another_name varchar(31), another_conn_id int, execution_context varchar(31) ) SQL SECURITY DEFINER
    as
    begin
        execution_context = rdb$get_context('SYSTEM', 'EFFECTIVE_USER');
        for
            select mon$user, mon$attachment_id
            from mon$attachments a
            where a.mon$system_flag is distinct from 1 and a.mon$attachment_id != current_connection
        into
            another_name,
            another_conn_id
        do suspend;
    end
"""

sp_invoker_ddl = """
    create or alter procedure sp_test_invoker returns( another_name varchar(31), another_conn_id int, execution_context varchar(31) ) SQL SECURITY INVOKER
    as
    begin
        execution_context = rdb$get_context('SYSTEM', 'EFFECTIVE_USER');
        for
            select mon$user, mon$attachment_id
            from mon$attachments a
            where
                a.mon$system_flag is distinct from 1
                and a.mon$attachment_id != current_connection
                and a.mon$user = current_user
        into
            another_name,
            another_conn_id
        do suspend;
    end
"""

test_user = user_factory(name='TMP$C5892', password='123')

@pytest.mark.version('>=4.0')
def test_1(act_1: Action, test_user: User, capsys):
    sql_chk_definer = 'select current_user as "definer_-_who_am_i", d.another_name as "definer_-_who_else_here", d.execution_context as "definer_-_effective_user" from rdb$database r left join sp_test_definer d on 1=1'
    sql_chk_invoker = 'select current_user as "invoker_-_who_am_i", d.another_name as "invoker_-_who_else_here", d.execution_context as "invoker_-_effective_user" from rdb$database r left join sp_test_invoker d on 1=1'
    with act_1.db.connect() as con1, \
         act_1.db.connect(user=test_user.name, password=test_user.password) as con2, \
         act_1.db.connect(user=test_user.name, password=test_user.password) as con3:
        #
        con1.execute_immediate(sp_definer_ddl)
        con1.execute_immediate(sp_invoker_ddl)
        con1.commit()
        con1.execute_immediate('grant execute on procedure sp_test_definer to public')
        con1.execute_immediate('grant execute on procedure sp_test_invoker to public')
        con1.commit()
        #
        with con2.cursor() as c2:
            c2.execute(sql_chk_definer)
            act_1.print_data_list(c2)
        #
        with con2.cursor() as c2:
            c2.execute(sql_chk_invoker)
            act_1.print_data_list(c2)
    # Check
    act_1.expected_stdout = expected_stdout_1
    act_1.stdout = capsys.readouterr().out
    assert act_1.clean_stdout == act_1.clean_expected_stdout
