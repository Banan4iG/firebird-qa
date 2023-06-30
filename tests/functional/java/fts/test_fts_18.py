#coding:utf-8

"""
ID:          java.fts.fts-18
TITLE:       
DESCRIPTION: 
  Test for search based on morphological forms.
FBTEST:      functional.java.fts.fts_18
"""

import pytest
from firebird.qa import *

# version: 3.0

db_1 = db_factory(from_backup='fts_new.fbk')

act_1 = python_act('db_1', substitutions=[('SQL>.*', ''), ('CON>', '')])

expected_stdout_1 = """FTS$SCORE FTS$RELATION                    FTS$HIGHLIGHT
======================= =============================== ===============================================================================
0.7459743022918701 TABLE3                           chemical but <B>experts</B> fight copy chalk crush addition do copper blue enough deep bone existence dear drain <B>experience</B> colour end cold existence body bit competition dear blow book
0.5592164993286133 TABLE3                           fish fall division back chance back ball feeble amusement arm <B>expert</B> east <B>expert</B> between animal day event earth direction after division comfort boat after distance camera adjustment
0.4068950712680817 TABLE3                           certain dress expansion care <B>expert&#x27;s</B> cook account existence cork by father family cord danger butter art answer flight comb finger blue camera death chin amount animal do authority
0.3496516048908234 TABLE3                           automatic butter apple carriage bag copy comfort bridge attention fertile cook band different <B>experience</B> canvas bottle end chain cork death building down cheap adjustment curve
0.3340292274951935 TABLE3                           cat animal circle and end among bone far building drain brass design engine different box back bread chief birth effect board clear authority example body down fish cloth <B>experience</B>
0.3340292274951935 TABLE3                           drop art finger bottle complex drawer flag all bright dark carriage art cold education circle crush common blue circle cow every enough arch every apparatus <B>experience</B> colour egg
"""

@pytest.mark.skip('FIXME: Not IMPLEMENTED')
@pytest.mark.java
@pytest.mark.version('>=3.0,<4.0')
def test_1(act_1: Action):
    pytest.fail("Not IMPLEMENTED")

# Original python code for this test:
# -----------------------------------
# 
# import os
# 
# fts_script_path = os.path.join(context['rdb_path'], 'misc', 'fts.sql')
# 
# init_script = """
# connect '%s';
# create role fts;
# grant default fts to sysdba;
# commit;
# connect '%s';
# input '%s';
# commit;
# """ % (dsn, dsn, fts_script_path)
# 
# test_script = """
# CONNECT '%s';
# commit;
# EXECUTE PROCEDURE FTS$CREATE_INDEX('TEST_INDEX', 'English');
# commit;
# EXECUTE PROCEDURE FTS$ADD_FIELD_TO_INDEX('TEST_INDEX', 'TABLE3','F_VCHAR');
# commit;
# 
# EXECUTE PROCEDURE FTS$REINDEX('TEST_INDEX');
# commit;
# 
# SELECT fts$score, fts$relation, FTS$HIGHLIGHT from FTS$SEARCH('TEST_INDEX', NULL, 'expert~', 500);
# EXECUTE PROCEDURE FTS$DROP_INDEX('TEST_INDEX');
# commit;
# 
# """ % dsn
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], init_script)
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script)
# -----------------------------------

# version: 4.0

db_2 = db_factory(from_backup='fts_new.fbk')

act_2 = python_act('db_2', substitutions=[('SQL>.*', ''), ('CON>', '')])

expected_stdout_2 = """FTS$SCORE FTS$RELATION                    FTS$HIGHLIGHT
======================= =============================== ================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
1.641143560409546 TABLE3                           chemical but <B>experts</B> fight copy chalk crush addition do copper blue enough deep bone existence dear drain <B>experience</B> colour end cold existence body bit competition dear blow book
1.230276346206665 TABLE3                           fish fall division back chance back ball feeble amusement arm <B>expert</B> east <B>expert</B> between animal day event earth direction after division comfort boat after distance camera adjustment
0.8951691985130310 TABLE3                           certain dress expansion care <B>expert's</B> cook account existence cork by father family cord danger butter art answer flight comb finger blue camera death chin amount animal do authority
0.7692335247993469 TABLE3                           automatic butter apple carriage bag copy comfort bridge attention fertile cook band different <B>experience</B> canvas bottle end chain cork death building down cheap adjustment curve
0.7348642945289612 TABLE3                           cat animal circle and end among bone far building drain brass design engine different box back bread chief birth effect board clear authority example body down fish cloth <B>experience</B>
0.7348642945289612 TABLE3                           drop art finger bottle complex drawer flag all bright dark carriage art cold education circle crush common blue circle cow every enough arch every apparatus <B>experience</B> colour egg
"""

@pytest.mark.skip('FIXME: Not IMPLEMENTED')
@pytest.mark.java
@pytest.mark.version('>=4.0,<5.0')
def test_2(act_2: Action):
    pytest.fail("Not IMPLEMENTED")

# Original python code for this test:
# -----------------------------------
# 
# import os
# 
# fts_script_path = os.path.join(context['rdb_path'], 'misc', 'fts.sql')
# 
# init_script = """
# connect '%s';
# create role fts;
# grant default fts to sysdba;
# commit;
# connect '%s';
# input '%s';
# commit;
# """ % (dsn, dsn, fts_script_path)
# 
# test_script = """
# CONNECT '%s';
# commit;
# EXECUTE PROCEDURE FTS$CREATE_INDEX('TEST_INDEX', 'English');
# commit;
# EXECUTE PROCEDURE FTS$ADD_FIELD_TO_INDEX('TEST_INDEX', 'TABLE3','F_VCHAR');
# commit;
# 
# EXECUTE PROCEDURE FTS$REINDEX('TEST_INDEX');
# commit;
# 
# SELECT fts$score, fts$relation, FTS$HIGHLIGHT from FTS$SEARCH('TEST_INDEX', NULL, 'expert~', 500);
# EXECUTE PROCEDURE FTS$DROP_INDEX('TEST_INDEX');
# commit;
# 
# """ % dsn
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], init_script)
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script)
# -----------------------------------

# version: 5.0

db_3 = db_factory(from_backup='fts_new.fbk')

act_3 = python_act('db_3', substitutions=[('SQL>.*', ''), ('CON>', '')])

expected_stdout_3 = """FTS$RELATION                    FTS$HIGHLIGHT
=============================== ================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
TABLE3                           chemical but <B>experts</B> fight copy chalk crush addition do copper blue enough deep bone existence dear drain <B>experience</B> colour end cold existence body bit competition dear blow book
TABLE3                           fish fall division back chance back ball feeble amusement arm <B>expert</B> east <B>expert</B> between animal day event earth direction after division comfort boat after distance camera adjustment
TABLE3                           certain dress expansion care <B>expert&#x27;s</B> cook account existence cork by father family cord danger butter art answer flight comb finger blue camera death chin amount animal do authority
TABLE3                           automatic butter apple carriage bag copy comfort bridge attention fertile cook band different <B>experience</B> canvas bottle end chain cork death building down cheap adjustment curve
TABLE3                           cat animal circle and end among bone far building drain brass design engine different box back bread chief birth effect board clear authority example body down fish cloth <B>experience</B>
TABLE3                           drop art finger bottle complex drawer flag all bright dark carriage art cold education circle crush common blue circle cow every enough arch every apparatus <B>experience</B> colour egg
"""

@pytest.mark.skip('FIXME: Not IMPLEMENTED')
@pytest.mark.java
@pytest.mark.version('>=5.0')
def test_3(act_3: Action):
    pytest.fail("Not IMPLEMENTED")

# Original python code for this test:
# -----------------------------------
# 
# import os
# 
# fts_script_path = os.path.join(context['rdb_path'], 'misc', 'fts.sql')
# 
# init_script = """
# connect '%s';
# create role fts;
# grant default fts to sysdba;
# commit;
# connect '%s';
# input '%s';
# commit;
# """ % (dsn, dsn, fts_script_path)
# 
# test_script = """
# CONNECT '%s';
# commit;
# EXECUTE PROCEDURE FTS$CREATE_INDEX('TEST_INDEX', 'English');
# commit;
# EXECUTE PROCEDURE FTS$ADD_FIELD_TO_INDEX('TEST_INDEX', 'TABLE3','F_VCHAR');
# commit;
# 
# EXECUTE PROCEDURE FTS$REINDEX('TEST_INDEX');
# commit;
# 
# SELECT fts$relation, FTS$HIGHLIGHT from FTS$SEARCH('TEST_INDEX', NULL, 'expert~', 500);
# EXECUTE PROCEDURE FTS$DROP_INDEX('TEST_INDEX');
# commit;
# 
# """ % dsn
# 
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], init_script)
# runProgram('isql', ['-user', user_name,'-password', user_password, '-q'], test_script)
# -----------------------------------
