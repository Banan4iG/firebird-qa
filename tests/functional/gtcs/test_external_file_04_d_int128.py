#coding:utf-8

"""
ID:          gtcs.external-file-04-C
FBTEST:      functional.gtcs.external_file_04_d_int128
TITLE:       Test for external table with field of INT128 datatype
DESCRIPTION:
  There is no similar test in GTCS, but for INTEGER datatype see:
  https://github.com/FirebirdSQL/fbtcs/blob/master/GTCS/tests/EXT_REL_0_4_D.script
NOTES:
  [31.07.2022] pzotov
  FB config must allow creation of external tables, check parameter 'ExternalFileAccess'.
  Otherwise: SQLSTATE = 28000 / Use of external file at location ... is not allowed ...
  Checked on 4.0.1.2692, 5.0.0.591
"""

from pathlib import Path
import pytest
from firebird.qa import *

db = db_factory()

act = python_act('db', substitutions=[('[ \t]+', ' '), ('(INPUT|OUTPUT)\\s+message .*', ''), (':\\s+(name:|table:)\\s+.*', '') ])

tmp_ext_file = temp_file('tmp_gtcs_external_file_04_int128.dat')

expected_stderr = """
"""

expected_stdout = """
    01: sqltype: 32752 INT128 Nullable scale: 0 subtype: 0 len: 16
    F01 -170141183460469231731687303715884105728
    F01 -1
    F01 0
    F01 1
    F01 170141183460469231731687303715884105727
    Records affected: 5
"""

@pytest.mark.version('>=4.0')
def test_1(act: Action, tmp_ext_file: Path):
    
    sql_cmd = f'''
        create table ext_table external file '{str(tmp_ext_file)}' (f01 int128);
        commit;
        insert into ext_table (f01) values ( 170141183460469231731687303715884105727);
        insert into ext_table (f01) values (-170141183460469231731687303715884105728);
        insert into ext_table (f01) values (1);
        insert into ext_table (f01) values (-1);
        insert into ext_table (f01) values (0);
        commit;
        set list on;
        set count on;
        set sqlda_display on;
        select * from ext_table order by f01;
        commit;
        drop table ext_table;
        exit;
    '''

    act.expected_stdout = expected_stdout
    act.expected_stderr = expected_stderr

    act.isql(switches=['-q'], input = sql_cmd )

    assert (act.clean_stderr == act.clean_expected_stderr and
            act.clean_stdout == act.clean_expected_stdout)
