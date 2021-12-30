#coding:utf-8
#
# id:           bugs.gh_6798
# title:        Add built-in functions UNICODE_CHAR and UNICODE_VAL to convert between Unicode code point and character
# decription:   
#                   NB. Only basic checks are peformed here.
#                   This test mostly will be re-implemented later in order to check more complex cases.
#                   Lists of unicode characters and their codes:
#                       https://en.wikipedia.org/wiki/List_of_Unicode_characters
#                       https://gist.github.com/ngs/2782436
#               
#                   Checked on 5.0.0.29.
#                 
# tracker_id:   
# min_versions: ['5.0']
# versions:     5.0
# qmid:         

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 5.0
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """
    set list on;
    select unicode_val('') as "uv_empty_string" from rdb$database;
    select unicode_val('	') as "uv_tab_character" from rdb$database;
    select unicode_val('
    ') as "uv_line_feed" from rdb$database;
    select unicode_val(null) as "uv_empty_null" from rdb$database;

    --------------------------------------------------------------------

    select unicode_val('Λ') as "uv_lambda_uppercase" from rdb$database;  -- Greec Lambda, capital // 923
    select unicode_val('ß') as "uv_eszett_uppercase" from rdb$database;  -- Deutch Eszett // 223

    --------------------------------------------------------------------

    select unicode_char(923) as "uc_lambda_uppercase" from rdb$database; -- Lambda, uppercase
    select unicode_char(223) as "uv_eszett_uppercase" from rdb$database; -- Eszett, uppercase

    select ascii_char(0) = unicode_char(0) as "unicode_char(0)=ascii_char(0) ?" from rdb$database; -- must return <true>

    -- Statement failed, SQLSTATE = 22000
    -- arithmetic exception, numeric overflow, or string truncation
    -- -Malformed string
    select unicode_char(0xd800) from rdb$database;
    select unicode_char(0xDFFF) from rdb$database;
    select unicode_char(0xDC00) from rdb$database;

    --------------------------------------------------------------------
    -- Invalid arguments:
    select unicode_char(-2147483648) from rdb$database;
    select unicode_char( 2147483647) from rdb$database;
    select unicode_char(-9223372036854775808) from rdb$database;
    select unicode_char( 9223372036854775807) from rdb$database;
    select unicode_char(-170141183460469231731687303715884105728) from rdb$database;
    select unicode_char( 170141183460469231731687303715884105727) from rdb$database;
"""

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    uv_empty_string                 0
    uv_tab_character                9
    uv_line_feed                    10
    uv_empty_null                   <null>
    uv_lambda_uppercase             923
    uv_eszett_uppercase             223
    uc_lambda_uppercase             Λ
    uv_eszett_uppercase             ß
    unicode_char(0)=ascii_char(0) ? <true>
"""
expected_stderr_1 = """
    Statement failed, SQLSTATE = 22000
    arithmetic exception, numeric overflow, or string truncation
    -Malformed string
    Statement failed, SQLSTATE = 22000
    arithmetic exception, numeric overflow, or string truncation
    -Malformed string
    Statement failed, SQLSTATE = 22000
    arithmetic exception, numeric overflow, or string truncation
    -Malformed string
    Statement failed, SQLSTATE = 42000
    expression evaluation not supported
    -Argument for UNICODE_CHAR must be zero or positive
    Statement failed, SQLSTATE = 22000
    arithmetic exception, numeric overflow, or string truncation
    -Malformed string
    Statement failed, SQLSTATE = 22003
    arithmetic exception, numeric overflow, or string truncation
    -numeric value is out of range
    Statement failed, SQLSTATE = 22003
    arithmetic exception, numeric overflow, or string truncation
    -numeric value is out of range
    Statement failed, SQLSTATE = 22003
    arithmetic exception, numeric overflow, or string truncation
    -Integer overflow.  The result of an integer operation caused the most significant bit of the result to carry.
    Statement failed, SQLSTATE = 22003
    arithmetic exception, numeric overflow, or string truncation
    -Integer overflow.  The result of an integer operation caused the most significant bit of the result to carry.
"""

@pytest.mark.version('>=5.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.expected_stderr = expected_stderr_1
    act_1.execute()
    assert act_1.clean_stderr == act_1.clean_expected_stderr

    assert act_1.clean_stdout == act_1.clean_expected_stdout
