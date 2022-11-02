#coding:utf-8

"""
ID:          issue-5903
ISSUE:       5903
TITLE:       string right truncation on restore of security db
DESCRIPTION:
NOTES:
[25.10.2019] Refactored
  restored DB state must be changed to full shutdown in order to make sure tha all attachments are gone.
  Otherwise got on CS: "WindowsError: 32 The process cannot access the file because it is being used by another process".
JIRA:        CORE-5637
FBTEST:      bugs.core_5637
"""

import pytest
import zipfile
from difflib import unified_diff
from pathlib import Path
from firebird.qa import *
from firebird.driver import SrvRestoreFlag, ShutdownMode, ShutdownMethod
import re

db = db_factory()

act = python_act('db')

sec_fbk = temp_file('core5637-security3.fbk')
sec_fdb = temp_file('core5637-security3.fdb')

@pytest.mark.version('>=4.0')
def test_1(act: Action, sec_fbk: Path, sec_fdb: Path):
    zipped_fbk_file = zipfile.Path(act.files_dir / 'core_5637.zip', at='core5637-security3.fbk')
    sec_fbk.write_bytes(zipped_fbk_file.read_bytes())
    #
    log_before = act.get_firebird_log()
    # Restore security database
    with act.connect_server() as srv:
        srv.database.restore(database=sec_fdb, backup=sec_fbk, flags=SrvRestoreFlag.REPLACE)
        restore_log = srv.readlines()
        #
        log_after = act.get_firebird_log()
        # Don't take into account messages about shutdown mode during a restore process.
        # We cannot clear entire log because it may contain old messages about shutdown.
        # Thus we should clean only log diff.
        # --------------------------------------------------------------------------
        # Clear log diff
        full_pattern = r'^\-{3}(\s|\\n|\\r)*\+{3}(\s|\\n|\\r)*@@.*@@(\s|\\n|\\r)*Username:.*(\s|\\n|\\r)*Change of attribute ForcedWrite from true to false(\s|\\n|\\r)*$'
        single_pattern = 	r'^\+\s*(\\n|\\r)*\+.*\d{2}:\d{2}:\d{2}\s\d{4}\s*(\\n|\\r)*\+\s*IP:.*\s*(\\n|\\r)*\+\s*DATABASE:.*\s*(\\n|\\r)*\+\s*USERNAME: SYSDBA\s*(\\n|\\r)*\+\s*SET SHUTDOWN MODE TO SINGLE.\s*(\\n|\\r)*\+\s*$'
        normal_pattern = 	r'^\+\s*(\\n|\\r)*\+.*\d{2}:\d{2}:\d{2}\s\d{4}\s*(\\n|\\r)*\+\s*IP:.*\s*(\\n|\\r)*\+\s*DATABASE:.*\s*(\\n|\\r)*\+\s*USERNAME: SYSDBA\s*(\\n|\\r)*\+\s*SET SHUTDOWN MODE TO NORMAL.\s*(\\n|\\r)*\+\s*$'
        force_pattern = 	r'^\+\s*(\\n|\\r)*\+.*\d{2}:\d{2}:\d{2}\s\d{4}\s*(\\n|\\r)*\+\s*IP:.*\s*(\\n|\\r)*\+\s*DATABASE:.*\s*(\\n|\\r)*\+\s*USERNAME: SYSDBA\s*(\\n|\\r)*\+\s*CHANGE OF ATTRIBUTE FORCEDWRITE FROM FALSE TO TRUE\s*(\\n|\\r)*\+\s*$'
        difftext = ''.join(unified_diff(log_before, log_after))
        delete_full = re.sub(full_pattern, '', difftext, count=1, flags=re.M)
        delete_single = re.sub(single_pattern, '', delete_full, count=1, flags=re.M|re.I)
        delete_normal = re.sub(normal_pattern, '', delete_single, count=1, flags=re.M|re.I)
        diff_clean = re.sub(force_pattern, '', delete_normal, count=1, flags=re.M|re.I)
        # --------------------------------------------------------------------------
        #
        srv.database.validate(database=sec_fdb)
        validation_log = srv.readlines()
        srv.database.shutdown(database=sec_fdb, mode=ShutdownMode.FULL, method=ShutdownMethod.FORCED, timeout=0)
    #
    #
    assert [line for line in restore_log if 'ERROR' in line.upper()] == []
    assert [line for line in validation_log if 'ERROR' in line.upper()] == []
    assert diff_clean.split() == []
