#coding:utf-8
#
# id:           bugs.core_1384
# title:        LIKE doesn't work correctly with collations using SPECIALS-FIRST=1
# decription:
#                   02-mar-2021. Re-implemented in ordeer to have ability to run this test on Linux.
#                   We run 'init_script' using charset = utf8 but then run separate ISQL-process
#                   with request to establish connection using charset = ISO8859_1.
#
#                   *** NOTE ***
#                   Script that must be executed by ISQL does NOT contain any non-ascii characters.
#                   Query with diacritical symbols was moved into view V_TEST which is created in init_script
#                   using charset ***UTF-8*** (otherwise is seems to be unable to run this test on Linux).
#
#                   Checked on:
#                   * Windows: 4.0.0.2377, 3.0.8.33420, 2.5.9.27152
#                   * Linux:   4.0.0.2377, 3.0.8.33415
#
# tracker_id:   CORE-1384
# min_versions: ['2.1.7']
# versions:     2.1.7
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 2.1.7
# resources: None

substitutions_1 = []

init_script_1 = """
	create collation coll_es for iso8859_1 from external ('ES_ES_CI_AI') 'SPECIALS-FIRST=1';
	create collation coll_fr for iso8859_1 from external ('FR_FR') CASE INSENSITIVE accent insensitive 'SPECIALS-FIRST=1';
	commit;

	create or alter view v_test as
	select
	   iif( _iso8859_1 'Ja ' collate coll_es like _iso8859_1 '% a%' collate coll_es, 1, 0) result_for_es_ci_ai
	   ,iif( _iso8859_1 'ka ' collate coll_fr like _iso8859_1 '% a%' collate coll_fr, 1, 0) result_for_fr_ci_ai
	from rdb$database
	UNION ALL -- added comparison to pattern with diactiric mark:
	select
	   iif( _iso8859_1 'Jà ' collate coll_es like _iso8859_1 '% à %' collate coll_es, 1, 0) result_for_es_ci_ai
	   ,iif( _iso8859_1 'kà ' collate coll_fr like _iso8859_1 '% à %' collate coll_fr, 1, 0) result_for_fr_ci_ai
	from rdb$database
	;
"""

db_1 = db_factory(charset='UTF8', sql_dialect=3, init=init_script_1)

# test_script_1
#---
#
#  sql_cmd='''
#      set names ISO8859_1;
#      connect '%(dsn)s' user '%(user_name)s' password '%(user_password)s';
#      set list on;
#      show collation;
#      select * from v_test;
#  ''' % dict(globals(), **locals())
#
#  runProgram( 'isql', [ '-q' ], sql_cmd)
#
#
#---

test_script_1 = """
set list on;
show collation;
select * from v_test;
"""

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
	COLL_ES, CHARACTER SET ISO8859_1, FROM EXTERNAL ('ES_ES_CI_AI'), 'SPECIALS-FIRST=1'
	COLL_FR, CHARACTER SET ISO8859_1, FROM EXTERNAL ('FR_FR'), CASE INSENSITIVE, ACCENT INSENSITIVE, 'SPECIALS-FIRST=1'
	RESULT_FOR_ES_CI_AI             0
	RESULT_FOR_FR_CI_AI             0
	RESULT_FOR_ES_CI_AI             0
	RESULT_FOR_FR_CI_AI             0
"""

@pytest.mark.version('>=2.1.7')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute(charset='ISO8859_1')
    assert act_1.clean_stdout == act_1.clean_expected_stdout


