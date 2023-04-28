#coding:utf-8

"""
ID:          procedure.alter_blr.with_psql_stat
TITLE:       Alter procedure with psql stat
DESCRIPTION:
FBTEST:      functional.procedure.alter_blr_with_psql_stat
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

    CREATE PROCEDURE TEST_PROC
    AS
        DECLARE VARIABLE p1 SMALLINT;
    BEGIN
        p1=1+1;      
        begin
            EXCEPTION test;   
        end
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
    END ^
    
    CREATE PROCEDURE BLR_PROC 
    AS
        declare variable a integer;
    BEGIN
        a = 10;
    END ^
    SET TERM ;^
    commit;
"""

db = db_factory(init=init_script)

expected_stdout = """
RDB$PROCEDURE_NAME: BLR_PROC
RDB$PROCEDURE_SOURCE: None

Error: exception 1
-TEST
-test exception
-At procedure 'BLR_PROC'
"""

act = python_act('db')

@pytest.mark.version('>=4.0')
def test_1(act: Action, capsys):
    with act.db.connect() as con:
        with con.cursor() as cur:
            try:
                cur.execute("SELECT base64_encode(rdb$procedure_blr) from rdb$procedures where rdb$procedure_name = 'TEST_PROC'")
                for row in cur.fetchall():
                    cur.execute(f"alter procedure BLR_PROC as '{row[0]}'")
                    con.commit()
                    cur.execute("SELECT rdb$procedure_name,rdb$procedure_source, base64_encode(rdb$procedure_blr) from rdb$procedures where rdb$procedure_name = 'BLR_PROC'")
                    for range in cur.fetchall():
                        if row[0]==range[2]:
                            print(f"RDB$PROCEDURE_NAME: {range[0]}")
                            print(f"RDB$PROCEDURE_SOURCE: {range[1]}")
                cur.execute("execute procedure BLR_PROC;")
                for row in cur.fetchall():
                    print(f"BLR_PROC: {row[0]}")
            except Exception as e:
                print("Error:", e)

    act.expected_stdout = expected_stdout
    act.stdout = capsys.readouterr().out
    assert act.clean_stdout == act.clean_expected_stdout
