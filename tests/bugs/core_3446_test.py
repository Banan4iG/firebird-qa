#coding:utf-8

"""
ID:          issue-3807
ISSUE:       3807
TITLE:       Allow conversion from/to BLOBs and others types in the API functions (XSQLVAR or blr messages)
DESCRIPTION:
  We try to write varchar value into blob field and vice-versa, using execute statement
  with parameters of corresp. types
JIRA:        CORE-3446
FBTEST:      bugs.core_3446
"""

import pytest
from firebird.qa import *

init_script = """
recreate table test( s varchar(8187) character set utf8 collate unicode_ci_ai, b blob sub_type 1 character set utf8 collate unicode_ci_ai);
commit;

insert into test (s, b )
values(
'Sur le boulevard Montmorency, au n° 53, s''élève une maison portant,
encastré dans son balcon, un profil lauré de Louis XV, en bronze
doré, qui a tout l''air d''être le médaillon, dont était décorée la
tribune de musique de la salle à manger de Luciennes, représenté dans
l''aquarelle de Moreau que l''on voit au Louvre. Cette tête, que quelques
promeneurs regardent d''un œil farouche, n''est point,--ai-je besoin de
le dire?--une affiche des opinions politiques du propriétaire, elle est
tout bonnement l''enseigne d''un des nids les plus pleins de choses du
XVIIIe siècle qui existent à Paris.

La porte noire, que surmonte un élégant dessus de grille de chapelle
jésuite en fer forgé, la porte ouverte, du bas de l''escalier, de
l''entrée du vestibule, du seuil de la maison, le visiteur est accueilli
par des terres cuites, des bronzes, des dessins, des porcelaines du
siècle aimable par excellence, mêlés à des objets de l''Extrême-Orient,
qui se trouvaient faire si bon ménage dans les collections de Madame de
Pompadour et de tous les _curieux_ et les _curiolets_ du temps.

La vie d''aujourd''hui est une vie de combattivité; elle demande dans
toutes les carrières une concentration, un effort, un travail, qui, en
son foyer enferment l''homme, dont l''existence n''est plus extérieure
comme au XVIIIe siècle, n''est plus papillonnante parmi la société
depuis ses dix-sept ans jusqu''à sa mort. De notre temps on va bien
encore dans le monde, mais toute la vie ne s''y dépense plus, et le
_chez-soi_ a cessé d''être l''hôtel garni où l''on ne faisait que coucher.
Dans cette vie assise au coin du feu, renfermée, sédentaire, la
créature humaine, et la première venue, a été poussée à vouloir les
quatre murs de son _home_ agréables, plaisants, amusants aux yeux; et
cet entour et ce décor de son intérieur, elle l''a cherché et trouvé
naturellement dans l''objet d''art pur ou dans l''objet d''art industriel,
plus accessible au goût de tous. Du même coup, ces habitudes moins
mondaines amenaient un amoindrissement du rôle de la femme dans la
pensée masculine; elle n''était plus pour nous l''occupation galante de
toute notre existence, cette occupation qui était autrefois la carrière
du plus grand nombre, et, à la suite de cette modification dans les
mœurs, il arrivait ceci: c''est que l''intérêt de l''homme, s''en allant
de l''être charmant, se reportait en grande partie sur les jolis objets
inanimés dont la passion revêt un peu de la nature et du caractère
de l''amour. Au XVIIIe siècle, il n''y a pas de _bibeloteurs_ jeunes:
c''est là la différence des deux siècles. Pour notre génération, la
_bricabracomanie_ n''est qu''un bouche-trou de la femme qui ne possède
plus l''imagination de l''homme, et j''ai fait à mon égard cette remarque,
que, lorsque par hasard mon cœur s''est trouvé occupé, l''objet d''art ne
m''était de rien.

Oui, cette passion devenue générale, ce plaisir solitaire, auquel se
livre presque toute une nation, doit son développement au vide, à
l''ennui du cœur, et aussi, il faut le reconnaître, à la tristesse
des jours actuels, à l''incertitude des lendemains, à l''enfantement,
les pieds devant, de la société nouvelle, à des soucis et à des
préoccupations qui poussent, comme à la veille d''un déluge, les désirs
et les envies à se donner la jouissance immédiate de tout ce qui les
charme, les séduit, les tente: l''oubli du moment dans l''assouvissement
artistique.

Ce sont ces causes, et incontestablement l''éducation de l''œil des
gens du XIXe siècle, et encore un sentiment tout nouveau, la tendresse
presque humaine pour les _choses_, qui font, à l''heure qu''il est, de
presque tout le monde, des collectionneurs et de moi en particulier le
plus passionné de tous les collectionneurs.

Un riant pavé en marbre blanc et en marbre rouge du Languedoc, avec,
pour revêtement aux murs et au plafond, un cuir moderne peuplé de
perroquets fantastiques dorés et peints sur un fond vert d''eau.

Sur ce cuir, dans un désordre cherché, dans un pittoresque
d''antichambre et d''atelier, toutes sortes de choses voyantes et
claquantes, de brillants cuivres découpés, des poteries dorées, des
broderies du Japon et encore des objets bizarres, inattendus, étonnant
par leur originalité, leur exotisme, et vis-à-vis d''un certain nombre
desquels je me fais un peu l''effet du bon Père Buffier quand il disait:
«Voilà des choses que je ne sais pas, il faut que je fasse un livre
dessus.»

Ça, une petite jardinière à suspension, fabriquée d''une coloquinte
excentrique, dont la tige tournante et recroquevillée est une tige de
bronze qui a la flexibilité d''une liane; cette grande planchette fruste
de bois, toute parcourue des tortils d''un feuillage de lierre, exécuté
en nacre et en écaille: le porte-éventail qui tient dans l''appartement
l''éventail ouvert contre le mur; cette petite boule de porcelaine
jaune impérial si délicatement treillagée: la cage au grillon ou à
la mouche bourdonnante, que le Chinois aime suspendre au chevet de
son lit; et cette plaque de faïence figurant une branche de pêcher en
fleur, modelée à jour dans un cadre de bois en forme d''écran, vous
représente la décoration de l''angle religieux et mystique d''une chambre
de prostituée de maison de thé, l''espèce de tableau d''autel devant
lequel elle place une fleur dans un vase.

Des broderies du Japon, ai-je dit plus haut, c''est là, dans leurs
cadres de bambous, la riche, la splendide, l''_éclairante_ décoration
des murs du vestibule et un peu de toute la maison. Ces carrés de soie
brodés appelés _fusha_ ou _foukousa_ font la chatoyante couverture
sous laquelle on a l''habitude, dans l''Empire du Lever du Soleil,
d''envoyer tout présent quelconque, et le plus minime, fût-il même de
deux œufs[1]. Les anciens _foukousas_ fabriqués à Kioto[2] sont des
produits d''un art tout particulier au Japon, et auxquels l''Europe
ne peut rien opposer: de la peinture, de vrais tableaux composés
et exécutés en soie par un brodeur, où sur les fonds aux adorables
nuances, et telles qu''en donne le satin ou le crêpe, un oiseau, un
poisson, une fleur se détache dans le haut relief d''une broderie.
Et rien là dedans du travail d''un art mécanique, du dessin bête de
vieille fille de nos broderies à nous, mais des silhouettes d''êtres
pleins de vie, avec leurs pattes d''oiseau d''un si grand style, avec
leurs nageoires de poisson d''un si puissant contournement. Quelquefois
des parties peintes, peintes à l''encre de Chine, s''associent de la
manière la plus heureuse à la broderie. Je connais, chez Mme Auguste
Sichel, une fusée de fleurs brodée dans un vase en sparterie peint ou
imprimé, qui est bien la plus harmonieuse chose qu''il soit possible
de voir. M. de Nittis a fait un écran, d''un admirable et singulier
carré, où deux grues, brodées en noir sur un fond rose saumoné, ont,
comme accompagnement et adoucissement de la broderie, des demi-teintes
doucement lavées d''encre de Chine sur l''étoffe enchanteresse. Et dans
ce vestibule, il y a, sur un fond lilas, des carpes nageant au milieu
de branchages de presle brodées en or, et dont le ventre apparaît comme
argenté par un reflet de bourbe: un effet obtenu par une réserve au
milieu du fond tout teinté et obscuré d''encre de Chine. Il est même un
certain nombre de foukousas absolument peints. J''ai coloriée, sur un
crêpe gris, dans l''orbe d''un soleil rouge comme du feu, l''échancrure
pittoresque d''un passage de sept grues, exécuté avec la science que les
Japonais possèdent du vol de l''échassier. J''ai encore, jetées sur un
fond maïs, sans aucun détail de terrain, deux grandes grues blanches,
à la petite crête rougie de vermillon, au cou, aux pattes, à la queue,
teintés d''encre de Chine. Et ne vous étonnez pas de rencontrer si
souvent sur les broderies la grue, cet oiseau qui apparaît dans le
haut du ciel aux Japonais comme un messager céleste, et qu''ils saluent
de l''appellation: _O Tsouri Sama_, Sa Seigneurie la Grue.

[1] Il n''est guère besoin de dire que le carré est toujours
rapporté à son maître par le porteur du présent.

[2] Les foukousas modernes seraient aujourd''hui fabriqués à
Togané, d''où on les expédierait à Yedo.
'
, -----------
'Sur le boulevard Montmorency, au n° 53, s''élève une maison portant,
encastré dans son balcon, un profil lauré de Louis XV, en bronze
doré, qui a tout l''air d''être le médaillon, dont était décorée la
tribune de musique de la salle à manger de Luciennes, représenté dans
l''aquarelle de Moreau que l''on voit au Louvre. Cette tête, que quelques
promeneurs regardent d''un œil farouche, n''est point,--ai-je besoin de
le dire?--une affiche des opinions politiques du propriétaire, elle est
tout bonnement l''enseigne d''un des nids les plus pleins de choses du
XVIIIe siècle qui existent à Paris.

La porte noire, que surmonte un élégant dessus de grille de chapelle
jésuite en fer forgé, la porte ouverte, du bas de l''escalier, de
l''entrée du vestibule, du seuil de la maison, le visiteur est accueilli
par des terres cuites, des bronzes, des dessins, des porcelaines du
siècle aimable par excellence, mêlés à des objets de l''Extrême-Orient,
qui se trouvaient faire si bon ménage dans les collections de Madame de
Pompadour et de tous les _curieux_ et les _curiolets_ du temps.

La vie d''aujourd''hui est une vie de combattivité; elle demande dans
toutes les carrières une concentration, un effort, un travail, qui, en
son foyer enferment l''homme, dont l''existence n''est plus extérieure
comme au XVIIIe siècle, n''est plus papillonnante parmi la société
depuis ses dix-sept ans jusqu''à sa mort. De notre temps on va bien
encore dans le monde, mais toute la vie ne s''y dépense plus, et le
_chez-soi_ a cessé d''être l''hôtel garni où l''on ne faisait que coucher.
Dans cette vie assise au coin du feu, renfermée, sédentaire, la
créature humaine, et la première venue, a été poussée à vouloir les
quatre murs de son _home_ agréables, plaisants, amusants aux yeux; et
cet entour et ce décor de son intérieur, elle l''a cherché et trouvé
naturellement dans l''objet d''art pur ou dans l''objet d''art industriel,
plus accessible au goût de tous. Du même coup, ces habitudes moins
mondaines amenaient un amoindrissement du rôle de la femme dans la
pensée masculine; elle n''était plus pour nous l''occupation galante de
toute notre existence, cette occupation qui était autrefois la carrière
du plus grand nombre, et, à la suite de cette modification dans les
mœurs, il arrivait ceci: c''est que l''intérêt de l''homme, s''en allant
de l''être charmant, se reportait en grande partie sur les jolis objets
inanimés dont la passion revêt un peu de la nature et du caractère
de l''amour. Au XVIIIe siècle, il n''y a pas de _bibeloteurs_ jeunes:
c''est là la différence des deux siècles. Pour notre génération, la
_bricabracomanie_ n''est qu''un bouche-trou de la femme qui ne possède
plus l''imagination de l''homme, et j''ai fait à mon égard cette remarque,
que, lorsque par hasard mon cœur s''est trouvé occupé, l''objet d''art ne
m''était de rien.

Oui, cette passion devenue générale, ce plaisir solitaire, auquel se
livre presque toute une nation, doit son développement au vide, à
l''ennui du cœur, et aussi, il faut le reconnaître, à la tristesse
des jours actuels, à l''incertitude des lendemains, à l''enfantement,
les pieds devant, de la société nouvelle, à des soucis et à des
préoccupations qui poussent, comme à la veille d''un déluge, les désirs
et les envies à se donner la jouissance immédiate de tout ce qui les
charme, les séduit, les tente: l''oubli du moment dans l''assouvissement
artistique.

Ce sont ces causes, et incontestablement l''éducation de l''œil des
gens du XIXe siècle, et encore un sentiment tout nouveau, la tendresse
presque humaine pour les _choses_, qui font, à l''heure qu''il est, de
presque tout le monde, des collectionneurs et de moi en particulier le
plus passionné de tous les collectionneurs.

Un riant pavé en marbre blanc et en marbre rouge du Languedoc, avec,
pour revêtement aux murs et au plafond, un cuir moderne peuplé de
perroquets fantastiques dorés et peints sur un fond vert d''eau.

Sur ce cuir, dans un désordre cherché, dans un pittoresque
d''antichambre et d''atelier, toutes sortes de choses voyantes et
claquantes, de brillants cuivres découpés, des poteries dorées, des
broderies du Japon et encore des objets bizarres, inattendus, étonnant
par leur originalité, leur exotisme, et vis-à-vis d''un certain nombre
desquels je me fais un peu l''effet du bon Père Buffier quand il disait:
«Voilà des choses que je ne sais pas, il faut que je fasse un livre
dessus.»

Ça, une petite jardinière à suspension, fabriquée d''une coloquinte
excentrique, dont la tige tournante et recroquevillée est une tige de
bronze qui a la flexibilité d''une liane; cette grande planchette fruste
de bois, toute parcourue des tortils d''un feuillage de lierre, exécuté
en nacre et en écaille: le porte-éventail qui tient dans l''appartement
l''éventail ouvert contre le mur; cette petite boule de porcelaine
jaune impérial si délicatement treillagée: la cage au grillon ou à
la mouche bourdonnante, que le Chinois aime suspendre au chevet de
son lit; et cette plaque de faïence figurant une branche de pêcher en
fleur, modelée à jour dans un cadre de bois en forme d''écran, vous
représente la décoration de l''angle religieux et mystique d''une chambre
de prostituée de maison de thé, l''espèce de tableau d''autel devant
lequel elle place une fleur dans un vase.

Des broderies du Japon, ai-je dit plus haut, c''est là, dans leurs
cadres de bambous, la riche, la splendide, l''_éclairante_ décoration
des murs du vestibule et un peu de toute la maison. Ces carrés de soie
brodés appelés _fusha_ ou _foukousa_ font la chatoyante couverture
sous laquelle on a l''habitude, dans l''Empire du Lever du Soleil,
d''envoyer tout présent quelconque, et le plus minime, fût-il même de
deux œufs[1]. Les anciens _foukousas_ fabriqués à Kioto[2] sont des
produits d''un art tout particulier au Japon, et auxquels l''Europe
ne peut rien opposer: de la peinture, de vrais tableaux composés
et exécutés en soie par un brodeur, où sur les fonds aux adorables
nuances, et telles qu''en donne le satin ou le crêpe, un oiseau, un
poisson, une fleur se détache dans le haut relief d''une broderie.
Et rien là dedans du travail d''un art mécanique, du dessin bête de
vieille fille de nos broderies à nous, mais des silhouettes d''êtres
pleins de vie, avec leurs pattes d''oiseau d''un si grand style, avec
leurs nageoires de poisson d''un si puissant contournement. Quelquefois
des parties peintes, peintes à l''encre de Chine, s''associent de la
manière la plus heureuse à la broderie. Je connais, chez Mme Auguste
Sichel, une fusée de fleurs brodée dans un vase en sparterie peint ou
imprimé, qui est bien la plus harmonieuse chose qu''il soit possible
de voir. M. de Nittis a fait un écran, d''un admirable et singulier
carré, où deux grues, brodées en noir sur un fond rose saumoné, ont,
comme accompagnement et adoucissement de la broderie, des demi-teintes
doucement lavées d''encre de Chine sur l''étoffe enchanteresse. Et dans
ce vestibule, il y a, sur un fond lilas, des carpes nageant au milieu
de branchages de presle brodées en or, et dont le ventre apparaît comme
argenté par un reflet de bourbe: un effet obtenu par une réserve au
milieu du fond tout teinté et obscuré d''encre de Chine. Il est même un
certain nombre de foukousas absolument peints. J''ai coloriée, sur un
crêpe gris, dans l''orbe d''un soleil rouge comme du feu, l''échancrure
pittoresque d''un passage de sept grues, exécuté avec la science que les
Japonais possèdent du vol de l''échassier. J''ai encore, jetées sur un
fond maïs, sans aucun détail de terrain, deux grandes grues blanches,
à la petite crête rougie de vermillon, au cou, aux pattes, à la queue,
teintés d''encre de Chine. Et ne vous étonnez pas de rencontrer si
souvent sur les broderies la grue, cet oiseau qui apparaît dans le
haut du ciel aux Japonais comme un messager céleste, et qu''ils saluent
de l''appellation: _O Tsouri Sama_, Sa Seigneurie la Grue.

[1] Il n''est guère besoin de dire que le carré est toujours
rapporté à son maître par le porteur du présent.

[2] Les foukousas modernes seraient aujourd''hui fabriqués à
Togané, d''où on les expédierait à Yedo.
'
);
commit;
"""

db = db_factory(init=init_script)

test_script = """
	set list on;
	set blob all;
	set term ^;
	execute block returns(s_new type of column test.s, b_new type of column test.b) as
		declare v_char type of column test.s;
		declare v_blob type of column test.b;
	begin
		select s, b from test rows 1 into v_char, v_blob;
		execute statement ( 'select ''|'' || replace(s, :x_blob, '''') || ''|'' s_empty, ''|'' || replace( b, :x_char, '''') || ''|'' b_empty '
							||' from test where s = :x_blob and b = :x_char'
							--                  ^       ^       ^       ^
							--                char     blob    blob    char
						  )
						  ( x_char := v_char,  x_blob := v_blob )
		into s_new, b_new;
		suspend;
	end
	^ set term ;^
    -- 2.5.0:
    -- Statement failed, SQLSTATE = 0A000
    -- Dynamic SQL Error
    -- -SQL error code = -303
    -- -feature is not supported
    -- -BLOB and array data types are not supported for move operation
    -- 2.5.1 and 2.5.2: client crash, "INET/inet_error: connect errno = 10061"
    -- 2.5.3 and later: works OK, but limit of varchar field is 8187 characters,
    -- otherwise get exception:
    -- Statement failed, SQLSTATE = 54000
    -- Dynamic SQL Error
    -- -SQL error code = -204
    -- -Implementation limit exceeded
    -- -block size exceeds implementation restriction
"""

act = isql_act('db', test_script, substitutions=[('B_NEW.*', '')])

expected_stdout = """
	S_NEW                           ||
	B_NEW                           0:f
	||
"""

@pytest.mark.version('>=3')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

