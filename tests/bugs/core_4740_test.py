#coding:utf-8

"""
ID:          issue-5045
ISSUE:       5045
TITLE:       SIMILAR TO with quantifier {n,} in the pattern: 1) fails on 2.5
  ("Invalid pattern"), 2) strange result in 3.0
DESCRIPTION:
JIRA:        CORE-4740
FBTEST:      bugs.core_4740
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    set list on;
    with
    d(txt,ptn) as(
      select
        'abcZ', '[[:lower:]]{1,}Z' from rdb$database union all select
        'abcz', '[[:lower:]]{1,}z' from rdb$database union all select
        'abcz', '[[:lower:]]*z' from rdb$database union all select
        'abcz', '[[:lower:]]+z' from rdb$database union all select
        'aggagg', '([[:lOwEr:]]{1}gg){2,}' from rdb$database union all select
        'aggagg', '([[:lOWeR:]]{1,}gg){2,}' from rdb$database union all select
        'aggagg', '(a{1}gg){2}' from rdb$database union all select
        'aggagg', '(a{0,}gg){2}' from rdb$database union all select
        'aggagg', '(a{1}__){2}' from rdb$database union all select
        'aggagg', '(a{1}__){1,}' from rdb$database union all select
        'aggagg', '(a{1}[b-z]{2}){2}' from rdb$database union all select
        'XabaXa', '([X](a|b){1,3}){2}' from rdb$database union all select
        'XabaXaba', '([X](a|b){3}){2}' from rdb$database union all select
        'XabaX', '([X](a|b){0,3}){1,}' from rdb$database union all select
        'XabaX', '([X](a|b){0,3}){2}' from rdb$database union all select
        'XaX', '([X](a){0,1}){2}' from rdb$database union all select
        'XaXa', '([X](a){1}){2}' from rdb$database union all select
        'XaXa', '([X]a{1}){2}' from rdb$database
    )
    select txt, ptn, case when trim(txt) similar to trim(ptn) then 1 else 0 end is_match
    from d;
"""

act = isql_act('db', test_script)

expected_stdout = """
    TXT                             abcZ
    PTN                             [[:lower:]]{1,}Z
    IS_MATCH                        1

    TXT                             abcz
    PTN                             [[:lower:]]{1,}z
    IS_MATCH                        1

    TXT                             abcz
    PTN                             [[:lower:]]*z
    IS_MATCH                        1

    TXT                             abcz
    PTN                             [[:lower:]]+z
    IS_MATCH                        1

    TXT                             aggagg
    PTN                             ([[:lOwEr:]]{1}gg){2,}
    IS_MATCH                        1

    TXT                             aggagg
    PTN                             ([[:lOWeR:]]{1,}gg){2,}
    IS_MATCH                        1

    TXT                             aggagg
    PTN                             (a{1}gg){2}
    IS_MATCH                        1

    TXT                             aggagg
    PTN                             (a{0,}gg){2}
    IS_MATCH                        1

    TXT                             aggagg
    PTN                             (a{1}__){2}
    IS_MATCH                        1

    TXT                             aggagg
    PTN                             (a{1}__){1,}
    IS_MATCH                        1

    TXT                             aggagg
    PTN                             (a{1}[b-z]{2}){2}
    IS_MATCH                        1

    TXT                             XabaXa
    PTN                             ([X](a|b){1,3}){2}
    IS_MATCH                        1

    TXT                             XabaXaba
    PTN                             ([X](a|b){3}){2}
    IS_MATCH                        1

    TXT                             XabaX
    PTN                             ([X](a|b){0,3}){1,}
    IS_MATCH                        1

    TXT                             XabaX
    PTN                             ([X](a|b){0,3}){2}
    IS_MATCH                        1

    TXT                             XaX
    PTN                             ([X](a){0,1}){2}
    IS_MATCH                        1

    TXT                             XaXa
    PTN                             ([X](a){1}){2}
    IS_MATCH                        1

    TXT                             XaXa
    PTN                             ([X]a{1}){2}
    IS_MATCH                        1
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

