#coding:utf-8

"""
ID:          java.esp.functions.without-parameters.firebirdblob-result
TITLE:       External function call with org.firebirdsql.jdbc.FirebirdBlob type of result and without input parameter
DESCRIPTION: 
  External function is declared with SQL types compatible with org.firebirdsql.jdbc.FirebirdBlob Java type.
FBTEST:      functional.java.esp.functions.without_parameters.firebirdblob_result
"""

import pytest
from firebird.qa import *

init_script = """
create function test() 
returns blob
external name 'esp.TestFunction.firebirdblobOut()' 
engine java;
commit;
"""

db = db_factory(init=init_script)

test_script = """
SELECT cast(TEST() as varchar(20)) "TEST"  FROM RDB$DATABASE;
"""

act = isql_act('db', test_script)

expected_stdout = """
	
TEST
====================
FirebirdBlob
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
