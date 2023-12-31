#coding:utf-8

"""
ID:          issue-1298
ISSUE:       1298
TITLE:       Error "context already in use" for the simple case function with a sub-select operand
DESCRIPTION:
JIRA:        CORE-3296
FBTEST:      bugs.core_3296
"""

import pytest
from firebird.qa import *

init_script = """CREATE TABLE VAT_ZAK
(
  ID Integer NOT NULL,
  SYS_NR Integer,
  CONSTRAINT PK_VAT_ZAK__ID PRIMARY KEY (ID)
);

CREATE TABLE ELEMENTY
(
   ID Integer NOT NULL,
  ID_VAT_SPRZ Integer,
CONSTRAINT PK_ELEMENTY__ID PRIMARY KEY (ID)
);
COMMIT;"""

db = db_factory(charset='UTF8', init=init_script)

test_script = """UPDATE
ELEMENTY E
SET
E.ID_VAT_SPRZ=
CASE
WHEN (SELECT V.SYS_NR FROM VAT_ZAK V WHERE V.ID=E.ID_VAT_SPRZ) = 1 THEN (SELECT V.ID FROM VAT_ZAK V WHERE V.SYS_NR=7)
WHEN (SELECT V.SYS_NR FROM VAT_ZAK V WHERE V.ID=E.ID_VAT_SPRZ) = 2 THEN (SELECT V.ID FROM VAT_ZAK V WHERE V.SYS_NR=8)
WHEN (SELECT V.SYS_NR FROM VAT_ZAK V WHERE V.ID=E.ID_VAT_SPRZ) = 3 THEN (SELECT V.ID FROM VAT_ZAK V WHERE V.SYS_NR=9)
ELSE E.ID_VAT_SPRZ END;
COMMIT;
UPDATE
ELEMENTY E
SET
E.ID_VAT_SPRZ=
CASE
(SELECT V.SYS_NR FROM VAT_ZAK V WHERE V.ID=E.ID_VAT_SPRZ)
WHEN 1 THEN (SELECT V.ID FROM VAT_ZAK V WHERE V.SYS_NR=7)
WHEN 2 THEN (SELECT V.ID FROM VAT_ZAK V WHERE V.SYS_NR=8)
WHEN 3 THEN (SELECT V.ID FROM VAT_ZAK V WHERE V.SYS_NR=9)
ELSE E.ID_VAT_SPRZ END;
COMMIT;
"""

act = isql_act('db', test_script)

@pytest.mark.version('>=3')
def test_1(act: Action):
    act.execute()
