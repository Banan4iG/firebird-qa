#coding:utf-8

"""
ID:          java.esp.functions.type-compatibility.firebirdblob
TITLE:       External function call with org.firebirdsql.jdbc.FirebirdBlob type of result and input parameter
DESCRIPTION: 
  External function is declared with SQL types compatible with org.firebirdsql.jdbc.FirebirdBlob Java type. Parameter as a constant.
FBTEST:      functional.java.esp.functions.type_compatibility.firebirdblob
"""

import pytest
from firebird.qa import *

init_script = """
create function test(i BLOB) 
returns BLOB
external name 'esp.TestFunction.blobInOut(org.firebirdsql.jdbc.FirebirdBlob)'
engine java;
commit;

"""

db = db_factory(init=init_script)

test_script = """

SELECT cast(TEST('BLOB') as varchar(10)) as "TEST" FROM RDB$DATABASE;
SELECT cast(TEST(null) as varchar(10)) as "TEST" FROM RDB$DATABASE;
"""

act = isql_act('db', test_script)

expected_stdout = """
TEST
==========
BLOB
TEST
==========
<null>
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
