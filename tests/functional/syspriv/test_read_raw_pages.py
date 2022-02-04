#coding:utf-8

"""
ID:          syspriv.read-raw-pages
TITLE:       Check ability to get binary content of DB page by non-sysdba user who is
  granted with necessary system privilege
DESCRIPTION:
  Test uses ability to read binary content of DB page that is provided by FDB driver (see con.get_page_contents() call).
  We obtain content of page with ID=1 (this is PIP) and get its type (it must be 2).
  This action can be done by NON-dba user only if he has apropriate system privilege, otherwise FDB raises Python-related
  error. We catch this error in order to prevent failing of test with 'E' outcome and print text of exception.
FBTEST:      functional.syspriv.read_raw_pages
"""

import pytest
from firebird.qa import *

init_script = """
    set wng off;
    set bail on;
    set list on;
    set count on;

    create or alter
        user john_smith_raw_reader
        password '123'
        using plugin Srp
    ;
    create or alter
        user mike_adams_bad_hacker
        password '123'
        using plugin Srp
    ;
    commit;

    set term ^;
    execute block as
    begin
      execute statement 'drop role role_for_read_raw_pages';
      when any do begin end
    end^
    set term ;^
    commit;

    create role role_for_read_raw_pages set system privileges to READ_RAW_PAGES;
    commit;
    grant default role_for_read_raw_pages to user john_smith_raw_reader;
    commit;
  """

db = db_factory(init=init_script)

act = python_act('db')

expected_stdout = """
    User: mike_adams_bad_hacker
    Exception occured:
    Result code does not match request code.

    User: john_smith_raw_reader
    Successfully get content of page, its type: 2
"""

@pytest.mark.skip('FIXME: Not IMPLEMENTED')
@pytest.mark.version('>=4.0')
def test_1(act: Action):
    pytest.fail("Not IMPLEMENTED")

# test_script_1
#---
#
#  import os
#  from struct import unpack_from
#
#  db_file = db_conn.database_name
#  db_conn.close()
#
#  for i in ( 'mike_adams_bad_hacker', 'john_smith_raw_reader'):
#      print('User: %s' % i )
#      con = fdb.connect(dsn = dsn, user = i, password = '123', role = 'role_for_read_raw_pages')
#      try:
#          page_buffer = con.get_page_contents( 1 )
#          (page_type,) = unpack_from('<b',page_buffer)
#          print('Successfully get content of page, its type: %d' % page_type )
#      except Exception,e:
#          print('Exception occured:')
#          for x in e:
#              print(x)
#      finally:
#          con.close()
#
#  #------------------------
#
#  con = fdb.connect(dsn = dsn, user = user_name, password = user_password)
#  con.execute_immediate('drop user mike_adams_bad_hacker using plugin Srp')
#  con.execute_immediate('drop user john_smith_raw_reader using plugin Srp')
#  con.commit()
#  con.close()
#
#---
