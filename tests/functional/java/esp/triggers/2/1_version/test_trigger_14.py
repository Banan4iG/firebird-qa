#coding:utf-8

"""
ID:          java.esp.triggers.2.1-version.trigger-14
TITLE:       Set new value of not exist field from esp for BEFORE UPDATE trigger
DESCRIPTION: 
  Expected error:
  
  Statement failed, SQLCODE = -901
  java.lang.Exception: org.firebirdsql.gds.GDSException: internal gds software consistency check ("NOT_EXIST_FIELD" is a corrupt field name)
  org.firebirdsql.javaudf.Trigger.setNewValue(Trigger.java:86)
  esp.TestTrigger.setNewValue(TestTrigger.java:152)
  sun.reflect.GeneratedMethodAccessor1.invoke(Unknown Source)
  sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:25)
  java.lang.reflect.Method.invoke(Method.java:597)
  org.firebirdsql.javaudf.CallJavaMethod$mthCall.call(CallJavaMethod.java:421)
  org.firebirdsql.javaudf.CallJavaMethod.call(CallJavaMethod.java:347)
  
  -At trigger 'TEST_TRIGGER' line: 5, col: 3
FBTEST:      functional.java.esp.triggers.2.1_version.trigger_14
"""

import pytest
from firebird.qa import *

db = db_factory()

act = isql_act('db', """""")

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.execute()
