#coding:utf-8
#
# id:           bugs.core_2216
# title:        Nbackup as online dump
# decription:
#                  We create table and leave it empty, than we run "nbackup -b 0 <source_db> <nbk_level_0>".
#                  After this add one row in the table in source DB.
#                  Then we obtain database GUID of sourec DB and use it in following commands:
#                  1. nbackup -b <GUID> <source_db> <addi_file>
#                  2. nbackup -i -r <nbk_level_0> <addi_file>
#                  Finally, we:
#                  1. Check that inserted record actually does exist in <nbk_level_0>;
#                  2. Run online validation of <nbk_level_0> - it sould NOT produce any errors.
#
#                  40CS, build 4.0.0.651: OK, 5.031s.
#                  40SC, build 4.0.0.651: OK, 4.765s.
#                  40SS, build 4.0.0.680: OK, 4.031s.
#
# tracker_id:   CORE-2216
# min_versions: ['4.0']
# versions:     4.0
# qmid:

import pytest
from pathlib import Path
from firebird.qa import db_factory, python_act, Action, temp_file
from firebird.driver import SrvNBackupFlag

# version: 4.0
# resources: None

substitutions_1 = [('BLOB_ID.*', ''),
                   ('[0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9]', ''),
                   ('Relation [0-9]{3,4}', 'Relation')]

init_script_1 = """
create table test(id int, s varchar(10) unique using index test_s, t timestamp, b blob);
"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

# test_script_1
#---
#
#  import os
#  import subprocess
#  os.environ["ISC_USER"] = user_name
#  os.environ["ISC_PASSWORD"] = user_password
#  db_conn.close()
#
#  #-----------------------------------
#
#  def flush_and_close(file_handle):
#      # https://docs.python.org/2/library/os.html#os.fsync
#      # If you're starting with a Python file object f,
#      # first do f.flush(), and
#      # then do os.fsync(f.fileno()), to ensure that all internal buffers associated with f are written to disk.
#      global os
#
#      file_handle.flush()
#      os.fsync(file_handle.fileno())
#
#      file_handle.close()
#
#  #--------------------------------------------
#
#  def cleanup( f_names_list ):
#      global os
#      for i in range(len( f_names_list )):
#         if os.path.isfile( f_names_list[i]):
#              os.remove( f_names_list[i] )
#              if os.path.isfile( f_names_list[i]):
#                  print('ERROR: can not remove file ' + f_names_list[i])
#
#  #-------------------------------------------
#
#  dbfile='$(DATABASE_LOCATION)bugs.core_2216.fdb'
#  tmpnbk='$(DATABASE_LOCATION)bugs.core_2216_nb0.fdb'
#  tmpadd='$(DATABASE_LOCATION)bugs.core_2216_add.tmp'
#
#  if os.path.isfile(tmpnbk):
#       os.remove(tmpnbk)
#  if os.path.isfile(tmpadd):
#       os.remove(tmpadd)
#
#  f_nbk1_log=open( os.path.join(context['temp_directory'],'tmp_nbk1_2216.log'), 'w')
#  f_nbk1_err=open( os.path.join(context['temp_directory'],'tmp_nbk1_2216.err'), 'w')
#  subprocess.call( [ context['nbackup_path'], '-b', '0', dbfile, tmpnbk], stdout=f_nbk1_log,stderr=f_nbk1_err )
#  flush_and_close( f_nbk1_log )
#  flush_and_close( f_nbk1_err )
#
#
#  f_run_sql=open( os.path.join(context['temp_directory'],'tmp_run_2216.sql'), 'w')
#  f_run_sql.write('set list on; select rb.rdb$guid as db_guid from rdb$backup_history rb;')
#  f_run_sql.close()
#
#  f_run_log=open( os.path.join(context['temp_directory'],'tmp_run_2216.log'), 'w')
#  subprocess.call( [ context['isql_path'], dsn, '-i', f_run_sql.name], stdout=f_run_log,stderr=subprocess.STDOUT )
#  flush_and_close( f_run_log )
#
#  with open( f_run_log.name,'r') as f:
#    for line in f:
#      if line.split():
#        db_guid=line.split()[1]
#
#  runProgram('isql',[dsn], "insert into test(id,s,t,b) values(1, 'qwerty','11.12.2013 14:15:16.178', 'foo-rio-bar');")
#
#  # nbackup -b {28287188-0E3A-4662-29AB-61F7E117E1C0} C:\\MIX\\firebird\\QA\\fbt-repo\\tmp\\E40.FDB C:\\MIX\\firebird\\QA\\fbt-repo\\tmp\\e40.bku
#  # nbackup -i -r C:\\MIX\\firebird\\QA\\fbt-repo\\tmp\\e40.nb0 C:\\MIX\\firebird\\QA\\fbt-repo\\tmp\\e40.bku
#
#  f_nbk2_log=open( os.path.join(context['temp_directory'],'tmp_nbk2_2216.log'), 'w')
#  f_nbk2_err=open( os.path.join(context['temp_directory'],'tmp_nbk2_2216.err'), 'w')
#  subprocess.call( [ context['nbackup_path'], '-b', db_guid, dbfile, tmpadd], stdout=f_nbk2_log, stderr=f_nbk2_err )
#  flush_and_close( f_nbk2_log )
#  flush_and_close( f_nbk2_err )
#
#
#
#  f_nbk3_log=open( os.path.join(context['temp_directory'],'tmp_nbk3_2216.log'), 'w')
#  f_nbk3_err=open( os.path.join(context['temp_directory'],'tmp_nbk3_2216.err'), 'w')
#  subprocess.call( [ context['nbackup_path'], '-i', '-r', tmpnbk, tmpadd], stdout=f_nbk3_log, stderr=f_nbk3_err )
#  flush_and_close( f_nbk3_log )
#  flush_and_close( f_nbk3_err )
#
#  # Checking query:
#  #################
#  runProgram('isql',['localhost:'+tmpnbk],"set list on;set count on;set blob all;select id,s,t,b as blob_id from test;" )
#
#  f_val_log=open( os.path.join(context['temp_directory'],'tmp_val_2216.log'), "w")
#  f_val_err=open( os.path.join(context['temp_directory'],'tmp_val_2216.err'), "w")
#
#  subprocess.call([ context['fbsvcmgr_path'],"localhost:service_mgr",
#                    "action_validate",
#                    "dbname", tmpnbk
#                  ],
#                  stdout=f_val_log,
#                  stderr=f_val_err)
#  flush_and_close( f_val_log )
#  flush_and_close( f_val_err )
#
#  with open( f_val_log.name,'r') as f:
#      print(f.read())
#
#  # All of these files must be empty:
#  ###################################
#  f_list=(f_nbk1_err, f_nbk2_err, f_nbk3_err, f_val_err)
#  for i in range(len(f_list)):
#      with open( f_list[i].name,'r') as f:
#          for line in f:
#              if line.split():
#                  print( 'UNEXPECTED STDERR in file '+f_list[i].name+': '+line.upper() )
#
#  # Cleanup.
#  ###############################
#  cleanup( [i.name for i in ( f_run_sql,f_run_log, f_nbk1_log,f_nbk1_err, f_nbk2_log,f_nbk2_err, f_nbk3_log,f_nbk3_err, f_val_log,f_val_err) ] )
#
#  os.remove(tmpnbk)
#  os.remove(tmpadd)
#
#
#---

act_1 = python_act('db_1', substitutions=substitutions_1)

nbak_file_base = temp_file('nbak-file.fdb')
nbak_file_add = temp_file('nbak-file.add')

expected_stdout_1_a = """
    ID                              1
    S                               qwerty
    T                               2013-12-11 14:15:16.1780
    foo-rio-bar
    Records affected: 1
"""

expected_stdout_1_b = """
    Validation started
    Relation (TEST)
    process pointer page    0 of    1
    Index 1 (TEST_S)
    Relation (TEST) is ok
    Validation finished
"""

@pytest.mark.version('>=4.0')
def test_1(act_1: Action, nbak_file_base: Path, nbak_file_add: Path):
    with act_1.connect_server() as srv, act_1.db.connect() as con:
        # Backup base database
        srv.database.nbackup(database=str(act_1.db.db_path), backup=str(nbak_file_base),
                             level=0)
        c = con.cursor()
        # get db GUID
        c.execute('select rb.rdb$guid as db_guid from rdb$backup_history rb')
        db_guid = c.fetchone()[0]
        # Insert data
        c.execute("insert into test(id,s,t,b) values(1, 'qwerty', '11.12.2013 14:15:16.178', 'foo-rio-bar')")
        con.commit()
        # Backup changes
        srv.database.nbackup(database=str(act_1.db.db_path), backup=str(nbak_file_add),
                             guid=db_guid)
        # Restore inplace
        srv.database.nrestore(flags=SrvNBackupFlag.IN_PLACE, database=str(nbak_file_base),
                              backups=[str(nbak_file_add)])
        # Check restored database
        act_1.expected_stdout = expected_stdout_1_a
        act_1.isql(switches=['-user', act_1.db.user, '-password', act_1.db.password, str(nbak_file_base)],
                   connect_db=False,
                   input="set list on;set count on;set blob all;select id,s,t,b as blob_id from test;")
        assert act_1.clean_stdout == act_1.clean_expected_stdout
        # Validate restored database
        srv.database.validate(database=str(nbak_file_base))
        act_1.reset()
        act_1.expected_stdout = expected_stdout_1_b
        act_1.stdout = '\n'.join(srv.readlines())
        assert act_1.clean_stdout == act_1.clean_expected_stdout
