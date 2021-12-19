#coding:utf-8
#
# id:           bugs.core_6166
# title:        Problems with long object names (> 255 bytes)
# decription:
#                   We define several objects with non-ascii names of max allowed length (63 characters) and make check statements.
#               	Result no matter, but these statements must finished without errors.
#               	Then we extract metadata and add the same set of check statements to this sql script.
#               	Applying of this script to empty (another) database must end also without any error.
#
#               	Confirmed problem on 4.0.0.1633: ISQL crashed when performing script which contains DDL with non-ascii names
#               	of  max allowed len (63 characters).
#
#               	Checked on 4.0.0.1635: OK, 4.821s.
#
# tracker_id:   CORE-6166
# min_versions: ['4.0']
# versions:     4.0
# qmid:         None

import pytest
from firebird.qa import db_factory, python_act, Action

# version: 4.0
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(charset='UTF8', sql_dialect=3, init=init_script_1)

# test_script_1
#---
#
#  import os
#  import subprocess
#  import time
#
#  os.environ["ISC_USER"] = user_name
#  os.environ["ISC_PASSWORD"] = user_password
#  db_conn.close()
#
#  #--------------------------------------------
#
#  def flush_and_close( file_handle ):
#      # https://docs.python.org/2/library/os.html#os.fsync
#      # If you're starting with a Python file object f,
#      # first do f.flush(), and
#      # then do os.fsync(f.fileno()), to ensure that all internal buffers associated with f are written to disk.
#      global os
#
#      file_handle.flush()
#      if file_handle.mode not in ('r', 'rb') and file_handle.name != os.devnull:
#          # otherwise: "OSError: [Errno 9] Bad file descriptor"!
#          os.fsync(file_handle.fileno())
#      file_handle.close()
#
#  #--------------------------------------------
#
#  def cleanup( f_names_list ):
#      global os
#      for f in f_names_list:
#         if type(f) == file:
#            del_name = f.name
#         elif type(f) == str:
#            del_name = f
#         else:
#            print('Unrecognized type of element:', f, ' - can not be treated as file.')
#            del_name = None
#
#         if del_name and os.path.isfile( del_name ):
#             os.remove( del_name )
#
#  #--------------------------------------------
#
#
#  sql_ddl='''
#  	set term ^;
#  	recreate package "ПакетДляРешенияЛинейныхГиперболическихИТрансцендентныхУравнений" as
#  	begin
#  		function "МетодЗейделяДляЛинейныхГиперболическихИТрансцендентныхУравнений"() returns int;
#  		function "МетодНьютонаДляЛинейныхГиперболическихИТрансцендентныхУравнений"() returns int;
#  	end
#  	^
#  	recreate package body "ПакетДляРешенияЛинейныхГиперболическихИТрансцендентныхУравнений" as
#  	begin
#  		function "МетодЗейделяДляЛинейныхГиперболическихИТрансцендентныхУравнений"() returns int as
#  		begin
#  			return 123;
#  		end
#  		function "МетодНьютонаДляЛинейныхГиперболическихИТрансцендентныхУравнений"() returns int as
#  		begin
#  			return 456;
#  		end
#
#  	end
#  	^
#  	set term ;^
#  	commit;
#  	create table "КоэффициентыДляЛинейныхГиперболическихИТрансцендентныхУравнений" (
#  		"КоэффициентЦДляЛинейныхГиперболическихИТрансцендентныхУравнений" int
#  	   ,"КоэффициентЫДляЛинейныхГиперболическихИТрансцендентныхУравнений" int
#  	   ,"КоэффициентЧДляЛинейныхГиперболическихИТрансцендентныхУравнений" int
#  	);
#  	create unique index "КоэффициентыЛинейныхГиперболическихИТрансцендентныхУравненийЦЫЧ"
#  	on "КоэффициентыДляЛинейныхГиперболическихИТрансцендентныхУравнений" (
#  		"КоэффициентЦДляЛинейныхГиперболическихИТрансцендентныхУравнений"
#  	   ,"КоэффициентЫДляЛинейныхГиперболическихИТрансцендентныхУравнений"
#  	   ,"КоэффициентЧДляЛинейныхГиперболическихИТрансцендентныхУравнений"
#  	);
#  	commit;
#
#  '''
#
#  sql_chk='''
#
#      show package;
#  	show index "КоэффициентыДляЛинейныхГиперболическихИТрансцендентныхУравнений";
#  	set list on;
#  	select "ПакетДляРешенияЛинейныхГиперболическихИТрансцендентныхУравнений"."МетодЗейделяДляЛинейныхГиперболическихИТрансцендентныхУравнений"() from rdb$database;
#  	select "ПакетДляРешенияЛинейныхГиперболическихИТрансцендентныхУравнений"."МетодНьютонаДляЛинейныхГиперболическихИТрансцендентныхУравнений"() from rdb$database;
#  	rollback;
#  '''
#
#
#  f_chk_query_sql=open( os.path.join(context['temp_directory'],'tmp_6166_chk_query.sql'), 'w')
#  f_chk_query_sql.write( sql_ddl + sql_chk )
#  flush_and_close( f_chk_query_sql )
#
#  f_chk_query_log = open( os.path.join(context['temp_directory'],'tmp_isql_6166_chk_query.log'), 'w' )
#  f_chk_query_err = open( os.path.join(context['temp_directory'],'tmp_isql_6166_chk_query.err'), 'w')
#  subprocess.call( [context['isql_path'], dsn, "-ch", "utf8", "-i", f_chk_query_sql.name], stdout=f_chk_query_log, stderr=f_chk_query_err )
#  flush_and_close( f_chk_query_log )
#  flush_and_close( f_chk_query_err )
#
#
#  if os.path.getsize( f_chk_query_err.name ) == 0:
#  	with open( f_chk_query_log.name,'r') as f:
#  		for line in f:
#  			if line.split():
#  				print('CHECK STATEMENTS, INITIAL: '+line)
#
#  	f_chk_metadata_sql=open( os.path.join(context['temp_directory'],'tmp_6166_metadata.sql'), 'w')
#  	subprocess.call( [context['isql_path'], dsn, "-ch", "utf8", "-x" ], stdout=f_chk_metadata_sql, stderr=subprocess.STDOUT )
#  	f_chk_metadata_sql.write( sql_chk )
#  	flush_and_close( f_chk_metadata_sql )
#
#  	f_chk_metadata_fdb = os.path.join(context['temp_directory'],'tmp_6166_metadata.fdb')
#  	if os.path.isfile( f_chk_metadata_fdb ):
#  		os.remove( f_chk_metadata_fdb )
#  	chk_conn = fdb.create_database( dsn = 'localhost:'+f_chk_metadata_fdb )
#  	chk_conn.close()
#
#  	f_chk_metadata_log = open( os.path.join(context['temp_directory'],'tmp_6166_metadata.log'), 'w' )
#  	f_chk_metadata_err = open( os.path.join(context['temp_directory'],'tmp_6166_metadata.err'), 'w' )
#  	subprocess.call( [context['isql_path'], 'localhost:'+f_chk_metadata_fdb, "-ch", "utf8", "-i", f_chk_metadata_sql.name ], stdout=f_chk_metadata_log, stderr=f_chk_metadata_err )
#  	flush_and_close( f_chk_metadata_log )
#  	flush_and_close( f_chk_metadata_err )
#
#  	with open( f_chk_metadata_err.name,'r') as f:
#  		for line in f:
#  			if line.split():
#  				print('UNEXPECTED ERROR IN THE EXTRACTED METADATA SQL: '+line)
#
#  	with open( f_chk_metadata_log.name,'r') as f:
#  		for line in f:
#  			if line.split():
#  				print('CHECK STATEMENTS ON EXTRACTED METADATA: '+line)
#
#  else:
#  	with open( f_chk_query_err.name,'r') as f:
#  		for line in f:
#  			if line.split():
#  				print('UNEXPECTED ERROR IN INITIAL CHECK STATEMENTS: '+line)
#
#  # cleanup:
#  ##########
#  time.sleep(1)
#  cleanup( ( f_chk_query_sql, f_chk_query_log, f_chk_query_err, f_chk_metadata_sql, f_chk_metadata_log, f_chk_metadata_err,f_chk_metadata_fdb ) )
#
#---

act_1 = python_act('db_1', substitutions=substitutions_1)

expected_stdout_1 = """
    ПакетДляРешенияЛинейныхГиперболическихИТрансцендентныхУравнений
    КоэффициентыЛинейныхГиперболическихИТрансцендентныхУравненийЦЫЧ UNIQUE INDEX ON КоэффициентыДляЛинейныхГиперболическихИТрансцендентныхУравнений(КоэффициентЦДляЛинейныхГиперболическихИТрансцендентныхУравнений, КоэффициентЫДляЛинейныхГиперболическихИТрансцендентныхУравнений, КоэффициентЧДляЛинейныхГиперболическихИТрансцендентныхУравнений)
    МетодЗейделяДляЛинейныхГиперболическихИТрансцендентныхУравнений 123
    МетодНьютонаДляЛинейныхГиперболическихИТрансцендентныхУравнений 456
"""

ddl_script = """
    set term ^;
    recreate package "ПакетДляРешенияЛинейныхГиперболическихИТрансцендентныхУравнений" as
    begin
            function "МетодЗейделяДляЛинейныхГиперболическихИТрансцендентныхУравнений"() returns int;
            function "МетодНьютонаДляЛинейныхГиперболическихИТрансцендентныхУравнений"() returns int;
    end
    ^
    recreate package body "ПакетДляРешенияЛинейныхГиперболическихИТрансцендентныхУравнений" as
    begin
            function "МетодЗейделяДляЛинейныхГиперболическихИТрансцендентныхУравнений"() returns int as
            begin
                    return 123;
            end
            function "МетодНьютонаДляЛинейныхГиперболическихИТрансцендентныхУравнений"() returns int as
            begin
                    return 456;
            end

    end
    ^
    set term ;^
    commit;
    create table "КоэффициентыДляЛинейныхГиперболическихИТрансцендентныхУравнений" (
            "КоэффициентЦДляЛинейныхГиперболическихИТрансцендентныхУравнений" int
       ,"КоэффициентЫДляЛинейныхГиперболическихИТрансцендентныхУравнений" int
       ,"КоэффициентЧДляЛинейныхГиперболическихИТрансцендентныхУравнений" int
    );
    create unique index "КоэффициентыЛинейныхГиперболическихИТрансцендентныхУравненийЦЫЧ"
    on "КоэффициентыДляЛинейныхГиперболическихИТрансцендентныхУравнений" (
            "КоэффициентЦДляЛинейныхГиперболическихИТрансцендентныхУравнений"
       ,"КоэффициентЫДляЛинейныхГиперболическихИТрансцендентныхУравнений"
       ,"КоэффициентЧДляЛинейныхГиперболическихИТрансцендентныхУравнений"
    );
    commit;
"""

test_script = """
    show package;
    show index "КоэффициентыДляЛинейныхГиперболическихИТрансцендентныхУравнений";
    set list on;
    select "ПакетДляРешенияЛинейныхГиперболическихИТрансцендентныхУравнений"."МетодЗейделяДляЛинейныхГиперболическихИТрансцендентныхУравнений"() from rdb$database;
    select "ПакетДляРешенияЛинейныхГиперболическихИТрансцендентныхУравнений"."МетодНьютонаДляЛинейныхГиперболическихИТрансцендентныхУравнений"() from rdb$database;
    rollback;
"""

@pytest.mark.version('>=4.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.isql(switches=[], input=ddl_script + test_script, charset='utf8')
    assert act_1.clean_stdout == act_1.clean_expected_stdout
    # Extract metadata
    act_1.reset()
    act_1.isql(switches=['-x'], charset='utf8')
    meta = act_1.stdout
    # drop + recreate database
    act_1.db.drop()
    act_1.db.create(sql_dialect=3)
    # Recereate metadata
    act_1.reset()
    act_1.isql(switches=[], input=meta, charset='utf8')
    # Check 2
    act_1.reset()
    act_1.expected_stdout = expected_stdout_1
    act_1.isql(switches=[], input=test_script, charset='utf8')
    assert act_1.clean_stdout == act_1.clean_expected_stdout
