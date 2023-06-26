#coding:utf-8

"""
ID:          intfunc.math.greatest
TITLE:       Test the GREATEST function
DESCRIPTION: GREATEST returns the maximum value of a list of values.
"""

import pytest
from firebird.qa import *

init_script = """
recreate table TEST    (    ID INT, PRICE DECIMAL(10, 2),   CASHBACK DECIMAL(10, 2),     PRIORITY INT    );
--------------------------------------------------------------------------------------------------
insert into TEST values(    1545,   null,                   -3688.43,                    -664            );
insert into TEST values(    1360,   2310.21,                null,                        -515            );
insert into TEST values(    833,    248.12,                 -6069.49,                    null            );
insert into TEST values(    989,    -7747.90,               -9779.67,                    573             );
insert into TEST values(    1670,   7005.38,                5125.77,                     497             );
insert into TEST values(    945,    2040.07,                6240.22,                     -285            );
insert into TEST values(    766,    9028.09,                -251.14,                     1832            );
commit;
"""

db = db_factory(init=init_script)

test_script = """
-- Explicit data values ------------------------------------------------
-- Positive and negative (check GREATEST header)
select greatest(10.7, 54.2, -87, 0) from rdb$database;
-- Only negative 
select greatest(-54.2, -10.7, -87) as TEST2 from rdb$database;
-- Negative and zero
select greatest(-54.2, -10.7, 0, -87) as TEST3 from rdb$database;
-- Null value
select greatest(-54.2, NULL, 0, 87) as TEST4 from rdb$database;
-- String values
select greatest('String', 'String5test','String5') as TEST5 from rdb$database;
-- Boolean values
select greatest(TRUE, FALSE, FALSE) as TEST6 from rdb$database;
-- Numeric vs numeric as string
select greatest(10.7, '54.2', -87, '0') as TEST7 from rdb$database;
-- Numeric vs text
select greatest(10.7, 'text', -87, 'other text') as TEST8 from rdb$database;
-- String vs boolean
select greatest('TEXT', TRUE) as TEST9 from rdb$database;
    
-- Data values from a table ---------------------------------------------
select greatest(ID, PRICE, CASHBACK, PRIORITY) as TEST10 from TEST;
-- Inside aggregate function --
select max(greatest(ID, PRICE, CASHBACK, PRIORITY)) as TEST11 from TEST;
-- Arithmetic operations --
select greatest(ID*10, PRICE+1000, CASHBACK/2, PRIORITY-10) as TEST12 from TEST;
-- Math function (ABS) --
select greatest(ID, PRICE, ABS(CASHBACK), ABS(PRIORITY)) as TEST13 from TEST;
-- Compare with constant
select greatest(6000, ID, PRICE, CASHBACK, PRIORITY) as TEST14 from TEST;
"""

act = python_act('db', substitutions=[('===*','='*10)])

expected_stdout = """
             GREATEST
=====================
                 54.2

                TEST2
=====================
                -10.7

                TEST3
=====================
                  0.0

                TEST4
=====================
               <null>

TEST5
===========
String5test

  TEST6
=======
<true>

TEST7
=====================
54.2

TEST8
=====================
Statement failed, SQLSTATE = 22018
conversion error from string "text"

TEST9
============
Statement failed, SQLSTATE = 22018
conversion error from string "TEXT"

        TEST10
==============
        <null>
        <null>
        <null>
        989.00
       7005.38
       6240.22
       9028.09

        TEST11
==============
       9028.09

                 TEST12 
======================= 
                 <null> 
                 <null> 
                 <null> 
                9890.00 
               16700.00 
                9450.00 
               10028.09

        TEST13 
============== 
        <null> 
        <null> 
        <null> 
       9779.67 
       7005.38 
       6240.22 
       9028.09

        TEST14 
============== 
        <null> 
        <null> 
        <null> 
       6000.00 
       7005.38
       6240.22
       9028.09
"""

@pytest.mark.version('>=5.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.isql(switches=['-q'], input=test_script, combine_output=True)
    assert act.clean_stdout == act.clean_expected_stdout
