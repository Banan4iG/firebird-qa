#coding:utf-8

"""
ID:          new-database-11
TITLE:       New DB - RDB$FUNCTION_ARGUMENTS
DESCRIPTION: Check for correct content of RDB$FUNCTION_ARGUMENTS in a new database.
FBTEST:      functional.basic.db.11
NOTES:
[17.01.2023] pzotov
    DISABLED after discussion with dimitr, letters 17-sep-2022 11:23.
    Reasons:
        * There is no much sense to keep such tests because they fails extremely often during new major FB developing.
        * There is no chanse to get successful outcome for the whole test suite is some of system table became invalid,
          i.e. lot of other tests will be failed in such case.
    Single test for check DDL (type of columns, their order and total number) will be implemented for all RDB-tables.
"""

import pytest
from firebird.qa import *
db = db_factory()

test_script = """
    set list on;
    set count on;
    select *
    from rdb$function_arguments fa
    order by fa.rdb$function_name, fa.rdb$argument_position;
"""

act = isql_act('db', test_script)

# version: 3.0

expected_stdout_1 = """
    Records affected: 0
"""

@pytest.mark.version('>=3.0,<4.0')
@pytest.mark.skip("DISABLED: see notes")
def test_1(act: Action):
    act.expected_stdout = expected_stdout_1
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

# version: 4.0

expected_stdout_2 = """
    RDB$FUNCTION_NAME               DATABASE_VERSION
    RDB$ARGUMENT_POSITION           0
    RDB$MECHANISM                   <null>
    RDB$FIELD_TYPE                  <null>
    RDB$FIELD_SCALE                 <null>
    RDB$FIELD_LENGTH                <null>
    RDB$FIELD_SUB_TYPE              <null>
    RDB$CHARACTER_SET_ID            <null>
    RDB$FIELD_PRECISION             <null>
    RDB$CHARACTER_LENGTH            <null>
    RDB$PACKAGE_NAME                RDB$TIME_ZONE_UTIL
    RDB$ARGUMENT_NAME               <null>
    RDB$FIELD_SOURCE                RDB$DBTZ_VERSION
    RDB$DEFAULT_VALUE               <null>
    RDB$DEFAULT_SOURCE              <null>
    RDB$COLLATION_ID                <null>
    RDB$NULL_FLAG                   1
    RDB$ARGUMENT_MECHANISM          <null>
    RDB$FIELD_NAME                  <null>
    RDB$RELATION_NAME               <null>
    RDB$SYSTEM_FLAG                 1
    RDB$DESCRIPTION                 <null>

    Records affected: 1
"""

@pytest.mark.version('>=4.0,<5.0')
@pytest.mark.skip("DISABLED: see notes")
def test_2(act: Action):
    act.expected_stdout = expected_stdout_2
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

# version: 5.0

expected_stdout_3 = """
    RDB$FUNCTION_NAME               DATABASE_VERSION                                                                                                                                                                                                                                            
    RDB$ARGUMENT_POSITION           0
    RDB$MECHANISM                   <null>
    RDB$FIELD_TYPE                  <null>
    RDB$FIELD_SCALE                 <null>
    RDB$FIELD_LENGTH                <null>
    RDB$FIELD_SUB_TYPE              <null>
    RDB$CHARACTER_SET_ID            <null>
    RDB$FIELD_PRECISION             <null>
    RDB$CHARACTER_LENGTH            <null>
    RDB$PACKAGE_NAME                RDB$TIME_ZONE_UTIL                                                                                                                                                                                                                                          
    RDB$ARGUMENT_NAME               <null>
    RDB$FIELD_SOURCE                RDB$DBTZ_VERSION                                                                                                                                                                                                                                            
    RDB$DEFAULT_VALUE               <null>
    RDB$DEFAULT_SOURCE              <null>
    RDB$COLLATION_ID                <null>
    RDB$NULL_FLAG                   1
    RDB$ARGUMENT_MECHANISM          <null>
    RDB$FIELD_NAME                  <null>
    RDB$RELATION_NAME               <null>
    RDB$SYSTEM_FLAG                 1
    RDB$DESCRIPTION                 <null>

    RDB$FUNCTION_NAME               START_SESSION                                                                                                                                                                                                                                               
    RDB$ARGUMENT_POSITION           0
    RDB$MECHANISM                   <null>
    RDB$FIELD_TYPE                  <null>
    RDB$FIELD_SCALE                 <null>
    RDB$FIELD_LENGTH                <null>
    RDB$FIELD_SUB_TYPE              <null>
    RDB$CHARACTER_SET_ID            <null>
    RDB$FIELD_PRECISION             <null>
    RDB$CHARACTER_LENGTH            <null>
    RDB$PACKAGE_NAME                RDB$PROFILER                                                                                                                                                                                                                                                
    RDB$ARGUMENT_NAME               <null>
    RDB$FIELD_SOURCE                RDB$PROFILE_SESSION_ID                                                                                                                                                                                                                                      
    RDB$DEFAULT_VALUE               <null>
    RDB$DEFAULT_SOURCE              <null>
    RDB$COLLATION_ID                <null>
    RDB$NULL_FLAG                   1
    RDB$ARGUMENT_MECHANISM          <null>
    RDB$FIELD_NAME                  <null>
    RDB$RELATION_NAME               <null>
    RDB$SYSTEM_FLAG                 1
    RDB$DESCRIPTION                 <null>

    RDB$FUNCTION_NAME               START_SESSION                                                                                                                                                                                                                                               
    RDB$ARGUMENT_POSITION           1
    RDB$MECHANISM                   <null>
    RDB$FIELD_TYPE                  <null>
    RDB$FIELD_SCALE                 <null>
    RDB$FIELD_LENGTH                <null>
    RDB$FIELD_SUB_TYPE              <null>
    RDB$CHARACTER_SET_ID            <null>
    RDB$FIELD_PRECISION             <null>
    RDB$CHARACTER_LENGTH            <null>
    RDB$PACKAGE_NAME                RDB$PROFILER                                                                                                                                                                                                                                                
    RDB$ARGUMENT_NAME               DESCRIPTION                                                                                                                                                                                                                                                 
    RDB$FIELD_SOURCE                RDB$SHORT_DESCRIPTION                                                                                                                                                                                                                                       
    RDB$DEFAULT_VALUE               f:1e0
    BLOB display set to subtype 1. This BLOB: subtype = 2
    RDB$DEFAULT_SOURCE              f:1e1
    default null
    RDB$COLLATION_ID                <null>
    RDB$NULL_FLAG                   0
    RDB$ARGUMENT_MECHANISM          <null>
    RDB$FIELD_NAME                  <null>
    RDB$RELATION_NAME               <null>
    RDB$SYSTEM_FLAG                 1
    RDB$DESCRIPTION                 <null>

    RDB$FUNCTION_NAME               START_SESSION                                                                                                                                                                                                                                               
    RDB$ARGUMENT_POSITION           2
    RDB$MECHANISM                   <null>
    RDB$FIELD_TYPE                  <null>
    RDB$FIELD_SCALE                 <null>
    RDB$FIELD_LENGTH                <null>
    RDB$FIELD_SUB_TYPE              <null>
    RDB$CHARACTER_SET_ID            <null>
    RDB$FIELD_PRECISION             <null>
    RDB$CHARACTER_LENGTH            <null>
    RDB$PACKAGE_NAME                RDB$PROFILER                                                                                                                                                                                                                                                
    RDB$ARGUMENT_NAME               FLUSH_INTERVAL                                                                                                                                                                                                                                              
    RDB$FIELD_SOURCE                RDB$SECONDS_INTERVAL                                                                                                                                                                                                                                        
    RDB$DEFAULT_VALUE               f:1e2
    BLOB display set to subtype 1. This BLOB: subtype = 2
    RDB$DEFAULT_SOURCE              f:1e3
    default null
    RDB$COLLATION_ID                <null>
    RDB$NULL_FLAG                   0
    RDB$ARGUMENT_MECHANISM          <null>
    RDB$FIELD_NAME                  <null>
    RDB$RELATION_NAME               <null>
    RDB$SYSTEM_FLAG                 1
    RDB$DESCRIPTION                 <null>

    RDB$FUNCTION_NAME               START_SESSION                                                                                                                                                                                                                                               
    RDB$ARGUMENT_POSITION           3
    RDB$MECHANISM                   <null>
    RDB$FIELD_TYPE                  <null>
    RDB$FIELD_SCALE                 <null>
    RDB$FIELD_LENGTH                <null>
    RDB$FIELD_SUB_TYPE              <null>
    RDB$CHARACTER_SET_ID            <null>
    RDB$FIELD_PRECISION             <null>
    RDB$CHARACTER_LENGTH            <null>
    RDB$PACKAGE_NAME                RDB$PROFILER                                                                                                                                                                                                                                                
    RDB$ARGUMENT_NAME               ATTACHMENT_ID                                                                                                                                                                                                                                               
    RDB$FIELD_SOURCE                RDB$ATTACHMENT_ID                                                                                                                                                                                                                                           
    RDB$DEFAULT_VALUE               f:1e4
    BLOB display set to subtype 1. This BLOB: subtype = 2
    RDB$DEFAULT_SOURCE              f:1e5
    default current_connection
    RDB$COLLATION_ID                <null>
    RDB$NULL_FLAG                   1
    RDB$ARGUMENT_MECHANISM          <null>
    RDB$FIELD_NAME                  <null>
    RDB$RELATION_NAME               <null>
    RDB$SYSTEM_FLAG                 1
    RDB$DESCRIPTION                 <null>

    RDB$FUNCTION_NAME               START_SESSION                                                                                                                                                                                                                                               
    RDB$ARGUMENT_POSITION           4
    RDB$MECHANISM                   <null>
    RDB$FIELD_TYPE                  <null>
    RDB$FIELD_SCALE                 <null>
    RDB$FIELD_LENGTH                <null>
    RDB$FIELD_SUB_TYPE              <null>
    RDB$CHARACTER_SET_ID            <null>
    RDB$FIELD_PRECISION             <null>
    RDB$CHARACTER_LENGTH            <null>
    RDB$PACKAGE_NAME                RDB$PROFILER                                                                                                                                                                                                                                                
    RDB$ARGUMENT_NAME               PLUGIN_NAME                                                                                                                                                                                                                                                 
    RDB$FIELD_SOURCE                RDB$FILE_NAME2                                                                                                                                                                                                                                              
    RDB$DEFAULT_VALUE               f:1e6
    BLOB display set to subtype 1. This BLOB: subtype = 2
    RDB$DEFAULT_SOURCE              f:1e7
    default null
    RDB$COLLATION_ID                <null>
    RDB$NULL_FLAG                   0
    RDB$ARGUMENT_MECHANISM          <null>
    RDB$FIELD_NAME                  <null>
    RDB$RELATION_NAME               <null>
    RDB$SYSTEM_FLAG                 1
    RDB$DESCRIPTION                 <null>

    RDB$FUNCTION_NAME               START_SESSION                                                                                                                                                                                                                                               
    RDB$ARGUMENT_POSITION           5
    RDB$MECHANISM                   <null>
    RDB$FIELD_TYPE                  <null>
    RDB$FIELD_SCALE                 <null>
    RDB$FIELD_LENGTH                <null>
    RDB$FIELD_SUB_TYPE              <null>
    RDB$CHARACTER_SET_ID            <null>
    RDB$FIELD_PRECISION             <null>
    RDB$CHARACTER_LENGTH            <null>
    RDB$PACKAGE_NAME                RDB$PROFILER                                                                                                                                                                                                                                                
    RDB$ARGUMENT_NAME               PLUGIN_OPTIONS                                                                                                                                                                                                                                              
    RDB$FIELD_SOURCE                RDB$SHORT_DESCRIPTION                                                                                                                                                                                                                                       
    RDB$DEFAULT_VALUE               f:1e8
    BLOB display set to subtype 1. This BLOB: subtype = 2
    RDB$DEFAULT_SOURCE              f:1e9
    default null
    RDB$COLLATION_ID                <null>
    RDB$NULL_FLAG                   0
    RDB$ARGUMENT_MECHANISM          <null>
    RDB$FIELD_NAME                  <null>
    RDB$RELATION_NAME               <null>
    RDB$SYSTEM_FLAG                 1
    RDB$DESCRIPTION                 <null>


    Records affected: 7
"""

@pytest.mark.version('>=5.0')
@pytest.mark.skip("DISABLED: see notes")
def test_3(act: Action):
    act.expected_stdout = expected_stdout_3
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
