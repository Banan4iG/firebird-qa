#coding:utf-8
#
# id:           bugs.core_6237
# title:        Performance problem when using SRP plugin
# decription:
#                   :::::::::::::::::::: N O T A   B E N E  :::::::::::::::::
#                   It is crucial for this test that firebird.conf have following _SEQUENCE_ of auth-plugins:  Srp, ...,  Legacy_Auth
#                   -- i.e. Srp must be specified BEFORE Legacy.
#                   Slow time of attach establishing can NOT be seen otherwise; rather almost no difference will be in that case.
#                   :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#
#                   Test creates two users: one usingLegacy plugin and second using Srp.
#                   Then we make ~20...30 pairs of attach/detach by each of these users and get total time difference for these actions.
#                   Ratio between these total differences must be limited with threshold. Its value was determined after dozen of runs
#                   and it seems to be reasonable assign to it value 1.25 (see MIN_RATIO_THRESHOLD in the code).
#
#                   Test output will contain ALERT if total time of <attaches_using_Srp> vs <attaches_using_Legacy>
#                   will be greater than MIN_RATIO_THRESHOLD.
#
#                   Reproduced on on several builds 4.x before 17.01.2020 (tested: 4.0.0.1712 CS, 4.0.0.1731 CS - got ratio = ~1.95).
#                   Reproduced also on 3.0.5.33221 Classic - got ratio ~1.50 ... 1.70; could NOT reproduce on 3.0.5 SuperClassic / SuperServer.
#                   Checked on:
#                       4.0.0.1763 SS: 15.592s.
#                       4.0.0.1763 CS: 23.725s.
#                       3.0.6.33240 SS: 7.294s.
#                       3.0.6.33240 CS: 17.407s.
#
#
# tracker_id:   CORE-6237
# min_versions: ['3.0.5']
# versions:     3.0.5
# qmid:         None

import pytest
import datetime
from firebird.qa import db_factory, python_act, Action, user_factory, User

# version: 3.0.5
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

# test_script_1
#---
# import os
#  import datetime
#  from datetime import timedelta
#
#  def showtime():
#       global datetime
#       return ''.join( (datetime.datetime.now().strftime("%H:%M:%S.%f")[:12],'.') )
#
#  os.environ["ISC_USER"] = user_name
#  os.environ["ISC_PASSWORD"] = user_password
#
#  # Number of attach/detach actions for each of checked plugin:
#  N_ITER=50
#
#  # Minimal ratio (for ALERT) between total time when Srp is used vs such value for Legacy auth plugin.
#  # Will be evaluated as datediff(millisecond ...) that were spent for making N_ITER attach/detach actions.
#
#  MIN_RATIO_THRESHOLD = 1.41
#  #                      ^
#  #                     ###################
#  #                     ###  THRESHOLD  ###
#  #                     ###################
#
#  db_conn.execute_immediate("create or alter user tmp_c6237_leg password 'leg' using plugin Legacy_UserManager")
#  db_conn.execute_immediate("create or alter user tmp_c6237_srp password 'srp' using plugin Srp")
#  db_conn.commit()
#  db_conn.close()
#
#
#  elap_ms_for_leg_auth, elap_ms_for_srp_auth = 0,0
#
#  for j in range(0,2):
#      v_user = 'tmp_c6237_leg' if j==0 else 'tmp_c6237_srp'
#      v_pass = 'leg' if j==0 else 'srp'
#
#      ta = datetime.datetime.now()
#      for i in range(0, N_ITER):
#          conx=fdb.connect(dsn = dsn, user = v_user, password = v_pass )
#          conx.close()
#
#      tb = datetime.datetime.now()
#      diff=tb-ta
#
#      if j == 0:
#          elap_ms_for_leg_auth = int(diff.seconds) * 1000  + diff.microseconds / 1000
#      else:
#          elap_ms_for_srp_auth = int(diff.seconds) * 1000  + diff.microseconds / 1000
#
#  db_conn = fdb.connect(dsn = dsn)
#  db_conn.execute_immediate("drop user tmp_c6237_leg using plugin Legacy_UserManager")
#  db_conn.execute_immediate("drop user tmp_c6237_srp using plugin Srp")
#  db_conn.commit()
#  db_conn.close()
#
#  # print( 'Legacy, ms: ', elap_ms_for_leg_auth, '; Srp, ms: ', elap_ms_for_srp_auth, '; 1.00  * elap_ms_for_srp_auth / elap_ms_for_leg_auth=', 1.00 * elap_ms_for_srp_auth / elap_ms_for_leg_auth )
#
#  elapsed_time_ratio = 1.00 * elap_ms_for_srp_auth / elap_ms_for_leg_auth
#  if  elapsed_time_ratio < MIN_RATIO_THRESHOLD:
#      msg = 'EXPECTED. Ratio of total elapsed time when use Srp vs Legacy is less then threshold.'
#  else:
#      msg = 'Ratio Srp/Legacy: %(elapsed_time_ratio)s - is GREATER than threshold = %(MIN_RATIO_THRESHOLD)s. Total time spent for Srp: %(elap_ms_for_srp_auth)s ms; for Legacy: %(elap_ms_for_leg_auth)s ms.' % locals()
#
#  print(msg)
#
#
#---

act_1 = python_act('db_1', substitutions=substitutions_1)

expected_stdout_1 = """
    EXPECTED. Ratio of total elapsed time when use Srp vs Legacy is less then threshold.
  """

leg_user = user_factory('db_1', name='tmp_c6237_leg', password='123', plugin='Legacy_UserManager')
srp_user = user_factory('db_1', name='tmp_c6237_srp', password='123', plugin='Srp')

@pytest.mark.version('>=3.0.5')
def test_1(act_1: Action, leg_user: User, srp_user: User, capsys):
    N_ITER = 50
    MIN_RATIO_THRESHOLD = 1.41
    elapsed = {leg_user.name: 0, srp_user.name: 0}
    #
    for user in [leg_user, srp_user]:
        start = datetime.datetime.now()
        for i in range(N_ITER):
            with act_1.db.connect(user=user.name, password=user.password):
                pass
        stop = datetime.datetime.now()
        diff = stop - start
        elapsed[user.name] = int(diff.seconds) * 1000 + diff.microseconds / 1000
    #
    elapsed_time_ratio = 1.00 * elapsed[srp_user.name] / elapsed[leg_user.name]
    if  elapsed_time_ratio < MIN_RATIO_THRESHOLD:
        print('EXPECTED. Ratio of total elapsed time when use Srp vs Legacy is less then threshold.')
    else:
        print(f'Ratio Srp/Legacy: {elapsed_time_ratio} - is GREATER than threshold = {MIN_RATIO_THRESHOLD}. Total time spent for Srp: {elapsed[srp_user.name]} ms; for Legacy: {elapsed[leg_user.name]} ms.')
    #
    act_1.expected_stdout = expected_stdout_1
    act_1.stdout = capsys.readouterr().out
    assert act_1.clean_stdout == act_1.clean_expected_stdout
