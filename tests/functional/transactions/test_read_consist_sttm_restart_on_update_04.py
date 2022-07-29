#coding:utf-8

"""
ID:          transactions.read-consist-sttm-restart-on-update-04
TITLE:       READ CONSISTENCY. Check creation of new statement-level snapshot and restarting changed caused by UPDATE. Test-04.
DESCRIPTION:
  Initial article for reading:
          https://asktom.oracle.com/pls/asktom/f?p=100:11:::::P11_QUESTION_ID:11504247549852
          Note on terms which are used there: "BLOCKER", "LONG" and "FIRSTLAST" - their names are slightly changed here
          to: LOCKER-1, WORKER and LOCKER-2 respectively.
      See also: doc/README.read_consistency.md

      **********************************************

      This test verifies that statement-level snapshot and restart will be performed when "main" session ("worker")
      performs UPDATE statement and is involved in update conflicts.
      ("When update conflict is detected <...> then engine <...> creates new statement-level snapshot and restart execution...")

      ::: NB :::
      This test uses script %FBT_REPO%/files/read-consist-sttm-restart-DDL.sql which contains common DDL for all other such tests.
      Particularly, it contains two TRIGGERS (TLOG_WANT and TLOG_DONE) which are used for logging of planned actions and actual
      results against table TEST. These triggers use AUTONOMOUS transactions in order to have ability to see results in any
      outcome of test.

      ###############
      Following scenario if executed here (see also: "doc/README.read_consistency.md"; hereafer is marked as "DOC"):
      * five rows are inserted into the table TEST, with ID = 1...5 and x = 1...5.

      * session 'locker-1' ("BLOCKER" in Tom Kyte's article ):
            update test set id = id where id = 1

      * session 'worker' ("LONG" in TK article) has mission:
            update test where set id = -id where id <= 2 order by id DESC rows 4; // using TIL = read committed read consistency

          // Execution will have PLAN ORDER <DESCENDING_INDEX>.
          // It will update rows starting with ID = 2 but can not change row with ID = 1 because of locker-1.
          // Update conflict appears here and, because of this, worker temporary changes its TIL to RC no record_version (RC NRV).
          // [DOC]: "a) transaction isolation mode temporarily switched to the READ COMMITTED *NO RECORD VERSION MODE*"
          // This (new) TIL allows worker further to see all committed versions, regardless of its own snapshot.

      * session 'locker-2' ("FIRSTLAST" in TK article): replaces ID = 5 with new value = -5, then commits
        and locks this record again:
            (1) commit;
            (2) update test set id = -5 where abs(id)=5;
            (3) commit;
            (4) update test set id = id where abs(id)=5;
         // session-'worker' remains waiting at this point because row with ID = 1 is still occupied by by locker-1.
         // but worker must further see record with (new) id = -5 because its TIL was changed to RC NO RECORD_VERSION.


      * session 'locker-1': replaces ID = 4 with new value = -4, then commits and locks this record again:
            (1) commit;
            (2) update test set id = -4 where abs(id)=4;
            (3) commit;
            (4) update test set id = id where abs(id)=4;

        // This: '(1) commit' - will release record with ID = 1. Worker sees this record and put write-lock on it.
        // [DOC]: "b) engine put write lock on conflicted record"
        // But it is only 2nd row of total 4 that worker must delete.
        // Because of TIL = RC NRV session-'worker' must see all committed records regardless on its own snapshot.
        // Worker resumes search for any rows with ID < 2, and it does this with taking in account required order
        // of its DML (i.e. 'ORDER BY ID DESC ...')
        // [DOC]: "c) engine continue to evaluate remaining records of update/delete cursor and put write locks on it too"
        // Worker starts to search records which must be involved in its DML and *found* first sucn row with ID = -5.
        // NB. This row currently can NOT be deleted by worker because locker-2 has uncommitted update of it.
        // BECAUSE OF FACT THAT AT LEAST ONE ROW *WAS FOUND* - STATEMENT-LEVEL RESTART *NOT* YET OCCURS HERE.
        // :::!! NB, AGAIN !! ::: restart NOT occurs here because at least one records found, see:
        // [DOC]: "d) when there is *no more* records to fetch, engine start to undo all actions performed since
        //            top-level statement execution starts and preserve already taken write locks
        //         e) then engine restores transaction isolation mode as READ COMMITTED *READ CONSISTENCY*,
        //            creates new statement-level snapshot and restart execution of top-level statement."

      * session 'locker-2': replaces ID = 3 with new value = -3, then commits and locks this record again:
            (1) commit;
            (2) update test set id = -3 where abs(id)=3;
            (3) commit;
            (4) update test set id = id where abs(id)=3;

        // This: '(1) commit' - will release record with ID = -5. Worker sees this record and put write-lock on it.
        // But this is only 3rd row of total 4 that worker must update.
        // Because of worker TIL = RC NRV, he must see all committed records regardless on its own snapshot.
        // Worker resumes search for any rows with ID < -5, and it does this with taking in account required order
        // of its DML (i.e. 'ORDER BY ID DESC ...')
        // [DOC]: "c) engine continue to evaluate remaining records of update/delete cursor and put write locks on it too"
        // There are no such rows in the table.
        // BECAUSE OF FACT THAT NO RECORDS FOUND, WORKER DOES UNDO BUT KEEP LOCKS AND THEN MAKES FIRST STATEMENT-LEVEL RESTART.
        // [DOC]: "d) when there is no more records to fetch, engine start to undo all actions ... and preserve already taken write locks
        //         e) then engine restores transaction isolation mode as READ COMMITTED *READ CONSISTENCY*,
        //           creates new statement-level snapshot and restart execution of top-level statement."

      * session 'locker-1':
            commit;
        // This will release record with ID=-4. Worker sees this record and put write-lock on it.
        // At this point worker has proceeded all required number of rows for DML: 2, 1, -4 and -5.
        // BECAUSE OF FACT THAT ALL ROWS WERE PROCEEDED, WORKER DOES UNDO BUT KEEP LOCKS AND THEN MAKES SECOND STATEMENT-LEVEL RESTART.
        // [DOC]: "d) when there is no more records to fetch, engine start to undo all actions ... and preserve already taken write locks
        //         e) then engine restores transaction isolation mode as READ COMMITTED *READ CONSISTENCY*,
        //            creates new statement-level snapshot and restart execution of top-level statement."
        // After this restart worker will waiting for row with ID = -3 (it sees this because of TIL = RC NRV).

      * session 'locker-2':
          commit.
        // This releases row with ID=-3. Worker sees this record and put write-lock on it.
        // Records with ID = 2, 1, -4 and -5 already have been locked, but worker must update only FOUR rows (see its DML statement).
        // Thus only rows with ID = 2, 1, -3 and -4 will be updated. Record with ID = -5 must *remain* in the table.
        // At this point worker has proceeded all required rows that meet condition for DML: 2, 1, -3 and -4.
        // BECAUSE OF FACT THAT ALL ROWS WERE PROCEEDED, WORKER DOES UNDO BUT KEEP LOCKS AND THEN MAKES THIRD STATEMENT-LEVEL RESTART.
        // [DOC]: "d) when there is no more records to fetch, engine start to undo all actions ... and preserve already taken write locks
        //         e) then engine restores transaction isolation mode as READ COMMITTED *READ CONSISTENCY*,
        //            creates new statement-level snapshot and restart execution of top-level statement."

      Expected result:
      * session-'worker' must *successfully* complete deletion of 4 rows (but only two of them did exist at the starting point).
        Record with ID = -5 must remain in the table.

      * four unique values must be in the column TLOG_DONE.SNAP_NO for session-'worker' when it performed UPDATE statement: first of them
        was created by initial statement start and all others reflect three restarts (this column has values which are evaluated using
        rdb$get_context('SYSTEM', 'SNAPSHOT_NUMBER') -- see trigger TEST_AIUD).
        It is enough to count these values using COUNT(*) or enumarate them by DENSE_RANK() function.

      NOTE: concrete values of fields TRN, GLOBAL_CN and SNAP_NO in the TLOG_DONE can differ from one to another run!
      This is because of concurrent nature of connections that work against database. We must not assume that these values will be constant.

      ################

      Checked on 4.0.0.2195 SS/CS
      26.09.2020: added for-loop in order to check different target objects: TABLE ('test') and VIEW ('v_test'), see 'checked_mode'.
FBTEST:      functional.transactions.read_consist_sttm_restart_on_update_04
NOTES:
[29.07.2022] pzotov
    Checked on 4.0.1.2692, 5.0.0.591
"""

import subprocess
import pytest
from firebird.qa import *
from pathlib import Path
import time

db = db_factory()

act = python_act('db', substitutions=[('=', ''), ('[ \t]+', ' ')])

fn_worker_sql = temp_file('tmp_worker.sql')
fn_worker_log = temp_file('tmp_worker.log')
fn_worker_err = temp_file('tmp_worker.err')

expected_stdout = """
    checked_mode: table, STDLOG: Records affected: 4


    checked_mode: table, STDLOG:      ID
    checked_mode: table, STDLOG: =======
    checked_mode: table, STDLOG:      -5
    checked_mode: table, STDLOG:      -2
    checked_mode: table, STDLOG:      -1
    checked_mode: table, STDLOG:       3
    checked_mode: table, STDLOG:       4
    checked_mode: table, STDLOG: Records affected: 5

    checked_mode: table, STDLOG:  OLD_ID OP              SNAP_NO_RANK
    checked_mode: table, STDLOG: ======= ====== =====================
    checked_mode: table, STDLOG:       2 UPD                        1
    checked_mode: table, STDLOG:       2 UPD                        2
    checked_mode: table, STDLOG:       1 UPD                        2
    checked_mode: table, STDLOG:       2 UPD                        3
    checked_mode: table, STDLOG:       1 UPD                        3
    checked_mode: table, STDLOG:       2 UPD                        4
    checked_mode: table, STDLOG:       1 UPD                        4
    checked_mode: table, STDLOG:      -3 UPD                        4
    checked_mode: table, STDLOG:      -4 UPD                        4
    checked_mode: table, STDLOG: Records affected: 9



    checked_mode: view, STDLOG: Records affected: 4


    checked_mode: view, STDLOG:      ID
    checked_mode: view, STDLOG: =======
    checked_mode: view, STDLOG:      -5
    checked_mode: view, STDLOG:      -2
    checked_mode: view, STDLOG:      -1
    checked_mode: view, STDLOG:       3
    checked_mode: view, STDLOG:       4
    checked_mode: view, STDLOG: Records affected: 5

    checked_mode: view, STDLOG:  OLD_ID OP              SNAP_NO_RANK
    checked_mode: view, STDLOG: ======= ====== =====================
    checked_mode: view, STDLOG:       2 UPD                        1
    checked_mode: view, STDLOG:       2 UPD                        2
    checked_mode: view, STDLOG:       1 UPD                        2
    checked_mode: view, STDLOG:       2 UPD                        3
    checked_mode: view, STDLOG:       1 UPD                        3
    checked_mode: view, STDLOG:       2 UPD                        4
    checked_mode: view, STDLOG:       1 UPD                        4
    checked_mode: view, STDLOG:      -3 UPD                        4
    checked_mode: view, STDLOG:      -4 UPD                        4
    checked_mode: view, STDLOG: Records affected: 9
"""

@pytest.mark.version('>=4.0')
def test_1(act: Action, fn_worker_sql: Path, fn_worker_log: Path, fn_worker_err: Path, capsys):
    sql_init = (act.files_dir / 'read-consist-sttm-restart-DDL.sql').read_text()

    for checked_mode in('table', 'view'):
        target_obj = 'test' if checked_mode == 'table' else 'v_test'

        sql_addi = f'''
            set term ^;
            execute block as
            begin
                rdb$set_context('USER_SESSION', 'WHO', 'INIT_DATA');
            end
            ^
            set term ;^
            insert into {target_obj}(id, x)
            select row_number()over(),row_number()over()
            from rdb$types rows 5;
            commit;
        '''

        act.isql(switches=['-q'], input = ''.join( (sql_init, sql_addi) ) )

        with act.db.connect() as con_lock_1, act.db.connect() as con_lock_2:
            for i,c in enumerate((con_lock_1,con_lock_2)):
                sttm = f"execute block as begin rdb$set_context('USER_SESSION', 'WHO', 'LOCKER #{i+1}'); end"
                c.execute_immediate(sttm)


            #########################
            ###  L O C K E R - 1  ###
            #########################

            con_lock_1.execute_immediate( f'update {target_obj} set id=id where id=1' )

            worker_sql = f'''
                set list on;
                set autoddl off;
                set term ^;
                execute block returns (whoami varchar(30)) as
                begin
                    whoami = 'WORKER'; -- , ATT#' || current_connection;
                    rdb$set_context('USER_SESSION','WHO', whoami);
                    -- suspend;
                end
                ^
                set term ;^
                commit;
                SET KEEP_TRAN_PARAMS ON;
                set transaction read committed read consistency;
                --select current_connection, current_transaction from rdb$database;
                set list off;
                set wng off;

                --set plan on;
                set count on;
                update {target_obj} set id = -id where id <= 2 order by id DESC rows 4; -- THIS MUST HANG BECAUSE OF LOCKERs

                -- check results:
                -- ###############

                select id from {target_obj} order by id; -- one record must remain, with ID = -5

                select v.old_id, v.op, v.snap_no_rank -- snap_no_rank must have four unique values: 1,2,3 and 4.
                from v_worker_log v
                where v.op = 'upd';

                --set width who 10;
                -- DO NOT check this! Values can differ here from one run to another!
                -- select id, trn, who, old_id, new_id, op, rec_vers, global_cn, snap_no from tlog_done order by id;
                rollback;

            '''

            fn_worker_sql.write_text(worker_sql)

            with fn_worker_log.open(mode='w') as hang_out, fn_worker_err.open(mode='w') as hang_err:

                ############################################################################
                ###  L A U N C H     W O R K E R    U S I N G     I S Q L,   A S Y N C.  ###
                ############################################################################
                p_worker = subprocess.Popen([act.vars['isql'], '-i', str(fn_worker_sql),
                                               '-user', act.db.user,
                                               '-password', act.db.password,
                                               '-pag', '999999',
                                               act.db.dsn
                                            ],
                                              stdout = hang_out,
                                              stderr = hang_err
                                           )
                time.sleep(1)


                #########################
                ###  L O C K E R - 2  ###
                #########################

                # Change ID so that it **will* be included in the set of rows that must be affected by session-worker:
                con_lock_2.execute_immediate( f'update {target_obj} set id = -5 where abs(id) = 5;' )
                con_lock_2.commit()
                con_lock_2.execute_immediate( f'update {target_obj} set id = id where abs(id) = 5;' )


                con_lock_1.commit() # releases record with ID=1 (allow it to be deleted by session-worker)

                # Change ID so that it **will* be included in the set of rows that must be affected by session-worker:
                con_lock_1.execute_immediate( f'update {target_obj} set id = -4 where abs(id) = 4;' )
                con_lock_1.commit()
                con_lock_1.execute_immediate( f'update {target_obj} set id = id where abs(id) = 4;' )


                con_lock_2.commit() # releases record with ID = -5, but session-worker is waiting for record with ID = -4 (that was changed by locker-1).
                con_lock_2.execute_immediate( f'update {target_obj} set id = -3 where abs(id) = 3;' )
                con_lock_2.commit()
                con_lock_2.execute_immediate( f'update {target_obj} set id = id where abs(id) = 3;' )

                con_lock_1.commit() # This releases row with ID=-4 but session-worker is waiting for ID = - 3 (changed by locker-2).
                con_lock_2.commit() # This releases row with ID=-3. No more locked rows so session-worker can finish its mission.

                # Here we wait for ISQL complete its mission:
                p_worker.wait()


        for g in (fn_worker_log, fn_worker_err):
            with g.open() as f:
                for line in f:
                    if line.split():
                        if g == fn_worker_log:
                            print(f'checked_mode: {checked_mode}, STDLOG: {line}')
                        else:
                            print(f'UNEXPECTED STDERR {line}')

    act.expected_stdout = expected_stdout
    act.stdout = capsys.readouterr().out
    assert act.clean_stdout == act.clean_expected_stdout
