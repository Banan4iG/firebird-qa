#coding:utf-8

"""
ID:          java.esp.triggers.2.1-version.trigger-22
TITLE:       Call ESP from trigger ON TRANSACTION COMMIT
DESCRIPTION: 
FBTEST:      functional.java.esp.triggers.2.1_version.trigger_22
"""

import pytest
from firebird.qa import *

db = db_factory()

act = isql_act('db', """""")

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.execute()
