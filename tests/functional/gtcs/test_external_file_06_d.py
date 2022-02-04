#coding:utf-8

"""
ID:          gtcs.external-file-06
FBTEST:      functional.gtcs.external_file_06_d
TITLE:       Test for external table with field of DOUBLE PRECISION datatype
DESCRIPTION:
  Original test see in:
  https://github.com/FirebirdSQL/fbtcs/blob/master/GTCS/tests/EXT_REL_0_6_D.script
NOTES:
[03.03.2021]
  Added substitution for zero value ('F02') as result of evaluating exp(-745.1332192):
  on Windows number of digits in decimal representation more than on Linux for 1.
"""

import pytest
from firebird.qa import *

db = db_factory()

act = python_act('db', substitutions=[('[ \t]+', ' '), ('0.0000000000000000', '0.000000000000000')])

expected_stdout = """
    F01 4.940656458412465e-324
    F02 0.0000000000000000
    F03 1.797693134862273e+308
    Records affected: 1
"""

@pytest.mark.skip('FIXME: Not IMPLEMENTED')
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    pytest.fail("Not IMPLEMENTED")

# test_script_1
#---
#
#  import os
#  import sys
#  import subprocess
#  import time
#
#  tmp_file = os.path.join(context['temp_directory'],'tmp_ext_06_d.tmp')
#  if os.path.isfile( tmp_file):
#       os.remove( tmp_file )
#
#  this_fdb = db_conn.database_name
#
#  sql_cmd='''
#      connect 'localhost:%(this_fdb)s' user '%(user_name)s' password '%(user_password)s';
#      create domain dm_dp double precision;
#      create table ext_table external file '%(tmp_file)s' (f01 dm_dp, f02 dm_dp, f03 dm_dp);
#      commit;
#      insert into ext_table (f01, f02, f03) values( exp(-745.1332191), exp(-745.1332192), exp(709.78271289338404) );
#      commit;
#      -- connect 'localhost:%(this_fdb)s' user '%(user_name)s' password '%(user_password)s';
#      set list on;
#      set count on;
#      select * from ext_table;
#  ''' % dict(globals(), **locals())
#
#  runProgram('isql', [ '-q' ], sql_cmd)
#
#  f_sql_chk = open( os.path.join(context['temp_directory'],'tmp_ext_06_d.sql'), 'w')
#  f_sql_chk.write(sql_cmd)
#  f_sql_chk.close()
#
#  time.sleep(1)
#
#  os.remove(f_sql_chk.name)
#  os.remove( tmp_file )
#
#---
