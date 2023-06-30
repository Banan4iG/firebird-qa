#coding:utf-8

"""
ID:          java.esp.misc.entrypoint-mapping
TITLE:       Restore backup from rdb26 with mapping file
DESCRIPTION: 
FBTEST:      functional.java.esp.misc.entrypoint_mapping
"""

import pytest
from firebird.qa import *
from pathlib import Path

substitutions = [('SQL>', ''), ("Database:  '.*', User: .*[\\s$]", ''), ('gbak:Skipped.*', '')]
db = db_factory(do_not_create=True)
act = python_act('db', substitutions=substitutions)

mapping_file = temp_file('mapping_file')
backup_filename = 'rdb26jespudf.fbk'

expected_stdout_rdb3 = """
gbak:Warning: The "mandatory access" feature is not supported
gbak:Updating entry point "esp.TestInOutParam.intInOut" -> "esp.TestInOutParam.intInOut(int)"
gbak:Updating entry point "esp.TestESP.procWithoutParam" -> "esp.TestESP.procWithoutParam()"
RDB$FUNCTION_NAME               RDB$FUNCTION_TYPE RDB$QUERY_NAME                    RDB$DESCRIPTION RDB$MODULE_NAME                                                                                                                                                                                                                                                 RDB$ENTRYPOINT                                                                                                                                                                                                                                                  RDB$RETURN_ARGUMENT RDB$SYSTEM_FLAG RDB$ENGINE_NAME                 RDB$PACKAGE_NAME                RDB$PRIVATE_FLAG RDB$FUNCTION_SOURCE RDB$FUNCTION_ID  RDB$FUNCTION_BLR RDB$VALID_BLR    RDB$DEBUG_INFO RDB$SECURITY_CLASS              RDB$OWNER_NAME                  RDB$LEGACY_FLAG RDB$DETERMINISTIC_FLAG RDB$SQL_SECURITY
=============================== ================= =============================== ================= =============================================================================== =============================================================================== =================== =============== =============================== =============================== ================ =================== =============== ================= ============= ================= =============================== =============================== =============== ====================== ================
TEST                                            0                                            <null> <null>                                                                                                                                                                                                                                                          esp.TestInOutParam.intInOut(int)                                                                                                                                                                                                                                                  0               0 JAVA                            <null>                                    <null>              <null>               1            <null>        <null>            <null> SQL$428                         SYSDBA                                        1                      0 <null>
RDB$FUNCTION_NAME               RDB$ARGUMENT_POSITION RDB$MECHANISM RDB$FIELD_TYPE RDB$FIELD_SCALE RDB$FIELD_LENGTH RDB$FIELD_SUB_TYPE RDB$CHARACTER_SET_ID RDB$FIELD_PRECISION RDB$CHARACTER_LENGTH RDB$PACKAGE_NAME                RDB$ARGUMENT_NAME               RDB$FIELD_SOURCE                RDB$DEFAULT_VALUE RDB$DEFAULT_SOURCE RDB$COLLATION_ID RDB$NULL_FLAG RDB$ARGUMENT_MECHANISM RDB$FIELD_NAME                  RDB$RELATION_NAME               RDB$SYSTEM_FLAG   RDB$DESCRIPTION
=============================== ===================== ============= ============== =============== ================ ================== ==================== =================== ==================== =============================== =============================== =============================== ================= ================== ================ ============= ====================== =============================== =============================== =============== =================
TEST                                                0             1              8               0                4                  0               <null>                   0               <null> <null>                          <null>                          <null>                                     <null>             <null>           <null>        <null>                      1 <null>                          <null>                                        0            <null>
TEST                                                1             1              8               0                4                  0               <null>                   0               <null> <null>                          <null>                          <null>                                     <null>             <null>           <null>        <null>                      1 <null>                          <null>                                        0            <null>
TEST
============
1
RDB$PROCEDURE_NAME              RDB$PROCEDURE_ID RDB$PROCEDURE_INPUTS RDB$PROCEDURE_OUTPUTS   RDB$DESCRIPTION RDB$PROCEDURE_SOURCE RDB$PROCEDURE_BLR RDB$SECURITY_CLASS              RDB$OWNER_NAME                        RDB$RUNTIME RDB$SYSTEM_FLAG RDB$PROCEDURE_TYPE RDB$VALID_BLR    RDB$DEBUG_INFO RDB$ENGINE_NAME                 RDB$ENTRYPOINT                                                                                                                                                                                                                                                  RDB$PACKAGE_NAME                RDB$PRIVATE_FLAG RDB$SQL_SECURITY
=============================== ================ ==================== ===================== ================= ==================== ================= =============================== =============================== ================= =============== ================== ============= ================= =============================== =============================================================================== =============================== ================ ================
TEST_P                                         1               <null>                     0            <null>               <null>              1a:0 SQL$429                         SYSDBA                                     <null>               0                  2             1              1a:1 JAVA                            esp.TestESP.procWithoutParam()                                                                                                                                                                                                                                  <null>                                    <null> <true>
==============================================================================
RDB$PROCEDURE_BLR:
BLOB display set to subtype 1. This BLOB: subtype = 2
==============================================================================
==============================================================================
RDB$DEBUG_INFO:
BLOB display set to subtype 1. This BLOB: subtype = 9
==============================================================================
"""

expected_stdout_rdb5 = """
gbak:Warning: The "mandatory access" feature is not supported
gbak:Updating entry point "esp.TestInOutParam.intInOut" -> "esp.TestInOutParam.intInOut(int)"
gbak:Updating entry point "esp.TestESP.procWithoutParam" -> "esp.TestESP.procWithoutParam()"
RDB$FUNCTION_NAME                                               RDB$FUNCTION_TYPE RDB$QUERY_NAME                                                    RDB$DESCRIPTION RDB$MODULE_NAME                                                                                                                                                                                                                                                 RDB$ENTRYPOINT                                                                                                                                                                                                                                                  RDB$RETURN_ARGUMENT RDB$SYSTEM_FLAG RDB$ENGINE_NAME                                                 RDB$PACKAGE_NAME                                                RDB$PRIVATE_FLAG RDB$FUNCTION_SOURCE RDB$FUNCTION_ID  RDB$FUNCTION_BLR RDB$VALID_BLR    RDB$DEBUG_INFO RDB$SECURITY_CLASS                                              RDB$OWNER_NAME                                                  RDB$LEGACY_FLAG RDB$DETERMINISTIC_FLAG RDB$SQL_SECURITY
=============================================================== ================= =============================================================== ================= =============================================================================================================================================================================================================================================================== =============================================================================================================================================================================================================================================================== =================== =============== =============================================================== =============================================================== ================ =================== =============== ================= ============= ================= =============================================================== =============================================================== =============== ====================== ================
DATABASE_VERSION                                                           <null> <null>                                                                     <null> <null>                                                                                                                                                                                                                                                          <null>                                                                                                                                                                                                                                                                            0               1 SYSTEM                                                          RDB$TIME_ZONE_UTIL                                                             0              <null>               1            <null>             1            <null> <null>                                                          SYSDBA                                                                   <null>                 <null> <null>
START_SESSION                                                              <null> <null>                                                                     <null> <null>                                                                                                                                                                                                                                                          <null>                                                                                                                                                                                                                                                                            0               1 SYSTEM                                                          RDB$PROFILER                                                                   0              <null>               2            <null>             1            <null> <null>                                                          SYSDBA                                                                   <null>                 <null> <null>

TEST                                                                            0                                                                            <null> <null>                                                                                                                                                                                                                                                          esp.TestInOutParam.intInOut(int)                                                                                                                                                                                                                                                  0               0 JAVA                                                            <null>                                                                    <null>              <null>               3            <null>        <null>            <null> SQL$478                                                         SYSDBA                                                                        1                      0 <null>

RDB$FUNCTION_NAME                                               RDB$ARGUMENT_POSITION RDB$MECHANISM RDB$FIELD_TYPE RDB$FIELD_SCALE RDB$FIELD_LENGTH RDB$FIELD_SUB_TYPE RDB$CHARACTER_SET_ID RDB$FIELD_PRECISION RDB$CHARACTER_LENGTH RDB$PACKAGE_NAME                                                RDB$ARGUMENT_NAME                                               RDB$FIELD_SOURCE                                                RDB$DEFAULT_VALUE RDB$DEFAULT_SOURCE RDB$COLLATION_ID RDB$NULL_FLAG RDB$ARGUMENT_MECHANISM RDB$FIELD_NAME                                                  RDB$RELATION_NAME                                               RDB$SYSTEM_FLAG   RDB$DESCRIPTION
=============================================================== ===================== ============= ============== =============== ================ ================== ==================== =================== ==================== =============================================================== =============================================================== =============================================================== ================= ================== ================ ============= ====================== =============================================================== =============================================================== =============== =================
DATABASE_VERSION                                                                    0        <null>         <null>          <null>           <null>             <null>               <null>              <null>               <null> RDB$TIME_ZONE_UTIL                                              <null>                                                          RDB$DBTZ_VERSION                                                           <null>             <null>           <null>             1                 <null> <null>                                                          <null>                                                                        1            <null>
START_SESSION                                                                       0        <null>         <null>          <null>           <null>             <null>               <null>              <null>               <null> RDB$PROFILER                                                    <null>                                                          RDB$PROFILE_SESSION_ID                                                     <null>             <null>           <null>             1                 <null> <null>                                                          <null>                                                                        1            <null>
START_SESSION                                                                       1        <null>         <null>          <null>           <null>             <null>               <null>              <null>               <null> RDB$PROFILER                                                    DESCRIPTION                                                     RDB$SHORT_DESCRIPTION                                                        f:ef               f:f0           <null>             0                 <null> <null>                                                          <null>                                                                        1            <null>
==============================================================================
RDB$DEFAULT_VALUE:
BLOB display set to subtype 1. This BLOB: subtype = 2
==============================================================================
==============================================================================
RDB$DEFAULT_SOURCE:
default null
==============================================================================
START_SESSION                                                                       2        <null>         <null>          <null>           <null>             <null>               <null>              <null>               <null> RDB$PROFILER                                                    FLUSH_INTERVAL                                                  RDB$SECONDS_INTERVAL                                                         f:f1               f:f2           <null>             0                 <null> <null>                                                          <null>                                                                        1            <null>
==============================================================================
RDB$DEFAULT_VALUE:
BLOB display set to subtype 1. This BLOB: subtype = 2
==============================================================================
==============================================================================
RDB$DEFAULT_SOURCE:
default null
==============================================================================
START_SESSION                                                                       3        <null>         <null>          <null>           <null>             <null>               <null>              <null>               <null> RDB$PROFILER                                                    ATTACHMENT_ID                                                   RDB$ATTACHMENT_ID                                                            f:f3               f:f4           <null>             1                 <null> <null>                                                          <null>                                                                        1            <null>
==============================================================================
RDB$DEFAULT_VALUE:
BLOB display set to subtype 1. This BLOB: subtype = 2
==============================================================================
==============================================================================
RDB$DEFAULT_SOURCE:
default current_connection
==============================================================================
START_SESSION                                                                       4        <null>         <null>          <null>           <null>             <null>               <null>              <null>               <null> RDB$PROFILER                                                    PLUGIN_NAME                                                     RDB$FILE_NAME2                                                               f:f5               f:f6           <null>             0                 <null> <null>                                                          <null>                                                                        1            <null>
==============================================================================
RDB$DEFAULT_VALUE:
BLOB display set to subtype 1. This BLOB: subtype = 2
==============================================================================
==============================================================================
RDB$DEFAULT_SOURCE:
default null
==============================================================================
START_SESSION                                                                       5        <null>         <null>          <null>           <null>             <null>               <null>              <null>               <null> RDB$PROFILER                                                    PLUGIN_OPTIONS                                                  RDB$SHORT_DESCRIPTION                                                        f:f7               f:f8           <null>             0                 <null> <null>                                                          <null>                                                                        1            <null>
==============================================================================
RDB$DEFAULT_VALUE:
BLOB display set to subtype 1. This BLOB: subtype = 2
==============================================================================
==============================================================================
RDB$DEFAULT_SOURCE:
default null
==============================================================================
TEST                                                                                0             1              8               0                4                  0               <null>                   0               <null> <null>                                                          <null>                                                          <null>                                                                     <null>             <null>           <null>        <null>                      1 <null>                                                          <null>                                                                        0            <null>
TEST                                                                                1             1              8               0                4                  0               <null>                   0               <null> <null>                                                          <null>                                                          <null>                                                                     <null>             <null>           <null>        <null>                      1 <null>                                                          <null>                                                                        0            <null>
TEST
============
1
RDB$PROCEDURE_NAME                                              RDB$PROCEDURE_ID RDB$PROCEDURE_INPUTS RDB$PROCEDURE_OUTPUTS   RDB$DESCRIPTION RDB$PROCEDURE_SOURCE RDB$PROCEDURE_BLR RDB$SECURITY_CLASS                                              RDB$OWNER_NAME                                                        RDB$RUNTIME RDB$SYSTEM_FLAG RDB$PROCEDURE_TYPE RDB$VALID_BLR    RDB$DEBUG_INFO RDB$ENGINE_NAME                                                 RDB$ENTRYPOINT                                                                                                                                                                                                                                                  RDB$PACKAGE_NAME                                                RDB$PRIVATE_FLAG RDB$SQL_SECURITY
=============================================================== ================ ==================== ===================== ================= ==================== ================= =============================================================== =============================================================== ================= =============== ================== ============= ================= =============================================================== =============================================================================================================================================================================================================================================================== =============================================================== ================ ================
TRANSITIONS                                                                    1                    3                     5            <null>               <null>            <null> <null>                                                          SYSDBA                                                                     <null>               1                  1             1            <null> SYSTEM                                                          <null>                                                                                                                                                                                                                                                          RDB$TIME_ZONE_UTIL                                                             0 <null>
CANCEL_SESSION                                                                 2                    1                     0            <null>               <null>            <null> <null>                                                          SYSDBA                                                                     <null>               1                  2             1            <null> SYSTEM                                                          <null>                                                                                                                                                                                                                                                          RDB$PROFILER                                                                   0 <null>
DISCARD                                                                        3                    1                     0            <null>               <null>            <null> <null>                                                          SYSDBA                                                                     <null>               1                  2             1            <null> SYSTEM                                                          <null>                                                                                                                                                                                                                                                          RDB$PROFILER                                                                   0 <null>
FINISH_SESSION                                                                 4                    2                     0            <null>               <null>            <null> <null>                                                          SYSDBA                                                                     <null>               1                  2             1            <null> SYSTEM                                                          <null>                                                                                                                                                                                                                                                          RDB$PROFILER                                                                   0 <null>
FLUSH                                                                          5                    1                     0            <null>               <null>            <null> <null>                                                          SYSDBA                                                                     <null>               1                  2             1            <null> SYSTEM                                                          <null>                                                                                                                                                                                                                                                          RDB$PROFILER                                                                   0 <null>
PAUSE_SESSION                                                                  6                    2                     0            <null>               <null>            <null> <null>                                                          SYSDBA                                                                     <null>               1                  2             1            <null> SYSTEM                                                          <null>                                                                                                                                                                                                                                                          RDB$PROFILER                                                                   0 <null>
RESUME_SESSION                                                                 7                    1                     0            <null>               <null>            <null> <null>                                                          SYSDBA                                                                     <null>               1                  2             1            <null> SYSTEM                                                          <null>                                                                                                                                                                                                                                                          RDB$PROFILER                                                                   0 <null>
SET_FLUSH_INTERVAL                                                             8                    2                     0            <null>               <null>            <null> <null>                                                          SYSDBA                                                                     <null>               1                  2             1            <null> SYSTEM                                                          <null>                                                                                                                                                                                                                                                          RDB$PROFILER                                                                   0 <null>

TEST_P                                                                         9               <null>                     0            <null>               <null>             1a:ef SQL$479                                                         SYSDBA                                                                     <null>               0                  2             1             1a:f0 JAVA                                                            esp.TestESP.procWithoutParam()                                                                                                                                                                                                                                  <null>                                                                    <null> <true>

==============================================================================
RDB$PROCEDURE_BLR:
BLOB display set to subtype 1. This BLOB: subtype = 2
==============================================================================
==============================================================================
RDB$DEBUG_INFO:
BLOB display set to subtype 1. This BLOB: subtype = 9
==============================================================================
RDB$PARAMETER_NAME                                              RDB$PROCEDURE_NAME                                              RDB$PARAMETER_NUMBER RDB$PARAMETER_TYPE RDB$FIELD_SOURCE                                                  RDB$DESCRIPTION RDB$SYSTEM_FLAG RDB$DEFAULT_VALUE RDB$DEFAULT_SOURCE RDB$COLLATION_ID RDB$NULL_FLAG RDB$PARAMETER_MECHANISM RDB$FIELD_NAME                                                  RDB$RELATION_NAME                                               RDB$PACKAGE_NAME
=============================================================== =============================================================== ==================== ================== =============================================================== ================= =============== ================= ================== ================ ============= ======================= =============================================================== =============================================================== ===============================================================
RDB$TIME_ZONE_NAME                                              TRANSITIONS                                                                        0                  0 RDB$TIME_ZONE_NAME                                                         <null>               1            <null>             <null>           <null>             1                       0 <null>                                                          <null>                                                          RDB$TIME_ZONE_UTIL
RDB$FROM_TIMESTAMP                                              TRANSITIONS                                                                        1                  0 RDB$TIMESTAMP_TZ                                                           <null>               1            <null>             <null>           <null>             1                       0 <null>                                                          <null>                                                          RDB$TIME_ZONE_UTIL
RDB$TO_TIMESTAMP                                                TRANSITIONS                                                                        2                  0 RDB$TIMESTAMP_TZ                                                           <null>               1            <null>             <null>           <null>             1                       0 <null>                                                          <null>                                                          RDB$TIME_ZONE_UTIL
RDB$START_TIMESTAMP                                             TRANSITIONS                                                                        0                  1 RDB$TIMESTAMP_TZ                                                           <null>               1            <null>             <null>           <null>             1                       0 <null>                                                          <null>                                                          RDB$TIME_ZONE_UTIL
RDB$END_TIMESTAMP                                               TRANSITIONS                                                                        1                  1 RDB$TIMESTAMP_TZ                                                           <null>               1            <null>             <null>           <null>             1                       0 <null>                                                          <null>                                                          RDB$TIME_ZONE_UTIL
RDB$ZONE_OFFSET                                                 TRANSITIONS                                                                        2                  1 RDB$TIME_ZONE_OFFSET                                                       <null>               1            <null>             <null>           <null>             1                       0 <null>                                                          <null>                                                          RDB$TIME_ZONE_UTIL
RDB$DST_OFFSET                                                  TRANSITIONS                                                                        3                  1 RDB$TIME_ZONE_OFFSET                                                       <null>               1            <null>             <null>           <null>             1                       0 <null>                                                          <null>                                                          RDB$TIME_ZONE_UTIL
RDB$EFFECTIVE_OFFSET                                            TRANSITIONS                                                                        4                  1 RDB$TIME_ZONE_OFFSET                                                       <null>               1            <null>             <null>           <null>             1                       0 <null>                                                          <null>                                                          RDB$TIME_ZONE_UTIL
ATTACHMENT_ID                                                   CANCEL_SESSION                                                                     0                  0 RDB$ATTACHMENT_ID                                                          <null>               1             1b:ef              1b:f0           <null>             1                       0 <null>                                                          <null>                                                          RDB$PROFILER
==============================================================================
RDB$DEFAULT_VALUE:
BLOB display set to subtype 1. This BLOB: subtype = 2
==============================================================================
==============================================================================
RDB$DEFAULT_SOURCE:
default current_connection
==============================================================================
ATTACHMENT_ID                                                   DISCARD                                                                            0                  0 RDB$ATTACHMENT_ID                                                          <null>               1             1b:f1              1b:f2           <null>             1                       0 <null>                                                          <null>                                                          RDB$PROFILER
==============================================================================
RDB$DEFAULT_VALUE:
BLOB display set to subtype 1. This BLOB: subtype = 2
==============================================================================
==============================================================================
RDB$DEFAULT_SOURCE:
default current_connection
==============================================================================
FLUSH                                                           FINISH_SESSION                                                                     0                  0 RDB$BOOLEAN                                                                <null>               1             1b:f3              1b:f4           <null>             1                       0 <null>                                                          <null>                                                          RDB$PROFILER
==============================================================================
RDB$DEFAULT_VALUE:
BLOB display set to subtype 1. This BLOB: subtype = 2
==============================================================================
==============================================================================
RDB$DEFAULT_SOURCE:
default true
==============================================================================
ATTACHMENT_ID                                                   FINISH_SESSION                                                                     1                  0 RDB$ATTACHMENT_ID                                                          <null>               1             1b:f5              1b:f6           <null>             1                       0 <null>                                                          <null>                                                          RDB$PROFILER
==============================================================================
RDB$DEFAULT_VALUE:
BLOB display set to subtype 1. This BLOB: subtype = 2
==============================================================================
==============================================================================
RDB$DEFAULT_SOURCE:
default current_connection
==============================================================================
ATTACHMENT_ID                                                   FLUSH                                                                              0                  0 RDB$ATTACHMENT_ID                                                          <null>               1             1b:f7              1b:f8           <null>             1                       0 <null>                                                          <null>                                                          RDB$PROFILER
==============================================================================
RDB$DEFAULT_VALUE:
BLOB display set to subtype 1. This BLOB: subtype = 2
==============================================================================
==============================================================================
RDB$DEFAULT_SOURCE:
default current_connection
==============================================================================
FLUSH                                                           PAUSE_SESSION                                                                      0                  0 RDB$BOOLEAN                                                                <null>               1             1b:f9              1b:fa           <null>             1                       0 <null>                                                          <null>                                                          RDB$PROFILER
==============================================================================
RDB$DEFAULT_VALUE:
BLOB display set to subtype 1. This BLOB: subtype = 2
==============================================================================
==============================================================================
RDB$DEFAULT_SOURCE:
default false
==============================================================================
ATTACHMENT_ID                                                   PAUSE_SESSION                                                                      1                  0 RDB$ATTACHMENT_ID                                                          <null>               1             1b:fb              1b:fc           <null>             1                       0 <null>                                                          <null>                                                          RDB$PROFILER
==============================================================================
RDB$DEFAULT_VALUE:
BLOB display set to subtype 1. This BLOB: subtype = 2
==============================================================================
==============================================================================
RDB$DEFAULT_SOURCE:
default current_connection
==============================================================================
ATTACHMENT_ID                                                   RESUME_SESSION                                                                     0                  0 RDB$ATTACHMENT_ID                                                          <null>               1             1b:fd              1b:fe           <null>             1                       0 <null>                                                          <null>                                                          RDB$PROFILER
==============================================================================
RDB$DEFAULT_VALUE:
BLOB display set to subtype 1. This BLOB: subtype = 2
==============================================================================
==============================================================================
RDB$DEFAULT_SOURCE:
default current_connection
==============================================================================
FLUSH_INTERVAL                                                  SET_FLUSH_INTERVAL                                                                 0                  0 RDB$SECONDS_INTERVAL                                                       <null>               1            <null>             <null>           <null>             1                       0 <null>                                                          <null>                                                          RDB$PROFILER
ATTACHMENT_ID                                                   SET_FLUSH_INTERVAL                                                                 1                  0 RDB$ATTACHMENT_ID                                                          <null>               1             1b:ff             1b:100           <null>             1                       0 <null>                                                          <null>                                                          RDB$PROFILER
==============================================================================
RDB$DEFAULT_VALUE:
BLOB display set to subtype 1. This BLOB: subtype = 2
==============================================================================
==============================================================================
RDB$DEFAULT_SOURCE:
default current_connection
==============================================================================
"""

@pytest.mark.java
@pytest.mark.version('>=3.0')
def test_1(act: Action, mapping_file: Path, capsys):
    mapping="""
        esp.TestInOutParam.intInOut int
    """
    mapping_file.write_text(mapping) 
    backup = act.vars['backups'] / backup_filename
    act.gbak(switches=['-c', str(backup), act.db.dsn])
    
    script = """
        select * from rdb$functions;
        select * from rdb$function_arguments;
        select test(1) from rdb$database;

        select * from rdb$procedures;
        select * from rdb$procedure_parameters;
        drop database;
    """
    act.isql(switches=['-q'], input=script)
    act.expected_stdout = expected_stdout_rdb5 if act.is_version('>=5') else expected_stdout_rdb3
    act.stdout = capsys.readouterr().out
    assert act.clean_stdout == act.clean_expected_stdout

