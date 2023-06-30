#coding:utf-8

"""
ID:          java.esp.functions.type-compatibility.sql-blob
TITLE:       External function call with java.sql.Blob type of result and input parameter
DESCRIPTION: 
  External function is declared with SQL types compatible with java.sql.Blob Java type. Parameter as a constant.
FBTEST:      functional.java.esp.functions.type_compatibility.sql_blob
"""

import pytest
from firebird.qa import *

init_script = """
create function test(b blob) 
returns blob
external name 'esp.TestFunction.blobInOut2(java.sql.Blob)' 
engine java;
commit;
"""

db = db_factory(init=init_script)

test_script = """
SELECT cast(TEST(cast('BLOB' as blob)) as varchar(10)) as "TEST"  FROM RDB$DATABASE;
"""

act = isql_act('db', test_script)

expected_stdout = """
TEST
==========
BLOB
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
