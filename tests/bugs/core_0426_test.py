#coding:utf-8
#
# id:           bugs.core_426
# title:        Wrong sort order when using es_ES collate
# decription:   Check if sort order for collate ES_ES is the one of DRAE , the oficial organization for standarization of spanish
# tracker_id:   CORE-426
# min_versions: []
# versions:     2.1
# qmid:         bugs.core_426

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 2.1
# resources: None

substitutions_1 = []

init_script_1 = """SET NAMES ISO8859_1;
CREATE TABLE TAB (A CHAR(3) CHARACTER SET ISO8859_1);
COMMIT;
INSERT INTO TAB VALUES ('zo');
INSERT INTO TAB VALUES ('ze');
INSERT INTO TAB VALUES ('yo');
INSERT INTO TAB VALUES ('ye');
INSERT INTO TAB VALUES ('xo');
INSERT INTO TAB VALUES ('xe');
INSERT INTO TAB VALUES ('vo');
INSERT INTO TAB VALUES ('ve');
INSERT INTO TAB VALUES ('uo');
INSERT INTO TAB VALUES ('ue');
INSERT INTO TAB VALUES ('to');
INSERT INTO TAB VALUES ('te');
INSERT INTO TAB VALUES ('so');
INSERT INTO TAB VALUES ('se');
INSERT INTO TAB VALUES ('ro');
INSERT INTO TAB VALUES ('re');
INSERT INTO TAB VALUES ('qo');
INSERT INTO TAB VALUES ('qe');
INSERT INTO TAB VALUES ('po');
INSERT INTO TAB VALUES ('pe');
INSERT INTO TAB VALUES ('oo');
INSERT INTO TAB VALUES ('oe');
INSERT INTO TAB VALUES ('no');
INSERT INTO TAB VALUES ('ne');
INSERT INTO TAB VALUES ('mo');
INSERT INTO TAB VALUES ('me');
INSERT INTO TAB VALUES ('llo');
INSERT INTO TAB VALUES ('lle');
INSERT INTO TAB VALUES ('lo');
INSERT INTO TAB VALUES ('le');
INSERT INTO TAB VALUES ('ko');
INSERT INTO TAB VALUES ('ke');
INSERT INTO TAB VALUES ('jo');
INSERT INTO TAB VALUES ('je');
INSERT INTO TAB VALUES ('io');
INSERT INTO TAB VALUES ('ie');
INSERT INTO TAB VALUES ('ho');
INSERT INTO TAB VALUES ('he');
INSERT INTO TAB VALUES ('go');
INSERT INTO TAB VALUES ('fe');
INSERT INTO TAB VALUES ('fo');
INSERT INTO TAB VALUES ('fe');
INSERT INTO TAB VALUES ('eo');
INSERT INTO TAB VALUES ('ee');
INSERT INTO TAB VALUES ('do');
INSERT INTO TAB VALUES ('de');
INSERT INTO TAB VALUES ('cho');
INSERT INTO TAB VALUES ('cha');
INSERT INTO TAB VALUES ('co');
INSERT INTO TAB VALUES ('ce');
INSERT INTO TAB VALUES ('bo');
INSERT INTO TAB VALUES ('be');
INSERT INTO TAB VALUES ('ao');
INSERT INTO TAB VALUES ('ae');"""

db_1 = db_factory(charset='ISO8859_1', sql_dialect=3, init=init_script_1)

test_script_1 = """SET HEADING OFF;
SELECT A FROM TAB ORDER BY A COLLATE ES_ES;
"""

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """ae
ao
be
bo
ce
cha
cho
co
de
do
ee
eo
fe
fe
fo
go
he
ho
ie
io
je
jo
ke
ko
le
lle
llo
lo
me
mo
ne
no
oe
oo
pe
po
qe
qo
re
ro
se
so
te
to
ue
uo
ve
vo
xe
xo
ye
yo
ze
zo

"""

@pytest.mark.version('>=2.1')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout

