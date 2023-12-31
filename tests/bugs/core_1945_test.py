#coding:utf-8

"""
ID:          issue-2384
ISSUE:       2384
TITLE:       Custom attribute for collation to sort numbers in numeric order
DESCRIPTION:
JIRA:        CORE-1945
FBTEST:      bugs.core_1945
"""

import pytest
from firebird.qa import *

db_1 = db_factory(charset='UTF8')

test_script = """
	-- Result were checked on LI-T3.0.0.31827 (64x) and WI-T3.0.0.31836 (32x).
	-- ::: NOTE ::: FB 2.5 (at least build 2.5.5.26870 what has been checked)
	-- produces WRONG output for such rows when using collation CI_AI:
	-- d111
	-- ð1
	-- Ð11
	-- Ð1111
	-- o7
	-- Õ7777
	-- Ø77
	-- ø777
	-- (it seems that trouble somehow related to letters with diagonal strokes as diacritical addition: Ð and Ø)

	-- Proper order:
	-- ð1
	-- Ð11
	-- d111
	-- Ð1111
	-- o7
	-- Ø77
	-- ø777
	-- Õ7777

	recreate table test(s varchar(50));
	commit;
	set term ^;
	execute block as
	begin
	  begin execute statement 'drop collation ns_coll'; when any do begin end end
	  begin execute statement 'drop collation ns_coll_ci'; when any do begin end end
	  begin execute statement 'drop collation ns_coll_ci_ai'; when any do begin end end
	end
	^
	set term ;^
	commit;

	create collation ns_coll for utf8 from unicode 'NUMERIC-SORT=1';
	create collation ns_coll_ci for utf8 from unicode case insensitive 'NUMERIC-SORT=1';
	create collation ns_coll_ci_ai for utf8 from unicode case insensitive accent insensitive 'NUMERIC-SORT=1';
	commit;

	recreate table test(
		s_norm varchar(50) character set utf8 collate ns_coll
		,s_ci varchar(50) character set utf8 collate ns_coll_ci
		,s_ciai varchar(50) character set utf8 collate ns_coll_ci_ai
	);
	commit;

	insert into test(s_norm, s_ci, s_ciai) values('n8888',  'ñ8888', 'Ñ8888');
	insert into test(s_norm, s_ci, s_ciai) values('n8',  'ñ8', 'ñ8');
	insert into test(s_norm, s_ci, s_ciai) values('N88',  'Ñ88', 'Ň88');

	insert into test(s_norm, s_ci, s_ciai) values( 'O77', 'õ77', 'Ø77');
	insert into test(s_norm, s_ci, s_ciai) values( 'o7777', 'Õ7777', 'Õ7777');
	insert into test(s_norm, s_ci, s_ciai) values( 'O7',  'Õ7',  'o7');
	insert into test(s_norm, s_ci, s_ciai) values( 'o777', 'õ777', 'ø777');

	insert into test(s_norm, s_ci, s_ciai) values('d1',  'd1',  'ð1');
	insert into test(s_norm, s_ci, s_ciai) values('D11',  'd11',  'Ð11');
	insert into test(s_norm, s_ci, s_ciai) values('D1111',  'D1111',  'Ð1111');
	insert into test(s_norm, s_ci, s_ciai) values('d111',  'd111',  'd111');

	insert into test(s_norm, s_ci, s_ciai ) values('a9999', 'ä9999', 'Ą9999'  );
	insert into test(s_norm, s_ci, s_ciai ) values('a9',    'Ä9',   'Á9'    );
	insert into test(s_norm, s_ci, s_ciai ) values('A99',   'ä99',   'à99'    );
	insert into test(s_norm, s_ci, s_ciai ) values('a999',  'ä999',  'â999'   );

	insert into test(s_norm, s_ci, s_ciai ) values('L444',  'Ł444',  'L444');
	insert into test(s_norm, s_ci, s_ciai ) values('l44444',  'ł44444',  'ł44444');

	insert into test(s_norm, s_ci, s_ciai ) values('c2',  'Ç2', 'ç2');
	insert into test(s_norm, s_ci, s_ciai ) values('C222',  'ç222', 'Ç222');
	insert into test(s_norm, s_ci, s_ciai ) values('c22',  'Ç22', 'C22');

	insert into test(s_norm, s_ci, s_ciai ) values('S55',   'Š55',  'Š55'  );
	insert into test(s_norm, s_ci, s_ciai ) values('s555',  'š555', 'ş555');
	insert into test(s_norm, s_ci, s_ciai ) values('s5',    'Š5',   'š5');

	set list on;
	select s_norm from test order by s_norm;
	select s_ci from test order by s_ci;
	select s_ciai from test order by s_ciai;
"""

act = isql_act('db_1', test_script)

expected_stdout = """
	S_NORM                          a9
	S_NORM                          A99
	S_NORM                          a999
	S_NORM                          a9999
	S_NORM                          c2
	S_NORM                          c22
	S_NORM                          C222
	S_NORM                          d1
	S_NORM                          D11
	S_NORM                          d111
	S_NORM                          D1111
	S_NORM                          L444
	S_NORM                          l44444
	S_NORM                          n8
	S_NORM                          N88
	S_NORM                          n8888
	S_NORM                          O7
	S_NORM                          O77
	S_NORM                          o777
	S_NORM                          o7777
	S_NORM                          s5
	S_NORM                          S55
	S_NORM                          s555

	S_CI                            Ä9
	S_CI                            ä99
	S_CI                            ä999
	S_CI                            ä9999
	S_CI                            Ç2
	S_CI                            Ç22
	S_CI                            ç222
	S_CI                            d1
	S_CI                            d11
	S_CI                            d111
	S_CI                            D1111
	S_CI                            Ł444
	S_CI                            ł44444
	S_CI                            ñ8
	S_CI                            Ñ88
	S_CI                            ñ8888
	S_CI                            Õ7
	S_CI                            õ77
	S_CI                            õ777
	S_CI                            Õ7777
	S_CI                            Š5
	S_CI                            Š55
	S_CI                            š555

	S_CIAI                          Á9
	S_CIAI                          à99
	S_CIAI                          â999
	S_CIAI                          Ą9999
	S_CIAI                          ç2
	S_CIAI                          C22
	S_CIAI                          Ç222
	S_CIAI                          ð1
	S_CIAI                          Ð11
	S_CIAI                          d111
	S_CIAI                          Ð1111
	S_CIAI                          L444
	S_CIAI                          ł44444
	S_CIAI                          ñ8
	S_CIAI                          Ň88
	S_CIAI                          Ñ8888
	S_CIAI                          o7
	S_CIAI                          Ø77
	S_CIAI                          ø777
	S_CIAI                          Õ7777
	S_CIAI                          š5
	S_CIAI                          Š55
	S_CIAI                          ş555
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

