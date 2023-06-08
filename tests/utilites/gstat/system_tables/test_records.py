#coding:utf-8
"""
ID:          utilites.gstat.system_tables.records
TITLE:       Check system tables records statistics for an empty table
DESCRIPTION: 
NOTES:
"""

import pytest
from firebird.qa import *

# Dont check system table metric values as they change frequently
#substitutions = [
#    ('Primary pointer page: \\d+\\.?\\d*', 'Primary pointer page:'),
#    ('Total formats: \\d+\\.?\\d*', 'Total formats:'),
#    ('used formats: \\d+\\.?\\d*', 'used formats:'),
#    ('Average record length: \\d+\\.?\\d*', 'Average record length:'),
#    ('total records: \\d+\\.?\\d*', 'total records:'),
#    ('Average version length: \\d+\\.?\\d*', 'Average version length:'),
#    ('total versions: \\d+\\.?\\d*', 'total versions:'),
#    ('max versions: \\d+\\.?\\d*', 'max versions:'),
#    ('Average fragment length: \\d+\\.?\\d*', 'Average fragment length:'),
#    ('total fragments: \\d+\\.?\\d*', 'total fragments:'),
#    ('max fragments: \\d+\\.?\\d*', 'max fragments:'),
#    ('Average unpacked length: \\d+\\.?\\d*', 'Average unpacked length:'),
#    ('compression ratio: \\d+\\.?\\d*', 'compression ratio:'),
#    ('Index root page: \\d+\\.?\\d*', 'Index root page:'),
#    ('Pointer pages: \\d+\\.?\\d*', 'Pointer pages:'),
#    ('data page slots: \\d+\\.?\\d*', 'data page slots:'),
#    ('Data pages: \\d+\\.?\\d*', 'Data pages:'),
#    ('average fill: \\d+\\.?\\d*', 'average fill:'),
#    ('Primary pages: \\d+\\.?\\d*', 'Primary pages:'),
#    ('Empty pages: \\d+\\.?\\d*', 'Empty pages:'),
#    ('full pages: \\d+\\.?\\d*', 'full pages:'),
#    ('Blobs: \\d+\\.?\\d*', 'Blobs:'),
#    ('total length: \\d+\\.?\\d*', 'total length:'),
#    ('blob pages: \\d+\\.?\\d*', 'blob pages:'),
#    ('Level 0: \\d+\\.?\\d*', 'Level 0:'),
#]

db = db_factory(filename='sys_index.fdb', page_size=8192)
act = python_act('db')

expected_stdout = """
RDB$AUTH_MAPPING (45)
    Primary pointer page: 72, Index root page: 73
    Total formats: 0, used formats: 0
    Average record length: 0.00, total records: 0
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
    Pointer pages: 1, data page slots: 0
    Data pages: 0, average fill: 0%
    Primary pages: 0, secondary pages: 0, swept pages: 0
    Empty pages: 0, full pages: 0
    Fill distribution:
	 0 - 19% = 0
	20 - 39% = 0
	40 - 59% = 0
	60 - 79% = 0
	80 - 99% = 0

RDB$BACKUP_HISTORY (32)
    Primary pointer page: 68, Index root page: 69
    Total formats: 0, used formats: 0
    Average record length: 0.00, total records: 0
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
    Pointer pages: 1, data page slots: 0
    Data pages: 0, average fill: 0%
    Primary pages: 0, secondary pages: 0, swept pages: 0
    Empty pages: 0, full pages: 0
    Fill distribution:
	 0 - 19% = 0
	20 - 39% = 0
	40 - 59% = 0
	60 - 79% = 0
	80 - 99% = 0

RDB$CHARACTER_SETS (28)
    Primary pointer page: 60, Index root page: 61
    Total formats: 0, used formats: 0
    Average record length: 64.54, total records: 52
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
    Pointer pages: 1, data page slots: 1
    Data pages: 1, average fill: 52%
    Primary pages: 1, secondary pages: 0, swept pages: 0
    Empty pages: 0, full pages: 0
    Fill distribution:
	 0 - 19% = 0
	20 - 39% = 0
	40 - 59% = 1
	60 - 79% = 0
	80 - 99% = 0

RDB$CHECK_CONSTRAINTS (24)
    Primary pointer page: 52, Index root page: 53
    Total formats: 0, used formats: 0
    Average record length: 0.00, total records: 0
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
    Pointer pages: 1, data page slots: 0
    Data pages: 0, average fill: 0%
    Primary pages: 0, secondary pages: 0, swept pages: 0
    Empty pages: 0, full pages: 0
    Fill distribution:
	 0 - 19% = 0
	20 - 39% = 0
	40 - 59% = 0
	60 - 79% = 0
	80 - 99% = 0

RDB$COLLATIONS (29)
    Primary pointer page: 62, Index root page: 63
    Total formats: 0, used formats: 0
    Average record length: 52.63, total records: 150
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
    Pointer pages: 1, data page slots: 3
    Data pages: 3, average fill: 46%
    Primary pages: 2, secondary pages: 1, swept pages: 0
    Empty pages: 0, full pages: 1
    Blobs: 11, total length: 362, blob pages: 0
        Level 0: 11, Level 1: 0, Level 2: 0
    Fill distribution:
	 0 - 19% = 1
	20 - 39% = 0
	40 - 59% = 1
	60 - 79% = 1
	80 - 99% = 0

RDB$DATABASE (1)
    Primary pointer page: 6, Index root page: 7
    Total formats: 0, used formats: 0
    Average record length: 35.00, total records: 1
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
    Pointer pages: 1, data page slots: 1
    Data pages: 1, average fill: 1%
    Primary pages: 1, secondary pages: 0, swept pages: 0
    Empty pages: 0, full pages: 0
    Fill distribution:
	 0 - 19% = 1
	20 - 39% = 0
	40 - 59% = 0
	60 - 79% = 0
	80 - 99% = 0

RDB$DB_CREATORS (47)
    Primary pointer page: 74, Index root page: 75
    Total formats: 0, used formats: 0
    Average record length: 0.00, total records: 0
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
    Pointer pages: 1, data page slots: 0
    Data pages: 0, average fill: 0%
    Primary pages: 0, secondary pages: 0, swept pages: 0
    Empty pages: 0, full pages: 0
    Fill distribution:
	 0 - 19% = 0
	20 - 39% = 0
	40 - 59% = 0
	60 - 79% = 0
	80 - 99% = 0

RDB$DEPENDENCIES (13)
    Primary pointer page: 30, Index root page: 31
    Total formats: 0, used formats: 0
    Average record length: 0.00, total records: 0
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
    Pointer pages: 1, data page slots: 0
    Data pages: 0, average fill: 0%
    Primary pages: 0, secondary pages: 0, swept pages: 0
    Empty pages: 0, full pages: 0
    Fill distribution:
	 0 - 19% = 0
	20 - 39% = 0
	40 - 59% = 0
	60 - 79% = 0
	80 - 99% = 0

RDB$EXCEPTIONS (30)
    Primary pointer page: 64, Index root page: 65
    Total formats: 0, used formats: 0
    Average record length: 0.00, total records: 0
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
    Pointer pages: 1, data page slots: 0
    Data pages: 0, average fill: 0%
    Primary pages: 0, secondary pages: 0, swept pages: 0
    Empty pages: 0, full pages: 0
    Fill distribution:
	 0 - 19% = 0
	20 - 39% = 0
	40 - 59% = 0
	60 - 79% = 0
	80 - 99% = 0

RDB$FIELDS (2)
    Primary pointer page: 8, Index root page: 9
    Total formats: 0, used formats: 0
    Average record length: 69.11, total records: 206
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
    Pointer pages: 1, data page slots: 4
    Data pages: 4, average fill: 55%
    Primary pages: 3, secondary pages: 1, swept pages: 0
    Empty pages: 0, full pages: 2
    Blobs: 4, total length: 54, blob pages: 0
        Level 0: 4, Level 1: 0, Level 2: 0
    Fill distribution:
	 0 - 19% = 1
	20 - 39% = 0
	40 - 59% = 0
	60 - 79% = 3
	80 - 99% = 0

RDB$FIELD_DIMENSIONS (21)
    Primary pointer page: 46, Index root page: 47
    Total formats: 0, used formats: 0
    Average record length: 0.00, total records: 0
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
    Pointer pages: 1, data page slots: 0
    Data pages: 0, average fill: 0%
    Primary pages: 0, secondary pages: 0, swept pages: 0
    Empty pages: 0, full pages: 0
    Fill distribution:
	 0 - 19% = 0
	20 - 39% = 0
	40 - 59% = 0
	60 - 79% = 0
	80 - 99% = 0

RDB$FILES (10)
    Primary pointer page: 24, Index root page: 25
    Total formats: 0, used formats: 0
    Average record length: 0.00, total records: 0
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
    Pointer pages: 1, data page slots: 0
    Data pages: 0, average fill: 0%
    Primary pages: 0, secondary pages: 0, swept pages: 0
    Empty pages: 0, full pages: 0
    Fill distribution:
	 0 - 19% = 0
	20 - 39% = 0
	40 - 59% = 0
	60 - 79% = 0
	80 - 99% = 0

RDB$FILTERS (16)
    Primary pointer page: 36, Index root page: 37
    Total formats: 0, used formats: 0
    Average record length: 0.00, total records: 0
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
    Pointer pages: 1, data page slots: 0
    Data pages: 0, average fill: 0%
    Primary pages: 0, secondary pages: 0, swept pages: 0
    Empty pages: 0, full pages: 0
    Fill distribution:
	 0 - 19% = 0
	20 - 39% = 0
	40 - 59% = 0
	60 - 79% = 0
	80 - 99% = 0

RDB$FORMATS (8)
    Primary pointer page: 20, Index root page: 21
    Total formats: 0, used formats: 0
    Average record length: 0.00, total records: 0
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
    Pointer pages: 1, data page slots: 0
    Data pages: 0, average fill: 0%
    Primary pages: 0, secondary pages: 0, swept pages: 0
    Empty pages: 0, full pages: 0
    Fill distribution:
	 0 - 19% = 0
	20 - 39% = 0
	40 - 59% = 0
	60 - 79% = 0
	80 - 99% = 0

RDB$FUNCTIONS (14)
    Primary pointer page: 32, Index root page: 33
    Total formats: 0, used formats: 0
    Average record length: 83.57, total records: 7
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
    Pointer pages: 1, data page slots: 1
    Data pages: 1, average fill: 9%
    Primary pages: 1, secondary pages: 0, swept pages: 0
    Empty pages: 0, full pages: 0
    Fill distribution:
	 0 - 19% = 1
	20 - 39% = 0
	40 - 59% = 0
	60 - 79% = 0
	80 - 99% = 0

RDB$FUNCTION_ARGUMENTS (15)
    Primary pointer page: 34, Index root page: 35
    Total formats: 0, used formats: 0
    Average record length: 84.90, total records: 21
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
    Pointer pages: 1, data page slots: 2
    Data pages: 2, average fill: 16%
    Primary pages: 1, secondary pages: 1, swept pages: 0
    Empty pages: 0, full pages: 0
    Blobs: 10, total length: 96, blob pages: 0
        Level 0: 10, Level 1: 0, Level 2: 0
    Fill distribution:
	 0 - 19% = 1
	20 - 39% = 1
	40 - 59% = 0
	60 - 79% = 0
	80 - 99% = 0

RDB$GENERATORS (20)
    Primary pointer page: 44, Index root page: 45
    Total formats: 0, used formats: 0
    Average record length: 63.67, total records: 12
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
    Pointer pages: 1, data page slots: 2
    Data pages: 2, average fill: 9%
    Primary pages: 1, secondary pages: 1, swept pages: 0
    Empty pages: 0, full pages: 0
    Blobs: 10, total length: 173, blob pages: 0
        Level 0: 10, Level 1: 0, Level 2: 0
    Fill distribution:
	 0 - 19% = 2
	20 - 39% = 0
	40 - 59% = 0
	60 - 79% = 0
	80 - 99% = 0

RDB$INDEX_SEGMENTS (3)
    Primary pointer page: 10, Index root page: 11
    Total formats: 0, used formats: 0
    Average record length: 44.56, total records: 79
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
    Pointer pages: 1, data page slots: 1
    Data pages: 1, average fill: 60%
    Primary pages: 1, secondary pages: 0, swept pages: 0
    Empty pages: 0, full pages: 0
    Fill distribution:
	 0 - 19% = 0
	20 - 39% = 0
	40 - 59% = 1
	60 - 79% = 0
	80 - 99% = 0

RDB$INDICES (4)
    Primary pointer page: 12, Index root page: 13
    Total formats: 0, used formats: 0
    Average record length: 59.49, total records: 61
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
    Pointer pages: 1, data page slots: 1
    Data pages: 1, average fill: 57%
    Primary pages: 1, secondary pages: 0, swept pages: 0
    Empty pages: 0, full pages: 0
    Fill distribution:
	 0 - 19% = 0
	20 - 39% = 0
	40 - 59% = 1
	60 - 79% = 0
	80 - 99% = 0

RDB$LOG_FILES (25)
    Primary pointer page: 54, Index root page: 55
    Total formats: 0, used formats: 0
    Average record length: 0.00, total records: 0
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
    Pointer pages: 1, data page slots: 0
    Data pages: 0, average fill: 0%
    Primary pages: 0, secondary pages: 0, swept pages: 0
    Empty pages: 0, full pages: 0
    Fill distribution:
	 0 - 19% = 0
	20 - 39% = 0
	40 - 59% = 0
	60 - 79% = 0
	80 - 99% = 0

RDB$PACKAGES (42)
    Primary pointer page: 70, Index root page: 71
    Total formats: 0, used formats: 0
    Average record length: 54.33, total records: 3
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
    Pointer pages: 1, data page slots: 1
    Data pages: 1, average fill: 3%
    Primary pages: 1, secondary pages: 0, swept pages: 0
    Empty pages: 0, full pages: 0
    Fill distribution:
	 0 - 19% = 1
	20 - 39% = 0
	40 - 59% = 0
	60 - 79% = 0
	80 - 99% = 0

RDB$PAGES (0)
    Primary pointer page: 3, Index root page: 4
    Total formats: 0, used formats: 0
    Average record length: 17.65, total records: 80
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
    Pointer pages: 1, data page slots: 1
    Data pages: 1, average fill: 34%
    Primary pages: 1, secondary pages: 0, swept pages: 0
    Empty pages: 0, full pages: 0
    Fill distribution:
	 0 - 19% = 0
	20 - 39% = 1
	40 - 59% = 0
	60 - 79% = 0
	80 - 99% = 0

RDB$PROCEDURES (26)
    Primary pointer page: 56, Index root page: 57
    Total formats: 0, used formats: 0
    Average record length: 87.90, total records: 10
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
    Pointer pages: 1, data page slots: 1
    Data pages: 1, average fill: 13%
    Primary pages: 1, secondary pages: 0, swept pages: 0
    Empty pages: 0, full pages: 0
    Fill distribution:
	 0 - 19% = 1
	20 - 39% = 0
	40 - 59% = 0
	60 - 79% = 0
	80 - 99% = 0

RDB$PROCEDURE_PARAMETERS (27)
    Primary pointer page: 58, Index root page: 59
    Total formats: 0, used formats: 0
    Average record length: 106.10, total records: 20
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
    Pointer pages: 1, data page slots: 2
    Data pages: 2, average fill: 21%
    Primary pages: 1, secondary pages: 1, swept pages: 0
    Empty pages: 0, full pages: 0
    Blobs: 18, total length: 287, blob pages: 0
        Level 0: 18, Level 1: 0, Level 2: 0
    Fill distribution:
	 0 - 19% = 1
	20 - 39% = 1
	40 - 59% = 0
	60 - 79% = 0
	80 - 99% = 0

RDB$PUBLICATIONS (51)
    Primary pointer page: 76, Index root page: 77
    Total formats: 0, used formats: 0
    Average record length: 38.00, total records: 1
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
    Pointer pages: 1, data page slots: 1
    Data pages: 1, average fill: 1%
    Primary pages: 1, secondary pages: 0, swept pages: 0
    Empty pages: 0, full pages: 0
    Fill distribution:
	 0 - 19% = 1
	20 - 39% = 0
	40 - 59% = 0
	60 - 79% = 0
	80 - 99% = 0

RDB$PUBLICATION_TABLES (52)
    Primary pointer page: 78, Index root page: 79
    Total formats: 0, used formats: 0
    Average record length: 0.00, total records: 0
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
    Pointer pages: 1, data page slots: 0
    Data pages: 0, average fill: 0%
    Primary pages: 0, secondary pages: 0, swept pages: 0
    Empty pages: 0, full pages: 0
    Fill distribution:
	 0 - 19% = 0
	20 - 39% = 0
	40 - 59% = 0
	60 - 79% = 0
	80 - 99% = 0

RDB$REF_CONSTRAINTS (23)
    Primary pointer page: 50, Index root page: 51
    Total formats: 0, used formats: 0
    Average record length: 0.00, total records: 0
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
    Pointer pages: 1, data page slots: 0
    Data pages: 0, average fill: 0%
    Primary pages: 0, secondary pages: 0, swept pages: 0
    Empty pages: 0, full pages: 0
    Fill distribution:
	 0 - 19% = 0
	20 - 39% = 0
	40 - 59% = 0
	60 - 79% = 0
	80 - 99% = 0

RDB$RELATIONS (6)
    Primary pointer page: 16, Index root page: 17
    Total formats: 0, used formats: 0
    Average record length: 86.65, total records: 60
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
    Pointer pages: 1, data page slots: 2
    Data pages: 2, average fill: 59%
    Primary pages: 1, secondary pages: 1, swept pages: 0
    Empty pages: 0, full pages: 0
    Blobs: 9, total length: 2656, blob pages: 0
        Level 0: 9, Level 1: 0, Level 2: 0
    Fill distribution:
	 0 - 19% = 0
	20 - 39% = 0
	40 - 59% = 1
	60 - 79% = 1
	80 - 99% = 0

RDB$RELATION_CONSTRAINTS (22)
    Primary pointer page: 48, Index root page: 49
    Total formats: 0, used formats: 0
    Average record length: 74.91, total records: 32
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
    Pointer pages: 1, data page slots: 1
    Data pages: 1, average fill: 36%
    Primary pages: 1, secondary pages: 0, swept pages: 0
    Empty pages: 0, full pages: 0
    Fill distribution:
	 0 - 19% = 0
	20 - 39% = 1
	40 - 59% = 0
	60 - 79% = 0
	80 - 99% = 0

RDB$RELATION_FIELDS (5)
    Primary pointer page: 14, Index root page: 15
    Total formats: 0, used formats: 0
    Average record length: 82.86, total records: 559
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
    Pointer pages: 1, data page slots: 16
    Data pages: 16, average fill: 43%
    Primary pages: 16, secondary pages: 0, swept pages: 0
    Empty pages: 7, full pages: 8
    Fill distribution:
	 0 - 19% = 7
	20 - 39% = 0
	40 - 59% = 0
	60 - 79% = 9
	80 - 99% = 0

RDB$ROLES (31)
    Primary pointer page: 66, Index root page: 67
    Total formats: 0, used formats: 0
    Average record length: 47.00, total records: 1
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
    Pointer pages: 1, data page slots: 1
    Data pages: 1, average fill: 1%
    Primary pages: 1, secondary pages: 0, swept pages: 0
    Empty pages: 0, full pages: 0
    Fill distribution:
	 0 - 19% = 1
	20 - 39% = 0
	40 - 59% = 0
	60 - 79% = 0
	80 - 99% = 0

RDB$SECURITY_CLASSES (9)
    Primary pointer page: 22, Index root page: 23
    Total formats: 0, used formats: 0
    Average record length: 25.32, total records: 559
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
    Pointer pages: 1, data page slots: 16
    Data pages: 16, average fill: 43%
    Primary pages: 11, secondary pages: 5, swept pages: 0
    Empty pages: 6, full pages: 8
    Blobs: 559, total length: 13262, blob pages: 0
        Level 0: 559, Level 1: 0, Level 2: 0
    Fill distribution:
	 0 - 19% = 7
	20 - 39% = 0
	40 - 59% = 5
	60 - 79% = 0
	80 - 99% = 4

RDB$TABLESPACES (58)
    Primary pointer page: 80, Index root page: 81
    Total formats: 0, used formats: 0
    Average record length: 0.00, total records: 0
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
    Pointer pages: 1, data page slots: 0
    Data pages: 0, average fill: 0%
    Primary pages: 0, secondary pages: 0, swept pages: 0
    Empty pages: 0, full pages: 0
    Fill distribution:
	 0 - 19% = 0
	20 - 39% = 0
	40 - 59% = 0
	60 - 79% = 0
	80 - 99% = 0

RDB$TRANSACTIONS (19)
    Primary pointer page: 42, Index root page: 43
    Total formats: 0, used formats: 0
    Average record length: 0.00, total records: 0
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
    Pointer pages: 1, data page slots: 0
    Data pages: 0, average fill: 0%
    Primary pages: 0, secondary pages: 0, swept pages: 0
    Empty pages: 0, full pages: 0
    Fill distribution:
	 0 - 19% = 0
	20 - 39% = 0
	40 - 59% = 0
	60 - 79% = 0
	80 - 99% = 0

RDB$TRIGGERS (12)
    Primary pointer page: 28, Index root page: 29
    Total formats: 0, used formats: 0
    Average record length: 68.23, total records: 26
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
    Pointer pages: 1, data page slots: 3
    Data pages: 3, average fill: 54%
    Primary pages: 1, secondary pages: 2, swept pages: 0
    Empty pages: 0, full pages: 1
    Blobs: 26, total length: 10042, blob pages: 0
        Level 0: 26, Level 1: 0, Level 2: 0
    Fill distribution:
	 0 - 19% = 0
	20 - 39% = 2
	40 - 59% = 0
	60 - 79% = 0
	80 - 99% = 1

RDB$TRIGGER_MESSAGES (17)
    Primary pointer page: 38, Index root page: 39
    Total formats: 0, used formats: 0
    Average record length: 49.44, total records: 32
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
    Pointer pages: 1, data page slots: 1
    Data pages: 1, average fill: 26%
    Primary pages: 1, secondary pages: 0, swept pages: 0
    Empty pages: 0, full pages: 0
    Fill distribution:
	 0 - 19% = 0
	20 - 39% = 1
	40 - 59% = 0
	60 - 79% = 0
	80 - 99% = 0

RDB$TYPES (11)
    Primary pointer page: 26, Index root page: 27
    Total formats: 0, used formats: 0
    Average record length: 49.51, total records: 295
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
    Pointer pages: 1, data page slots: 4
    Data pages: 4, average fill: 60%
    Primary pages: 4, secondary pages: 0, swept pages: 0
    Empty pages: 0, full pages: 3
    Fill distribution:
	 0 - 19% = 0
	20 - 39% = 1
	40 - 59% = 0
	60 - 79% = 3
	80 - 99% = 0

RDB$USER_PRIVILEGES (18)
    Primary pointer page: 40, Index root page: 41
    Total formats: 0, used formats: 0
    Average record length: 53.76, total records: 1222
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
    Pointer pages: 1, data page slots: 16
    Data pages: 16, average fill: 66%
    Primary pages: 16, secondary pages: 0, swept pages: 0
    Empty pages: 0, full pages: 15
    Fill distribution:
	 0 - 19% = 1
	20 - 39% = 0
	40 - 59% = 0
	60 - 79% = 15
	80 - 99% = 0

RDB$VIEW_RELATIONS (7)
    Primary pointer page: 18, Index root page: 19
    Total formats: 0, used formats: 0
    Average record length: 0.00, total records: 0
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
    Pointer pages: 1, data page slots: 0
    Data pages: 0, average fill: 0%
    Primary pages: 0, secondary pages: 0, swept pages: 0
    Empty pages: 0, full pages: 0
    Fill distribution:
	 0 - 19% = 0
	20 - 39% = 0
	40 - 59% = 0
	60 - 79% = 0
	80 - 99% = 0
"""

@pytest.mark.version('>=5.0')
def test_1(act: Action, gstat_helpers):
    act.expected_stdout = expected_stdout
    act.gstat(switches=['-s', '-d', '-r'])
    stats = gstat_helpers.get_full_stat(act.stdout, 'Analyzing database pages')
    act.stdout = stats
    assert act.clean_stdout == act.clean_expected_stdout
