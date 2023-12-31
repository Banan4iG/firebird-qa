#coding:utf-8

"""
ID:          tabloid.eqc-200762
TITLE:       Check results of CONTAINING when search pattern can span on one or several blob segments
DESCRIPTION: 
FBTEST:      functional.tabloid.eqc_200762
"""

import pytest
from firebird.qa import *

db = db_factory(page_size=8192)

test_script = """
    set list on;
    set term ^;
    execute block as
    begin
        execute statement 'drop sequence g'; when any do begin end
    end
    ^
    set term ;^
    commit;
    
    create sequence g;
    
    recreate table test (
        id int primary key,
        pattern varchar(32765),
        memotext blob sub_type 1 segment size 1024 character set none
    );
    
    set term ^;
    execute block returns(id int, ptrn_len int, blob_len int, ptrn_pos int) as
        declare v_pattern varchar(32765);
        declare v_db_page smallint;
        declare v_id int;
    begin
        
        select mon$page_size from mon$database into v_db_page;
    
        delete from test;
    
        v_pattern = 'qwertyuioplkjhgfdsa1234567890zxcvbnm';
    
        -- short pattern (len < 50 bytes), start on 1st segment and spans to 2nd:
        insert into test(id, pattern, memotext) 
        values( gen_id(g,1), :v_pattern, rpad( '', 1000, uuid_to_char(gen_uuid()) ) || :v_pattern );
    
        -- middle length pattern (len > 1024 and <= db_page_size)
    
        insert into test(id, pattern) 
        values(gen_id(g,1), rpad( '', 2.0/3 * :v_db_page, uuid_to_char(gen_uuid()) ) )
        returning id, pattern into v_id, v_pattern;
        update test set memotext = rpad( '', 1001, uuid_to_char(gen_uuid()) ) || :v_pattern
        where id = :v_id;
    
        insert into test(id, pattern) values(gen_id(g,1), rpad( '', 3.0/4 * :v_db_page, uuid_to_char(gen_uuid()) ) )
        returning id, pattern into v_id, v_pattern;
        update test set memotext = rpad( '', 1002, uuid_to_char(gen_uuid()) ) || :v_pattern
        where id = :v_id;
    
        insert into test(id, pattern) values(gen_id(g,1), rpad( '', :v_db_page, uuid_to_char(gen_uuid()) ) )
        returning id, pattern into v_id, v_pattern;
        update test set memotext = rpad( '', 1003, uuid_to_char(gen_uuid()) ) || :v_pattern
        where id = :v_id;
    
        -- large length pattern ( > db_page_size):
    
        insert into test(id, pattern) values(gen_id(g,1), rpad( '', 5.0/4 * :v_db_page, uuid_to_char(gen_uuid()) ) )
        returning id, pattern into v_id, v_pattern;
        update test set memotext = rpad( '', 1004, uuid_to_char(gen_uuid()) ) || :v_pattern
        where id = :v_id;
    
        insert into test(id, pattern) values(gen_id(g,1), rpad( '', 4.0/3 * :v_db_page, uuid_to_char(gen_uuid()) ) )
        returning id, pattern into v_id, v_pattern;
        update test set memotext = rpad( '', 1005, uuid_to_char(gen_uuid()) ) || :v_pattern
        where id = :v_id;
    
        insert into test(id, pattern) values(gen_id(g,1), rpad( '', 31724, uuid_to_char(gen_uuid()) ) )
        returning id, pattern into v_id, v_pattern;
        update test set memotext = rpad( '', 1006, uuid_to_char(gen_uuid()) ) || :v_pattern
        where id = :v_id;
    
        for
            select id, char_length(pattern), char_length(memotext), position(pattern in memotext)
            from test
            where memotext containing pattern
            order by id
            into id, ptrn_len, blob_len, ptrn_pos
        do 
            suspend;
    end
    ^
    set term ;^
    commit;
"""

act = isql_act('db', test_script)

expected_stdout = """
    ID                              1
    PTRN_LEN                        36
    BLOB_LEN                        1036
    PTRN_POS                        1001
    
    ID                              2
    PTRN_LEN                        4915
    BLOB_LEN                        5916
    PTRN_POS                        1002
    
    ID                              3
    PTRN_LEN                        5734
    BLOB_LEN                        6736
    PTRN_POS                        1003
    
    ID                              4
    PTRN_LEN                        8192
    BLOB_LEN                        9195
    PTRN_POS                        1004
    
    ID                              5
    PTRN_LEN                        9830
    BLOB_LEN                        10834
    PTRN_POS                        1005
    
    ID                              6
    PTRN_LEN                        10650
    BLOB_LEN                        11655
    PTRN_POS                        1006
    
    ID                              7
    PTRN_LEN                        31724
    BLOB_LEN                        32730
    PTRN_POS                        1007
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
