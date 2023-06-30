#coding:utf-8

"""
ID:          java.esp.procedures.type-compatibility.externalresultset
TITLE:       Call of external procedure which returns org.firebirdsql.fbjava.ExternalResultSet
DESCRIPTION: 
FBTEST:      functional.java.esp.procedures.type_compatibility.externalresultset
"""

import pytest
from firebird.qa import *

init_script = """
 
CREATE PROCEDURE TEST
RETURNS(s smallint, i integer, bi bigint, f float, d double precision, n numeric(10,2), de decimal(10,2), c char(100), v varchar(100), b blob, da date, t time, ts timestamp, bool boolean)
EXTERNAL NAME 'esp.TestProcedure.externalResultSetOut(Short[], int[], Long[], float[], Double[], java.math.BigDecimal[], java.math.BigDecimal[],  String[], String[], java.sql.Blob[], java.sql.Date[],java.sql.Time[], java.sql.Timestamp[], boolean[])' 
ENGINE JAVA;
commit;
 
"""

db = db_factory(init=init_script)

test_script = """

set list on;
select * from TEST;
commit;

"""

act = isql_act('db', test_script)

expected_stdout = """         
S                               1
I                               1
BI                              1
F                               1
D                               1.000000000000000
N                               1.00
DE                              1.00
C                               char_1
V                               varchar_1
B                               0:1
BLOB display set to subtype 1. This BLOB: subtype = 0
DA                              2008-04-09
T                               11:34:45.0000
TS                              2008-04-09 11:34:45.0000
BOOL                            <true>
S                               2
I                               2
BI                              2
F                               2
D                               2.000000000000000
N                               2.00
DE                              2.00
C                               char_2
V                               varchar_2
B                               0:2
BLOB display set to subtype 1. This BLOB: subtype = 0
DA                              2008-04-09
T                               11:34:45.0000
TS                              2008-04-09 11:34:45.0000
BOOL                            <true>
S                               3
I                               3
BI                              3
F                               3
D                               3.000000000000000
N                               3.00
DE                              3.00
C                               char_3
V                               varchar_3
B                               0:3
BLOB display set to subtype 1. This BLOB: subtype = 0
DA                              2008-04-09
T                               11:34:45.0000
TS                              2008-04-09 11:34:45.0000
BOOL                            <true>
S                               4
I                               4
BI                              4
F                               4
D                               4.000000000000000
N                               4.00
DE                              4.00
C                               char_4
V                               varchar_4
B                               0:4
BLOB display set to subtype 1. This BLOB: subtype = 0
DA                              2008-04-09
T                               11:34:45.0000
TS                              2008-04-09 11:34:45.0000
BOOL                            <true>
S                               5
I                               5
BI                              5
F                               5
D                               5.000000000000000
N                               5.00
DE                              5.00
C                               char_5
V                               varchar_5
B                               0:5
BLOB display set to subtype 1. This BLOB: subtype = 0
DA                              2008-04-09
T                               11:34:45.0000
TS                              2008-04-09 11:34:45.0000
BOOL                            <true>
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
