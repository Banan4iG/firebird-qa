#coding:utf-8

"""
ID:          java.esp.triggers.2.1-version.trigger-10
TITLE:       Get new value from esp for AFTER INSERT trigger
DESCRIPTION: 
FBTEST:      functional.java.esp.triggers.2.1_version.trigger_10
"""

import pytest
from firebird.qa import *

db = db_factory()

act = isql_act('db', """""")

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.execute()
