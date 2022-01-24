#coding:utf-8

"""
ID:          issue-5017
ISSUE:       5017
TITLE:       invalid request BLR at offset 361 context already in use (BLR error)
DESCRIPTION:
JIRA:        CORE-4710
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    set planonly;
    select
        (select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)

        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)

        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)

        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)

        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)

        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)

        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        --,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1) /* #2 */
        --,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1) /* #1 */
    from
    rdb$database;

    select
        (select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)

        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)

        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)

        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)

        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)

        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)

        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1) /* #2 */
        --,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1) /* #1 */
    from
    rdb$database;


    select
        (select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)

        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)

        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)

        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)

        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)

        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)

        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1)
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1) /* #2 */
        ,(select row_number() over() from rdb$database r full join rdb$database r2 on r2.rdb$relation_id=r.rdb$relation_id group by r.rdb$relation_id having count(*)>0 order by r.rdb$relation_id rows 1 to 1) /* #1 */
    from
    rdb$database;
"""

act = isql_act('db', test_script)

expected_stdout = """
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN SORT (SORT (JOIN (JOIN (R2 NATURAL, R NATURAL), JOIN (R NATURAL, R2 NATURAL))))
    PLAN (RDB$DATABASE NATURAL)
"""

expected_stderr = """
    Statement failed, SQLSTATE = 54001
    Dynamic SQL Error
    -Too many Contexts of Relation/Procedure/Views. Maximum allowed is 256

    Statement failed, SQLSTATE = 54001
    Dynamic SQL Error
    -Too many Contexts of Relation/Procedure/Views. Maximum allowed is 256
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.expected_stderr = expected_stderr
    act.execute()
    assert (act.clean_stderr == act.clean_expected_stderr and
            act.clean_stdout == act.clean_expected_stdout)

