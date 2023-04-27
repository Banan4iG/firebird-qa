#coding:utf-8

"""
ID:          function.create_blr.with_psql_stat
TITLE:       Create function with input parameters
DESCRIPTION:
FBTEST:      functional.function.create_blr_with_psql_stat
"""

import pytest
from firebird.qa import *

init_script = """
    CREATE EXCEPTION test 'test exception';
    CREATE TABLE tb(id INT, text VARCHAR(32));
    commit;
    SET TERM ^;
    CREATE PROCEDURE dummy (id INT) AS
    BEGIN
        id=id;
    END ^

    CREATE PROCEDURE dummy2 (id INT) RETURNS(newID INT) AS
    BEGIN
        newid=id;
    END ^

    CREATE FUNCTION TEST_FUNC
    RETURNS integer
    AS
        DECLARE VARIABLE p1 SMALLINT;
    BEGIN
        p1=1+1;      
        EXECUTE PROCEDURE dummy(:p1);    
        EXECUTE PROCEDURE dummy2(:p1) RETURNING_VALUES :p1;    
        EXIT;
        FOR SELECT id FROM tb INTO :p1 DO p1=p1+2;
        INSERT INTO tb(id) VALUES(:p1);
        UPDATE tb SET text='new text' WHERE id=:p1;
        DELETE FROM tb WHERE text=:p1+1;
        SELECT id FROM tb WHERE text='ggg' INTO :p1;
        IF(p1 IS NOT NULL) THEN p1=NULL;
        IF(p1 IS NULL) THEN p1=2;
        ELSE BEGIN
            p1=2;
        END
        POST_EVENT 'My Event';
        POST_EVENT p1;
        WHILE(p1>30) DO BEGIN
            p1=p1-1;
        END
        BEGIN
            EXCEPTION test;
            WHEN ANY DO p1=45;
        END
        return p1;
    END ^
    SET TERM ;^
    commit;
"""

db = db_factory(init=init_script)

expected_stdout = """
RDB$FUNCTION_NAME: BLR_FUNC
RDB$FUNCTION_SOURCE: None
BLR_FUNC: None
"""

act = python_act('db')

@pytest.mark.version('>=4.0')
def test_1(act: Action, capsys):
    with act.db.connect() as con:
        with con.cursor() as cur:
            cur.execute("SELECT	base64_encode(rdb$function_blr) from rdb$functions where rdb$function_name = 'TEST_FUNC'")
            for row in cur.fetchall():
                cur.execute(f"create function BLR_FUNC RETURNS integer as '{row[0]}'")
                con.commit()
                cur.execute("SELECT	rdb$function_name,rdb$function_source, base64_encode(rdb$function_blr) from rdb$functions where rdb$function_name = 'BLR_FUNC'")
                for range in cur.fetchall():
                    if row[0]==range[2]:
                        print(f"RDB$FUNCTION_NAME: {range[0]}")
                        print(f"RDB$FUNCTION_SOURCE: {range[1]}")

            cur.execute("select BLR_FUNC() from rdb$database;")
            for row in cur.fetchall():
                    print(f"BLR_FUNC: {row[0]}")

    act.expected_stdout = expected_stdout
    act.stdout = capsys.readouterr().out
    assert act.clean_stdout == act.clean_expected_stdout
