#coding:utf-8

"""
ID:          issue-6481
ISSUE:       6481
TITLE:       Performance problem when using SRP plugin
DESCRIPTION:
  :::::::::::::::::::: N O T A   B E N E  :::::::::::::::::
  It is crucial for this test that firebird.conf have following _SEQUENCE_ of auth-plugins:  Srp, ...,  Legacy_Auth
  -- i.e. Srp must be specified BEFORE Legacy.
  Slow time of attach establishing can NOT be seen otherwise; rather almost no difference will be in that case.
  :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

  Test creates two users: one usingLegacy plugin and second using Srp.
  Then we make ~20...30 pairs of attach/detach by each of these users and get total time difference for these actions.
  Ratio between these total differences must be limited with threshold. Its value was determined after dozen of runs
  and it seems to be reasonable assign to it value 1.25 (see MIN_RATIO_THRESHOLD in the code).

  Test output will contain ALERT if total time of <attaches_using_Srp> vs <attaches_using_Legacy>
  will be greater than MIN_RATIO_THRESHOLD.

  Reproduced on on several builds 4.x before 17.01.2020 (tested: 4.0.0.1712 CS, 4.0.0.1731 CS - got ratio = ~1.95).
  Reproduced also on 3.0.5.33221 Classic - got ratio ~1.50 ... 1.70; could NOT reproduce on 3.0.5 SuperClassic / SuperServer.
[09.02.2022] pcisar
  Fails on Windows 4.0.1 with ratio 1.98 - raw iron W10, does not fail with Linux on the same HW
JIRA:        CORE-6237
FBTEST:      bugs.core_6237
NOTES:
    [30.07.2022] pzotov
    Checked on 5.0.0.591, 4.0.1.2692, 3.0.8.33535 (windows only; pisix will be checked later).
"""

import pytest
import datetime
import platform
from firebird.qa import *

db = db_factory()

leg_user = user_factory('db', name='tmp_c6237_leg', password='123', plugin='Legacy_UserManager')
srp_user = user_factory('db', name='tmp_c6237_srp', password='123', plugin='Srp')

act = python_act('db')

#------------------
def median(lst):
    n = len(lst)
    s = sorted(lst)
    return (sum(s[n//2-1:n//2+1])/2.0, s[n//2])[n % 2] if n else None
#------------------


expected_stdout = """
    EXPECTED. Ratio of total elapsed time when use Srp vs Legacy is less then threshold.
"""

@pytest.mark.version('>=3.0.5')
def test_1(act: Action, leg_user: User, srp_user: User, capsys):
    N_COUNT = 100
    MIN_RATIO_THRESHOLD = 1.41
    sp_time = {}


    for user in [leg_user, srp_user]:
        for i in range(N_COUNT):
             start = datetime.datetime.now()
             stop = start
             with act.db.connect(user=user.name, password=user.password):
                stop = datetime.datetime.now()

             diff = stop - start
             sp_time[user.name, i] = int(diff.seconds) * 1000 + diff.microseconds / 1000

    leg_user_conn_time = [round(v,2) for k,v in sp_time.items() if k[0] == leg_user.name]
    srp_user_conn_time = [round(v,2) for k,v in sp_time.items() if k[0] == srp_user.name]


    conn_time_ratio = median(srp_user_conn_time) / median(leg_user_conn_time)
    if conn_time_ratio < MIN_RATIO_THRESHOLD:
        print('EXPECTED. Ratio of total elapsed time when use Srp vs Legacy is less then threshold.')
    else:
        print(f'Ratio Srp/Legacy: {conn_time_ratio} - is GREATER than threshold = {MIN_RATIO_THRESHOLD}.')
        print(f'    Median for Srp: {median(srp_user_conn_time)}')
        print(f'    Median for Legacy: {median(leg_user_conn_time)}')

    act.expected_stdout = expected_stdout
    act.stdout = capsys.readouterr().out
    assert act.clean_stdout == act.clean_expected_stdout
