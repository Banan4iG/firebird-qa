#coding:utf-8

"""
ID:          RS-92275
ISSUE:       https://http://tracker.red-soft.biz/issues/92275
TITLE:       Uncommitted records may become visible after the database sweep
DESCRIPTION:
    Create a table with field size exceeding db page size.
    Insert one record in the table. Record data must be poorly compressible so that the record is divided into two or more pages.
    Use repeated substring '0123456789'. This way we guarantee that adjacent characters will not be repeated.
    Commit a transaction and close connection.
    Run sweep by gfix.
    Insert several uncompressible records into test table.
    Rollback a transaction and close connection.
    Run sweep by gfix again.
    Select count of records in the test table and see that there are more that one record.
NOTES:
    FB/RDB5+ requires only 1 uncommited record but we insert several ones to unify tests.
"""

import pytest
from firebird.qa import *
import time
import shutil

# Width of a string field in a test table.
FIELD_WIDTH = 17000
# Quantity of records in a test table
REC_QNT = 30

db = db_factory(page_size=16384)

act = python_act('db')

@pytest.mark.version('>=3.0')
def test_1(act: Action):
    substring='0123456789'
    length = len(substring)
    test_string=substring*(FIELD_WIDTH//length)+substring[:FIELD_WIDTH%length]

    create_script = f"""
        create table t1_big (id integer, str1 varchar({FIELD_WIDTH}));
        commit;
    """

    act.isql(switches=['-q'], input=create_script)

    commited_transaction = f"""
        insert into t1_big values(0, '{test_string}');
        commit;
        select * from rdb$database;
        commit;
    """

    act.isql(switches=['-q'], input=commited_transaction)

    act.gfix(switches=['-sweep', act.db.dsn])

    uncommited_transaction = f"""
        commit;
        set transaction no auto undo;
        set term ^;
        execute block
        as
        declare variable I integer;
        begin
            i = {REC_QNT};
        while (i > 0) do
        begin
            insert into t1_big values (1, '{test_string}');
            i = i - 1;
        end
        end^
        set term ;^
        rollback;
    """

    act.isql(switches=['-q'], input=uncommited_transaction)

    act.gfix(switches=['-sweep', act.db.dsn])

    with act.db.connect() as con3:
        with con3.cursor() as cur3:
            cur3.execute("select * from t1_big")
            cur3.execute("select count(*) from t1_big")
            result = cur3.fetchone()[0]

    assert result == 1