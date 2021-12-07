#coding:utf-8
#
# id:           bugs.core_3537
# title:        There is no need to undo changes made in GTT created with ON COMMIT DELETE ROWS option when transaction is rolled back
# decription:
#                   19.12.2016.
#                   After discuss with hvlad it was decided to use fetches & marks values that are issued in trace
#                   ROLLBACK_TRANSACTION statistics and evaluate ratio of these values with:
#                   1) number of inserted rows(see 'NUM_ROWS_TO_BE_ADDED' constant);
#                   2) number of data pages that table occupies (it's retieved via 'gstat -t T_FIX_TAB').
#
#                   We use three tables with the same DDL: permanent ('t_fix_tab'), GTT PRESERVE and GTT DELETE rows.
#                   All these tables are subject to DML which does insert rows.
#                   Permanent table is used for retrieving statistics of data pages that are in use after this DML.
#                   Number of rows that we add into tables should not be very high, otherwise rollback will be done via TIP,
#                   i.e. without real undone actions ==> we will not see proper ratios.
#                   After serveral runs it was decided to use value = 45000 (rows).
#
#                   All ratios should belong to some range with +/-5% of possible difference from one run to another.
#                   Concrete values of ratio were found after several runs on 2.5.7, 3.0.2 & 4.0.0
#
#                   Checked on 2.5.7.27030 (SS/SC), WI-V3.0.2.32644 (SS/SC/CS) and WI-T4.0.0.468 (SS/SC); 4.0.0.633 (CS/SS)
#
#                   Notes.
#                   1. We can estimate volume of UNDO changes in trace statistics for ROLLBACK event.
#                      This statistics was added since 2.5.2 (see CORE-3598).
#                   2. We have to use 'gstat -t <table>'instead of 'fbsvcmgr sts_table <...>'in 2.5.x - see CORE-5426.
#
#                   19.08.2020. Fixed wrong expression for difference evaluation in percents. Checked on:
#                       4.0.0.2164 SS: 8.674s.
#                       4.0.0.2119 SS: 9.736s.
#                       4.0.0.2164 CS: 10.328s.
#                       3.0.7.33356 SS: 7.333s.
#                       3.0.7.33356 CS: 9.700s.
#                       2.5.9.27150 SC: 5.884s.
#
#
# tracker_id:   CORE-3537
# min_versions: ['2.5.2']
# versions:     2.5.2
# qmid:         None

import pytest
import time
from threading import Thread, Barrier
from firebird.qa import db_factory, python_act, Action
from firebird.driver import DbWriteMode

# version: 2.5.2
# resources: None

substitutions_1 = []

init_script_1 = """
    set bail on;
    set echo on;
    create or alter procedure sp_fill_fix_tab as begin end;
    create or alter procedure sp_fill_gtt_del_rows as begin end;
    create or alter procedure sp_fill_gtt_sav_rows as begin end;

    recreate view v_field_len as
    select rf.rdb$relation_name as rel_name, f.rdb$field_length as fld_len
    from rdb$relation_fields rf
    join rdb$fields f on rf.rdb$field_source = f.rdb$field_name
    ;

    recreate table t_fix_tab(
      s1 varchar(50)
      -- unique using index t_fix_tab_s1
    );

    recreate global temporary table t_gtt_del_rows(
      s1 varchar(50)
      -- unique using index t_gtt_del_rows_s1
    ) on commit DELETE rows;

    recreate global temporary table t_gtt_sav_rows(
      s1 varchar(50)
      -- unique using index t_gtt_sav_rows_s1
    ) on commit PRESERVE rows;

    commit;

    set term ^;
    create or alter procedure sp_fill_fix_tab(a_rows int) as
        declare k int;
        declare w int;
    begin
        k=a_rows;
        select v.fld_len from v_field_len v where v.rel_name=upper('t_fix_tab') into w;
        while(k>0) do
        begin
            insert into t_fix_tab(s1) values( rpad('', :w, uuid_to_char(gen_uuid()) ) );
            if (mod(k-1, 5000) = 0) then
                rdb$set_context('USER_SESSION','DBG_FILL_FIX_TAB',a_rows - k); -- to be watched in the trace log (4DEBUG)
            k = k - 1;
        end
    end
    ^
    create or alter procedure sp_fill_gtt_del_rows(a_rows int) as
        declare k int;
        declare w int;
    begin
        k=a_rows;
        select v.fld_len from v_field_len v where v.rel_name=upper('t_gtt_del_rows') into w;
        while(k>0) do
        begin
            insert into t_gtt_del_rows(s1) values( rpad('', :w, uuid_to_char(gen_uuid()) ) );
            if (mod(k-1, 5000) = 0) then
                rdb$set_context('USER_SESSION','DBG_FILL_GTT_DEL',a_rows - k); -- to be watched in the trace log (4DEBUG)
            k = k - 1;
        end
        rdb$set_context('USER_SESSION','DBG_FILL_GTT_DEL',a_rows);
    end
    ^
    create or alter procedure sp_fill_gtt_sav_rows(a_rows int) as
        declare k int;
        declare w int;
    begin
        k=a_rows;
        select v.fld_len from v_field_len v where v.rel_name=upper('t_gtt_sav_rows') into w;
        while(k>0) do
        begin
            insert into t_gtt_sav_rows(s1) values( rpad('', :w, uuid_to_char(gen_uuid()) ) );
            if (mod(k-1, 5000) = 0) then
                rdb$set_context('USER_SESSION','DBG_FILL_GTT_SAV',a_rows - k); -- to be watched in the trace log (4DEBUG)
            k = k - 1;
        end
        rdb$set_context('USER_SESSION','DBG_FILL_GTT_SAV',a_rows);
    end
    ^
    set term ;^
    commit;
"""

db_1 = db_factory(page_size=4096, sql_dialect=3, init=init_script_1)

# test_script_1
#---
#
#  import os
#  import subprocess
#  import time
#  from fdb import services
#  from subprocess import Popen
#
#  os.environ["ISC_USER"] = user_name
#  os.environ["ISC_PASSWORD"] = user_password
#
#  # Obtain engine version:
#  engine = str(db_conn.engine_version) # convert to text because 'float' object has no attribute 'startswith'
#  db_file = db_conn.database_name
#  db_conn.close()
#
#  #---------------------------------------------
#
#  def flush_and_close(file_handle):
#      # https://docs.python.org/2/library/os.html#os.fsync
#      # If you're starting with a Python file object f,
#      # first do f.flush(), and
#      # then do os.fsync(f.fileno()), to ensure that all internal buffers associated with f are written to disk.
#      global os
#
#      file_handle.flush()
#      if file_handle.mode not in ('r', 'rb'):
#          # otherwise: "OSError: [Errno 9] Bad file descriptor"!
#          os.fsync(file_handle.fileno())
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
#  #--------------------------------------------
#
#  # Change FW to OFF in order to speed up initial data filling:
#  ##################
#
#  fn_nul = open(os.devnull, 'w')
#
#  subprocess.call([ context['fbsvcmgr_path'], "localhost:service_mgr",
#                    "action_properties", "prp_write_mode", "prp_wm_async",
#                    "dbname", db_file ],
#                    stdout = fn_nul,
#                    stderr = subprocess.STDOUT
#                 )
#
#  fn_nul.close()
#
#
#
#  # ::: NB ::: Trace config file format in 3.0 differs from 2.5 one:
#  # 1) header section must be enclosed in "[" and "]",
#  # 2) parameter-value pairs must be separated with '=' sign:
#  #    services
#  #    {
#  #      parameter =  value
#  #    }
#
#  if engine.startswith('2.5'):
#      txt = '''# Generated auto, do not edit!
#        <database %[\\\\\\\\/]security?.fdb>
#            enabled false
#        </database>
#
#        <database %[\\\\\\\\/]bugs.core_3537.fdb>
#            enabled true
#            time_threshold 0
#            log_transactions true
#            log_initfini false
#            print_perf true
#        </database>
#      '''
#  else:
#      txt = '''# Generated auto, do not edit!
#        database=%[\\\\\\\\/]security?.fdb
#        {
#            enabled = false
#        }
#        database=%[\\\\\\\\/]bugs.core_3537.fdb
#        {
#            enabled = true
#            time_threshold = 0
#            log_transactions = true
#            print_perf = true
#
#            #log_connections = true
#            #log_context = true
#            log_initfini = false
#        }
#      '''
#
#  f_trc_cfg=open( os.path.join(context['temp_directory'],'tmp_trace_3537.cfg'), 'w')
#  f_trc_cfg.write(txt)
#  flush_and_close( f_trc_cfg )
#
#  ############################
#  NUM_ROWS_TO_BE_ADDED = 45000
#  ############################
#
#  con1 = fdb.connect(dsn=dsn)
#  cur1=con1.cursor()
#
#  # Make initial data filling into PERMANENT table for retrieving later number of data pages
#  # (it should be the same for any kind of tables, including GTTs):
#  cur1.callproc('sp_fill_fix_tab', (NUM_ROWS_TO_BE_ADDED,))
#  con1.commit()
#  con1.close()
#
#  # ##############################################################
#  # S T A R T   T R A C E   i n   S E P A R A T E    P R O C E S S
#  # ##############################################################
#
#  f_trc_log=open( os.path.join(context['temp_directory'],'tmp_trace_3537.log'), "w")
#  f_trc_err=open( os.path.join(context['temp_directory'],'tmp_trace_3537.err'), "w")
#
#  p_trace = Popen( [ context['fbsvcmgr_path'], 'localhost:service_mgr', 'action_trace_start' , 'trc_cfg', f_trc_cfg.name],stdout=f_trc_log,stderr=f_trc_err)
#
#  time.sleep(1)
#
#  con1 = fdb.connect(dsn=dsn)
#  cur1=con1.cursor()
#  cur1.callproc('sp_fill_gtt_sav_rows', (NUM_ROWS_TO_BE_ADDED,))
#  con1.rollback()
#  con1.close()
#
#  con1 = fdb.connect(dsn=dsn)
#  cur1=con1.cursor()
#  cur1.callproc('sp_fill_gtt_del_rows', (NUM_ROWS_TO_BE_ADDED,))
#  con1.rollback()
#  con1.close()
#
#
#  # ####################################################
#  # G E T  A C T I V E   T R A C E   S E S S I O N   I D
#  # ####################################################
#  # Save active trace session info into file for further parsing it and obtain session_id back (for stop):
#
#  f_trc_lst = open( os.path.join(context['temp_directory'],'tmp_trace_3537.lst'), 'w')
#  subprocess.call([context['fbsvcmgr_path'], 'localhost:service_mgr', 'action_trace_list'], stdout=f_trc_lst)
#  flush_and_close( f_trc_lst )
#
#  # !!! DO NOT REMOVE THIS LINE !!!
#  time.sleep(1)
#
#  trcssn=0
#  with open( f_trc_lst.name,'r') as f:
#      for line in f:
#          i=1
#          if 'Session ID' in line:
#              for word in line.split():
#                  if i==3:
#                      trcssn=word
#                  i=i+1
#              break
#  f.close()
#  # Result: `trcssn` is ID of active trace session. Now we have to terminate it:
#
#  # ####################################################
#  # S E N D   R E Q U E S T    T R A C E   T O   S T O P
#  # ####################################################
#  if trcssn>0:
#      fn_nul = open(os.devnull, 'w')
#      subprocess.call([context['fbsvcmgr_path'], 'localhost:service_mgr', 'action_trace_stop','trc_id', trcssn], stdout=fn_nul)
#      fn_nul.close()
#      # DO NOT REMOVE THIS LINE:
#      time.sleep(2)
#
#
#  p_trace.terminate()
#  flush_and_close( f_trc_log )
#  flush_and_close( f_trc_err )
#
#  ###################
#  # Obtain statistics for table T_FIX_TAB in order to estimate numberof data pages
#  ###################
#
#  f_stat_log = open( os.path.join(context['temp_directory'],'tmp_stat_3537.log'), 'w')
#  f_stat_err = open( os.path.join(context['temp_directory'],'tmp_stat_3537.err'), 'w')
#
#  subprocess.call( [ context['gstat_path'], dsn, "-t",  't_fix_tab'.upper() ],
#                   stdout = f_stat_log,
#                   stderr = f_stat_err
#                 )
#  flush_and_close( f_stat_log )
#  flush_and_close( f_stat_err )
#
#  # Following files should be EMPTY:
#  #################
#
#  f_list=[f_stat_err, f_trc_err]
#  for i in range(len(f_list)):
#     f_name=f_list[i].name
#     if os.path.getsize(f_name) > 0:
#         with open( f_name,'r') as f:
#             for line in f:
#                 print("Unexpected STDERR, file "+f_name+": "+line)
#
#
#  dp_cnt = -1
#  with open( f_stat_log.name,'r') as f:
#    for line in f:
#      if 'data pages' in line.lower():
#         # Data pages: 1098, data page slots: 1098, average fill: 74% ==> 1098
#         dp_cnt = int(line.replace(',',' ').split()[2])
#
#  gtt_sav_fetches=-1
#  gtt_sav_marks = -1
#  gtt_del_fetches=-1
#  gtt_del_marks = -1
#  gtt_del_trace = ''
#  gtt_sav_trace = ''
#
#  with open( f_trc_log.name,'r') as f:
#    for line in f:
#      if 'fetch' in line:
#         # 2.5.7:
#         # ['370', 'ms,', '1100', 'read(s),', '1358', 'write(s),', '410489', 'fetch(es),', '93294', 'mark(s)']
#         # ['2', 'ms,', '1', 'read(s),', '257', 'write(s),', '1105', 'fetch(es),', '1102', 'mark(s)']
#         # 3.0.2:
#         # 618 ms, 1 read(s), 2210 write(s), 231593 fetch(es), 92334 mark(s)
#         # 14 ms, 1109 write(s), 7 fetch(es), 4 mark(s)
#         words = line.split()
#         for k in range(len(words)):
#           if words[k].startswith('fetch'):
#             if gtt_sav_fetches == -1:
#               gtt_sav_fetches = int( words[k-1] )
#               gtt_sav_trace = line.strip()
#             else:
#               gtt_del_fetches = int( words[k-1] )
#               gtt_del_trace = line.strip()
#
#           if words[k].startswith('mark'):
#             if gtt_sav_marks==-1:
#               gtt_sav_marks = int( words[k-1] )
#             else:
#               gtt_del_marks = int( words[k-1] )
#
#                                                                          #  2.5.7      3.0.2, 4.0.0
#                                                                          # ---------------------
#  '''
#  ratio_fetches_to_row_count_for_GTT_PRESERVE_ROWS = (1.00 * gtt_sav_fetches / NUM_ROWS_TO_BE_ADDED,   9.1219,      5.1465  )
#  ratio_fetches_to_row_count_for_GTT_DELETE_ROWS = (1.00 * gtt_del_fetches / NUM_ROWS_TO_BE_ADDED,   0.0245,      0.00015 )
#  ratio_marks_to_row_count_for_GTT_PRESERVE_ROWS = (1.00 * gtt_sav_marks / NUM_ROWS_TO_BE_ADDED,       2.0732,      2.05186 )
#  ratio_marks_to_row_count_for_GTT_DELETE_ROWS = (1.00 * gtt_del_marks / NUM_ROWS_TO_BE_ADDED,       0.0245,      0.000089 )
#
#  ratio_fetches_to_datapages_for_GTT_PRESERVE_ROWS = (1.00 * gtt_sav_fetches / dp_cnt,                   373.85,      209.776 )
#  ratio_fetches_to_datapages_for_GTT_DELETE_ROWS = (1.00 * gtt_del_fetches / dp_cnt,                   1.0063,      0.00634 )
#  ratio_marks_to_datapages_for_GTT_PRESERVE_ROWS = (1.00 * gtt_sav_marks / dp_cnt,                       84.9672,     83.6358 )
#  ratio_marks_to_datapages_for_GTT_DELETE_ROWS = (1.00 * gtt_del_marks / dp_cnt,                       1.0036,      0.00362 )
#  '''
#                                                                             #  2.5.7      3.0.2, 4.0.0
#                                                                             # ------------------------
#  check_data={
#     'ratio_fetches_to_row_count_for_GTT_PRESERVE_ROWS' : (1.00 * gtt_sav_fetches / NUM_ROWS_TO_BE_ADDED,   9.1219,      5.1465  )
#    ,'ratio_fetches_to_row_count_for_GTT_DELETE_ROWS' : (1.00 * gtt_del_fetches / NUM_ROWS_TO_BE_ADDED,   0.0245,      0.00015 )
#    ,'ratio_marks_to_row_count_for_GTT_PRESERVE_ROWS' : (1.00 * gtt_sav_marks / NUM_ROWS_TO_BE_ADDED,       2.0732,      2.05186 )
#    ,'ratio_marks_to_row_count_for_GTT_DELETE_ROWS' : (1.00 * gtt_del_marks / NUM_ROWS_TO_BE_ADDED,       0.0245,      0.000089 )
#    ,'ratio_fetches_to_datapages_for_GTT_PRESERVE_ROWS' : (1.00 * gtt_sav_fetches / dp_cnt,                   373.85,      209.776 )
#    ,'ratio_fetches_to_datapages_for_GTT_DELETE_ROWS' : (1.00 * gtt_del_fetches / dp_cnt,                   1.0063,      0.00634 )
#    ,'ratio_marks_to_datapages_for_GTT_PRESERVE_ROWS' : (1.00 * gtt_sav_marks / dp_cnt,                       84.9672,     83.6358 )
#    ,'ratio_marks_to_datapages_for_GTT_DELETE_ROWS' : (1.00 * gtt_del_marks / dp_cnt,                       1.0036,      0.00362 )
#  }
#
#
#  i = 1 if engine.startswith('2.5') else 2
#
#  MAX_DIFF_PERCENT=5.00
#  #                ^
#  #############################
#  ###   T H R E S H O L D   ###
#  #############################
#
#  fail = False
#  for k, v in sorted(check_data.iteritems()):
#    msg = ( 'Check ' + k + ': ' +
#            ( 'OK' if v[i] * ((100 - MAX_DIFF_PERCENT)/100) <= v[0] <= v[i] * (100+MAX_DIFF_PERCENT)/100
#              else 'value '+str(v[0])+' not in range '+str( v[i] ) + ' +/-'+str(MAX_DIFF_PERCENT)+'%'
#            )
#          )
#    print(msg)
#    failed_flag = ('not in range' in msg)
#
#  if failed_flag:
#     print('Trace for GTT PRESERVE rows: ' + gtt_sav_trace)
#     print('Trace for GTT DELETE   rows: ' + gtt_del_trace)
#
#  # CLEANUP
#  #########
#  cleanup( [i.name for i in (f_trc_cfg, f_trc_log, f_trc_err, f_stat_log, f_stat_err, f_trc_lst) ] )
#
#
#---

act_1 = python_act('db_1', substitutions=substitutions_1)

expected_stdout_1 = """
    Check ratio_fetches_to_datapages_for_GTT_DELETE_ROWS: OK
    Check ratio_fetches_to_datapages_for_GTT_PRESERVE_ROWS: OK
    Check ratio_fetches_to_row_count_for_GTT_DELETE_ROWS: OK
    Check ratio_fetches_to_row_count_for_GTT_PRESERVE_ROWS: OK
    Check ratio_marks_to_datapages_for_GTT_DELETE_ROWS: OK
    Check ratio_marks_to_datapages_for_GTT_PRESERVE_ROWS: OK
    Check ratio_marks_to_row_count_for_GTT_DELETE_ROWS: OK
    Check ratio_marks_to_row_count_for_GTT_PRESERVE_ROWS: OK
"""

def trace_session(act: Action, b: Barrier):
    cfg30 = ['# Trace config, format for 3.0. Generated auto, do not edit!',
             f'database=%[\\\\/]{act.db.db_path.name}',
             '{',
             '  enabled = true',
             '  log_transactions = true',
             '  print_perf = true',
             #'  log_connections = true',
             #'  log_procedure_start = true',
             #'  log_procedure_finish = true',
             '  log_initfini = false',
             '}']
    with act.connect_server() as srv:
        srv.trace.start(config='\n'.join(cfg30))
        b.wait()
        for line in srv:
            print(line)

@pytest.mark.version('>=2.5.2')
def test_1(act_1: Action, capsys):
    NUM_ROWS_TO_BE_ADDED = 45000
    # Change FW to OFF in order to speed up initial data filling
    with act_1.connect_server() as srv:
        srv.database.set_write_mode(database=act_1.db.db_path, mode=DbWriteMode.ASYNC)
    # Make initial data filling into PERMANENT table for retrieving later number of data pages
    # (it should be the same for any kind of tables, including GTTs):
    with act_1.db.connect() as con:
        c = con.cursor()
        c.call_procedure('sp_fill_fix_tab', [NUM_ROWS_TO_BE_ADDED])
        con.commit()
    #
    b = Barrier(2)
    trace_thread = Thread(target=trace_session, args=[act_1, b])
    trace_thread.start()
    b.wait()
    #
    with act_1.db.connect() as con1:
        c = con1.cursor()
        c.call_procedure('sp_fill_gtt_sav_rows', [NUM_ROWS_TO_BE_ADDED])
        con1.rollback()

    with act_1.db.connect() as con2:
        c = con2.cursor()
        c.call_procedure('sp_fill_gtt_del_rows', [NUM_ROWS_TO_BE_ADDED])
        con2.rollback()
    # Somehow sleep is necessary otherwise "sp_fill_gtt_del_rows" will not show up in trace log
    time.sleep(3)
    with act_1.connect_server() as srv:
        for session in list(srv.trace.sessions.keys()):
            srv.trace.stop(session_id=session)
        trace_thread.join(3.0)
        if trace_thread.is_alive():
            pytest.fail('Trace thread still alive')
    trace_output = capsys.readouterr().out
    # Obtain statistics for table T_FIX_TAB in order to estimate numberof data pages
    dp_cnt = 0
    act_1.gstat(switches=['-a','-t', 'T_FIX_TAB', '-u', act_1.db.user, '-p', act_1.db.password])
    for line in act_1.stdout.splitlines():
        if 'data pages' in line.lower():
            # Data pages: 1098, data page slots: 1098, average fill: 74% ==> 1098
            dp_cnt = int(line.replace(',', ' ').split()[2])
    #
    gtt_sav_fetches = -1
    gtt_sav_marks = -1
    gtt_del_fetches = -1
    gtt_del_marks = -1
    gtt_del_trace = ''
    gtt_sav_trace = ''
    for line in trace_output.splitlines():
        if 'fetch' in line:
            # 2.5.7:
            # ['370', 'ms,', '1100', 'read(s),', '1358', 'write(s),', '410489', 'fetch(es),', '93294', 'mark(s)']
            # ['2', 'ms,', '1', 'read(s),', '257', 'write(s),', '1105', 'fetch(es),', '1102', 'mark(s)']
            # 3.0.2:
            # 618 ms, 1 read(s), 2210 write(s), 231593 fetch(es), 92334 mark(s)
            # 14 ms, 1109 write(s), 7 fetch(es), 4 mark(s)
            words = line.split()
            for k in range(len(words)):
                if words[k].startswith('fetch'):
                    if gtt_sav_fetches == -1:
                        gtt_sav_fetches = int(words[k-1])
                        gtt_sav_trace = line.strip()
                    else:
                        gtt_del_fetches = int(words[k-1])
                        gtt_del_trace = line.strip()

                if words[k].startswith('mark'):
                    if gtt_sav_marks==-1:
                        gtt_sav_marks = int(words[k-1])
                    else:
                        gtt_del_marks = int(words[k-1])
    #
    check_data = {
        'ratio_fetches_to_row_count_for_GTT_PRESERVE_ROWS' : (1.00 * gtt_sav_fetches / NUM_ROWS_TO_BE_ADDED, 9.1219,  5.1465),
        'ratio_fetches_to_row_count_for_GTT_DELETE_ROWS' : (1.00 * gtt_del_fetches / NUM_ROWS_TO_BE_ADDED,   0.0245,  0.00015),
        'ratio_marks_to_row_count_for_GTT_PRESERVE_ROWS' : (1.00 * gtt_sav_marks / NUM_ROWS_TO_BE_ADDED,     2.0732,  2.05186),
        'ratio_marks_to_row_count_for_GTT_DELETE_ROWS' : (1.00 * gtt_del_marks / NUM_ROWS_TO_BE_ADDED,       0.0245,  0.000089),
        'ratio_fetches_to_datapages_for_GTT_PRESERVE_ROWS' : (1.00 * gtt_sav_fetches / dp_cnt,               373.85,  209.776),
        'ratio_fetches_to_datapages_for_GTT_DELETE_ROWS' : (1.00 * gtt_del_fetches / dp_cnt,                 1.0063,  0.00634),
        'ratio_marks_to_datapages_for_GTT_PRESERVE_ROWS' : (1.00 * gtt_sav_marks / dp_cnt,                   84.9672, 83.6358),
        'ratio_marks_to_datapages_for_GTT_DELETE_ROWS' : (1.00 * gtt_del_marks / dp_cnt,                     1.0036,  0.00362),
    }
    i = 2 #  FB 3+
    MAX_DIFF_PERCENT = 5.0
    # THRESHOLD
    failed_flag = False
    for k, v in sorted(check_data.items()):
        msg = ('Check ' + k + ': ' +
               ('OK' if v[i] * ((100 - MAX_DIFF_PERCENT)/100) <= v[0] <= v[i] * (100+MAX_DIFF_PERCENT) / 100
                else 'value '+str(v[0])+' not in range '+str( v[i] ) + ' +/-' + str(MAX_DIFF_PERCENT) + '%')
               )
        print(msg)
        failed_flag = 'not in range' in msg

    if failed_flag:
        print('Trace for GTT PRESERVE rows: ' + gtt_sav_trace)
        print('Trace for GTT DELETE   rows: ' + gtt_del_trace)
    #
    act_1.expected_stdout = expected_stdout_1
    act_1.stdout = capsys.readouterr().out
    assert act_1.clean_stdout == act_1.clean_expected_stdout
