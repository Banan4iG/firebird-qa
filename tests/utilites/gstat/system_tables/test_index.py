#coding:utf-8
"""
ID:          utilites.gstat.system_tables.index
TITLE:       Check system tables index statistics for an empty table
DESCRIPTION: 
NOTES:
"""

import pytest
from firebird.qa import *

# Dont check system table metric values as they change frequently
#substitutions = [
#    ('File.*sys_index.fdb', 'File sys_index.fdb'),
#    ('Root page: \\d+\\.?\\d*', 'Root page:'),
#    ('depth: \\d+\\.?\\d*', 'depth:'),
#    ('leaf buckets: \\d+\\.?\\d*', 'leaf buckets:'),
#    ('nodes: \\d+\\.?\\d*', 'nodes:'),
#    ('Average node length: \\d+\\.?\\d*', 'Average node length:'),
#    ('total dup: \\d+\\.?\\d*', 'total dup:'),
#    ('max dup: \\d+\\.?\\d*', 'max dup:'),
#    ('Average key length: \\d+\\.?\\d*', 'Average key length:'),
#    ('compression ratio: \\d+\\.?\\d*', 'compression ratio:'),
#    ('Average prefix length: \\d+\\.?\\d*', 'Average prefix length:'),
#    ('average data length: \\d+\\.?\\d*', 'average data length:'),
#    ('Clustering factor: \\d+\\.?\\d*', 'Clustering factor:'),
#    (', ratio: \\d+\\.?\\d*', ', ratio:'),
#]

db = db_factory(filename='sys_index.fdb', page_size=8192)
act = python_act('db', substitutions=[('File.*sys_index.fdb', 'File sys_index.fdb')])

expected_stdout = """
File sys_index.fdb is the only file
RDB$AUTH_MAPPING (45)

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

RDB$DB_CREATORS (47)

RDB$DEPENDENCIES (13)

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

    Index RDB$INDEX_2 (0)
	Root page: 132, depth: 1, leaf buckets: 1, nodes: 206
	Average node length: 11.83, total dup: 0, max dup: 0
	Average key length: 10.82, compression ratio: 1.45
	Average prefix length: 7.86, average data length: 7.85
	Clustering factor: 85, ratio: 0.41
	Fill distribution:
	     0 - 19% = 0
	    20 - 39% = 1
	    40 - 59% = 0
	    60 - 79% = 0
	    80 - 99% = 0

RDB$FIELD_DIMENSIONS (21)

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

RDB$FILTERS (16)

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

RDB$PACKAGES (42)

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

    Index RDB$INDEX_15 (2)
	Root page: 147, depth: 2, leaf buckets: 2, nodes: 559
	Average node length: 27.09, total dup: 0, max dup: 0
	Average key length: 26.08, compression ratio: 1.55
	Average prefix length: 17.42, average data length: 23.09
	Clustering factor: 358, ratio: 0.64
	Fill distribution:
	     0 - 19% = 0
	    20 - 39% = 0
	    40 - 59% = 0
	    60 - 79% = 0
	    80 - 99% = 2

    Index RDB$INDEX_3 (0)
	Root page: 133, depth: 1, leaf buckets: 1, nodes: 559
	Average node length: 6.02, total dup: 366, max dup: 24
	Average key length: 5.01, compression ratio: 2.95
	Average prefix length: 12.11, average data length: 2.68
	Clustering factor: 271, ratio: 0.48
	Fill distribution:
	     0 - 19% = 0
	    20 - 39% = 0
	    40 - 59% = 1
	    60 - 79% = 0
	    80 - 99% = 0

    Index RDB$INDEX_4 (1)
	Root page: 134, depth: 1, leaf buckets: 1, nodes: 559
	Average node length: 4.16, total dup: 499, max dup: 30
	Average key length: 3.15, compression ratio: 4.70
	Average prefix length: 13.77, average data length: 1.05
	Clustering factor: 57, ratio: 0.10
	Fill distribution:
	     0 - 19% = 0
	    20 - 39% = 1
	    40 - 59% = 0
	    60 - 79% = 0
	    80 - 99% = 0

RDB$ROLES (31)

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

    Index RDB$INDEX_7 (0)
	Root page: 137, depth: 1, leaf buckets: 1, nodes: 559
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

    Index RDB$INDEX_29 (0)
	Root page: 161, depth: 1, leaf buckets: 1, nodes: 1222
	Average node length: 5.81, total dup: 802, max dup: 12
	Average key length: 4.38, compression ratio: 2.92
	Average prefix length: 10.73, average data length: 2.08
	Clustering factor: 363, ratio: 0.30
	Fill distribution:
	     0 - 19% = 0
	    20 - 39% = 0
	    40 - 59% = 0
	    60 - 79% = 0
	    80 - 99% = 1

    Index RDB$INDEX_30 (1)
	Root page: 162, depth: 1, leaf buckets: 1, nodes: 1222
	Average node length: 3.43, total dup: 1217, max dup: 723
	Average key length: 2.01, compression ratio: 2.95
	Average prefix length: 5.93, average data length: 0.01
	Clustering factor: 33, ratio: 0.03
	Fill distribution:
	     0 - 19% = 0
	    20 - 39% = 0
	    40 - 59% = 1
	    60 - 79% = 0
	    80 - 99% = 0

RDB$VIEW_RELATIONS (7)

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
    act.gstat(switches=['-s', '-i'])
    stats = gstat_helpers.get_full_stat(act.stdout, 'Database file sequence')
    act.stdout = stats
    assert act.clean_stdout == act.clean_expected_stdout
