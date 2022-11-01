#coding:utf-8

"""
ID:          isql-04
ISSUE:       1383
TITLE:       ISQL - SHOW SYSTEM parameters
DESCRIPTION: Extend ISQL SHOW SYSTEM command to accept parameters TABLES, COLLATIONS and FUNCTIONS
FBTEST:      functional.basic.isql.03

NOTES:
[28.04.2022] pzotov
    Checked on 5.0.0.488, 4.0.1.2692, 3.0.8.33535.
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    SHOW SYSTEM TABLES;
    SHOW SYSTEM COLLATIONS;
    SHOW SYSTEM FUNCTIONS;
"""

#E         - CP943C_UNICODE, CHARACTER SET CP943C, PAD SPACE, SYSTEM
#E         + CP943C_UNICODE, CHARACTER SET CP943C, PAD SPACE, 'COLL-VERSION=58.0.6.50', SYSTEM

substitutions = \
    [
        ("'COLL-VERSION=\\d+.\\d+(;ICU-VERSION=\\d+.\\d+)?.*'(, )?", '')
    ]

act = isql_act('db', test_script, substitutions = substitutions)


# version: 3.0

expected_stdout_1 = """
       MON$ATTACHMENTS                        MON$CALL_STACK
       MON$CONTEXT_VARIABLES                  MON$DATABASE
       MON$IO_STATS                           MON$MEMORY_USAGE
       MON$RECORD_STATS                       MON$STATEMENTS
       MON$TABLE_STATS                        MON$TRANSACTIONS
       RDB$AUTH_MAPPING                       RDB$BACKUP_HISTORY
       RDB$CHARACTER_SETS                     RDB$CHECK_CONSTRAINTS
       RDB$COLLATIONS                         RDB$DATABASE
       RDB$DB_CREATORS                        RDB$DEPENDENCIES
       RDB$EXCEPTIONS                         RDB$FIELDS
       RDB$FIELD_DIMENSIONS                   RDB$FILES
       RDB$FILTERS                            RDB$FORMATS
       RDB$FUNCTIONS                          RDB$FUNCTION_ARGUMENTS
       RDB$GENERATORS                         RDB$INDEX_SEGMENTS
       RDB$INDICES                            RDB$LOG_FILES
       RDB$PACKAGES                           RDB$PAGES
       RDB$PROCEDURES                         RDB$PROCEDURE_PARAMETERS
       RDB$REF_CONSTRAINTS                    RDB$RELATIONS
       RDB$RELATION_CONSTRAINTS               RDB$RELATION_FIELDS
       RDB$ROLES                              RDB$SECURITY_CLASSES
       RDB$TRANSACTIONS                       RDB$TRIGGERS
       RDB$TRIGGER_MESSAGES                   RDB$TYPES
       RDB$USER_PRIVILEGES                    RDB$VIEW_RELATIONS
       SEC$DB_CREATORS                        SEC$GLOBAL_AUTH_MAPPING
       SEC$USERS                              SEC$USER_ATTRIBUTES

ASCII, CHARACTER SET ASCII, PAD SPACE, SYSTEM
BIG_5, CHARACTER SET BIG_5, PAD SPACE, SYSTEM
BS_BA, CHARACTER SET WIN1250, PAD SPACE, SYSTEM
CP943C, CHARACTER SET CP943C, PAD SPACE, SYSTEM
CP943C_UNICODE, CHARACTER SET CP943C, PAD SPACE, SYSTEM
CS_CZ, CHARACTER SET ISO8859_2, PAD SPACE, SYSTEM
CYRL, CHARACTER SET CYRL, PAD SPACE, SYSTEM
DA_DA, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
DB_CSY, CHARACTER SET DOS852, PAD SPACE, SYSTEM
DB_DAN865, CHARACTER SET DOS865, PAD SPACE, SYSTEM
DB_DEU437, CHARACTER SET DOS437, PAD SPACE, SYSTEM
DB_DEU850, CHARACTER SET DOS850, PAD SPACE, SYSTEM
DB_ESP437, CHARACTER SET DOS437, PAD SPACE, SYSTEM
DB_ESP850, CHARACTER SET DOS850, PAD SPACE, SYSTEM
DB_FIN437, CHARACTER SET DOS437, PAD SPACE, SYSTEM
DB_FRA437, CHARACTER SET DOS437, PAD SPACE, SYSTEM
DB_FRA850, CHARACTER SET DOS850, PAD SPACE, SYSTEM
DB_FRC850, CHARACTER SET DOS850, PAD SPACE, SYSTEM
DB_FRC863, CHARACTER SET DOS863, PAD SPACE, SYSTEM
DB_ITA437, CHARACTER SET DOS437, PAD SPACE, SYSTEM
DB_ITA850, CHARACTER SET DOS850, PAD SPACE, SYSTEM
DB_NLD437, CHARACTER SET DOS437, PAD SPACE, SYSTEM
DB_NLD850, CHARACTER SET DOS850, PAD SPACE, SYSTEM
DB_NOR865, CHARACTER SET DOS865, PAD SPACE, SYSTEM
DB_PLK, CHARACTER SET DOS852, PAD SPACE, SYSTEM
DB_PTB850, CHARACTER SET DOS850, PAD SPACE, SYSTEM
DB_PTG860, CHARACTER SET DOS860, PAD SPACE, SYSTEM
DB_RUS, CHARACTER SET CYRL, PAD SPACE, SYSTEM
DB_SLO, CHARACTER SET DOS852, PAD SPACE, SYSTEM
DB_SVE437, CHARACTER SET DOS437, PAD SPACE, SYSTEM
DB_SVE850, CHARACTER SET DOS850, PAD SPACE, SYSTEM
DB_TRK, CHARACTER SET DOS857, PAD SPACE, SYSTEM
DB_UK437, CHARACTER SET DOS437, PAD SPACE, SYSTEM
DB_UK850, CHARACTER SET DOS850, PAD SPACE, SYSTEM
DB_US437, CHARACTER SET DOS437, PAD SPACE, SYSTEM
DB_US850, CHARACTER SET DOS850, PAD SPACE, SYSTEM
DE_DE, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
DOS437, CHARACTER SET DOS437, PAD SPACE, SYSTEM
DOS737, CHARACTER SET DOS737, PAD SPACE, SYSTEM
DOS775, CHARACTER SET DOS775, PAD SPACE, SYSTEM
DOS850, CHARACTER SET DOS850, PAD SPACE, SYSTEM
DOS852, CHARACTER SET DOS852, PAD SPACE, SYSTEM
DOS857, CHARACTER SET DOS857, PAD SPACE, SYSTEM
DOS858, CHARACTER SET DOS858, PAD SPACE, SYSTEM
DOS860, CHARACTER SET DOS860, PAD SPACE, SYSTEM
DOS861, CHARACTER SET DOS861, PAD SPACE, SYSTEM
DOS862, CHARACTER SET DOS862, PAD SPACE, SYSTEM
DOS863, CHARACTER SET DOS863, PAD SPACE, SYSTEM
DOS864, CHARACTER SET DOS864, PAD SPACE, SYSTEM
DOS865, CHARACTER SET DOS865, PAD SPACE, SYSTEM
DOS866, CHARACTER SET DOS866, PAD SPACE, SYSTEM
DOS869, CHARACTER SET DOS869, PAD SPACE, SYSTEM
DU_NL, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
EN_UK, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
EN_US, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
ES_ES, CHARACTER SET ISO8859_1, PAD SPACE, 'DISABLE-COMPRESSIONS=1;SPECIALS-FIRST=1', SYSTEM
ES_ES_CI_AI, CHARACTER SET ISO8859_1, PAD SPACE, CASE INSENSITIVE, ACCENT INSENSITIVE, 'DISABLE-COMPRESSIONS=1;SPECIALS-FIRST=1', SYSTEM
EUCJ_0208, CHARACTER SET EUCJ_0208, PAD SPACE, SYSTEM
FI_FI, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
FR_CA, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
FR_CA_CI_AI, CHARACTER SET ISO8859_1, FROM EXTERNAL ('FR_CA'), PAD SPACE, CASE INSENSITIVE, ACCENT INSENSITIVE, 'SPECIALS-FIRST=1', SYSTEM
FR_FR, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
FR_FR_CI_AI, CHARACTER SET ISO8859_1, FROM EXTERNAL ('FR_FR'), PAD SPACE, CASE INSENSITIVE, ACCENT INSENSITIVE, 'SPECIALS-FIRST=1', SYSTEM
GB18030, CHARACTER SET GB18030, PAD SPACE, SYSTEM
GB18030_UNICODE, CHARACTER SET GB18030, PAD SPACE, SYSTEM
GBK, CHARACTER SET GBK, PAD SPACE, SYSTEM
GBK_UNICODE, CHARACTER SET GBK, PAD SPACE, SYSTEM
GB_2312, CHARACTER SET GB_2312, PAD SPACE, SYSTEM
ISO8859_1, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
ISO8859_13, CHARACTER SET ISO8859_13, PAD SPACE, SYSTEM
ISO8859_2, CHARACTER SET ISO8859_2, PAD SPACE, SYSTEM
ISO8859_3, CHARACTER SET ISO8859_3, PAD SPACE, SYSTEM
ISO8859_4, CHARACTER SET ISO8859_4, PAD SPACE, SYSTEM
ISO8859_5, CHARACTER SET ISO8859_5, PAD SPACE, SYSTEM
ISO8859_6, CHARACTER SET ISO8859_6, PAD SPACE, SYSTEM
ISO8859_7, CHARACTER SET ISO8859_7, PAD SPACE, SYSTEM
ISO8859_8, CHARACTER SET ISO8859_8, PAD SPACE, SYSTEM
ISO8859_9, CHARACTER SET ISO8859_9, PAD SPACE, SYSTEM
ISO_HUN, CHARACTER SET ISO8859_2, PAD SPACE, SYSTEM
ISO_PLK, CHARACTER SET ISO8859_2, PAD SPACE, SYSTEM
IS_IS, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
IT_IT, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
KOI8R, CHARACTER SET KOI8R, PAD SPACE, SYSTEM
KOI8R_RU, CHARACTER SET KOI8R, PAD SPACE, SYSTEM
KOI8U, CHARACTER SET KOI8U, PAD SPACE, SYSTEM
KOI8U_UA, CHARACTER SET KOI8U, PAD SPACE, SYSTEM
KSC_5601, CHARACTER SET KSC_5601, PAD SPACE, SYSTEM
KSC_DICTIONARY, CHARACTER SET KSC_5601, PAD SPACE, SYSTEM
LT_LT, CHARACTER SET ISO8859_13, PAD SPACE, SYSTEM
NEXT, CHARACTER SET NEXT, PAD SPACE, SYSTEM
NONE, CHARACTER SET NONE, PAD SPACE, SYSTEM
NO_NO, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
NXT_DEU, CHARACTER SET NEXT, PAD SPACE, SYSTEM
NXT_ESP, CHARACTER SET NEXT, PAD SPACE, SYSTEM
NXT_FRA, CHARACTER SET NEXT, PAD SPACE, SYSTEM
NXT_ITA, CHARACTER SET NEXT, PAD SPACE, SYSTEM
NXT_US, CHARACTER SET NEXT, PAD SPACE, SYSTEM
OCTETS, CHARACTER SET OCTETS, PAD SPACE, SYSTEM
PDOX_ASCII, CHARACTER SET DOS437, PAD SPACE, SYSTEM
PDOX_CSY, CHARACTER SET DOS852, PAD SPACE, SYSTEM
PDOX_CYRL, CHARACTER SET CYRL, PAD SPACE, SYSTEM
PDOX_HUN, CHARACTER SET DOS852, PAD SPACE, SYSTEM
PDOX_INTL, CHARACTER SET DOS437, PAD SPACE, SYSTEM
PDOX_ISL, CHARACTER SET DOS861, PAD SPACE, SYSTEM
PDOX_NORDAN4, CHARACTER SET DOS865, PAD SPACE, SYSTEM
PDOX_PLK, CHARACTER SET DOS852, PAD SPACE, SYSTEM
PDOX_SLO, CHARACTER SET DOS852, PAD SPACE, SYSTEM
PDOX_SWEDFIN, CHARACTER SET DOS437, PAD SPACE, SYSTEM
PT_BR, CHARACTER SET ISO8859_1, PAD SPACE, CASE INSENSITIVE, ACCENT INSENSITIVE, SYSTEM
PT_PT, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
PXW_CSY, CHARACTER SET WIN1250, PAD SPACE, SYSTEM
PXW_CYRL, CHARACTER SET WIN1251, PAD SPACE, SYSTEM
PXW_GREEK, CHARACTER SET WIN1253, PAD SPACE, SYSTEM
PXW_HUN, CHARACTER SET WIN1250, PAD SPACE, SYSTEM
PXW_HUNDC, CHARACTER SET WIN1250, PAD SPACE, SYSTEM
PXW_INTL, CHARACTER SET WIN1252, PAD SPACE, SYSTEM
PXW_INTL850, CHARACTER SET WIN1252, PAD SPACE, SYSTEM
PXW_NORDAN4, CHARACTER SET WIN1252, PAD SPACE, SYSTEM
PXW_PLK, CHARACTER SET WIN1250, PAD SPACE, SYSTEM
PXW_SLOV, CHARACTER SET WIN1250, PAD SPACE, SYSTEM
PXW_SPAN, CHARACTER SET WIN1252, PAD SPACE, SYSTEM
PXW_SWEDFIN, CHARACTER SET WIN1252, PAD SPACE, SYSTEM
PXW_TURK, CHARACTER SET WIN1254, PAD SPACE, SYSTEM
SJIS_0208, CHARACTER SET SJIS_0208, PAD SPACE, SYSTEM
SV_SV, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
TIS620, CHARACTER SET TIS620, PAD SPACE, SYSTEM
TIS620_UNICODE, CHARACTER SET TIS620, PAD SPACE, SYSTEM
UCS_BASIC, CHARACTER SET UTF8, PAD SPACE, SYSTEM
UNICODE, CHARACTER SET UTF8, PAD SPACE, SYSTEM
UNICODE_CI, CHARACTER SET UTF8, FROM EXTERNAL ('UNICODE'), PAD SPACE, CASE INSENSITIVE, SYSTEM
UNICODE_CI_AI, CHARACTER SET UTF8, FROM EXTERNAL ('UNICODE'), PAD SPACE, CASE INSENSITIVE, ACCENT INSENSITIVE, SYSTEM
UNICODE_FSS, CHARACTER SET UNICODE_FSS, PAD SPACE, SYSTEM
UTF8, CHARACTER SET UTF8, PAD SPACE, SYSTEM
WIN1250, CHARACTER SET WIN1250, PAD SPACE, SYSTEM
WIN1251, CHARACTER SET WIN1251, PAD SPACE, SYSTEM
WIN1251_UA, CHARACTER SET WIN1251, PAD SPACE, SYSTEM
WIN1252, CHARACTER SET WIN1252, PAD SPACE, SYSTEM
WIN1253, CHARACTER SET WIN1253, PAD SPACE, SYSTEM
WIN1254, CHARACTER SET WIN1254, PAD SPACE, SYSTEM
WIN1255, CHARACTER SET WIN1255, PAD SPACE, SYSTEM
WIN1256, CHARACTER SET WIN1256, PAD SPACE, SYSTEM
WIN1257, CHARACTER SET WIN1257, PAD SPACE, SYSTEM
WIN1257_EE, CHARACTER SET WIN1257, PAD SPACE, SYSTEM
WIN1257_LT, CHARACTER SET WIN1257, PAD SPACE, SYSTEM
WIN1257_LV, CHARACTER SET WIN1257, PAD SPACE, SYSTEM
WIN1258, CHARACTER SET WIN1258, PAD SPACE, SYSTEM
WIN_CZ, CHARACTER SET WIN1250, PAD SPACE, CASE INSENSITIVE, SYSTEM
WIN_CZ_CI_AI, CHARACTER SET WIN1250, PAD SPACE, CASE INSENSITIVE, ACCENT INSENSITIVE, SYSTEM
WIN_PTBR, CHARACTER SET WIN1252, PAD SPACE, CASE INSENSITIVE, ACCENT INSENSITIVE, SYSTEM
"""

@pytest.mark.version('>=3.0,<4.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout_1
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

# version: 4.0

expected_stdout_2 = """
    MON$ATTACHMENTS
    MON$CALL_STACK
    MON$CONTEXT_VARIABLES
    MON$DATABASE
    MON$IO_STATS
    MON$MEMORY_USAGE
    MON$RECORD_STATS
    MON$STATEMENTS
    MON$TABLE_STATS
    MON$TRANSACTIONS
    RDB$AUTH_MAPPING
    RDB$BACKUP_HISTORY
    RDB$CHARACTER_SETS
    RDB$CHECK_CONSTRAINTS
    RDB$COLLATIONS
    RDB$CONFIG
    RDB$DATABASE
    RDB$DB_CREATORS
    RDB$DEPENDENCIES
    RDB$EXCEPTIONS
    RDB$FIELDS
    RDB$FIELD_DIMENSIONS
    RDB$FILES
    RDB$FILTERS
    RDB$FORMATS
    RDB$FUNCTIONS
    RDB$FUNCTION_ARGUMENTS
    RDB$GENERATORS
    RDB$INDEX_SEGMENTS
    RDB$INDICES
    RDB$LOG_FILES
    RDB$PACKAGES
    RDB$PAGES
    RDB$PROCEDURES
    RDB$PROCEDURE_PARAMETERS
    RDB$PUBLICATIONS
    RDB$PUBLICATION_TABLES
    RDB$REF_CONSTRAINTS
    RDB$RELATIONS
    RDB$RELATION_CONSTRAINTS
    RDB$RELATION_FIELDS
    RDB$ROLES
    RDB$SECURITY_CLASSES
    RDB$TIME_ZONES
    RDB$TRANSACTIONS
    RDB$TRIGGERS
    RDB$TRIGGER_MESSAGES
    RDB$TYPES
    RDB$USER_PRIVILEGES
    RDB$VIEW_RELATIONS
    SEC$DB_CREATORS
    SEC$GLOBAL_AUTH_MAPPING
    SEC$USERS
    SEC$USER_ATTRIBUTES

    ASCII, CHARACTER SET ASCII, PAD SPACE, SYSTEM
    BIG_5, CHARACTER SET BIG_5, PAD SPACE, SYSTEM
    BS_BA, CHARACTER SET WIN1250, PAD SPACE, SYSTEM
    CP943C, CHARACTER SET CP943C, PAD SPACE, SYSTEM
    CP943C_UNICODE, CHARACTER SET CP943C, PAD SPACE, 'COLL-VERSION=153.88', SYSTEM
    CS_CZ, CHARACTER SET ISO8859_2, PAD SPACE, SYSTEM
    CYRL, CHARACTER SET CYRL, PAD SPACE, SYSTEM
    DA_DA, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
    DB_CSY, CHARACTER SET DOS852, PAD SPACE, SYSTEM
    DB_DAN865, CHARACTER SET DOS865, PAD SPACE, SYSTEM
    DB_DEU437, CHARACTER SET DOS437, PAD SPACE, SYSTEM
    DB_DEU850, CHARACTER SET DOS850, PAD SPACE, SYSTEM
    DB_ESP437, CHARACTER SET DOS437, PAD SPACE, SYSTEM
    DB_ESP850, CHARACTER SET DOS850, PAD SPACE, SYSTEM
    DB_FIN437, CHARACTER SET DOS437, PAD SPACE, SYSTEM
    DB_FRA437, CHARACTER SET DOS437, PAD SPACE, SYSTEM
    DB_FRA850, CHARACTER SET DOS850, PAD SPACE, SYSTEM
    DB_FRC850, CHARACTER SET DOS850, PAD SPACE, SYSTEM
    DB_FRC863, CHARACTER SET DOS863, PAD SPACE, SYSTEM
    DB_ITA437, CHARACTER SET DOS437, PAD SPACE, SYSTEM
    DB_ITA850, CHARACTER SET DOS850, PAD SPACE, SYSTEM
    DB_NLD437, CHARACTER SET DOS437, PAD SPACE, SYSTEM
    DB_NLD850, CHARACTER SET DOS850, PAD SPACE, SYSTEM
    DB_NOR865, CHARACTER SET DOS865, PAD SPACE, SYSTEM
    DB_PLK, CHARACTER SET DOS852, PAD SPACE, SYSTEM
    DB_PTB850, CHARACTER SET DOS850, PAD SPACE, SYSTEM
    DB_PTG860, CHARACTER SET DOS860, PAD SPACE, SYSTEM
    DB_RUS, CHARACTER SET CYRL, PAD SPACE, SYSTEM
    DB_SLO, CHARACTER SET DOS852, PAD SPACE, SYSTEM
    DB_SVE437, CHARACTER SET DOS437, PAD SPACE, SYSTEM
    DB_SVE850, CHARACTER SET DOS850, PAD SPACE, SYSTEM
    DB_TRK, CHARACTER SET DOS857, PAD SPACE, SYSTEM
    DB_UK437, CHARACTER SET DOS437, PAD SPACE, SYSTEM
    DB_UK850, CHARACTER SET DOS850, PAD SPACE, SYSTEM
    DB_US437, CHARACTER SET DOS437, PAD SPACE, SYSTEM
    DB_US850, CHARACTER SET DOS850, PAD SPACE, SYSTEM
    DE_DE, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
    DOS437, CHARACTER SET DOS437, PAD SPACE, SYSTEM
    DOS737, CHARACTER SET DOS737, PAD SPACE, SYSTEM
    DOS775, CHARACTER SET DOS775, PAD SPACE, SYSTEM
    DOS850, CHARACTER SET DOS850, PAD SPACE, SYSTEM
    DOS852, CHARACTER SET DOS852, PAD SPACE, SYSTEM
    DOS857, CHARACTER SET DOS857, PAD SPACE, SYSTEM
    DOS858, CHARACTER SET DOS858, PAD SPACE, SYSTEM
    DOS860, CHARACTER SET DOS860, PAD SPACE, SYSTEM
    DOS861, CHARACTER SET DOS861, PAD SPACE, SYSTEM
    DOS862, CHARACTER SET DOS862, PAD SPACE, SYSTEM
    DOS863, CHARACTER SET DOS863, PAD SPACE, SYSTEM
    DOS864, CHARACTER SET DOS864, PAD SPACE, SYSTEM
    DOS865, CHARACTER SET DOS865, PAD SPACE, SYSTEM
    DOS866, CHARACTER SET DOS866, PAD SPACE, SYSTEM
    DOS869, CHARACTER SET DOS869, PAD SPACE, SYSTEM
    DU_NL, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
    EN_UK, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
    EN_US, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
    ES_ES, CHARACTER SET ISO8859_1, PAD SPACE, 'DISABLE-COMPRESSIONS=1;SPECIALS-FIRST=1', SYSTEM
    ES_ES_CI_AI, CHARACTER SET ISO8859_1, PAD SPACE, CASE INSENSITIVE, ACCENT INSENSITIVE, 'DISABLE-COMPRESSIONS=1;SPECIALS-FIRST=1', SYSTEM
    EUCJ_0208, CHARACTER SET EUCJ_0208, PAD SPACE, SYSTEM
    FI_FI, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
    FR_CA, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
    FR_CA_CI_AI, CHARACTER SET ISO8859_1, FROM EXTERNAL ('FR_CA'), PAD SPACE, CASE INSENSITIVE, ACCENT INSENSITIVE, 'SPECIALS-FIRST=1', SYSTEM
    FR_FR, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
    FR_FR_CI_AI, CHARACTER SET ISO8859_1, FROM EXTERNAL ('FR_FR'), PAD SPACE, CASE INSENSITIVE, ACCENT INSENSITIVE, 'SPECIALS-FIRST=1', SYSTEM
    GB18030, CHARACTER SET GB18030, PAD SPACE, SYSTEM
    GB18030_UNICODE, CHARACTER SET GB18030, PAD SPACE, 'COLL-VERSION=153.88', SYSTEM
    GBK, CHARACTER SET GBK, PAD SPACE, SYSTEM
    GBK_UNICODE, CHARACTER SET GBK, PAD SPACE, 'COLL-VERSION=153.88', SYSTEM
    GB_2312, CHARACTER SET GB_2312, PAD SPACE, SYSTEM
    ISO8859_1, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
    ISO8859_13, CHARACTER SET ISO8859_13, PAD SPACE, SYSTEM
    ISO8859_2, CHARACTER SET ISO8859_2, PAD SPACE, SYSTEM
    ISO8859_3, CHARACTER SET ISO8859_3, PAD SPACE, SYSTEM
    ISO8859_4, CHARACTER SET ISO8859_4, PAD SPACE, SYSTEM
    ISO8859_5, CHARACTER SET ISO8859_5, PAD SPACE, SYSTEM
    ISO8859_6, CHARACTER SET ISO8859_6, PAD SPACE, SYSTEM
    ISO8859_7, CHARACTER SET ISO8859_7, PAD SPACE, SYSTEM
    ISO8859_8, CHARACTER SET ISO8859_8, PAD SPACE, SYSTEM
    ISO8859_9, CHARACTER SET ISO8859_9, PAD SPACE, SYSTEM
    ISO_HUN, CHARACTER SET ISO8859_2, PAD SPACE, SYSTEM
    ISO_PLK, CHARACTER SET ISO8859_2, PAD SPACE, SYSTEM
    IS_IS, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
    IT_IT, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
    KOI8R, CHARACTER SET KOI8R, PAD SPACE, SYSTEM
    KOI8R_RU, CHARACTER SET KOI8R, PAD SPACE, SYSTEM
    KOI8U, CHARACTER SET KOI8U, PAD SPACE, SYSTEM
    KOI8U_UA, CHARACTER SET KOI8U, PAD SPACE, SYSTEM
    KSC_5601, CHARACTER SET KSC_5601, PAD SPACE, SYSTEM
    KSC_DICTIONARY, CHARACTER SET KSC_5601, PAD SPACE, SYSTEM
    LT_LT, CHARACTER SET ISO8859_13, PAD SPACE, SYSTEM
    NEXT, CHARACTER SET NEXT, PAD SPACE, SYSTEM
    NONE, CHARACTER SET NONE, PAD SPACE, SYSTEM
    NO_NO, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
    NXT_DEU, CHARACTER SET NEXT, PAD SPACE, SYSTEM
    NXT_ESP, CHARACTER SET NEXT, PAD SPACE, SYSTEM
    NXT_FRA, CHARACTER SET NEXT, PAD SPACE, SYSTEM
    NXT_ITA, CHARACTER SET NEXT, PAD SPACE, SYSTEM
    NXT_US, CHARACTER SET NEXT, PAD SPACE, SYSTEM
    OCTETS, CHARACTER SET OCTETS, PAD SPACE, SYSTEM
    PDOX_ASCII, CHARACTER SET DOS437, PAD SPACE, SYSTEM
    PDOX_CSY, CHARACTER SET DOS852, PAD SPACE, SYSTEM
    PDOX_CYRL, CHARACTER SET CYRL, PAD SPACE, SYSTEM
    PDOX_HUN, CHARACTER SET DOS852, PAD SPACE, SYSTEM
    PDOX_INTL, CHARACTER SET DOS437, PAD SPACE, SYSTEM
    PDOX_ISL, CHARACTER SET DOS861, PAD SPACE, SYSTEM
    PDOX_NORDAN4, CHARACTER SET DOS865, PAD SPACE, SYSTEM
    PDOX_PLK, CHARACTER SET DOS852, PAD SPACE, SYSTEM
    PDOX_SLO, CHARACTER SET DOS852, PAD SPACE, SYSTEM
    PDOX_SWEDFIN, CHARACTER SET DOS437, PAD SPACE, SYSTEM
    PT_BR, CHARACTER SET ISO8859_1, PAD SPACE, CASE INSENSITIVE, ACCENT INSENSITIVE, SYSTEM
    PT_PT, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
    PXW_CSY, CHARACTER SET WIN1250, PAD SPACE, SYSTEM
    PXW_CYRL, CHARACTER SET WIN1251, PAD SPACE, SYSTEM
    PXW_GREEK, CHARACTER SET WIN1253, PAD SPACE, SYSTEM
    PXW_HUN, CHARACTER SET WIN1250, PAD SPACE, SYSTEM
    PXW_HUNDC, CHARACTER SET WIN1250, PAD SPACE, SYSTEM
    PXW_INTL, CHARACTER SET WIN1252, PAD SPACE, SYSTEM
    PXW_INTL850, CHARACTER SET WIN1252, PAD SPACE, SYSTEM
    PXW_NORDAN4, CHARACTER SET WIN1252, PAD SPACE, SYSTEM
    PXW_PLK, CHARACTER SET WIN1250, PAD SPACE, SYSTEM
    PXW_SLOV, CHARACTER SET WIN1250, PAD SPACE, SYSTEM
    PXW_SPAN, CHARACTER SET WIN1252, PAD SPACE, SYSTEM
    PXW_SWEDFIN, CHARACTER SET WIN1252, PAD SPACE, SYSTEM
    PXW_TURK, CHARACTER SET WIN1254, PAD SPACE, SYSTEM
    SJIS_0208, CHARACTER SET SJIS_0208, PAD SPACE, SYSTEM
    SV_SV, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
    TIS620, CHARACTER SET TIS620, PAD SPACE, SYSTEM
    TIS620_UNICODE, CHARACTER SET TIS620, PAD SPACE, 'COLL-VERSION=153.88', SYSTEM
    UCS_BASIC, CHARACTER SET UTF8, PAD SPACE, SYSTEM
    UNICODE, CHARACTER SET UTF8, PAD SPACE, 'COLL-VERSION=153.88', SYSTEM
    UNICODE_CI, CHARACTER SET UTF8, FROM EXTERNAL ('UNICODE'), PAD SPACE, CASE INSENSITIVE, 'COLL-VERSION=153.88', SYSTEM
    UNICODE_CI_AI, CHARACTER SET UTF8, FROM EXTERNAL ('UNICODE'), PAD SPACE, CASE INSENSITIVE, ACCENT INSENSITIVE, 'COLL-VERSION=153.88', SYSTEM
    UNICODE_FSS, CHARACTER SET UNICODE_FSS, PAD SPACE, SYSTEM
    UTF8, CHARACTER SET UTF8, PAD SPACE, SYSTEM
    WIN1250, CHARACTER SET WIN1250, PAD SPACE, SYSTEM
    WIN1251, CHARACTER SET WIN1251, PAD SPACE, SYSTEM
    WIN1251_UA, CHARACTER SET WIN1251, PAD SPACE, SYSTEM
    WIN1252, CHARACTER SET WIN1252, PAD SPACE, SYSTEM
    WIN1253, CHARACTER SET WIN1253, PAD SPACE, SYSTEM
    WIN1254, CHARACTER SET WIN1254, PAD SPACE, SYSTEM
    WIN1255, CHARACTER SET WIN1255, PAD SPACE, SYSTEM
    WIN1256, CHARACTER SET WIN1256, PAD SPACE, SYSTEM
    WIN1257, CHARACTER SET WIN1257, PAD SPACE, SYSTEM
    WIN1257_EE, CHARACTER SET WIN1257, PAD SPACE, SYSTEM
    WIN1257_LT, CHARACTER SET WIN1257, PAD SPACE, SYSTEM
    WIN1257_LV, CHARACTER SET WIN1257, PAD SPACE, SYSTEM
    WIN1258, CHARACTER SET WIN1258, PAD SPACE, SYSTEM
    WIN_CZ, CHARACTER SET WIN1250, PAD SPACE, CASE INSENSITIVE, SYSTEM
    WIN_CZ_CI_AI, CHARACTER SET WIN1250, PAD SPACE, CASE INSENSITIVE, ACCENT INSENSITIVE, SYSTEM
    WIN_PTBR, CHARACTER SET WIN1252, PAD SPACE, CASE INSENSITIVE, ACCENT INSENSITIVE, SYSTEM
"""

@pytest.mark.version('>=4.0,<5.0')
def test_2(act: Action):
    act.expected_stdout = expected_stdout_2
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

# version: 5.0

expected_stdout_3 = """
    MON$ATTACHMENTS
    MON$CALL_STACK
    MON$COMPILED_STATEMENTS
    MON$CONTEXT_VARIABLES
    MON$DATABASE
    MON$IO_STATS
    MON$MEMORY_USAGE
    MON$RECORD_STATS
    MON$STATEMENTS
    MON$TABLE_STATS
    MON$TRANSACTIONS
    RDB$AUTH_MAPPING
    RDB$BACKUP_HISTORY
    RDB$CHARACTER_SETS
    RDB$CHECK_CONSTRAINTS
    RDB$COLLATIONS
    RDB$CONFIG
    RDB$DATABASE
    RDB$DB_CREATORS
    RDB$DEPENDENCIES
    RDB$EXCEPTIONS
    RDB$FIELDS
    RDB$FIELD_DIMENSIONS
    RDB$FILES
    RDB$FILTERS
    RDB$FORMATS
    RDB$FUNCTIONS
    RDB$FUNCTION_ARGUMENTS
    RDB$GENERATORS
    RDB$INDEX_SEGMENTS
    RDB$INDICES
    RDB$JOBS
    RDB$JOBS_LOG
    RDB$KEYWORDS
    RDB$LOG_FILES
    RDB$PACKAGES
    RDB$PAGES
    RDB$PROCEDURES
    RDB$PROCEDURE_PARAMETERS
    RDB$PUBLICATIONS
    RDB$PUBLICATION_TABLES
    RDB$REF_CONSTRAINTS
    RDB$RELATIONS
    RDB$RELATION_CONSTRAINTS
    RDB$RELATION_FIELDS
    RDB$ROLES
    RDB$SECURITY_CLASSES
    RDB$TABLESPACES
    RDB$TIME_ZONES
    RDB$TRANSACTIONS
    RDB$TRIGGERS
    RDB$TRIGGER_MESSAGES
    RDB$TYPES
    RDB$USER_PRIVILEGES
    RDB$VIEW_RELATIONS
    SEC$DB_CREATORS
    SEC$GLOBAL_AUTH_MAPPING
    SEC$POLICIES
    SEC$USERS
    SEC$USER_ATTRIBUTES

    ASCII, CHARACTER SET ASCII, PAD SPACE, SYSTEM
    BIG_5, CHARACTER SET BIG_5, PAD SPACE, SYSTEM
    BS_BA, CHARACTER SET WIN1250, PAD SPACE, SYSTEM
    CP943C, CHARACTER SET CP943C, PAD SPACE, SYSTEM
    CP943C_UNICODE, CHARACTER SET CP943C, PAD SPACE, 'COLL-VERSION=153.88', SYSTEM
    CS_CZ, CHARACTER SET ISO8859_2, PAD SPACE, SYSTEM
    CYRL, CHARACTER SET CYRL, PAD SPACE, SYSTEM
    DA_DA, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
    DB_CSY, CHARACTER SET DOS852, PAD SPACE, SYSTEM
    DB_DAN865, CHARACTER SET DOS865, PAD SPACE, SYSTEM
    DB_DEU437, CHARACTER SET DOS437, PAD SPACE, SYSTEM
    DB_DEU850, CHARACTER SET DOS850, PAD SPACE, SYSTEM
    DB_ESP437, CHARACTER SET DOS437, PAD SPACE, SYSTEM
    DB_ESP850, CHARACTER SET DOS850, PAD SPACE, SYSTEM
    DB_FIN437, CHARACTER SET DOS437, PAD SPACE, SYSTEM
    DB_FRA437, CHARACTER SET DOS437, PAD SPACE, SYSTEM
    DB_FRA850, CHARACTER SET DOS850, PAD SPACE, SYSTEM
    DB_FRC850, CHARACTER SET DOS850, PAD SPACE, SYSTEM
    DB_FRC863, CHARACTER SET DOS863, PAD SPACE, SYSTEM
    DB_ITA437, CHARACTER SET DOS437, PAD SPACE, SYSTEM
    DB_ITA850, CHARACTER SET DOS850, PAD SPACE, SYSTEM
    DB_NLD437, CHARACTER SET DOS437, PAD SPACE, SYSTEM
    DB_NLD850, CHARACTER SET DOS850, PAD SPACE, SYSTEM
    DB_NOR865, CHARACTER SET DOS865, PAD SPACE, SYSTEM
    DB_PLK, CHARACTER SET DOS852, PAD SPACE, SYSTEM
    DB_PTB850, CHARACTER SET DOS850, PAD SPACE, SYSTEM
    DB_PTG860, CHARACTER SET DOS860, PAD SPACE, SYSTEM
    DB_RUS, CHARACTER SET CYRL, PAD SPACE, SYSTEM
    DB_SLO, CHARACTER SET DOS852, PAD SPACE, SYSTEM
    DB_SVE437, CHARACTER SET DOS437, PAD SPACE, SYSTEM
    DB_SVE850, CHARACTER SET DOS850, PAD SPACE, SYSTEM
    DB_TRK, CHARACTER SET DOS857, PAD SPACE, SYSTEM
    DB_UK437, CHARACTER SET DOS437, PAD SPACE, SYSTEM
    DB_UK850, CHARACTER SET DOS850, PAD SPACE, SYSTEM
    DB_US437, CHARACTER SET DOS437, PAD SPACE, SYSTEM
    DB_US850, CHARACTER SET DOS850, PAD SPACE, SYSTEM
    DE_DE, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
    DOS437, CHARACTER SET DOS437, PAD SPACE, SYSTEM
    DOS737, CHARACTER SET DOS737, PAD SPACE, SYSTEM
    DOS775, CHARACTER SET DOS775, PAD SPACE, SYSTEM
    DOS850, CHARACTER SET DOS850, PAD SPACE, SYSTEM
    DOS852, CHARACTER SET DOS852, PAD SPACE, SYSTEM
    DOS857, CHARACTER SET DOS857, PAD SPACE, SYSTEM
    DOS858, CHARACTER SET DOS858, PAD SPACE, SYSTEM
    DOS860, CHARACTER SET DOS860, PAD SPACE, SYSTEM
    DOS861, CHARACTER SET DOS861, PAD SPACE, SYSTEM
    DOS862, CHARACTER SET DOS862, PAD SPACE, SYSTEM
    DOS863, CHARACTER SET DOS863, PAD SPACE, SYSTEM
    DOS864, CHARACTER SET DOS864, PAD SPACE, SYSTEM
    DOS865, CHARACTER SET DOS865, PAD SPACE, SYSTEM
    DOS866, CHARACTER SET DOS866, PAD SPACE, SYSTEM
    DOS869, CHARACTER SET DOS869, PAD SPACE, SYSTEM
    DU_NL, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
    EN_UK, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
    EN_US, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
    ES_ES, CHARACTER SET ISO8859_1, PAD SPACE, 'DISABLE-COMPRESSIONS=1;SPECIALS-FIRST=1', SYSTEM
    ES_ES_CI_AI, CHARACTER SET ISO8859_1, PAD SPACE, CASE INSENSITIVE, ACCENT INSENSITIVE, 'DISABLE-COMPRESSIONS=1;SPECIALS-FIRST=1', SYSTEM
    EUCJ_0208, CHARACTER SET EUCJ_0208, PAD SPACE, SYSTEM
    FI_FI, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
    FR_CA, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
    FR_CA_CI_AI, CHARACTER SET ISO8859_1, FROM EXTERNAL ('FR_CA'), PAD SPACE, CASE INSENSITIVE, ACCENT INSENSITIVE, 'SPECIALS-FIRST=1', SYSTEM
    FR_FR, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
    FR_FR_CI_AI, CHARACTER SET ISO8859_1, FROM EXTERNAL ('FR_FR'), PAD SPACE, CASE INSENSITIVE, ACCENT INSENSITIVE, 'SPECIALS-FIRST=1', SYSTEM
    GB18030, CHARACTER SET GB18030, PAD SPACE, SYSTEM
    GB18030_UNICODE, CHARACTER SET GB18030, PAD SPACE, 'COLL-VERSION=153.88', SYSTEM
    GBK, CHARACTER SET GBK, PAD SPACE, SYSTEM
    GBK_UNICODE, CHARACTER SET GBK, PAD SPACE, 'COLL-VERSION=153.88', SYSTEM
    GB_2312, CHARACTER SET GB_2312, PAD SPACE, SYSTEM
    ISO8859_1, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
    ISO8859_13, CHARACTER SET ISO8859_13, PAD SPACE, SYSTEM
    ISO8859_2, CHARACTER SET ISO8859_2, PAD SPACE, SYSTEM
    ISO8859_3, CHARACTER SET ISO8859_3, PAD SPACE, SYSTEM
    ISO8859_4, CHARACTER SET ISO8859_4, PAD SPACE, SYSTEM
    ISO8859_5, CHARACTER SET ISO8859_5, PAD SPACE, SYSTEM
    ISO8859_6, CHARACTER SET ISO8859_6, PAD SPACE, SYSTEM
    ISO8859_7, CHARACTER SET ISO8859_7, PAD SPACE, SYSTEM
    ISO8859_8, CHARACTER SET ISO8859_8, PAD SPACE, SYSTEM
    ISO8859_9, CHARACTER SET ISO8859_9, PAD SPACE, SYSTEM
    ISO_HUN, CHARACTER SET ISO8859_2, PAD SPACE, SYSTEM
    ISO_PLK, CHARACTER SET ISO8859_2, PAD SPACE, SYSTEM
    IS_IS, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
    IT_IT, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
    KOI8R, CHARACTER SET KOI8R, PAD SPACE, SYSTEM
    KOI8R_RU, CHARACTER SET KOI8R, PAD SPACE, SYSTEM
    KOI8U, CHARACTER SET KOI8U, PAD SPACE, SYSTEM
    KOI8U_UA, CHARACTER SET KOI8U, PAD SPACE, SYSTEM
    KSC_5601, CHARACTER SET KSC_5601, PAD SPACE, SYSTEM
    KSC_DICTIONARY, CHARACTER SET KSC_5601, PAD SPACE, SYSTEM
    LT_LT, CHARACTER SET ISO8859_13, PAD SPACE, SYSTEM
    NEXT, CHARACTER SET NEXT, PAD SPACE, SYSTEM
    NONE, CHARACTER SET NONE, PAD SPACE, SYSTEM
    NO_NO, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
    NXT_DEU, CHARACTER SET NEXT, PAD SPACE, SYSTEM
    NXT_ESP, CHARACTER SET NEXT, PAD SPACE, SYSTEM
    NXT_FRA, CHARACTER SET NEXT, PAD SPACE, SYSTEM
    NXT_ITA, CHARACTER SET NEXT, PAD SPACE, SYSTEM
    NXT_US, CHARACTER SET NEXT, PAD SPACE, SYSTEM
    OCTETS, CHARACTER SET OCTETS, PAD SPACE, SYSTEM
    PDOX_ASCII, CHARACTER SET DOS437, PAD SPACE, SYSTEM
    PDOX_CSY, CHARACTER SET DOS852, PAD SPACE, SYSTEM
    PDOX_CYRL, CHARACTER SET CYRL, PAD SPACE, SYSTEM
    PDOX_HUN, CHARACTER SET DOS852, PAD SPACE, SYSTEM
    PDOX_INTL, CHARACTER SET DOS437, PAD SPACE, SYSTEM
    PDOX_ISL, CHARACTER SET DOS861, PAD SPACE, SYSTEM
    PDOX_NORDAN4, CHARACTER SET DOS865, PAD SPACE, SYSTEM
    PDOX_PLK, CHARACTER SET DOS852, PAD SPACE, SYSTEM
    PDOX_SLO, CHARACTER SET DOS852, PAD SPACE, SYSTEM
    PDOX_SWEDFIN, CHARACTER SET DOS437, PAD SPACE, SYSTEM
    PT_BR, CHARACTER SET ISO8859_1, PAD SPACE, CASE INSENSITIVE, ACCENT INSENSITIVE, SYSTEM
    PT_PT, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
    PXW_CSY, CHARACTER SET WIN1250, PAD SPACE, SYSTEM
    PXW_CYRL, CHARACTER SET WIN1251, PAD SPACE, SYSTEM
    PXW_GREEK, CHARACTER SET WIN1253, PAD SPACE, SYSTEM
    PXW_HUN, CHARACTER SET WIN1250, PAD SPACE, SYSTEM
    PXW_HUNDC, CHARACTER SET WIN1250, PAD SPACE, SYSTEM
    PXW_INTL, CHARACTER SET WIN1252, PAD SPACE, SYSTEM
    PXW_INTL850, CHARACTER SET WIN1252, PAD SPACE, SYSTEM
    PXW_NORDAN4, CHARACTER SET WIN1252, PAD SPACE, SYSTEM
    PXW_PLK, CHARACTER SET WIN1250, PAD SPACE, SYSTEM
    PXW_SLOV, CHARACTER SET WIN1250, PAD SPACE, SYSTEM
    PXW_SPAN, CHARACTER SET WIN1252, PAD SPACE, SYSTEM
    PXW_SWEDFIN, CHARACTER SET WIN1252, PAD SPACE, SYSTEM
    PXW_TURK, CHARACTER SET WIN1254, PAD SPACE, SYSTEM
    SJIS_0208, CHARACTER SET SJIS_0208, PAD SPACE, SYSTEM
    SV_SV, CHARACTER SET ISO8859_1, PAD SPACE, SYSTEM
    TIS620, CHARACTER SET TIS620, PAD SPACE, SYSTEM
    TIS620_UNICODE, CHARACTER SET TIS620, PAD SPACE, 'COLL-VERSION=153.88', SYSTEM
    UCS_BASIC, CHARACTER SET UTF8, PAD SPACE, SYSTEM
    UNICODE, CHARACTER SET UTF8, PAD SPACE, 'COLL-VERSION=153.88', SYSTEM
    UNICODE_CI, CHARACTER SET UTF8, FROM EXTERNAL ('UNICODE'), PAD SPACE, CASE INSENSITIVE, 'COLL-VERSION=153.88', SYSTEM
    UNICODE_CI_AI, CHARACTER SET UTF8, FROM EXTERNAL ('UNICODE'), PAD SPACE, CASE INSENSITIVE, ACCENT INSENSITIVE, 'COLL-VERSION=153.88', SYSTEM
    UNICODE_FSS, CHARACTER SET UNICODE_FSS, PAD SPACE, SYSTEM
    UTF8, CHARACTER SET UTF8, PAD SPACE, SYSTEM
    WIN1250, CHARACTER SET WIN1250, PAD SPACE, SYSTEM
    WIN1251, CHARACTER SET WIN1251, PAD SPACE, SYSTEM
    WIN1251_CI_AI, CHARACTER SET WIN1251, PAD SPACE, CASE INSENSITIVE, ACCENT INSENSITIVE, SYSTEM
    WIN1251_UA, CHARACTER SET WIN1251, PAD SPACE, SYSTEM
    WIN1252, CHARACTER SET WIN1252, PAD SPACE, SYSTEM
    WIN1253, CHARACTER SET WIN1253, PAD SPACE, SYSTEM
    WIN1254, CHARACTER SET WIN1254, PAD SPACE, SYSTEM
    WIN1255, CHARACTER SET WIN1255, PAD SPACE, SYSTEM
    WIN1256, CHARACTER SET WIN1256, PAD SPACE, SYSTEM
    WIN1257, CHARACTER SET WIN1257, PAD SPACE, SYSTEM
    WIN1257_EE, CHARACTER SET WIN1257, PAD SPACE, SYSTEM
    WIN1257_LT, CHARACTER SET WIN1257, PAD SPACE, SYSTEM
    WIN1257_LV, CHARACTER SET WIN1257, PAD SPACE, SYSTEM
    WIN1258, CHARACTER SET WIN1258, PAD SPACE, SYSTEM
    WIN_CZ, CHARACTER SET WIN1250, PAD SPACE, CASE INSENSITIVE, SYSTEM
    WIN_CZ_CI_AI, CHARACTER SET WIN1250, PAD SPACE, CASE INSENSITIVE, ACCENT INSENSITIVE, SYSTEM
    WIN_PTBR, CHARACTER SET WIN1252, PAD SPACE, CASE INSENSITIVE, ACCENT INSENSITIVE, SYSTEM
"""

expected_stderr = "There are no user-defined functions in this database"

@pytest.mark.version('>=5.0')
def test_3(act: Action):
    act.expected_stdout = expected_stdout_3
    act.expected_stderr = expected_stderr
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
    assert act.clean_stderr == act.clean_expected_stderr
