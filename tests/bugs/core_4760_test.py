#coding:utf-8

"""
ID:          issue-5063
ISSUE:       5063
TITLE:       Can not create user with non-ascii (multi-byte) characters in it's name
DESCRIPTION:
NOTES:
[24.11.2021] pcisar
  1. This problem is covered by test for #5048 (CORE-4743) as side effect
  2. For sake of completness, it was reimplemented by simply using
     user_factory fixture.
[09.02.2022] pcisar
  On Windows the act.db.connect() fails with "Your user name and password are not defined."
JIRA:        CORE-4760
FBTEST:      bugs.core_4760
"""

import pytest
import platform
from firebird.qa import *

db = db_factory(charset='UTF8')

non_ascii_user = user_factory('db', name='"Εὐκλείδης"', password='123')

act = python_act('db')

@pytest.mark.skipif(platform.system() == 'Windows', reason='FIXME: see notes')
@pytest.mark.version('>=4.0')
def test_1(act: Action, non_ascii_user: User):
    with act.db.connect(user=non_ascii_user.name, password=non_ascii_user.password) as con:
        pass


