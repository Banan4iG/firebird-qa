#coding:utf-8

"""
ID:          java.esp.procedures.type-compatibility.sql-blob
TITLE:       External function call with java.sql.Blob type of input parameter
DESCRIPTION: 
  External function is declared with SQL types compatible with java.sql.Blob Java type. Parameter as a constant.
FBTEST:      functional.java.esp.procedures.type_compatibility.sql_blob
"""

import pytest
from firebird.qa import *

init_script = """
 
CREATE TABLE TEST_TABLE(F_BLOB BLOB);
commit;

CREATE PROCEDURE TEST(B BLOB)
EXTERNAL NAME 'esp.TestProcedure.sqlblobIn(java.sql.Blob)' 
ENGINE JAVA;
commit;
"""

db = db_factory(init=init_script)

test_script = """
EXECUTE PROCEDURE TEST('test_blob');
commit;

SELECT cast(F_BLOB as varchar(10)) FROM TEST_TABLE;
"""

act = isql_act('db', test_script)

expected_stdout = """
CAST
==========
test_blob
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
