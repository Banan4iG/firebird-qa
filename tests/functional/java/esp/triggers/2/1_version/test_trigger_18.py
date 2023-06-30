#coding:utf-8

"""
ID:          java.esp.triggers.2.1-version.trigger-18
TITLE:       Set new value into type blob field from esp for BEFORE UPDATE trigger
DESCRIPTION: 
  Работа с блобами пока не реализована
FBTEST:      functional.java.esp.triggers.2.1_version.trigger_18
"""

import pytest
from firebird.qa import *

db = db_factory()

act = isql_act('db', """""")

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.execute()
