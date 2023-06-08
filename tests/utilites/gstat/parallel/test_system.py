#coding:utf-8
"""
ID:          utilites.gstat.parallel.system
TITLE:       Check system tables statistics with parallel key
DESCRIPTION: 
NOTES:
"""

import pytest
from firebird.qa import *

# Check only presence of system table metrics but not their values as they change frequently
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

    Index RDB$INDEX_52 (0)
	Root page: 184, depth: 1, leaf buckets: 1, nodes: 0
	Average node length: 0.00, total dup: 0, max dup: 0
	Average key length: 0.00, compression ratio: 0.00
	Average prefix length: 0.00, average data length: 0.00
	Clustering factor: 0, ratio: 0.00
	Fill distribution:
	     0 - 19% = 1
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

    Index RDB$INDEX_44 (0)
	Root page: 176, depth: 1, leaf buckets: 1, nodes: 0
	Average node length: 0.00, total dup: 0, max dup: 0
	Average key length: 0.00, compression ratio: 0.00
	Average prefix length: 0.00, average data length: 0.00
	Clustering factor: 0, ratio: 0.00
	Fill distribution:
	     0 - 19% = 1
	    20 - 39% = 0
	    40 - 59% = 0
	    60 - 79% = 0
	    80 - 99% = 0

    Index RDB$INDEX_54 (1)
	Root page: 186, depth: 1, leaf buckets: 1, nodes: 0
	Average node length: 0.00, total dup: 0, max dup: 0
	Average key length: 0.00, compression ratio: 0.00
	Average prefix length: 0.00, average data length: 0.00
	Clustering factor: 0, ratio: 0.00
	Fill distribution:
	     0 - 19% = 1
	    20 - 39% = 0
	    40 - 59% = 0
	    60 - 79% = 0
	    80 - 99% = 0

    Index RDB$INDEX_57 (2)
	Root page: 189, depth: 1, leaf buckets: 1, nodes: 0
	Average node length: 0.00, total dup: 0, max dup: 0
	Average key length: 0.00, compression ratio: 0.00
	Average prefix length: 0.00, average data length: 0.00
	Clustering factor: 0, ratio: 0.00
	Fill distribution:
	     0 - 19% = 1
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

    Index RDB$INDEX_19 (0)
	Root page: 151, depth: 1, leaf buckets: 1, nodes: 52
	Average node length: 6.42, total dup: 0, max dup: 0
	Average key length: 5.15, compression ratio: 1.31
	Average prefix length: 3.79, average data length: 2.98
	Clustering factor: 1, ratio: 0.02
	Fill distribution:
	     0 - 19% = 1
	    20 - 39% = 0
	    40 - 59% = 0
	    60 - 79% = 0
	    80 - 99% = 0

    Index RDB$INDEX_25 (1)
	Root page: 157, depth: 1, leaf buckets: 1, nodes: 52
	Average node length: 4.08, total dup: 0, max dup: 0
	Average key length: 3.02, compression ratio: 0.75
	Average prefix length: 1.23, average data length: 1.04
	Clustering factor: 1, ratio: 0.02
	Fill distribution:
	     0 - 19% = 1
	    20 - 39% = 0
	    40 - 59% = 0
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

    Index RDB$INDEX_14 (0)
	Root page: 144, depth: 1, leaf buckets: 1, nodes: 0
	Average node length: 0.00, total dup: 0, max dup: 0
	Average key length: 0.00, compression ratio: 0.00
	Average prefix length: 0.00, average data length: 0.00
	Clustering factor: 0, ratio: 0.00
	Fill distribution:
	     0 - 19% = 1
	    20 - 39% = 0
	    40 - 59% = 0
	    60 - 79% = 0
	    80 - 99% = 0

    Index RDB$INDEX_40 (1)
	Root page: 172, depth: 1, leaf buckets: 1, nodes: 0
	Average node length: 0.00, total dup: 0, max dup: 0
	Average key length: 0.00, compression ratio: 0.00
	Average prefix length: 0.00, average data length: 0.00
	Clustering factor: 0, ratio: 0.00
	Fill distribution:
	     0 - 19% = 1
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

    Index RDB$INDEX_20 (0)
	Root page: 152, depth: 1, leaf buckets: 1, nodes: 150
	Average node length: 7.54, total dup: 0, max dup: 0
	Average key length: 6.43, compression ratio: 1.21
	Average prefix length: 4.00, average data length: 3.75
	Clustering factor: 34, ratio: 0.23
	Fill distribution:
	     0 - 19% = 1
	    20 - 39% = 0
	    40 - 59% = 0
	    60 - 79% = 0
	    80 - 99% = 0

    Index RDB$INDEX_26 (1)
	Root page: 158, depth: 1, leaf buckets: 1, nodes: 150
	Average node length: 5.02, total dup: 0, max dup: 0
	Average key length: 4.01, compression ratio: 2.06
	Average prefix length: 6.50, average data length: 1.77
	Clustering factor: 37, ratio: 0.25
	Fill distribution:
	     0 - 19% = 1
	    20 - 39% = 0
	    40 - 59% = 0
	    60 - 79% = 0
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

    Index RDB$INDEX_27 (0)
	Root page: 159, depth: 1, leaf buckets: 1, nodes: 0
	Average node length: 0.00, total dup: 0, max dup: 0
	Average key length: 0.00, compression ratio: 0.00
	Average prefix length: 0.00, average data length: 0.00
	Clustering factor: 0, ratio: 0.00
	Fill distribution:
	     0 - 19% = 1
	    20 - 39% = 0
	    40 - 59% = 0
	    60 - 79% = 0
	    80 - 99% = 0

    Index RDB$INDEX_28 (1)
	Root page: 160, depth: 1, leaf buckets: 1, nodes: 0
	Average node length: 0.00, total dup: 0, max dup: 0
	Average key length: 0.00, compression ratio: 0.00
	Average prefix length: 0.00, average data length: 0.00
	Clustering factor: 0, ratio: 0.00
	Fill distribution:
	     0 - 19% = 1
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

    Index RDB$INDEX_23 (0)
	Root page: 155, depth: 1, leaf buckets: 1, nodes: 0
	Average node length: 0.00, total dup: 0, max dup: 0
	Average key length: 0.00, compression ratio: 0.00
	Average prefix length: 0.00, average data length: 0.00
	Clustering factor: 0, ratio: 0.00
	Fill distribution:
	     0 - 19% = 1
	    20 - 39% = 0
	    40 - 59% = 0
	    60 - 79% = 0
	    80 - 99% = 0

    Index RDB$INDEX_24 (1)
	Root page: 156, depth: 1, leaf buckets: 1, nodes: 0
	Average node length: 0.00, total dup: 0, max dup: 0
	Average key length: 0.00, compression ratio: 0.00
	Average prefix length: 0.00, average data length: 0.00
	Clustering factor: 0, ratio: 0.00
	Fill distribution:
	     0 - 19% = 1
	    20 - 39% = 0
	    40 - 59% = 0
	    60 - 79% = 0
	    80 - 99% = 0

RDB$FIELDS (2)
    Primary pointer page: 8, Index root page: 9
    Total formats: 0, used formats: 0
    Average record length: 69.11, total records: 205
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

    Index RDB$INDEX_2 (0)
	Root page: 132, depth: 1, leaf buckets: 1, nodes: 205
	Average node length: 11.79, total dup: 0, max dup: 0
	Average key length: 10.78, compression ratio: 1.46
	Average prefix length: 7.88, average data length: 7.81
	Clustering factor: 85, ratio: 0.41
	Fill distribution:
	     0 - 19% = 0
	    20 - 39% = 1
	    40 - 59% = 0
	    60 - 79% = 0
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

    Index RDB$INDEX_36 (0)
	Root page: 168, depth: 1, leaf buckets: 1, nodes: 0
	Average node length: 0.00, total dup: 0, max dup: 0
	Average key length: 0.00, compression ratio: 0.00
	Average prefix length: 0.00, average data length: 0.00
	Clustering factor: 0, ratio: 0.00
	Fill distribution:
	     0 - 19% = 1
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

    Index RDB$INDEX_17 (0)
	Root page: 149, depth: 1, leaf buckets: 1, nodes: 0
	Average node length: 0.00, total dup: 0, max dup: 0
	Average key length: 0.00, compression ratio: 0.00
	Average prefix length: 0.00, average data length: 0.00
	Clustering factor: 0, ratio: 0.00
	Fill distribution:
	     0 - 19% = 1
	    20 - 39% = 0
	    40 - 59% = 0
	    60 - 79% = 0
	    80 - 99% = 0

    Index RDB$INDEX_45 (1)
	Root page: 177, depth: 1, leaf buckets: 1, nodes: 0
	Average node length: 0.00, total dup: 0, max dup: 0
	Average key length: 0.00, compression ratio: 0.00
	Average prefix length: 0.00, average data length: 0.00
	Clustering factor: 0, ratio: 0.00
	Fill distribution:
	     0 - 19% = 1
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

    Index RDB$INDEX_16 (0)
	Root page: 148, depth: 1, leaf buckets: 1, nodes: 0
	Average node length: 0.00, total dup: 0, max dup: 0
	Average key length: 0.00, compression ratio: 0.00
	Average prefix length: 0.00, average data length: 0.00
	Clustering factor: 0, ratio: 0.00
	Fill distribution:
	     0 - 19% = 1
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

    Index RDB$INDEX_53 (1)
	Root page: 185, depth: 1, leaf buckets: 1, nodes: 7
	Average node length: 4.29, total dup: 0, max dup: 0
	Average key length: 3.00, compression ratio: 0.62
	Average prefix length: 0.71, average data length: 1.14
	Clustering factor: 1, ratio: 0.14
	Fill distribution:
	     0 - 19% = 1
	    20 - 39% = 0
	    40 - 59% = 0
	    60 - 79% = 0
	    80 - 99% = 0

    Index RDB$INDEX_9 (0)
	Root page: 139, depth: 1, leaf buckets: 1, nodes: 7
	Average node length: 23.14, total dup: 0, max dup: 0
	Average key length: 22.00, compression ratio: 1.49
	Average prefix length: 13.71, average data length: 19.14
	Clustering factor: 1, ratio: 0.14
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

    Index RDB$INDEX_10 (0)
	Root page: 140, depth: 1, leaf buckets: 1, nodes: 21
	Average node length: 9.71, total dup: 14, max dup: 5
	Average key length: 8.67, compression ratio: 3.60
	Average prefix length: 24.81, average data length: 6.38
	Clustering factor: 1, ratio: 0.05
	Fill distribution:
	     0 - 19% = 1
	    20 - 39% = 0
	    40 - 59% = 0
	    60 - 79% = 0
	    80 - 99% = 0

    Index RDB$INDEX_49 (1)
	Root page: 181, depth: 1, leaf buckets: 1, nodes: 21
	Average node length: 9.76, total dup: 10, max dup: 3
	Average key length: 8.71, compression ratio: 1.69
	Average prefix length: 8.48, average data length: 6.24
	Clustering factor: 1, ratio: 0.05
	Fill distribution:
	     0 - 19% = 1
	    20 - 39% = 0
	    40 - 59% = 0
	    60 - 79% = 0
	    80 - 99% = 0

    Index RDB$INDEX_51 (2)
	Root page: 183, depth: 1, leaf buckets: 1, nodes: 21
	Average node length: 2.00, total dup: 20, max dup: 20
	Average key length: 1.00, compression ratio: 0.00
	Average prefix length: 0.00, average data length: 0.00
	Clustering factor: 1, ratio: 0.05
	Fill distribution:
	     0 - 19% = 1
	    20 - 39% = 0
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

    Index RDB$INDEX_11 (0)
	Root page: 141, depth: 1, leaf buckets: 1, nodes: 12
	Average node length: 15.83, total dup: 0, max dup: 0
	Average key length: 14.67, compression ratio: 1.05
	Average prefix length: 3.50, average data length: 11.83
	Clustering factor: 1, ratio: 0.08
	Fill distribution:
	     0 - 19% = 1
	    20 - 39% = 0
	    40 - 59% = 0
	    60 - 79% = 0
	    80 - 99% = 0

    Index RDB$INDEX_46 (1)
	Root page: 178, depth: 1, leaf buckets: 1, nodes: 12
	Average node length: 4.17, total dup: 0, max dup: 0
	Average key length: 3.00, compression ratio: 0.64
	Average prefix length: 0.83, average data length: 1.08
	Clustering factor: 1, ratio: 0.08
	Fill distribution:
	     0 - 19% = 1
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

    Index RDB$INDEX_6 (0)
	Root page: 136, depth: 1, leaf buckets: 1, nodes: 79
	Average node length: 3.91, total dup: 18, max dup: 2
	Average key length: 2.90, compression ratio: 4.09
	Average prefix length: 10.96, average data length: 0.90
	Clustering factor: 1, ratio: 0.01
	Fill distribution:
	     0 - 19% = 1
	    20 - 39% = 0
	    40 - 59% = 0
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

    Index RDB$INDEX_31 (1)
	Root page: 163, depth: 1, leaf buckets: 1, nodes: 61
	Average node length: 9.20, total dup: 26, max dup: 2
	Average key length: 8.18, compression ratio: 2.01
	Average prefix length: 10.85, average data length: 5.62
	Clustering factor: 1, ratio: 0.02
	Fill distribution:
	     0 - 19% = 1
	    20 - 39% = 0
	    40 - 59% = 0
	    60 - 79% = 0
	    80 - 99% = 0

    Index RDB$INDEX_41 (2)
	Root page: 173, depth: 1, leaf buckets: 1, nodes: 61
	Average node length: 2.00, total dup: 60, max dup: 60
	Average key length: 1.00, compression ratio: 0.00
	Average prefix length: 0.00, average data length: 0.00
	Clustering factor: 1, ratio: 0.02
	Fill distribution:
	     0 - 19% = 1
	    20 - 39% = 0
	    40 - 59% = 0
	    60 - 79% = 0
	    80 - 99% = 0

    Index RDB$INDEX_5 (0)
	Root page: 135, depth: 1, leaf buckets: 1, nodes: 61
	Average node length: 4.18, total dup: 0, max dup: 0
	Average key length: 3.16, compression ratio: 3.74
	Average prefix length: 10.67, average data length: 1.16
	Clustering factor: 1, ratio: 0.02
	Fill distribution:
	     0 - 19% = 1
	    20 - 39% = 0
	    40 - 59% = 0
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

    Index RDB$INDEX_47 (0)
	Root page: 179, depth: 1, leaf buckets: 1, nodes: 3
	Average node length: 15.67, total dup: 0, max dup: 0
	Average key length: 14.33, compression ratio: 1.00
	Average prefix length: 2.67, average data length: 11.67
	Clustering factor: 1, ratio: 0.33
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

    Index RDB$INDEX_60 (0)
	Root page: 192, depth: 1, leaf buckets: 1, nodes: 80
	Average node length: 4.47, total dup: 0, max dup: 0
	Average key length: 3.46, compression ratio: 2.31
	Average prefix length: 6.67, average data length: 1.32
	Clustering factor: 1, ratio: 0.01
	Fill distribution:
	     0 - 19% = 1
	    20 - 39% = 0
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

    Index RDB$INDEX_21 (0)
	Root page: 153, depth: 1, leaf buckets: 1, nodes: 10
	Average node length: 23.20, total dup: 0, max dup: 0
	Average key length: 22.10, compression ratio: 1.46
	Average prefix length: 13.10, average data length: 19.20
	Clustering factor: 1, ratio: 0.10
	Fill distribution:
	     0 - 19% = 1
	    20 - 39% = 0
	    40 - 59% = 0
	    60 - 79% = 0
	    80 - 99% = 0

    Index RDB$INDEX_22 (1)
	Root page: 154, depth: 1, leaf buckets: 1, nodes: 10
	Average node length: 4.20, total dup: 0, max dup: 0
	Average key length: 3.00, compression ratio: 0.63
	Average prefix length: 0.80, average data length: 1.10
	Clustering factor: 1, ratio: 0.10
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

    Index RDB$INDEX_18 (0)
	Root page: 150, depth: 1, leaf buckets: 1, nodes: 20
	Average node length: 29.00, total dup: 0, max dup: 0
	Average key length: 27.95, compression ratio: 1.91
	Average prefix length: 28.40, average data length: 25.00
	Clustering factor: 1, ratio: 0.05
	Fill distribution:
	     0 - 19% = 1
	    20 - 39% = 0
	    40 - 59% = 0
	    60 - 79% = 0
	    80 - 99% = 0

    Index RDB$INDEX_48 (1)
	Root page: 180, depth: 1, leaf buckets: 1, nodes: 20
	Average node length: 7.55, total dup: 12, max dup: 6
	Average key length: 6.50, compression ratio: 2.55
	Average prefix length: 12.40, average data length: 4.15
	Clustering factor: 1, ratio: 0.05
	Fill distribution:
	     0 - 19% = 1
	    20 - 39% = 0
	    40 - 59% = 0
	    60 - 79% = 0
	    80 - 99% = 0

    Index RDB$INDEX_50 (2)
	Root page: 182, depth: 1, leaf buckets: 1, nodes: 20
	Average node length: 2.00, total dup: 19, max dup: 19
	Average key length: 1.00, compression ratio: 0.00
	Average prefix length: 0.00, average data length: 0.00
	Clustering factor: 1, ratio: 0.05
	Fill distribution:
	     0 - 19% = 1
	    20 - 39% = 0
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

    Index RDB$INDEX_55 (0)
	Root page: 187, depth: 1, leaf buckets: 1, nodes: 1
	Average node length: 15.00, total dup: 0, max dup: 0
	Average key length: 13.00, compression ratio: 0.85
	Average prefix length: 0.00, average data length: 11.00
	Clustering factor: 1, ratio: 1.00
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

    Index RDB$INDEX_56 (0)
	Root page: 188, depth: 1, leaf buckets: 1, nodes: 0
	Average node length: 0.00, total dup: 0, max dup: 0
	Average key length: 0.00, compression ratio: 0.00
	Average prefix length: 0.00, average data length: 0.00
	Clustering factor: 0, ratio: 0.00
	Fill distribution:
	     0 - 19% = 1
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

    Index RDB$INDEX_13 (0)
	Root page: 143, depth: 1, leaf buckets: 1, nodes: 0
	Average node length: 0.00, total dup: 0, max dup: 0
	Average key length: 0.00, compression ratio: 0.00
	Average prefix length: 0.00, average data length: 0.00
	Clustering factor: 0, ratio: 0.00
	Fill distribution:
	     0 - 19% = 1
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

    Index RDB$INDEX_0 (0)
	Root page: 128, depth: 1, leaf buckets: 1, nodes: 60
	Average node length: 13.80, total dup: 0, max dup: 0
	Average key length: 12.75, compression ratio: 1.19
	Average prefix length: 5.43, average data length: 9.80
	Clustering factor: 1, ratio: 0.02
	Fill distribution:
	     0 - 19% = 1
	    20 - 39% = 0
	    40 - 59% = 0
	    60 - 79% = 0
	    80 - 99% = 0

    Index RDB$INDEX_1 (1)
	Root page: 131, depth: 1, leaf buckets: 1, nodes: 60
	Average node length: 4.03, total dup: 0, max dup: 0
	Average key length: 2.98, compression ratio: 0.74
	Average prefix length: 1.18, average data length: 1.02
	Clustering factor: 1, ratio: 0.02
	Fill distribution:
	     0 - 19% = 1
	    20 - 39% = 0
	    40 - 59% = 0
	    60 - 79% = 0
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

    Index RDB$INDEX_12 (0)
	Root page: 142, depth: 1, leaf buckets: 1, nodes: 32
	Average node length: 4.53, total dup: 0, max dup: 0
	Average key length: 3.50, compression ratio: 3.38
	Average prefix length: 10.41, average data length: 1.41
	Clustering factor: 1, ratio: 0.03
	Fill distribution:
	     0 - 19% = 1
	    20 - 39% = 0
	    40 - 59% = 0
	    60 - 79% = 0
	    80 - 99% = 0

    Index RDB$INDEX_42 (1)
	Root page: 174, depth: 1, leaf buckets: 1, nodes: 32
	Average node length: 18.72, total dup: 9, max dup: 1
	Average key length: 17.69, compression ratio: 1.64
	Average prefix length: 13.94, average data length: 15.00
	Clustering factor: 1, ratio: 0.03
	Fill distribution:
	     0 - 19% = 1
	    20 - 39% = 0
	    40 - 59% = 0
	    60 - 79% = 0
	    80 - 99% = 0

    Index RDB$INDEX_43 (2)
	Root page: 175, depth: 1, leaf buckets: 1, nodes: 32
	Average node length: 4.53, total dup: 0, max dup: 0
	Average key length: 3.50, compression ratio: 3.38
	Average prefix length: 10.41, average data length: 1.41
	Clustering factor: 1, ratio: 0.03
	Fill distribution:
	     0 - 19% = 1
	    20 - 39% = 0
	    40 - 59% = 0
	    60 - 79% = 0
	    80 - 99% = 0

RDB$RELATION_FIELDS (5)
    Primary pointer page: 14, Index root page: 15
    Total formats: 0, used formats: 0
    Average record length: 82.84, total records: 558
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

    Index RDB$INDEX_15 (2)
	Root page: 147, depth: 2, leaf buckets: 2, nodes: 558
	Average node length: 27.06, total dup: 0, max dup: 0
	Average key length: 26.06, compression ratio: 1.55
	Average prefix length: 17.44, average data length: 23.06
	Clustering factor: 356, ratio: 0.64
	Fill distribution:
	     0 - 19% = 0
	    20 - 39% = 0
	    40 - 59% = 0
	    60 - 79% = 0
	    80 - 99% = 2

    Index RDB$INDEX_3 (0)
	Root page: 133, depth: 1, leaf buckets: 1, nodes: 558
	Average node length: 5.99, total dup: 366, max dup: 24
	Average key length: 4.99, compression ratio: 2.96
	Average prefix length: 12.12, average data length: 2.66
	Clustering factor: 271, ratio: 0.49
	Fill distribution:
	     0 - 19% = 0
	    20 - 39% = 0
	    40 - 59% = 1
	    60 - 79% = 0
	    80 - 99% = 0

    Index RDB$INDEX_4 (1)
	Root page: 134, depth: 1, leaf buckets: 1, nodes: 558
	Average node length: 4.16, total dup: 498, max dup: 29
	Average key length: 3.16, compression ratio: 4.70
	Average prefix length: 13.77, average data length: 1.05
	Clustering factor: 57, ratio: 0.10
	Fill distribution:
	     0 - 19% = 0
	    20 - 39% = 1
	    40 - 59% = 0
	    60 - 79% = 0
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

    Index RDB$INDEX_39 (0)
	Root page: 171, depth: 1, leaf buckets: 1, nodes: 1
	Average node length: 13.00, total dup: 0, max dup: 0
	Average key length: 11.00, compression ratio: 0.82
	Average prefix length: 0.00, average data length: 9.00
	Clustering factor: 1, ratio: 1.00
	Fill distribution:
	     0 - 19% = 1
	    20 - 39% = 0
	    40 - 59% = 0
	    60 - 79% = 0
	    80 - 99% = 0

RDB$SECURITY_CLASSES (9)
    Primary pointer page: 22, Index root page: 23
    Total formats: 0, used formats: 0
    Average record length: 25.32, total records: 558
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
    Pointer pages: 1, data page slots: 16
    Data pages: 16, average fill: 43%
    Primary pages: 11, secondary pages: 5, swept pages: 0
    Empty pages: 6, full pages: 8
    Blobs: 558, total length: 13239, blob pages: 0
        Level 0: 558, Level 1: 0, Level 2: 0
    Fill distribution:
	 0 - 19% = 7
	20 - 39% = 0
	40 - 59% = 5
	60 - 79% = 0
	80 - 99% = 4

    Index RDB$INDEX_7 (0)
	Root page: 137, depth: 1, leaf buckets: 1, nodes: 558
	Average node length: 4.20, total dup: 0, max dup: 0
	Average key length: 3.20, compression ratio: 2.36
	Average prefix length: 6.38, average data length: 1.17
	Clustering factor: 98, ratio: 0.18
	Fill distribution:
	     0 - 19% = 0
	    20 - 39% = 1
	    40 - 59% = 0
	    60 - 79% = 0
	    80 - 99% = 0

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

    Index RDB$INDEX_58 (0)
	Root page: 190, depth: 1, leaf buckets: 1, nodes: 0
	Average node length: 0.00, total dup: 0, max dup: 0
	Average key length: 0.00, compression ratio: 0.00
	Average prefix length: 0.00, average data length: 0.00
	Clustering factor: 0, ratio: 0.00
	Fill distribution:
	     0 - 19% = 1
	    20 - 39% = 0
	    40 - 59% = 0
	    60 - 79% = 0
	    80 - 99% = 0

    Index RDB$INDEX_59 (1)
	Root page: 191, depth: 1, leaf buckets: 1, nodes: 0
	Average node length: 0.00, total dup: 0, max dup: 0
	Average key length: 0.00, compression ratio: 0.00
	Average prefix length: 0.00, average data length: 0.00
	Clustering factor: 0, ratio: 0.00
	Fill distribution:
	     0 - 19% = 1
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

    Index RDB$INDEX_32 (0)
	Root page: 164, depth: 1, leaf buckets: 1, nodes: 0
	Average node length: 0.00, total dup: 0, max dup: 0
	Average key length: 0.00, compression ratio: 0.00
	Average prefix length: 0.00, average data length: 0.00
	Clustering factor: 0, ratio: 0.00
	Fill distribution:
	     0 - 19% = 1
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

    Index RDB$INDEX_38 (1)
	Root page: 170, depth: 1, leaf buckets: 1, nodes: 26
	Average node length: 7.46, total dup: 17, max dup: 4
	Average key length: 6.42, compression ratio: 2.83
	Average prefix length: 14.04, average data length: 4.12
	Clustering factor: 1, ratio: 0.04
	Fill distribution:
	     0 - 19% = 1
	    20 - 39% = 0
	    40 - 59% = 0
	    60 - 79% = 0
	    80 - 99% = 0

    Index RDB$INDEX_8 (0)
	Root page: 138, depth: 1, leaf buckets: 1, nodes: 26
	Average node length: 4.50, total dup: 0, max dup: 0
	Average key length: 3.46, compression ratio: 3.99
	Average prefix length: 12.35, average data length: 1.46
	Clustering factor: 1, ratio: 0.04
	Fill distribution:
	     0 - 19% = 1
	    20 - 39% = 0
	    40 - 59% = 0
	    60 - 79% = 0
	    80 - 99% = 0

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

    Index RDB$INDEX_35 (0)
	Root page: 167, depth: 1, leaf buckets: 1, nodes: 32
	Average node length: 4.03, total dup: 12, max dup: 5
	Average key length: 3.00, compression ratio: 4.57
	Average prefix length: 12.72, average data length: 1.00
	Clustering factor: 1, ratio: 0.03
	Fill distribution:
	     0 - 19% = 1
	    20 - 39% = 0
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

    Index RDB$INDEX_37 (0)
	Root page: 169, depth: 1, leaf buckets: 1, nodes: 295
	Average node length: 9.52, total dup: 16, max dup: 2
	Average key length: 8.44, compression ratio: 1.16
	Average prefix length: 3.98, average data length: 5.82
	Clustering factor: 120, ratio: 0.41
	Fill distribution:
	     0 - 19% = 0
	    20 - 39% = 1
	    40 - 59% = 0
	    60 - 79% = 0
	    80 - 99% = 0

RDB$USER_PRIVILEGES (18)
    Primary pointer page: 40, Index root page: 41
    Total formats: 0, used formats: 0
    Average record length: 53.75, total records: 1220
    Average version length: 0.00, total versions: 0, max versions: 0
    Average fragment length: 0.00, total fragments: 0, max fragments: 0
    Average unpacked length: 0.00, compression ratio: 0.00
    Pointer pages: 1, data page slots: 16
    Data pages: 16, average fill: 66%
    Primary pages: 16, secondary pages: 0, swept pages: 0
    Empty pages: 1, full pages: 14
    Fill distribution:
	 0 - 19% = 1
	20 - 39% = 0
	40 - 59% = 0
	60 - 79% = 15
	80 - 99% = 0

    Index RDB$INDEX_29 (0)
	Root page: 161, depth: 1, leaf buckets: 1, nodes: 1220
	Average node length: 5.80, total dup: 801, max dup: 12
	Average key length: 4.37, compression ratio: 2.93
	Average prefix length: 10.73, average data length: 2.07
	Clustering factor: 358, ratio: 0.29
	Fill distribution:
	     0 - 19% = 0
	    20 - 39% = 0
	    40 - 59% = 0
	    60 - 79% = 0
	    80 - 99% = 1

    Index RDB$INDEX_30 (1)
	Root page: 162, depth: 1, leaf buckets: 1, nodes: 1220
	Average node length: 3.43, total dup: 1215, max dup: 722
	Average key length: 2.01, compression ratio: 2.95
	Average prefix length: 5.93, average data length: 0.01
	Clustering factor: 31, ratio: 0.03
	Fill distribution:
	     0 - 19% = 0
	    20 - 39% = 0
	    40 - 59% = 1
	    60 - 79% = 0
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

    Index RDB$INDEX_33 (0)
	Root page: 165, depth: 1, leaf buckets: 1, nodes: 0
	Average node length: 0.00, total dup: 0, max dup: 0
	Average key length: 0.00, compression ratio: 0.00
	Average prefix length: 0.00, average data length: 0.00
	Clustering factor: 0, ratio: 0.00
	Fill distribution:
	     0 - 19% = 1
	    20 - 39% = 0
	    40 - 59% = 0
	    60 - 79% = 0
	    80 - 99% = 0

    Index RDB$INDEX_34 (1)
	Root page: 166, depth: 1, leaf buckets: 1, nodes: 0
	Average node length: 0.00, total dup: 0, max dup: 0
	Average key length: 0.00, compression ratio: 0.00
	Average prefix length: 0.00, average data length: 0.00
	Clustering factor: 0, ratio: 0.00
	Fill distribution:
	     0 - 19% = 1
	    20 - 39% = 0
	    40 - 59% = 0
	    60 - 79% = 0
	    80 - 99% = 0
"""

@pytest.mark.version('>=5.0')
def test_1(act: Action, gstat_helpers):
    act.expected_stdout = expected_stdout
    act.gstat(switches=['-s', '-d', '-r', '-i', '-par', '4'])
    stats = gstat_helpers.get_full_stat(act.stdout, 'Analyzing database pages')
    act.stdout = stats
    assert act.clean_stdout == act.clean_expected_stdout
