#coding:utf-8

"""
ID:          issue-5939
ISSUE:       5939
TITLE:       Unique constraint not working in encrypted database on first command
DESCRIPTION:

    Test uses Firebird built-in encryption plugin wich actually does encryption using trivial algorithm.
    Before running this test following prerequisites must be met:
        1. Files fbSampleDbCrypt.conf and libfbSampleDbCrypt.so/fbSampleDbCrypt.dll must present in the $FB_HOME/plugins folder;
        2. File fbSampleDbCrypt.conf must contain line: Auto = yes
        3. File $QA_HOME/pytest.ini must contain line with 'encryption' marker declaration.
    ### ACHTUNG ###
    Unfortunately, there is no files fbSampleDbCrypt.* in FB 3.x snapshots (at least for June-2022).
    One need to take both thiese files from any FB 4.x snapshot (they have backward compatibility).
    On FB 4.x these files can be found here: $FB_HOME/examples/prebuilt/plugins/
    ###############

    We open connection to DB and run 'ALTER DATABASE ENCRYPT.../DECRYPT'.
    One need to keep connection opened for several seconds in order to give encryption thread be fully completed.
    Duration of this delay depends on concurrent workload, usually it is almost zero.
    But in this test it can be tuned - see variable 'MAX_ENCRYPT_DECRYPT_MS'.
    Immediately after launch encryption/decryption, we run isql and ask it to give result of 'SHOW DATABASE' command.
    If this output contains text 'Database [not] encrypted' and *not* contains phrase 'not complete' then we can assume
    that encryption/decryption thread completed. Otherwise we loop until such conditions will raise or timeout expired.

    After this we make TWO attempts to insert duplicates and catch exceptions for each of them and print exception details.
    Expected result: two exception must occur here -- see 'expected_stdout_uniq_violation' variable.

JIRA:        CORE-5673
FBTEST:      bugs.core_5673
NOTES:
    [06.06.2022] pzotov
    Checked on 4.0.1.2692, 3.0.8.33535 - both on Linux and Windows.

    [20.02.2023] Zuev
    Disable the test until RdbCrypt is added.
"""

import time
import datetime as py_dt
from datetime import timedelta

import pytest
from firebird.qa import *
from firebird.driver import DatabaseError
from firebird.driver import TPB, Isolation

MAX_ENCRYPT_DECRYPT_MS = 5000

init_script = """
    recreate table test(db_state varchar(20), x int, constraint test_unq unique(db_state, x));
    commit;
"""

db = db_factory(init = init_script)

act = python_act('db')

custom_tpb = TPB(isolation=Isolation.READ_COMMITTED_RECORD_VERSION, lock_timeout=0)

@pytest.mark.skip("DISABLED: see notes")
@pytest.mark.version('>=3.0.3')
@pytest.mark.encryption
def test_1(act: Action, capsys):
    for m in ('encryption', 'decryption'):

        expected_stdout_show_db = f"""
            Expected: {m} status presents in the 'SHOW DATABASE' output.
        """

        with act.db.connect() as con:

            tx1 = con.transaction_manager(default_tpb=custom_tpb.get_buffer())
            tx1.begin()
            cur1 = tx1.cursor()

            cur1 = con.cursor()
            cur1.execute( f"insert into test(db_state, x) values('{m}', 1)" )

            t1=py_dt.datetime.now()
            d1 = t1-t1
            sttm = 'alter database '  + ('encrypt with "fbSampleDbCrypt" key "Red"' if m == 'encryption' else 'decrypt')
            try:
                con.execute_immediate(sttm)
                con.commit()
            except DatabaseError as e:
                print( e.__str__() )

            act.expected_stdout = ''
            act.stdout = capsys.readouterr().out
            assert act.clean_stdout == act.clean_expected_stdout
            act.reset()

            while True:
                t2=py_dt.datetime.now()
                d1=t2-t1
                if d1.seconds*1000 + d1.microseconds//1000 > MAX_ENCRYPT_DECRYPT_MS:
                    break

                # Possible output:
                #     Database not encrypted
                #     Database encrypted, crypt thread not complete
                act.isql(switches=['-q'], input = 'show database;', combine_output = True)
                if m == 'encryption' and 'Database encrypted' in act.stdout or m == 'decryption' and 'Database not encrypted' in act.stdout:
                    if 'not complete' in act.stdout:
                        pass
                    else:
                        break
                act.reset()

            if d1.seconds*1000 + d1.microseconds//1000 <= MAX_ENCRYPT_DECRYPT_MS:
                print(expected_stdout_show_db)
            else:
                print(f'BREAK ON TIMEOUT EXPIRATION: {m.upper()} took {d1.seconds*1000 + d1.microseconds//1000} ms which exceeds limit = {MAX_ENCRYPT_DECRYPT_MS} ms.')

            act.expected_stdout = expected_stdout_show_db
            act.stdout = capsys.readouterr().out
            assert act.clean_stdout == act.clean_expected_stdout
            act.reset()


            #------------------------------------------------------------------------------------------------------

            expected_stdout_uniq_violation = f"""
                violation of PRIMARY or UNIQUE KEY constraint "TEST_UNQ" on table "TEST"
                -Problematic key value is ("DB_STATE" = '{m}', "X" = 1)
                violation of PRIMARY or UNIQUE KEY constraint "TEST_UNQ" on table "TEST"
                -Problematic key value is ("DB_STATE" = '{m}', "X" = 1)
            """

            tx2 = con.transaction_manager(default_tpb=custom_tpb.get_buffer())
            tx2.begin()
            cur2 = tx2.cursor()

            try:
                cur2.execute( f"insert into test(db_state, x) values( '{m}', 1)" )
            except DatabaseError as e:
                print( e.__str__() )

            try:
                cur2.execute( f"insert into test(db_state, x) values( '{m}', 1)" )
            except DatabaseError as e:
                print( e.__str__() )


            act.expected_stdout = expected_stdout_uniq_violation
            act.stdout = capsys.readouterr().out
            assert act.clean_stdout == act.clean_expected_stdout
            act.reset()
