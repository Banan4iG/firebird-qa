#coding:utf-8

"""
ID:          issue-5639
ISSUE:       5639
TITLE:       Regression: could not use CASE expression with more than 255 conditions
DESCRIPTION:
JIRA:        CORE-5366
FBTEST:      bugs.core_5366
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    set TERM ^;
    create or alter procedure sp_test (
      "Class" bigint)
    returns (
      "Result" varchar(64))
    as
    begin
      "Result" = trim(
        case "Class"
          when null then null
          when 439 then 'test'
          when 63456 then 'test'
          when 63479 then 'test'
          when 63487 then 'test'
          when 63491 then 'test'
          when 63499 then 'test'
          when 63501 then 'test'
          when 63533 then 'test'
          when 63569 then 'test'
          when 63610 then 'test'
          when 63622 then 'test'
          when 63639 then 'test'
          when 63655 then 'test'
          when 63657 then 'test'
          when 63659 then 'test'
          when 63660 then 'test'
          when 63661 then 'test'
          when 63662 then 'test'
          when 63663 then 'test'
          when 63697 then 'test'
          when 63702 then 'test'
          when 63704 then 'test'
          when 63707 then 'test'
          when 63778 then 'test'
          when 63779 then 'test'
          when 63798 then 'test'
          when 63878 then 'test'
          when 63879 then 'test'
          when 63920 then 'test'
          when 63942 then 'test'
          when 63960 then 'test'
          when 63970 then 'test'
          when 64042 then 'test'
          when 64073 then 'test'
          when 64085 then 'test'
          when 64086 then 'test'
          when 64622 then 'test'
          when 64657 then 'test'
          when 64697 then 'test'
          when 64731 then 'test'
          when 64764 then 'test'
          when 64785 then 'test'
          when 64841 then 'test'
          when 64855 then 'test'
          when 64856 then 'test'
          when 65128 then 'test'
          when 65141 then 'test'
          when 65185 then 'test'
          when 65621 then 'test'
          when 65629 then 'test'
          when 65659 then 'test'
          when 65949 then 'test'
          when 66123 then 'test'
          when 66142 then 'test'
          when 66161 then 'test'
          when 66196 then 'test'
          when 66206 then 'test'
          when 66337 then 'test'
          when 66362 then 'test'
          when 66383 then 'test'
          when 66415 then 'test'
          when 66636 then 'test'
          when 66661 then 'test'
          when 66689 then 'test'
          when 66722 then 'test'
          when 66781 then 'test'
          when 66787 then 'test'
          when 66839 then 'test'
          when 66850 then 'test'
          when 66953 then 'test'
          when 66963 then 'test'
          when 66964 then 'test'
          when 67064 then 'test'
          when 67076 then 'test'
          when 67206 then 'test'
          when 67229 then 'test'
          when 67251 then 'test'
          when 67306 then 'test'
          when 67326 then 'test'
          when 70434 then 'test'
          when 70474 then 'test'
          when 73835 then 'test'
          when 150093 then 'test'
          when 320101 then 'test'
          when 320102 then 'test'
          when 320103 then 'test'
          when 320543 then 'test'
          when 320831 then 'test'
          when 320838 then 'test'
          when 320982 then 'test'
          when 342166 then 'test'
          when 343655 then 'test'
          when 459484 then 'test'
          when 459637 then 'test'
          when 460287 then 'test'
          when 460288 then 'test'
          when 460290 then 'test'
          when 460291 then 'test'
          when 460292 then 'test'
          when 460293 then 'test'
          when 460294 then 'test'
          when 460296 then 'test'
          when 460298 then 'test'
          when 640789 then 'test'
          when 640903 then 'test'
          when 651564 then 'test'
          when 678189 then 'test'
          when 780399 then 'test'
          when 787843 then 'test'
          when 787955 then 'test'
          when 789099 then 'test'
          when 820215 then 'test'
          when 827077 then 'test'
          when 827352 then 'test'
          when 835229 then 'test'
          when 837108 then 'test'
          when 837718 then 'test'
          when 890841 then 'test'
          when 890879 then 'test'
          when 890885 then 'test'
          when 890980 then 'test'
          when 891005 then 'test'
          when 891007 then 'test'
          when 891009 then 'test'
          when 891035 then 'test'
          when 891093 then 'test'
          when 892318 then 'test'
          when 905608 then 'test'
          when 905627 then 'test'
          when 913744 then 'test'
          when 913753 then 'test'
          when 916244 then 'test'
          when 916265 then 'test'
          when 916273 then 'test'
          when 916334 then 'test'
          when 916346 then 'test'
          when 916351 then 'test'
          when 916360 then 'test'
          when 935588 then 'test'
          when 935623 then 'test'
          when 935648 then 'test'
          when 2478129 then 'test'
          when 2915244 then 'test'
          when 3257588 then 'test'
          when 3257761 then 'test'
          when 3319392 then 'test'
          when 3321575 then 'test'
          when 3340716 then 'test'
          when 3355291 then 'test'
          when 3356388 then 'test'
          when 3358162 then 'test'
          when 3382051 then 'test'
          when 3383662 then 'test'
          when 3420043 then 'test'
          when 3420159 then 'test'
          when 3450179 then 'test'
          when 3452688 then 'test'
          when 3453211 then 'test'
          when 3460436 then 'test'
          when 3483933 then 'test'
          when 3716039 then 'test'
          when 3756014 then 'test'
          when 3915294 then 'test'
          when 3984675 then 'test'
          when 3993573 then 'test'
          when 4002668 then 'test'
          when 4002670 then 'test'
          when 4017059 then 'test'
          when 4017121 then 'test'
          when 4032403 then 'test'
          when 4032603 then 'test'
          when 4037129 then 'test'
          when 4077764 then 'test'
          when 4077782 then 'test'
          when 4077947 then 'test'
          when 4077955 then 'test'
          when 4078411 then 'test'
          when 4081351 then 'test'
          when 4084613 then 'test'
          when 4084832 then 'test'
          when 4089569 then 'test'
          when 4092258 then 'test'
          when 4092406 then 'test'
          when 4103178 then 'test'
          when 4104045 then 'test'
          when 4107074 then 'test'
          when 4107278 then 'test'
          when 4107482 then 'test'
          when 4107630 then 'test'
          when 4107924 then 'test'
          when 4114129 then 'test'
          when 4125291 then 'test'
          when 4179806 then 'test'
          when 4192560 then 'test'
          when 4194013 then 'test'
          when 4194703 then 'test'
          when 4194704 then 'test'
          when 4194706 then 'test'
          when 4194707 then 'test'
          when 4195442 then 'test'
          when 4300071 then 'test'
          when 4300073 then 'test'
          when 4300075 then 'test'
          when 4304215 then 'test'
          when 4304673 then 'test'
          when 4304752 then 'test'
          when 4310521 then 'test'
          when 4311220 then 'test'
          when 4311222 then 'test'
          when 4311224 then 'test'
          when 4314331 then 'test'
          when 4314447 then 'test'
          when 4322367 then 'test'
          when 4325243 then 'test'
          when 4326759 then 'test'
          when 4327323 then 'test'
          when 4328037 then 'test'
          when 4328303 then 'test'
          when 4328305 then 'test'
          when 4328307 then 'test'
          when 4328309 then 'test'
          when 4328318 then 'test'
          when 4336060 then 'test'
          when 4337487 then 'test'
          when 4337516 then 'test'
          when 4337626 then 'test'
          when 4339439 then 'test'
          when 4341099 then 'test'
          when 4341196 then 'test'
          when 4341425 then 'test'
          when 4349966 then 'test'
          when 4351930 then 'test'
          when 4352853 then 'test'
          when 4352969 then 'test'
          when 4355074 then 'test'
          when 4355114 then 'test'
          when 4355858 then 'test'
          when 4371296 then 'test'
          when 4416501 then 'test'
          when 4418300 then 'test'
          when 4421281 then 'test'
          when 4421840 then 'test'
          when 4422068 then 'test'
          when 4422677 then 'test'
          when 4423043 then 'test'
          when 4429998 then 'test'
          when 4431236 then 'test'
          when 4435348 then 'test'
          when 4435676 then 'test'
          when 4440546 then 'test'
          when 4447884 then 'test'
          when 4454022 then 'test'
          when 4472466 then 'test'
          when 4502449 then 'test'
          when 4512948 then 'test'
          when 4558442 then 'test'
          when 4558448 then 'test'
          when 4558450 then 'test'
          when 4567499 then 'test'
          when 4567501 then 'test'
          when 4569241 then 'test'
          when 4569243 then 'test'
          when 4572117 then 'test'
          when 4573591 then 'test'
          when 4589022 then 'test'
          when 4623252 then 'test'
          when 4635919 then 'test'
          when 4645888 then 'test'
          when 4649966 then 'test'
          when 4650088 then 'test'
          when 4650173 then 'test'
          when 4650401 then 'test'
          when 4681332 then 'test'
          when 4745895 then 'test'
          when 4755573 then 'test'
          when 4762122 then 'test'
          when 4850659 then 'test'
          when 4850660 then 'test'
          when 4850661 then 'test'
          when 4876232 then 'test'
          when 4892331 then 'test'
          when 4900586 then 'test'
          when 4900591 then 'test'
          when 4900593 then 'test'
          when 4914540 then 'test'
          when 4914542 then 'test'
          when 4914587 then 'test'
          when 4936301 then 'test'
          when 4944698 then 'test'
          when 4944988 then 'test'
          when 4945334 then 'test'
          when 4968126 then 'test'
          when 5014366 then 'test'
          when 5055181 then 'test'
          when 5193460 then 'test'
          when 5383087 then 'test'
          when 5383089 then 'test'
          when 5383091 then 'test'
          when 5543680 then 'test'
          when 5592996 then 'test'
          when 5593256 then 'test'
          when 5594327 then 'test'
          when 5600265 then 'test'
          when 5655816 then 'test'
          when 5655818 then 'test'
          when 5666867 then 'test'
          when 5666869 then 'test'
          when 5876954 then 'test'
          when 5884798 then 'test'
          when 5912516 then 'test'
          when 5914761 then 'test'
          when 5957197 then 'test'
          when 5992166 then 'test'
          when 5992167 then 'test'
          when 6033375 then 'test'
          when 6203209 then 'test'
          when 6203636 then 'test'
          when 6204269 then 'test'
          when 6204271 then 'test'
          when 6204273 then 'test'
          when 6213155 then 'test'
          when 6213323 then 'test'
          when 6301141 then 'test'
          when 6301964 then 'test'
          when 6312533 then 'test'
          when 6316960 then 'test'
          when 6316965 then 'test'
          when 6319351 then 'test'
          when 6320539 then 'test'
          when 6321288 then 'test'
          when 6325447 then 'test'
          when 6325470 then 'test'
          when 6344050 then 'test'
          when 6358457 then 'test'
          when 6364261 then 'test'
          when 6364600 then 'test'
          when 6365524 then 'test'
          when 6365682 then 'test'
          when 6417870 then 'test'
          when 6418013 then 'test'
          when 6418015 then 'test'
          when 6467138 then 'test'
          when 6558972 then 'test'
          when 6609950 then 'test'
          when 6612377 then 'test'
          when 6612379 then 'test'
          when 6635581 then 'test'
          when 6642875 then 'test'
          when 6649739 then 'test'
          when 6649742 then 'test'
          when 6649747 then 'test'
          when 6652184 then 'test'
          when 6652567 then 'test'
          when 6667495 then 'test'
          when 6673208 then 'test'
          when 6683547 then 'test'
          when 6701017 then 'test'
          when 6701022 then 'test'
          when 6701654 then 'test'
          when 6705470 then 'test'
          when 6705924 then 'test'
          when 6705926 then 'test'
          when 6705928 then 'test'
          when 6705930 then 'test'
          when 6705947 then 'test'
          when 6705949 then 'test'
          when 6705951 then 'test'
          when 6705953 then 'test'
          when 6706392 then 'test'
          when 6708534 then 'test'
          when 6708681 then 'test'
          when 6708846 then 'test'
          when 6708998 then 'test'
          when 6828688 then 'test'
          when 6843679 then 'test'
          when 6844530 then 'test'
          when 6846408 then 'test'
          when 6846816 then 'test'
          when 6848563 then 'test'
          when 6849455 then 'test'
          when 6856175 then 'test'
          when 6859372 then 'test'
          when 6860314 then 'test'
          when 6866537 then 'test'
          when 6866957 then 'test'
          when 6901444 then 'test'
          when 6904268 then 'test'
          when 6904952 then 'test'
          when 6904954 then 'test'
          when 6905712 then 'test'
          when 6938436 then 'test'
          when 6939545 then 'test'
          when 6940014 then 'test'
          when 7079756 then 'test'
          when 7080194 then 'test'
          when 7101872 then 'test'
          when 7138242 then 'test'
          when 7138450 then 'test'
          when 7148537 then 'test'
          when 7150271 then 'test'
          when 7150273 then 'test'
          when 7150513 then 'test'
          when 7151690 then 'test'
          when 7152043 then 'test'
          when 7152866 then 'test'
          when 7159124 then 'test'
          when 7159482 then 'test'
          when 7159670 then 'test'
          when 7171290 then 'test'
          when 7187300 then 'test'
          when 7187979 then 'test'
          when 7187988 then 'test'
          when 7188039 then 'test'
          when 7188073 then 'test'
          when 7188190 then 'test'
          when 7188192 then 'test'
          when 7188200 then 'test'
          when 7188226 then 'test'
          when 7188228 then 'test'
          when 7188291 then 'test'
          when 7188351 then 'test'
          when 7188462 then 'test'
          when 7188699 then 'test'
          when 7188746 then 'test'
          when 7188748 then 'test'
          when 7188888 then 'test'
          when 7188889 then 'test'
          when 7188890 then 'test'
          when 7188891 then 'test'
          when 7203393 then 'test'
          when 7206715 then 'test'
          when 7206717 then 'test'
          when 7206719 then 'test'
          when 7207844 then 'test'
          when 7229114 then 'test'
          when 7229319 then 'test'
          when 7229474 then 'test'
          when 7238128 then 'test'
          when 7239486 then 'test'
          when 7239666 then 'test'
          when 7239931 then 'test'
          when 7242657 then 'test'
          when 7242659 then 'test'
          when 7246983 then 'test'
          when 7251258 then 'test'
          when 7253427 then 'test'
          when 7275788 then 'test'
          when 7276015 then 'test'
          when 7276164 then 'test'
          when 7276637 then 'test'
          when 7314109 then 'test'
          when 7314881 then 'test'
          when 7319806 then 'test'
          when 7366851 then 'test'
          when 7368696 then 'test'
          when 7368703 then 'test'
          when 7368760 then 'test'
          when 7380288 then 'test'
          when 7425756 then 'test'
          when 7425972 then 'test'
          when 7427947 then 'test'
          when 7427949 then 'test'
          when 7428010 then 'test'
          when 7428012 then 'test'
          when 7456599 then 'test'
          when 7469922 then 'test'
          when 7480114 then 'test'
          when 7497387 then 'test'
          when 7502178 then 'test'
          when 7502180 then 'test'
          when 7502182 then 'test'
          when 7503001 then 'test'
          when 7503003 then 'test'
          when 7512844 then 'test'
          when 7535816 then 'test'
        end);
      suspend;
    end^
    set term ;^
    commit;

    set list on;
    select * from sp_test(7535816);
"""

act = isql_act('db', test_script)

expected_stdout = """
    Result                          test
"""

@pytest.mark.version('>=3.0.2')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

