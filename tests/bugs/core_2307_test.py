#coding:utf-8

"""
ID:          issue-2731
ISSUE:       2731
TITLE:       Incomplete API information values
DESCRIPTION:
  Test creates lot of tables with names starting with 'TEST'.
  Then we retrieve from rdb$relations min and max values of this tables ID ('r_min', 'r_max').
  After each table is scanned via execute statement, statistics that we retrieve by call db_into()
  is filled with pair: {relation_id, number_of_seq_reads}.
  We have to ckeck that number of entries in this set with r_min <= relation_id <= rmax NOT LESS than
  number of created tables.
  Also, scan for every table should take at least 1 sequential read - and this is checked too.

  NOTE: we can SKIP checking concrete values of 'number_of_seq_reads', it does not matter in this test!

  Info about 'isc_info_read_seq_count':
  Number of sequential database reads, that is, the number of sequential table scans (row reads)
     Reported per table.
     Calculated since the current database attachment started.

  Confirmed bug on WI-V2.1.2.18118: db_into() received imcompleted data (i.e. not for all tables).
JIRA:        CORE-2307
"""

import pytest
from firebird.qa import *
from firebird.driver import DbInfoCode

db = db_factory()

act = python_act('db')

NUM_OF_TABLES = 1000

sql_ddl = f"""
    set term ^;
    Execute block as
        declare variable i integer = 0;
    begin
      while ( i < {NUM_OF_TABLES} )
      do
        begin
          execute statement 'create table test' || cast(:i as varchar(5)) || ' (c integer)';
          i = i + 1 ;
        end
    end ^
    commit ^

    execute block as
    declare variable i integer = 0;
    begin
      while (i < {NUM_OF_TABLES} )
      do
        begin
          execute statement 'insert into test' || cast(:i as varchar(5)) || ' (c) values (1)';
          i = i + 1 ;
        end
    end
    ^
    set term ;^
    commit;
"""

sql_dml = """
    execute block returns(r_min int, r_max int) as
        declare n varchar(31);
        declare i integer;
    begin
        for
            select min(rdb$relation_id),max(rdb$relation_id)
            from rdb$relations
            where rdb$relation_name starting with upper('test')
            into r_min, r_max
        do
            suspend;

        for
            select rdb$relation_name
            from rdb$relations
            --  4 debug only! >> rows 100
            into :n
        do
            execute statement 'select 1 as k from ' || :n || ' rows 1' into :i;
    end
"""

@pytest.mark.version('>=3')
def test_1(act: Action):
    # prepare DB for testing: create lot of tables:
    act.isql(switches=[], input=sql_ddl)
    with act.db.connect() as con:
        c = con.cursor()
        c.execute(sql_dml)
        r_min = 99999999
        r_max = -9999999
        for r in c:
            r_min = r[0] # minimal ID in rdb$relations for user tables ('TEST1')
            r_max = r[1] # maximal ID in rdb$relations for user tables ('TESTnnnnn')
        #
        info = con.info.get_info(DbInfoCode.READ_SEQ_COUNT)
        cnt = 0
        for k, v in info.items():
            cnt = cnt + 1 if k >= r_min and k <= r_max and v >= 1 else cnt
    assert cnt >= NUM_OF_TABLES
