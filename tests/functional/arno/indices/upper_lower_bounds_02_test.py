#coding:utf-8
#
# id:           functional.arno.indices.upper_lower_bounds_02
# title:        upper and lower bounds
# decription:   "Less or equal than" should be prefered above "less than" and "greater or equal than" above "greater than".
# tracker_id:   
# min_versions: []
# versions:     3.0
# qmid:         functional.arno.indexes.upper_lower_bounds_02

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 3.0
# resources: None

substitutions_1 = []

init_script_1 = """CREATE TABLE Table_1000 (
  ID INTEGER NOT NULL
);

SET TERM ^^ ;
CREATE PROCEDURE PR_FillTable_1000
AS
DECLARE VARIABLE FillID INTEGER;
BEGIN
  FillID = 1;
  WHILE (FillID <= 1000) DO
  BEGIN
    INSERT INTO Table_1000 (ID) VALUES (:FillID);
    FillID = FillID + 1;
  END
END
^^
SET TERM ; ^^

COMMIT;

EXECUTE PROCEDURE PR_FillTable_1000;

COMMIT;

CREATE UNIQUE ASC INDEX PK_Table_1000 ON Table_1000 (ID);

COMMIT;
"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

# test_script_1
#---
# class readsInformation:
#    sequential = {}
#    indexed = {}
#    sequentialStart = {}
#    indexedStart = {}
#    systemTables = False
#    #--
#    def start(self):
#      self.sequentialStart = db_conn.db_info(kdb.isc_info_read_seq_count)
#      self.indexedStart = db_conn.db_info(kdb.isc_info_read_idx_count)
#    #--
#    def addSequential(self, relationID, count):
#      self.sequential[relationID] = count - self.sequentialStart.get(relationID,0)
#    #--
#    def addIndexed(self, relationID, count):
#      self.indexed[relationID] = count - self.indexedStart.get(relationID,0)
#    #--
#    def difference(self):
#      seqReads = db_conn.db_info(kdb.isc_info_read_seq_count)
#      idxReads = db_conn.db_info(kdb.isc_info_read_idx_count)
#      for tabid, reads in seqReads.items():
#        if (self.systemTables) or (tabid >= 128):
#          self.addSequential(tabid, reads)
#      for tabid, reads in idxReads.items():
#        if (self.systemTables) or (tabid >= 128):
#          self.addIndexed(tabid, reads)
#    #--
#    def show(self):
#      print ('sequential : ',self.sequential)
#      print ('indexed    : ',self.indexed)
#  
#  cursor=db_conn.cursor()
#  
#  ri = readsInformation()
#  ri.start()
#  
#  cursor.execute("SELECT Count(*) FROM Table_1000 t1000 WHERE t1000.ID > 1 and t1000.ID >= 400 and t1000.ID <= 600 and t1000.ID < 1000")
#  printData(cursor)
#  
#  # Get statistics and put out differences
#  ri.difference()
#  ri.show()
#  
#  #SET PLAN ON;
#  #SET STATS ON;
#  #SELECT B.B_INFO, A.A_VALUE FROM TableB B LEFT JOIN TableA A ON (1 = 0);
#---
#act_1 = python_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """COUNT
--------------------
201
sequential :  {}
indexed    :  {128: 201}
"""

@pytest.mark.version('>=3.0')
@pytest.mark.xfail
def test_1(db_1):
    pytest.fail("Test not IMPLEMENTED")


