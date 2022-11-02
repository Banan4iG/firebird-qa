#coding:utf-8

"""
ID:          issue-5985
ISSUE:       5985
TITLE:       FB >= 3 crashes when restoring backup made by FB 2.5
DESCRIPTION:
  This test also present in GTCS list, see it here:
    https://github.com/FirebirdSQL/fbtcs/blob/master/GTCS/tests/SV_HIDDEN_VAR_2_5.script
JIRA:        CORE-5719
FBTEST:      bugs.core_5719
"""

import pytest
import zipfile
from difflib import unified_diff
from pathlib import Path
from firebird.qa import *
from firebird.driver import SrvRestoreFlag
import re

db = db_factory()

act = python_act('db')

fbk_file = temp_file('core5719-ods-11_2.fbk')
fdb_file = temp_file('check_restored_5719.fdb')

@pytest.mark.version('>=3.0')
def test_1(act: Action, fbk_file: Path, fdb_file: Path):
    zipped_fbk_file = zipfile.Path(act.files_dir / 'core_5719-ods-11_2.zip',
                                   at='core5719-ods-11_2.fbk')
    fbk_file.write_bytes(zipped_fbk_file.read_bytes())
    log_before = act.get_firebird_log()
    #
    with act.connect_server() as srv:
        srv.database.restore(backup=fbk_file, database=fdb_file,
                             flags=SrvRestoreFlag.REPLACE, verbose=True)
        restore_err = [line for line in srv if 'ERROR' in line.upper()]
        #
        log_after = act.get_firebird_log()
        # Check messages about shutdown mode during a restore process.
        # We cannot check entire log because it may contain old messages about shutdown.
        # Thus we should check only log diff.
        # --------------------------------------------------------------------------
        # Check messages and clear log diff to ensure there are no others messages in log
        full_pattern = r'^\-{3}(\s|\\n|\\r)*\+{3}(\s|\\n|\\r)*@@.*@@(\s|\\n|\\r)*Username:.*(\s|\\n|\\r)*Change of attribute ForcedWrite from true to false(\s|\\n|\\r)*$'
        single_pattern = 	r'^\+\s*(\\n|\\r)*\+.*\d{2}:\d{2}:\d{2}\s\d{4}\s*(\\n|\\r)*\+\s*IP:.*\s*(\\n|\\r)*\+\s*DATABASE:.*\s*(\\n|\\r)*\+\s*USERNAME: SYSDBA\s*(\\n|\\r)*\+\s*SET SHUTDOWN MODE TO SINGLE.\s*(\\n|\\r)*\+\s*$'
        normal_pattern = 	r'^\+\s*(\\n|\\r)*\+.*\d{2}:\d{2}:\d{2}\s\d{4}\s*(\\n|\\r)*\+\s*IP:.*\s*(\\n|\\r)*\+\s*DATABASE:.*\s*(\\n|\\r)*\+\s*USERNAME: SYSDBA\s*(\\n|\\r)*\+\s*SET SHUTDOWN MODE TO NORMAL.\s*(\\n|\\r)*\+\s*$'
        force_pattern = 	r'^\+\s*(\\n|\\r)*\+.*\d{2}:\d{2}:\d{2}\s\d{4}\s*(\\n|\\r)*\+\s*IP:.*\s*(\\n|\\r)*\+\s*DATABASE:.*\s*(\\n|\\r)*\+\s*USERNAME: SYSDBA\s*(\\n|\\r)*\+\s*CHANGE OF ATTRIBUTE FORCEDWRITE FROM FALSE TO FALSE\s*(\\n|\\r)*\+\s*$'
        difftext = ''.join(unified_diff(log_before, log_after))
        delete_header = re.sub(full_pattern, '', difftext, count=1, flags=re.M)
        expected_messages = ['SET SHUTDOWN MODE TO SINGLE', 'SET SHUTDOWN MODE TO NORMAL', 'CHANGE OF ATTRIBUTE FORCEDWRITE FROM FALSE TO FALSE']
        messages_check = []
        if re.search(single_pattern, delete_header, flags=re.M|re.I):
            messages_check.append('SET SHUTDOWN MODE TO SINGLE')
        delete_single = re.sub(single_pattern, '', delete_header, count=1, flags=re.M|re.I)

        if re.search(normal_pattern, delete_single, flags=re.M|re.I):
            messages_check.append('SET SHUTDOWN MODE TO NORMAL')
        delete_normal = re.sub(normal_pattern, '', delete_single, count=1, flags=re.M|re.I)

        if re.search(force_pattern, delete_normal, flags=re.M|re.I):
            messages_check.append('CHANGE OF ATTRIBUTE FORCEDWRITE FROM FALSE TO FALSE')
        delete_force = re.sub(force_pattern, '', delete_normal, count=1, flags=re.M|re.I)
        #
        srv.database.validate(database=fdb_file)
        validate_err = [line for line in srv if 'ERROR' in line.upper()]
    #
    assert restore_err == []
    assert validate_err == []
    assert delete_force.split() == []
    assert messages_check == expected_messages
