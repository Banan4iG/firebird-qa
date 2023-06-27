#coding:utf-8
"""
ID:          utilites.gfix.sweep.full_mend_log_diff
TITLE:       Check that validation log messages for mend and full keys are different.
DESCRIPTION:
"""

import pytest
from firebird.qa import *
import locale
import re
from difflib import unified_diff

db = db_factory()
act = python_act('db')

expected_stdout_log_diff = """
    +	Validation started
    +	Validation finished: 0 errors, 0 warnings, 0 fixed
    +	Validation (mend) started
    +	Validation (mend) finished: 0 errors, 0 warnings, 0 fixed
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action):
    with act.connect_server(encoding=locale.getpreferredencoding()) as srv:
        srv.info.get_log()
        fb_log_init = srv.readlines()

    actual_log_diff = []

    act.gfix(switches=['-v', '-full', '-n', act.db.dsn])
    with act.connect_server(encoding=locale.getpreferredencoding()) as srv:
        srv.info.get_log()
        fb_log_full = srv.readlines()

    diff_patterns = [
        "Validation started",
        "Validation finished: 0 errors, 0 warnings, 0 fixed",
    ]
    diff_patterns = [re.compile(s) for s in diff_patterns]
    for line in unified_diff(fb_log_init, fb_log_full):
        if line.startswith('+'):
            if act.match_any(line, diff_patterns):
                actual_log_diff.append(line)

    act.gfix(switches=['-mend', '-n', act.db.dsn])
    with act.connect_server(encoding=locale.getpreferredencoding()) as srv:
        srv.info.get_log()
        fb_log_mend = srv.readlines()

    diff_patterns = [
        "Validation \\(mend\\) started",
        "Validation \\(mend\\) finished: 0 errors, 0 warnings, 0 fixed"
    ]
    diff_patterns = [re.compile(s) for s in diff_patterns]

    for line in unified_diff(fb_log_full, fb_log_mend):
        if line.startswith('+'):
            if act.match_any(line, diff_patterns):
                actual_log_diff.append(line)

    act.expected_stdout = expected_stdout_log_diff
    act.stdout = '\n'.join(actual_log_diff)
    assert act.clean_stdout == act.clean_expected_stdout
