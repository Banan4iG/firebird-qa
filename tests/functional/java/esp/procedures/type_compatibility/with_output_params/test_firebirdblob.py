#coding:utf-8

"""
ID:          java.esp.procedures.type-compatibility.with-output-params.firebirdblob
TITLE:       External function call with org.firebirdsql.jdbc.FirebirdBlob type of input and output parameters
DESCRIPTION: 
  External function is declared with SQL types compatible with org.firebirdsql.jdbc.FirebirdBlob Java type. Parameter as a constant.
FBTEST:      functional.java.esp.procedures.type_compatibility.with_output_params.firebirdblob
"""

import pytest
from firebird.qa import *

# version: 3.0

init_script_1 = """
 
CREATE PROCEDURE TEST(B BLOB)
returns(o blob)
EXTERNAL NAME 'esp.TestProcedure.blobInOut(org.firebirdsql.jdbc.FirebirdBlob, org.firebirdsql.jdbc.FirebirdBlob[])' 
ENGINE JAVA;
commit;
"""

db_1 = db_factory(init=init_script_1)

test_script_1 = """

select cast(o as varchar(100)) from TEST('test_blob');
"""

act_1 = isql_act('db_1', test_script_1)

expected_stdout_1 = """
CAST
===============================================================================
test_blob
"""

@pytest.mark.java
@pytest.mark.version('>=3.0,<4.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_stdout == act_1.clean_expected_stdout

# version: 4.0

init_script_2 = """

CREATE PROCEDURE TEST(B BLOB)
returns(o blob)
EXTERNAL NAME 'esp.TestProcedure.blobInOut(org.firebirdsql.jdbc.FirebirdBlob, org.firebirdsql.jdbc.FirebirdBlob[])'
ENGINE JAVA;
commit;
"""

db_2 = db_factory(init=init_script_2)

test_script_2 = """

select cast(o as varchar(100)) from TEST('test_blob');
"""

act_2 = isql_act('db_2', test_script_2)

expected_stdout_2 = """
CAST
====================================================================================================
test_blob
"""

@pytest.mark.java
@pytest.mark.version('>=4.0')
def test_2(act_2: Action):
    act_2.expected_stdout = expected_stdout_2
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
