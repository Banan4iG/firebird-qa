#coding:utf-8

"""
ID:          issue-1276
ISSUE:       1276
TITLE:       The built-in BLR printer doesn't support all FB2 features
DESCRIPTION:
JIRA:        CORE-883
FBTEST:      bugs.core_0883
"""

import pytest
from firebird.qa import *

db = db_factory(from_backup='core0883-ods12.fbk')

test_script = """
    set list on;
    set blob all;
    select rdb$procedure_blr
    from rdb$procedures
    where rdb$procedure_name = upper('sp1');
"""

act = isql_act('db', test_script, substitutions=[('RDB\\$PROCEDURE_BLR.*', '')])

expected_stdout = """
RDB$PROCEDURE_BLR               1a:f1
        	blr_version5,
        	blr_begin,
        	   blr_message, 1, 1,0,
        	      blr_short, 0,
        	   blr_begin,
        	      blr_declare, 0,0, blr_sql_time,
        	      blr_assignment,
        	         blr_null,
        	         blr_variable, 0,0,
        	      blr_declare, 1,0, blr_timestamp,
        	      blr_assignment,
        	         blr_null,
        	         blr_variable, 1,0,
        	      blr_declare, 2,0, blr_long, 0,
        	      blr_assignment,
        	         blr_null,
        	         blr_variable, 2,0,
        	      blr_declare, 3,0, blr_blob2, 0,0, 0,0,
        	      blr_assignment,
        	         blr_null,
        	         blr_variable, 3,0,
        	      blr_declare, 4,0, blr_blob2, 0,0, 0,0,
        	      blr_assignment,
        	         blr_null,
        	         blr_variable, 4,0,
        	      blr_dcl_cursor, 0,0,
        	         blr_rse, 1,
        	            blr_relation2, 14, 'R','D','B','$','P','R','O','C','E','D','U','R','E','S',
        	               8, 'C','_','S','T','T','M',32,'P', 0,
        	            blr_end,
        	         3,0,
        	         blr_derived_expr, 1, 0,
        	            blr_field, 0, 16, 'R','D','B','$','P','R','O','C','E','D','U','R','E','_','I','D',
        	         blr_derived_expr, 1, 0,
        	            blr_field, 0, 20, 'R','D','B','$','P','R','O','C','E','D','U','R','E','_','S','O','U','R','C','E',
        	         blr_derived_expr, 1, 0,
        	            blr_field, 0, 17, 'R','D','B','$','P','R','O','C','E','D','U','R','E','_','B','L','R',
        	      blr_stall,
        	      blr_label, 0,
        	         blr_begin,
        	            blr_begin,
        	               blr_assignment,
        	                  blr_current_time2, 3,
        	                  blr_variable, 0,0,
        	               blr_assignment,
        	                  blr_current_timestamp,
        	                  blr_variable, 1,0,
        	               blr_cursor_stmt, 0, 0,0,

        	               blr_begin,
        	                  blr_end,
        	               blr_label, 1,
        	                  blr_loop,
        	                     blr_begin,
        	                        blr_if,
        	                           blr_eql,
        	                              blr_literal, blr_long, 0, 1,0,0,0,
        	                              blr_literal, blr_long, 0, 1,0,0,0,
        	                           blr_begin,
        	                              blr_begin,
        	                                 blr_cursor_stmt, 2, 0,0,

        	                                 blr_begin,
        	                                    blr_assignment,
        	                                       blr_field, 0, 16, 'R','D','B','$','P','R','O','C','E','D','U','R','E','_','I','D',
        	                                       blr_variable, 2,0,
        	                                    blr_assignment,
        	                                       blr_field, 0, 20, 'R','D','B','$','P','R','O','C','E','D','U','R','E','_','S','O','U','R','C','E',
        	                                       blr_variable, 3,0,
        	                                    blr_assignment,
        	                                       blr_field, 0, 17, 'R','D','B','$','P','R','O','C','E','D','U','R','E','_','B','L','R',
        	                                       blr_variable, 4,0,
        	                                    blr_end,
        	                                 blr_if,
        	                                    blr_eql,
        	                                       blr_internal_info,
        	                                          blr_literal, blr_long, 0, 5,0,0,0,
        	                                       blr_literal, blr_long, 0, 0,0,0,0,
        	                                    blr_leave, 1,
        	                                    blr_end,
        	                                 blr_end,
        	                              blr_end,
        	                           blr_leave, 1,
        	                        blr_end,
        	               blr_cursor_stmt, 1, 0,0,

        	               blr_begin,
        	                  blr_end,
        	               blr_end,
        	            blr_end,
        	      blr_end,
        	   blr_send, 1,
        	      blr_begin,
        	         blr_assignment,
        	            blr_literal, blr_short, 0, 0,0,
        	            blr_parameter, 1, 0,0,
        	         blr_end,
        	   blr_end,
        	blr_eoc
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

