#coding:utf-8

"""
ID:          issue-2119
ISSUE:       2119
TITLE:       Bug in create/alter Database trigger (with Russian comment)
DESCRIPTION:
JIRA:        CORE-1694
FBTEST:      bugs.core_1694
"""

import pytest
from firebird.qa import *

db = db_factory(charset='UTF8')

test_script = """
create domain varchar_domain as varchar(50) character set utf8 collate utf8;
create domain varchar_domain2 as varchar(50) character set utf8 collate utf8;
commit;

set term ^;
execute block as
begin
execute statement '
create or alter trigger trg_conn active on connect position 0
as
    /*
    — Eh bien, mon prince. Gênes et Lucques ne sont plus que des apanages, des поместья,
    de la famille Buonaparte. Non, je vous préviens que si vous ne me dites pas que nous
    avons la guerre, si vous vous permettez encore de pallier toutes les infamies, toutes
    les atrocités de cet Antichrist (ma parole, j''y crois) — je ne vous connais plus, vous
    n''êtes plus mon ami, vous n''êtes plus мой верный раб, comme vous dites.
    Ну, здравствуйте, здравствуйте. Je vois que je vous fais peur, садитесь и рассказывайте.
    Так говорила в июле 1805 года известная Анна Павловна Шерер, фрейлина и приближенная
    императрицы Марии Феодоровны, встречая важного и чиновного князя Василия, первого
    приехавшего на ее вечер. Анна Павловна кашляла несколько дней, у нее был грипп, как она
    говорила (грипп был тогда новое слово, употреблявшееся только редкими).
    */
    declare u int;
    declare variable new_var1 varchar(50) character set utf8 collate utf8 default ''Que voulez-vous ?'';
    declare variable new_var3 type of varchar_domain default ''Что делать ?'';
    declare variable new_var4 type of varchar_domain2 default ''Кто виноват ?'';
    /*
    Dieu, quelle virulente sortie! 4 — отвечал, нисколько не смутясь такою встречей, вошедший
    князь, в придворном, шитом мундире, в чулках, башмаках и звездах, с светлым выражением
    плоского лица. Он говорил на том изысканном французском языке, на котором не только говорили,
    но и думали наши деды, и с теми, тихими, покровительственными интонациями, которые свойственны
    состаревшемуся в свете и при дворе значительному человеку. Он подошел к Анне Павловне,
    поцеловал ее руку, подставив ей свою надушенную и сияющую лысину, и покойно уселся на диване.
    */
    declare v int = 2;
    /*
    — Ne me tourmentez pas. Eh bien, qu''a-t-on décidé par rapport à la dépêche de Novosilzoff?
    Vous savez tout.
    — Как вам сказать? — сказал князь холодным, скучающим тоном. — Qu''a-t-on décidé? On a décidé
    que Buonaparte a brûlé ses vaisseaux, et je crois que nous sommes en train de brûler les nôtres 8.
    Князь Василий говорил всегда лениво, как актер говорит роль старой пиесы. Анна Павловна Шерер,
    напротив, несмотря на свои сорок лет, была преисполнена оживления и порывов.
    */
    declare w int = 3;
begin
    u =
    /*
    Ах, не говорите мне про Австрию! Я ничего не понимаю, может быть, но Австрия никогда не хотела
    и не хочет войны. Она предает нас. Россия одна должна быть спасительницей Европы. Наш благодетель
    знает свое высокое призвание и будет верен ему. Вот одно, во что я верю. Нашему доброму и чудному
    */
    v +
    /*государю предстоит величайшая роль в мире, и он так добродетелен и хорош, что Бог не оставит его,
    и он исполнит свое призвание задавить гидру революции, которая теперь еще ужаснее в лице этого
    убийцы и злодея. Мы одни должны искупить кровь праведника. На кого нам надеяться, я вас спрашиваю?..
    */
    w;
    /*
    Англия с своим коммерческим духом не поймет и не может понять всю высоту души императора Александра
    */
end'
;
end
^
set term ;^
commit;

show trigger trg_conn;
"""

act = isql_act('db', test_script,
                 substitutions=[('[+++].*', ''), ('[===].*', ''), ('Trigger text.*', '')])

expected_stdout = """
TRG_CONN, Sequence: 0, Type: ON CONNECT, Active
as
    /*
    — Eh bien, mon prince. Gênes et Lucques ne sont plus que des apanages, des поместья,
    de la famille Buonaparte. Non, je vous préviens que si vous ne me dites pas que nous
    avons la guerre, si vous vous permettez encore de pallier toutes les infamies, toutes
    les atrocités de cet Antichrist (ma parole, j'y crois) — je ne vous connais plus, vous
    n'êtes plus mon ami, vous n'êtes plus мой верный раб, comme vous dites.
    Ну, здравствуйте, здравствуйте. Je vois que je vous fais peur, садитесь и рассказывайте.
    Так говорила в июле 1805 года известная Анна Павловна Шерер, фрейлина и приближенная
    императрицы Марии Феодоровны, встречая важного и чиновного князя Василия, первого
    приехавшего на ее вечер. Анна Павловна кашляла несколько дней, у нее был грипп, как она
    говорила (грипп был тогда новое слово, употреблявшееся только редкими).
    */
    declare u int;
    declare variable new_var1 varchar(50) character set utf8 collate utf8 default 'Que voulez-vous ?';
    declare variable new_var3 type of varchar_domain default 'Что делать ?';
    declare variable new_var4 type of varchar_domain2 default 'Кто виноват ?';
    /*
    Dieu, quelle virulente sortie! 4 — отвечал, нисколько не смутясь такою встречей, вошедший
    князь, в придворном, шитом мундире, в чулках, башмаках и звездах, с светлым выражением
    плоского лица. Он говорил на том изысканном французском языке, на котором не только говорили,
    но и думали наши деды, и с теми, тихими, покровительственными интонациями, которые свойственны
    состаревшемуся в свете и при дворе значительному человеку. Он подошел к Анне Павловне,
    поцеловал ее руку, подставив ей свою надушенную и сияющую лысину, и покойно уселся на диване.
    */
    declare v int = 2;
    /*
    — Ne me tourmentez pas. Eh bien, qu'a-t-on décidé par rapport à la dépêche de Novosilzoff?
    Vous savez tout.
    — Как вам сказать? — сказал князь холодным, скучающим тоном. — Qu'a-t-on décidé? On a décidé
    que Buonaparte a brûlé ses vaisseaux, et je crois que nous sommes en train de brûler les nôtres 8.
    Князь Василий говорил всегда лениво, как актер говорит роль старой пиесы. Анна Павловна Шерер,
    напротив, несмотря на свои сорок лет, была преисполнена оживления и порывов.
    */
    declare w int = 3;
begin
    u =
    /*
    Ах, не говорите мне про Австрию! Я ничего не понимаю, может быть, но Австрия никогда не хотела
    и не хочет войны. Она предает нас. Россия одна должна быть спасительницей Европы. Наш благодетель
    знает свое высокое призвание и будет верен ему. Вот одно, во что я верю. Нашему доброму и чудному
    */
    v +
    /*государю предстоит величайшая роль в мире, и он так добродетелен и хорош, что Бог не оставит его,
    и он исполнит свое призвание задавить гидру революции, которая теперь еще ужаснее в лице этого
    убийцы и злодея. Мы одни должны искупить кровь праведника. На кого нам надеяться, я вас спрашиваю?..
    */
    w;
    /*
    Англия с своим коммерческим духом не поймет и не может понять всю высоту души императора Александра
    */
end
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""

@pytest.mark.version('>=3')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

