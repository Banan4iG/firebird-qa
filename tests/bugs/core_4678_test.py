#coding:utf-8

"""
ID:          issue-4987
ISSUE:       4987
TITLE:       BLOB not found in SuperClassic and Classic on Uncommitted Transactions
DESCRIPTION:
JIRA:        CORE-4678
FBTEST:      bugs.core_4678
"""

import pytest
from firebird.qa import *

init_script = """
    recreate table test(id int);
    commit;

    set term ^;
    execute block as
    begin
        execute statement 'drop sequence gen_memo_id';
        when any do begin end
    end ^
    set term ;^
    commit;

    create generator gen_memo_id;

    recreate table test (
        id int not null,
        memo blob sub_type 1 segment size 100 character set ascii
    );
    create index memo_idx1 on test computed by (upper(trim(cast(substring(memo from 1 for 128) as varchar(128)))));

    set term ^ ;
    create or alter trigger test_bi for test
    active before insert position 0
    as
    begin
      if (new.id is null) then
        new.id = gen_id(gen_memo_id,1);
    end
    ^
    set term ; ^
    commit;
"""

db = db_factory(init=init_script)

test_script = """
    insert into test(memo) values( 'foo-rio-bar' );
    rollback;
    -- Confirmed on WI-V2.5.2.26540 (official release):
    -- exception on ROLLBACK raises with text:
    -- ===
    -- Statement failed, SQLSTATE = HY000
    -- BLOB not found
    -- ===
    -- No reconnect is required, all can be done in one ISQL attachment.
"""

act = isql_act('db', test_script)

@pytest.mark.version('>=3')
def test_1(act: Action):
    act.execute()
