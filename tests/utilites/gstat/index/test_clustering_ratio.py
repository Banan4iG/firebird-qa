#coding:utf-8
"""
ID:          utilites.gstat.index.clustering_ratio
TITLE:       Check the index clustering factor and its ratio to the number of nodes
DESCRIPTION: 
NOTES: Add enough records in test tables so that gstat can use several threads.
"""

import pytest
from firebird.qa import *
from math import floor
import random

PAGE_SIZE = 4096
FIELD_WIDTH = 1500
DP_QNT = 8001
RECS_PER_DP = floor(PAGE_SIZE/FIELD_WIDTH)
REC_QNT = RECS_PER_DP*DP_QNT

substring='0123456789'
length = len(substring)
test_string=substring*(FIELD_WIDTH//length)+substring[:FIELD_WIDTH%length]

create_table = f"""
    create table TEST(id int, str varchar({FIELD_WIDTH}));
    commit;
"""

db = db_factory(page_size=PAGE_SIZE, init=create_table)
act = python_act('db')

create_index = "create INDEX IDX_TEST on TEST(ID); commit;"

@pytest.mark.version('>=3.0')
def test_sorted_data(act: Action, gstat_helpers):
    insert_data = f"""
        -- Insert records
        set term ^;
        
        execute block as
            declare variable i integer;
        begin
            i = 0;
            while (i < {REC_QNT}) do
            begin
                insert into TEST values (:i, '{test_string}');
                i = i + 1;
            end
        end^

        set term ;^
        commit;
    """
    act.isql(switches=[], input=(insert_data + create_index))
    act.reset()

    act.gstat(switches=['-i'])
    factor = gstat_helpers.get_metric(act.stdout, 'TEST', 'Clustering factor')
    assert factor == DP_QNT
    ratio = gstat_helpers.get_metric(act.stdout, 'TEST', 'ratio')
    assert ratio == (1/RECS_PER_DP)

@pytest.mark.version('>=3.0')
def test_unsorted_data(act: Action, gstat_helpers):
    insert_data = f"""
        -- Insert records
        set term ^;
        
        execute block as
            declare variable i integer;
            declare variable asc integer;
            declare variable desc integer;
        begin
            i = {REC_QNT//2};
            asc = 0;
            desc = {REC_QNT};
            while (i > 0 ) do
            begin
                insert into TEST values (:asc, '{test_string}');
                insert into TEST values (:desc, '{test_string}');
                i = i - 1;
            end
        end^

        set term ;^
        commit;
    """
    act.isql(switches=[], input=(insert_data + create_index))
    act.reset()

    act.gstat(switches=['-i'])
    factor = gstat_helpers.get_metric(act.stdout, 'TEST', 'Clustering factor')
    assert factor == REC_QNT
    ratio = gstat_helpers.get_metric(act.stdout, 'TEST', 'ratio')
    assert ratio == 1
