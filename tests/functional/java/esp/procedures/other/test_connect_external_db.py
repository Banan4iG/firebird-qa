#coding:utf-8

"""
ID:          java.esp.procedures.other.connect-external-db
TITLE:       Working with the other database
DESCRIPTION: 
FBTEST:      functional.java.esp.procedures.other.connect_external_db
"""

import pytest
from firebird.qa import *

init_script = """
    CREATE TABLE TEST_TABLE(f varchar(100));
    commit;

    CREATE PROCEDURE TEST(s varchar(100))
    EXTERNAL NAME 'esp.TestProcedure.interConnect(String)' 
    ENGINE JAVA;
    commit;
"""

db = db_factory(init=init_script)
act = python_act('db')

db_2= db_factory(filename='db2.fdb')

expected_stdout = """
F
===============================================================================
anna
michael
olga
alex
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action, db_2: Database):
    script="""
        create table test_table(name varchar(100));
        insert into test_table values('anna');
        insert into test_table values('michael');
        insert into test_table values('olga');
        insert into test_table values('alex');
    """
    act.isql(switches=[db_2.dsn,'-q'], input=script, connect_db=False)

    script=f"""	
        execute procedure test('{db_2.db_path}');
        commit;
        select * from test_table;	
    """
    act.reset()
    act.expected_stdout = expected_stdout
    act.isql(switches=['-q'], input=script)
    assert act.clean_expected_stdout == act.clean_expected_stdout
