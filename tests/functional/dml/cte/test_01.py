#coding:utf-8

"""
ID:          dml.cte-01
TITLE:       Non-Recursive CTEs
FBTEST:      functional.dml.cte.01
DESCRIPTION:
  Rules for Non-Recursive CTEs :
  - Multiple table expressions can be defined in one query
  - Any clause legal in a SELECT specification is legal in table expressions
  - Table expressions can reference one another
  - References between expressions should not have loops
  - Table expressions can be used within any part of the main query or another table expression
  - The same table expression can be used more than once in the main query
  - Table expressions (as subqueries) can be used in INSERT, UPDATE and DELETE statements
  - Table expressions are legal in PSQL code
  - WITH statements can not be nested
"""

import pytest
from firebird.qa import *

init_script = """
		CREATE TABLE employee( id_employee INTEGER , prenom VARCHAR(20) ,id_department INTEGER,age INTEGER ,  PRIMARY KEY(id_employee));

		CREATE TABLE department(id_department INTEGER, name VARCHAR(20));

		INSERT INTO department(id_department, name) values(1,'service compta');
		INSERT INTO department(id_department, name) values(2,'production');
		INSERT INTO employee(id_employee, prenom,id_department,age) VALUES (1,'benoit',1 , 30 );
		INSERT INTO employee(id_employee, prenom,id_department,age) VALUES (2,'ludivine',1 , 30 );
		INSERT INTO employee(id_employee, prenom,id_department,age) VALUES (3,'michel',1 , 27 );
		INSERT INTO employee(id_employee, prenom,id_department,age) VALUES (4,'Gilbert',1 , 42 );
		INSERT INTO employee(id_employee, prenom,id_department,age) VALUES (5,'tom',2 ,23);
		INSERT INTO employee(id_employee, prenom,id_department,age) VALUES (6,'jacque',2,44 );
		INSERT INTO employee(id_employee, prenom,id_department,age) VALUES (7,'justine',2,30 );
		INSERT INTO employee(id_employee, prenom,id_department,age) VALUES (8,'martine',2,31 );
INSERT INTO employee(id_employee, prenom,id_department,age) VALUES (9,'noemie',2,39 );

"""

db = db_factory(init=init_script)

test_script = """WITH
  repartition_by_age AS (
SELECT age/10 as trancheage , id_department,
        COUNT(1) AS nombre
      FROM employee
    GROUP BY age/10, id_department
)
select d.name , jeune.nombre as jeune , trentenaire.nombre as trentenaire, quarentenaire.nombre as quantenaire
from department d
left join repartition_by_age jeune
on d.id_department = jeune.id_department
and jeune.trancheage = 2
left join repartition_by_age trentenaire
on d.id_department = trentenaire.id_department
and trentenaire.trancheage = 3
left join repartition_by_age quarentenaire
on d.id_department = quarentenaire.id_department
and quarentenaire.trancheage = 4 ;

"""

act = isql_act('db', test_script)

expected_stdout = """
NAME                                 JEUNE           TRENTENAIRE           QUANTENAIRE
==================== ===================== ===================== =====================
service compta                           1                     2                     1
production                               1                     3                     1
"""

@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
