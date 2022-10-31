#coding:utf-8

"""
ID:          new-database-19
TITLE:       New DB - RDB$PROCEDURE_PARAMETERS content
DESCRIPTION: Check the correct content of RDB$PROCEDURE_PARAMETERS in new database.
FBTEST:      functional.basic.db.19
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    set list on;
    set count on;
    select *
    from rdb$procedure_parameters
    order by rdb$procedure_name,rdb$parameter_name,rdb$parameter_number;
"""

act = isql_act('db', test_script)

# version: 3.0

expected_stdout_1 = """
    Records affected: 0
"""

@pytest.mark.version('>=3.0,<4.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout_1
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

# version: 4.0

expected_stdout_2 = """

    RDB$PARAMETER_NAME              RDB$DST_OFFSET
    RDB$PROCEDURE_NAME              TRANSITIONS
    RDB$PARAMETER_NUMBER            3
    RDB$PARAMETER_TYPE              1
    RDB$FIELD_SOURCE                RDB$TIME_ZONE_OFFSET
    RDB$DESCRIPTION                 <null>
    RDB$SYSTEM_FLAG                 1
    RDB$DEFAULT_VALUE               <null>
    RDB$DEFAULT_SOURCE              <null>
    RDB$COLLATION_ID                <null>
    RDB$NULL_FLAG                   1
    RDB$PARAMETER_MECHANISM         0
    RDB$FIELD_NAME                  <null>
    RDB$RELATION_NAME               <null>
    RDB$PACKAGE_NAME                RDB$TIME_ZONE_UTIL

    RDB$PARAMETER_NAME              RDB$EFFECTIVE_OFFSET
    RDB$PROCEDURE_NAME              TRANSITIONS
    RDB$PARAMETER_NUMBER            4
    RDB$PARAMETER_TYPE              1
    RDB$FIELD_SOURCE                RDB$TIME_ZONE_OFFSET
    RDB$DESCRIPTION                 <null>
    RDB$SYSTEM_FLAG                 1
    RDB$DEFAULT_VALUE               <null>
    RDB$DEFAULT_SOURCE              <null>
    RDB$COLLATION_ID                <null>
    RDB$NULL_FLAG                   1
    RDB$PARAMETER_MECHANISM         0
    RDB$FIELD_NAME                  <null>
    RDB$RELATION_NAME               <null>
    RDB$PACKAGE_NAME                RDB$TIME_ZONE_UTIL

    RDB$PARAMETER_NAME              RDB$END_TIMESTAMP
    RDB$PROCEDURE_NAME              TRANSITIONS
    RDB$PARAMETER_NUMBER            1
    RDB$PARAMETER_TYPE              1
    RDB$FIELD_SOURCE                RDB$TIMESTAMP_TZ
    RDB$DESCRIPTION                 <null>
    RDB$SYSTEM_FLAG                 1
    RDB$DEFAULT_VALUE               <null>
    RDB$DEFAULT_SOURCE              <null>
    RDB$COLLATION_ID                <null>
    RDB$NULL_FLAG                   1
    RDB$PARAMETER_MECHANISM         0
    RDB$FIELD_NAME                  <null>
    RDB$RELATION_NAME               <null>
    RDB$PACKAGE_NAME                RDB$TIME_ZONE_UTIL

    RDB$PARAMETER_NAME              RDB$FROM_TIMESTAMP
    RDB$PROCEDURE_NAME              TRANSITIONS
    RDB$PARAMETER_NUMBER            1
    RDB$PARAMETER_TYPE              0
    RDB$FIELD_SOURCE                RDB$TIMESTAMP_TZ
    RDB$DESCRIPTION                 <null>
    RDB$SYSTEM_FLAG                 1
    RDB$DEFAULT_VALUE               <null>
    RDB$DEFAULT_SOURCE              <null>
    RDB$COLLATION_ID                <null>
    RDB$NULL_FLAG                   1
    RDB$PARAMETER_MECHANISM         0
    RDB$FIELD_NAME                  <null>
    RDB$RELATION_NAME               <null>
    RDB$PACKAGE_NAME                RDB$TIME_ZONE_UTIL

    RDB$PARAMETER_NAME              RDB$START_TIMESTAMP
    RDB$PROCEDURE_NAME              TRANSITIONS
    RDB$PARAMETER_NUMBER            0
    RDB$PARAMETER_TYPE              1
    RDB$FIELD_SOURCE                RDB$TIMESTAMP_TZ
    RDB$DESCRIPTION                 <null>
    RDB$SYSTEM_FLAG                 1
    RDB$DEFAULT_VALUE               <null>
    RDB$DEFAULT_SOURCE              <null>
    RDB$COLLATION_ID                <null>
    RDB$NULL_FLAG                   1
    RDB$PARAMETER_MECHANISM         0
    RDB$FIELD_NAME                  <null>
    RDB$RELATION_NAME               <null>
    RDB$PACKAGE_NAME                RDB$TIME_ZONE_UTIL

    RDB$PARAMETER_NAME              RDB$TIME_ZONE_NAME
    RDB$PROCEDURE_NAME              TRANSITIONS
    RDB$PARAMETER_NUMBER            0
    RDB$PARAMETER_TYPE              0
    RDB$FIELD_SOURCE                RDB$TIME_ZONE_NAME
    RDB$DESCRIPTION                 <null>
    RDB$SYSTEM_FLAG                 1
    RDB$DEFAULT_VALUE               <null>
    RDB$DEFAULT_SOURCE              <null>
    RDB$COLLATION_ID                <null>
    RDB$NULL_FLAG                   1
    RDB$PARAMETER_MECHANISM         0
    RDB$FIELD_NAME                  <null>
    RDB$RELATION_NAME               <null>
    RDB$PACKAGE_NAME                RDB$TIME_ZONE_UTIL

    RDB$PARAMETER_NAME              RDB$TO_TIMESTAMP
    RDB$PROCEDURE_NAME              TRANSITIONS
    RDB$PARAMETER_NUMBER            2
    RDB$PARAMETER_TYPE              0
    RDB$FIELD_SOURCE                RDB$TIMESTAMP_TZ
    RDB$DESCRIPTION                 <null>
    RDB$SYSTEM_FLAG                 1
    RDB$DEFAULT_VALUE               <null>
    RDB$DEFAULT_SOURCE              <null>
    RDB$COLLATION_ID                <null>
    RDB$NULL_FLAG                   1
    RDB$PARAMETER_MECHANISM         0
    RDB$FIELD_NAME                  <null>
    RDB$RELATION_NAME               <null>
    RDB$PACKAGE_NAME                RDB$TIME_ZONE_UTIL

    RDB$PARAMETER_NAME              RDB$ZONE_OFFSET
    RDB$PROCEDURE_NAME              TRANSITIONS
    RDB$PARAMETER_NUMBER            2
    RDB$PARAMETER_TYPE              1
    RDB$FIELD_SOURCE                RDB$TIME_ZONE_OFFSET
    RDB$DESCRIPTION                 <null>
    RDB$SYSTEM_FLAG                 1
    RDB$DEFAULT_VALUE               <null>
    RDB$DEFAULT_SOURCE              <null>
    RDB$COLLATION_ID                <null>
    RDB$NULL_FLAG                   1
    RDB$PARAMETER_MECHANISM         0
    RDB$FIELD_NAME                  <null>
    RDB$RELATION_NAME               <null>
    RDB$PACKAGE_NAME                RDB$TIME_ZONE_UTIL

    Records affected: 8
"""

@pytest.mark.version('>=4.0,<5.0')
def test_2(act: Action):
    act.expected_stdout = expected_stdout_2
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

# version: 5.0

test_script = """
    set blob all;
    set list on;
    set count on;
    select *
    from rdb$procedure_parameters
    order by rdb$procedure_name,rdb$parameter_name,rdb$parameter_number;
"""

act_2 = isql_act('db', test_script)

expected_stdout_3 = """
    RDB$PARAMETER_NAME              ATTACHMENT_ID                                                                                                                                                                                                                                               
    RDB$PROCEDURE_NAME              CANCEL_SESSION                                                                                                                                                                                                                                              
    RDB$PARAMETER_NUMBER            0
    RDB$PARAMETER_TYPE              0
    RDB$FIELD_SOURCE                RDB$ATTACHMENT_ID                                                                                                                                                                                                                                           
    RDB$DESCRIPTION                 <null>
    RDB$SYSTEM_FLAG                 1
    RDB$DEFAULT_VALUE               1b:1e0
            	blr_version5,
            	blr_internal_info,
            	   blr_literal, blr_long, 0, 1,0,0,0,
            	blr_eoc

    RDB$DEFAULT_SOURCE              1b:1e1
    default current_connection
    RDB$COLLATION_ID                <null>
    RDB$NULL_FLAG                   1
    RDB$PARAMETER_MECHANISM         0
    RDB$FIELD_NAME                  <null>
    RDB$RELATION_NAME               <null>
    RDB$PACKAGE_NAME                RDB$PROFILER                                                                                                                                                                                                                                                

    RDB$PARAMETER_NAME              ATTACHMENT_ID                                                                                                                                                                                                                                               
    RDB$PROCEDURE_NAME              DISCARD                                                                                                                                                                                                                                                     
    RDB$PARAMETER_NUMBER            0
    RDB$PARAMETER_TYPE              0
    RDB$FIELD_SOURCE                RDB$ATTACHMENT_ID                                                                                                                                                                                                                                           
    RDB$DESCRIPTION                 <null>
    RDB$SYSTEM_FLAG                 1
    RDB$DEFAULT_VALUE               1b:1e2
            	blr_version5,
            	blr_internal_info,
            	   blr_literal, blr_long, 0, 1,0,0,0,
            	blr_eoc

    RDB$DEFAULT_SOURCE              1b:1e3
    default current_connection
    RDB$COLLATION_ID                <null>
    RDB$NULL_FLAG                   1
    RDB$PARAMETER_MECHANISM         0
    RDB$FIELD_NAME                  <null>
    RDB$RELATION_NAME               <null>
    RDB$PACKAGE_NAME                RDB$PROFILER                                                                                                                                                                                                                                                

    RDB$PARAMETER_NAME              ATTACHMENT_ID                                                                                                                                                                                                                                               
    RDB$PROCEDURE_NAME              FINISH_SESSION                                                                                                                                                                                                                                              
    RDB$PARAMETER_NUMBER            1
    RDB$PARAMETER_TYPE              0
    RDB$FIELD_SOURCE                RDB$ATTACHMENT_ID                                                                                                                                                                                                                                           
    RDB$DESCRIPTION                 <null>
    RDB$SYSTEM_FLAG                 1
    RDB$DEFAULT_VALUE               1b:1e6
            	blr_version5,
            	blr_internal_info,
            	   blr_literal, blr_long, 0, 1,0,0,0,
            	blr_eoc

    RDB$DEFAULT_SOURCE              1b:1e7
    default current_connection
    RDB$COLLATION_ID                <null>
    RDB$NULL_FLAG                   1
    RDB$PARAMETER_MECHANISM         0
    RDB$FIELD_NAME                  <null>
    RDB$RELATION_NAME               <null>
    RDB$PACKAGE_NAME                RDB$PROFILER                                                                                                                                                                                                                                                

    RDB$PARAMETER_NAME              FLUSH                                                                                                                                                                                                                                                       
    RDB$PROCEDURE_NAME              FINISH_SESSION                                                                                                                                                                                                                                              
    RDB$PARAMETER_NUMBER            0
    RDB$PARAMETER_TYPE              0
    RDB$FIELD_SOURCE                RDB$BOOLEAN                                                                                                                                                                                                                                                 
    RDB$DESCRIPTION                 <null>
    RDB$SYSTEM_FLAG                 1
    RDB$DEFAULT_VALUE               1b:1e4
            	blr_version5,
            	blr_literal, blr_bool, 1,
            	blr_eoc

    RDB$DEFAULT_SOURCE              1b:1e5
    default true
    RDB$COLLATION_ID                <null>
    RDB$NULL_FLAG                   1
    RDB$PARAMETER_MECHANISM         0
    RDB$FIELD_NAME                  <null>
    RDB$RELATION_NAME               <null>
    RDB$PACKAGE_NAME                RDB$PROFILER                                                                                                                                                                                                                                                

    RDB$PARAMETER_NAME              ATTACHMENT_ID                                                                                                                                                                                                                                               
    RDB$PROCEDURE_NAME              FLUSH                                                                                                                                                                                                                                                       
    RDB$PARAMETER_NUMBER            0
    RDB$PARAMETER_TYPE              0
    RDB$FIELD_SOURCE                RDB$ATTACHMENT_ID                                                                                                                                                                                                                                           
    RDB$DESCRIPTION                 <null>
    RDB$SYSTEM_FLAG                 1
    RDB$DEFAULT_VALUE               1b:1e8
            	blr_version5,
            	blr_internal_info,
            	   blr_literal, blr_long, 0, 1,0,0,0,
            	blr_eoc

    RDB$DEFAULT_SOURCE              1b:1e9
    default current_connection
    RDB$COLLATION_ID                <null>
    RDB$NULL_FLAG                   1
    RDB$PARAMETER_MECHANISM         0
    RDB$FIELD_NAME                  <null>
    RDB$RELATION_NAME               <null>
    RDB$PACKAGE_NAME                RDB$PROFILER                                                                                                                                                                                                                                                

    RDB$PARAMETER_NAME              ATTACHMENT_ID                                                                                                                                                                                                                                               
    RDB$PROCEDURE_NAME              PAUSE_SESSION                                                                                                                                                                                                                                               
    RDB$PARAMETER_NUMBER            1
    RDB$PARAMETER_TYPE              0
    RDB$FIELD_SOURCE                RDB$ATTACHMENT_ID                                                                                                                                                                                                                                           
    RDB$DESCRIPTION                 <null>
    RDB$SYSTEM_FLAG                 1
    RDB$DEFAULT_VALUE               1b:1ec
            	blr_version5,
            	blr_internal_info,
            	   blr_literal, blr_long, 0, 1,0,0,0,
            	blr_eoc

    RDB$DEFAULT_SOURCE              1b:1ed
    default current_connection
    RDB$COLLATION_ID                <null>
    RDB$NULL_FLAG                   1
    RDB$PARAMETER_MECHANISM         0
    RDB$FIELD_NAME                  <null>
    RDB$RELATION_NAME               <null>
    RDB$PACKAGE_NAME                RDB$PROFILER                                                                                                                                                                                                                                                

    RDB$PARAMETER_NAME              FLUSH                                                                                                                                                                                                                                                       
    RDB$PROCEDURE_NAME              PAUSE_SESSION                                                                                                                                                                                                                                               
    RDB$PARAMETER_NUMBER            0
    RDB$PARAMETER_TYPE              0
    RDB$FIELD_SOURCE                RDB$BOOLEAN                                                                                                                                                                                                                                                 
    RDB$DESCRIPTION                 <null>
    RDB$SYSTEM_FLAG                 1
    RDB$DEFAULT_VALUE               1b:1ea
            	blr_version5,
            	blr_literal, blr_bool, 0,
            	blr_eoc

    RDB$DEFAULT_SOURCE              1b:1eb
    default false
    RDB$COLLATION_ID                <null>
    RDB$NULL_FLAG                   1
    RDB$PARAMETER_MECHANISM         0
    RDB$FIELD_NAME                  <null>
    RDB$RELATION_NAME               <null>
    RDB$PACKAGE_NAME                RDB$PROFILER                                                                                                                                                                                                                                                

    RDB$PARAMETER_NAME              ATTACHMENT_ID                                                                                                                                                                                                                                               
    RDB$PROCEDURE_NAME              RESUME_SESSION                                                                                                                                                                                                                                              
    RDB$PARAMETER_NUMBER            0
    RDB$PARAMETER_TYPE              0
    RDB$FIELD_SOURCE                RDB$ATTACHMENT_ID                                                                                                                                                                                                                                           
    RDB$DESCRIPTION                 <null>
    RDB$SYSTEM_FLAG                 1
    RDB$DEFAULT_VALUE               1b:1ee
            	blr_version5,
            	blr_internal_info,
            	   blr_literal, blr_long, 0, 1,0,0,0,
            	blr_eoc

    RDB$DEFAULT_SOURCE              1b:1ef
    default current_connection
    RDB$COLLATION_ID                <null>
    RDB$NULL_FLAG                   1
    RDB$PARAMETER_MECHANISM         0
    RDB$FIELD_NAME                  <null>
    RDB$RELATION_NAME               <null>
    RDB$PACKAGE_NAME                RDB$PROFILER                                                                                                                                                                                                                                                

    RDB$PARAMETER_NAME              ATTACHMENT_ID                                                                                                                                                                                                                                               
    RDB$PROCEDURE_NAME              SET_FLUSH_INTERVAL                                                                                                                                                                                                                                          
    RDB$PARAMETER_NUMBER            1
    RDB$PARAMETER_TYPE              0
    RDB$FIELD_SOURCE                RDB$ATTACHMENT_ID                                                                                                                                                                                                                                           
    RDB$DESCRIPTION                 <null>
    RDB$SYSTEM_FLAG                 1
    RDB$DEFAULT_VALUE               1b:1f0
            	blr_version5,
            	blr_internal_info,
            	   blr_literal, blr_long, 0, 1,0,0,0,
            	blr_eoc

    RDB$DEFAULT_SOURCE              1b:1f1
    default current_connection
    RDB$COLLATION_ID                <null>
    RDB$NULL_FLAG                   1
    RDB$PARAMETER_MECHANISM         0
    RDB$FIELD_NAME                  <null>
    RDB$RELATION_NAME               <null>
    RDB$PACKAGE_NAME                RDB$PROFILER                                                                                                                                                                                                                                                

    RDB$PARAMETER_NAME              FLUSH_INTERVAL                                                                                                                                                                                                                                              
    RDB$PROCEDURE_NAME              SET_FLUSH_INTERVAL                                                                                                                                                                                                                                          
    RDB$PARAMETER_NUMBER            0
    RDB$PARAMETER_TYPE              0
    RDB$FIELD_SOURCE                RDB$SECONDS_INTERVAL                                                                                                                                                                                                                                        
    RDB$DESCRIPTION                 <null>
    RDB$SYSTEM_FLAG                 1
    RDB$DEFAULT_VALUE               <null>
    RDB$DEFAULT_SOURCE              <null>
    RDB$COLLATION_ID                <null>
    RDB$NULL_FLAG                   1
    RDB$PARAMETER_MECHANISM         0
    RDB$FIELD_NAME                  <null>
    RDB$RELATION_NAME               <null>
    RDB$PACKAGE_NAME                RDB$PROFILER                                                                                                                                                                                                                                                

    RDB$PARAMETER_NAME              RDB$DST_OFFSET                                                                                                                                                                                                                                              
    RDB$PROCEDURE_NAME              TRANSITIONS                                                                                                                                                                                                                                                 
    RDB$PARAMETER_NUMBER            3
    RDB$PARAMETER_TYPE              1
    RDB$FIELD_SOURCE                RDB$TIME_ZONE_OFFSET                                                                                                                                                                                                                                        
    RDB$DESCRIPTION                 <null>
    RDB$SYSTEM_FLAG                 1
    RDB$DEFAULT_VALUE               <null>
    RDB$DEFAULT_SOURCE              <null>
    RDB$COLLATION_ID                <null>
    RDB$NULL_FLAG                   1
    RDB$PARAMETER_MECHANISM         0
    RDB$FIELD_NAME                  <null>
    RDB$RELATION_NAME               <null>
    RDB$PACKAGE_NAME                RDB$TIME_ZONE_UTIL                                                                                                                                                                                                                                          

    RDB$PARAMETER_NAME              RDB$EFFECTIVE_OFFSET                                                                                                                                                                                                                                        
    RDB$PROCEDURE_NAME              TRANSITIONS                                                                                                                                                                                                                                                 
    RDB$PARAMETER_NUMBER            4
    RDB$PARAMETER_TYPE              1
    RDB$FIELD_SOURCE                RDB$TIME_ZONE_OFFSET                                                                                                                                                                                                                                        
    RDB$DESCRIPTION                 <null>
    RDB$SYSTEM_FLAG                 1
    RDB$DEFAULT_VALUE               <null>
    RDB$DEFAULT_SOURCE              <null>
    RDB$COLLATION_ID                <null>
    RDB$NULL_FLAG                   1
    RDB$PARAMETER_MECHANISM         0
    RDB$FIELD_NAME                  <null>
    RDB$RELATION_NAME               <null>
    RDB$PACKAGE_NAME                RDB$TIME_ZONE_UTIL                                                                                                                                                                                                                                          

    RDB$PARAMETER_NAME              RDB$END_TIMESTAMP                                                                                                                                                                                                                                           
    RDB$PROCEDURE_NAME              TRANSITIONS                                                                                                                                                                                                                                                 
    RDB$PARAMETER_NUMBER            1
    RDB$PARAMETER_TYPE              1
    RDB$FIELD_SOURCE                RDB$TIMESTAMP_TZ                                                                                                                                                                                                                                            
    RDB$DESCRIPTION                 <null>
    RDB$SYSTEM_FLAG                 1
    RDB$DEFAULT_VALUE               <null>
    RDB$DEFAULT_SOURCE              <null>
    RDB$COLLATION_ID                <null>
    RDB$NULL_FLAG                   1
    RDB$PARAMETER_MECHANISM         0
    RDB$FIELD_NAME                  <null>
    RDB$RELATION_NAME               <null>
    RDB$PACKAGE_NAME                RDB$TIME_ZONE_UTIL                                                                                                                                                                                                                                          

    RDB$PARAMETER_NAME              RDB$FROM_TIMESTAMP                                                                                                                                                                                                                                          
    RDB$PROCEDURE_NAME              TRANSITIONS                                                                                                                                                                                                                                                 
    RDB$PARAMETER_NUMBER            1
    RDB$PARAMETER_TYPE              0
    RDB$FIELD_SOURCE                RDB$TIMESTAMP_TZ                                                                                                                                                                                                                                            
    RDB$DESCRIPTION                 <null>
    RDB$SYSTEM_FLAG                 1
    RDB$DEFAULT_VALUE               <null>
    RDB$DEFAULT_SOURCE              <null>
    RDB$COLLATION_ID                <null>
    RDB$NULL_FLAG                   1
    RDB$PARAMETER_MECHANISM         0
    RDB$FIELD_NAME                  <null>
    RDB$RELATION_NAME               <null>
    RDB$PACKAGE_NAME                RDB$TIME_ZONE_UTIL                                                                                                                                                                                                                                          

    RDB$PARAMETER_NAME              RDB$START_TIMESTAMP                                                                                                                                                                                                                                         
    RDB$PROCEDURE_NAME              TRANSITIONS                                                                                                                                                                                                                                                 
    RDB$PARAMETER_NUMBER            0
    RDB$PARAMETER_TYPE              1
    RDB$FIELD_SOURCE                RDB$TIMESTAMP_TZ                                                                                                                                                                                                                                            
    RDB$DESCRIPTION                 <null>
    RDB$SYSTEM_FLAG                 1
    RDB$DEFAULT_VALUE               <null>
    RDB$DEFAULT_SOURCE              <null>
    RDB$COLLATION_ID                <null>
    RDB$NULL_FLAG                   1
    RDB$PARAMETER_MECHANISM         0
    RDB$FIELD_NAME                  <null>
    RDB$RELATION_NAME               <null>
    RDB$PACKAGE_NAME                RDB$TIME_ZONE_UTIL                                                                                                                                                                                                                                          

    RDB$PARAMETER_NAME              RDB$TIME_ZONE_NAME                                                                                                                                                                                                                                          
    RDB$PROCEDURE_NAME              TRANSITIONS                                                                                                                                                                                                                                                 
    RDB$PARAMETER_NUMBER            0
    RDB$PARAMETER_TYPE              0
    RDB$FIELD_SOURCE                RDB$TIME_ZONE_NAME                                                                                                                                                                                                                                          
    RDB$DESCRIPTION                 <null>
    RDB$SYSTEM_FLAG                 1
    RDB$DEFAULT_VALUE               <null>
    RDB$DEFAULT_SOURCE              <null>
    RDB$COLLATION_ID                <null>
    RDB$NULL_FLAG                   1
    RDB$PARAMETER_MECHANISM         0
    RDB$FIELD_NAME                  <null>
    RDB$RELATION_NAME               <null>
    RDB$PACKAGE_NAME                RDB$TIME_ZONE_UTIL                                                                                                                                                                                                                                          

    RDB$PARAMETER_NAME              RDB$TO_TIMESTAMP                                                                                                                                                                                                                                            
    RDB$PROCEDURE_NAME              TRANSITIONS                                                                                                                                                                                                                                                 
    RDB$PARAMETER_NUMBER            2
    RDB$PARAMETER_TYPE              0
    RDB$FIELD_SOURCE                RDB$TIMESTAMP_TZ                                                                                                                                                                                                                                            
    RDB$DESCRIPTION                 <null>
    RDB$SYSTEM_FLAG                 1
    RDB$DEFAULT_VALUE               <null>
    RDB$DEFAULT_SOURCE              <null>
    RDB$COLLATION_ID                <null>
    RDB$NULL_FLAG                   1
    RDB$PARAMETER_MECHANISM         0
    RDB$FIELD_NAME                  <null>
    RDB$RELATION_NAME               <null>
    RDB$PACKAGE_NAME                RDB$TIME_ZONE_UTIL                                                                                                                                                                                                                                          

    RDB$PARAMETER_NAME              RDB$ZONE_OFFSET                                                                                                                                                                                                                                             
    RDB$PROCEDURE_NAME              TRANSITIONS                                                                                                                                                                                                                                                 
    RDB$PARAMETER_NUMBER            2
    RDB$PARAMETER_TYPE              1
    RDB$FIELD_SOURCE                RDB$TIME_ZONE_OFFSET                                                                                                                                                                                                                                        
    RDB$DESCRIPTION                 <null>
    RDB$SYSTEM_FLAG                 1
    RDB$DEFAULT_VALUE               <null>
    RDB$DEFAULT_SOURCE              <null>
    RDB$COLLATION_ID                <null>
    RDB$NULL_FLAG                   1
    RDB$PARAMETER_MECHANISM         0
    RDB$FIELD_NAME                  <null>
    RDB$RELATION_NAME               <null>
    RDB$PACKAGE_NAME                RDB$TIME_ZONE_UTIL                                                                                                                                                                                                                                          


    Records affected: 18
"""

@pytest.mark.version('>=5.0')
def test_3(act_2: Action):
    act_2.expected_stdout = expected_stdout_3
    act_2.execute()
    assert act_2.clean_stdout == act_2.clean_expected_stdout
