#coding:utf-8

"""
ID:          issue-3254
ISSUE:       3254
TITLE:       View created from JOIN and LEFT JOIN doesnt order
DESCRIPTION:
JIRA:        CORE-2870
FBTEST:      bugs.core_2870
"""

import pytest
from firebird.qa import *

init_script = """
    recreate table employee(i int);
    recreate table department (i int);
    commit;

    recreate table country (
        country   varchar(15) not null
        ,currency  varchar(10) not null
    );

    recreate table department (
        dept_no     char(3) not null
        ,department  varchar(25) not null
        ,head_dept   char(3)
        ,mngr_no     smallint
        ,budget      decimal(12,2)
        ,location    varchar(15)
        ,phone_no    varchar(20) default '555-1234'
    );

    recreate table employee (
        emp_no       smallint not null
        ,first_name   varchar(15) not null
        ,last_name    varchar(20) not null
        ,phone_ext    varchar(4)
        ,hire_date    timestamp default 'now' not null
        ,dept_no      char(3) not null
        ,job_code     varchar(5) not null
        ,job_grade    smallint not null
        ,job_country  varchar(15) not null
        ,salary       numeric(10,2) not null
        ,full_name    computed by (last_name || ', ' || first_name)
    );

    create index namex on employee (last_name, first_name);
    create descending index budgetx on department (budget);
    commit;


    insert into country (country, currency) values ('usa', 'dollar');
    insert into country (country, currency) values ('england', 'pound');
    insert into country (country, currency) values ('canada', 'cdndlr');
    insert into country (country, currency) values ('switzerland', 'sfranc');
    insert into country (country, currency) values ('japan', 'yen');
    insert into country (country, currency) values ('italy', 'euro');
    insert into country (country, currency) values ('france', 'euro');
    insert into country (country, currency) values ('germany', 'euro');
    insert into country (country, currency) values ('australia', 'adollar');
    insert into country (country, currency) values ('hong kong', 'hkdollar');
    insert into country (country, currency) values ('netherlands', 'euro');
    insert into country (country, currency) values ('belgium', 'euro');
    insert into country (country, currency) values ('austria', 'euro');
    insert into country (country, currency) values ('fiji', 'fdollar');
    insert into country (country, currency) values ('russia', 'ruble');
    insert into country (country, currency) values ('romania', 'rleu');


    insert into department (dept_no, department, head_dept, mngr_no, budget, location, phone_no) values ('000', 'corporate headquarters', null, 105, 1000000, 'monterey', '(408) 555-1234');
    insert into department (dept_no, department, head_dept, mngr_no, budget, location, phone_no) values ('100', 'sales and marketing', '000', 85, 2000000, 'san francisco', '(415) 555-1234');
    insert into department (dept_no, department, head_dept, mngr_no, budget, location, phone_no) values ('600', 'engineering', '000', 2, 1100000, 'monterey', '(408) 555-1234');
    insert into department (dept_no, department, head_dept, mngr_no, budget, location, phone_no) values ('900', 'finance', '000', 46, 400000, 'monterey', '(408) 555-1234');
    insert into department (dept_no, department, head_dept, mngr_no, budget, location, phone_no) values ('180', 'marketing', '100', null, 1500000, 'san francisco', '(415) 555-1234');
    insert into department (dept_no, department, head_dept, mngr_no, budget, location, phone_no) values ('620', 'software products div.', '600', null, 1200000, 'monterey', '(408) 555-1234');
    insert into department (dept_no, department, head_dept, mngr_no, budget, location, phone_no) values ('621', 'software development', '620', null, 400000, 'monterey', '(408) 555-1234');
    insert into department (dept_no, department, head_dept, mngr_no, budget, location, phone_no) values ('622', 'quality assurance', '620', 9, 300000, 'monterey', '(408) 555-1234');
    insert into department (dept_no, department, head_dept, mngr_no, budget, location, phone_no) values ('623', 'customer support', '620', 15, 650000, 'monterey', '(408) 555-1234');
    insert into department (dept_no, department, head_dept, mngr_no, budget, location, phone_no) values ('670', 'consumer electronics div.', '600', 107, 1150000, 'burlington, vt', '(802) 555-1234');
    insert into department (dept_no, department, head_dept, mngr_no, budget, location, phone_no) values ('671', 'research and development', '670', 20, 460000, 'burlington, vt', '(802) 555-1234');
    insert into department (dept_no, department, head_dept, mngr_no, budget, location, phone_no) values ('672', 'customer services', '670', 94, 850000, 'burlington, vt', '(802) 555-1234');
    insert into department (dept_no, department, head_dept, mngr_no, budget, location, phone_no) values ('130', 'field office: east coast', '100', 11, 500000, 'boston', '(617) 555-1234');
    insert into department (dept_no, department, head_dept, mngr_no, budget, location, phone_no) values ('140', 'field office: canada', '100', 72, 500000, 'toronto', '(416) 677-1000');
    insert into department (dept_no, department, head_dept, mngr_no, budget, location, phone_no) values ('110', 'pacific rim headquarters', '100', 34, 600000, 'kuaui', '(808) 555-1234');
    insert into department (dept_no, department, head_dept, mngr_no, budget, location, phone_no) values ('115', 'field office: japan', '110', 118, 500000, 'tokyo', '3 5350 0901');
    insert into department (dept_no, department, head_dept, mngr_no, budget, location, phone_no) values ('116', 'field office: singapore', '110', null, 300000, 'singapore', '3 55 1234');
    insert into department (dept_no, department, head_dept, mngr_no, budget, location, phone_no) values ('120', 'european headquarters', '100', 36, 700000, 'london', '71 235-4400');
    insert into department (dept_no, department, head_dept, mngr_no, budget, location, phone_no) values ('121', 'field office: switzerland', '120', 141, 500000, 'zurich', '1 211 7767');
    insert into department (dept_no, department, head_dept, mngr_no, budget, location, phone_no) values ('123', 'field office: france', '120', 134, 400000, 'cannes', '58 68 11 12');
    insert into department (dept_no, department, head_dept, mngr_no, budget, location, phone_no) values ('125', 'field office: italy', '120', 121, 400000, 'milan', '2 430 39 39');


    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (2, 'robert', 'nelson', '250', '28-dec-1988 00:00:00', '600', 'vp', 2, 'usa', 105900);
    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (4, 'bruce', 'young', '233', '28-dec-1988 00:00:00', '621', 'eng', 2, 'usa', 97500);
    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (5, 'kim', 'lambert', '22', '6-feb-1989 00:00:00', '130', 'eng', 2, 'usa', 102750);
    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (8, 'leslie', 'johnson', '410', '5-apr-1989 00:00:00', '180', 'mktg', 3, 'usa', 64635);
    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (9, 'phil', 'forest', '229', '17-apr-1989 00:00:00', '622', 'mngr', 3, 'usa', 75060);
    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (11, 'k. j.', 'weston', '34', '17-jan-1990 00:00:00', '130', 'srep', 4, 'usa', 86292.94);
    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (12, 'terri', 'lee', '256', '1-may-1990 00:00:00', '000', 'admin', 4, 'usa', 53793);
    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (14, 'stewart', 'hall', '227', '4-jun-1990 00:00:00', '900', 'finan', 3, 'usa', 69482.63);
    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (15, 'katherine', 'young', '231', '14-jun-1990 00:00:00', '623', 'mngr', 3, 'usa', 67241.25);
    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (20, 'chris', 'papadopoulos', '887', '1-jan-1990 00:00:00', '671', 'mngr', 3, 'usa', 89655);
    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (24, 'pete', 'fisher', '888', '12-sep-1990 00:00:00', '671', 'eng', 3, 'usa', 81810.19);
    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (28, 'ann', 'bennet', '5', '1-feb-1991 00:00:00', '120', 'admin', 5, 'england', 22935);
    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (29, 'roger', 'de souza', '288', '18-feb-1991 00:00:00', '623', 'eng', 3, 'usa', 69482.63);
    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (34, 'janet', 'baldwin', '2', '21-mar-1991 00:00:00', '110', 'sales', 3, 'usa', 61637.81);
    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (36, 'roger', 'reeves', '6', '25-apr-1991 00:00:00', '120', 'sales', 3, 'england', 33620.63);
    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (37, 'willie', 'stansbury', '7', '25-apr-1991 00:00:00', '120', 'eng', 4, 'england', 39224.06);
    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (44, 'leslie', 'phong', '216', '3-jun-1991 00:00:00', '623', 'eng', 4, 'usa', 56034.38);
    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (45, 'ashok', 'ramanathan', '209', '1-aug-1991 00:00:00', '621', 'eng', 3, 'usa', 80689.5);
    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (46, 'walter', 'steadman', '210', '9-aug-1991 00:00:00', '900', 'cfo', 1, 'usa', 116100);
    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (52, 'carol', 'nordstrom', '420', '2-oct-1991 00:00:00', '180', 'prel', 4, 'usa', 42742.5);
    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (61, 'luke', 'leung', '3', '18-feb-1992 00:00:00', '110', 'srep', 4, 'usa', 68805);
    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (65, 'sue anne', 'o''brien', '877', '23-mar-1992 00:00:00', '670', 'admin', 5, 'usa', 31275);
    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (71, 'jennifer m.', 'burbank', '289', '15-apr-1992 00:00:00', '622', 'eng', 3, 'usa', 53167.5);
    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (72, 'claudia', 'sutherland', null, '20-apr-1992 00:00:00', '140', 'srep', 4, 'canada', 100914);
    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (83, 'dana', 'bishop', '290', '1-jun-1992 00:00:00', '621', 'eng', 3, 'usa', 62550);
    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (85, 'mary s.', 'macdonald', '477', '1-jun-1992 00:00:00', '100', 'vp', 2, 'usa', 111262.5);
    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (94, 'randy', 'williams', '892', '8-aug-1992 00:00:00', '672', 'mngr', 4, 'usa', 56295);
    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (105, 'oliver h.', 'bender', '255', '8-oct-1992 00:00:00', '000', 'ceo', 1, 'usa', 212850);
    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (107, 'kevin', 'cook', '894', '1-feb-1993 00:00:00', '670', 'dir', 2, 'usa', 111262.5);
    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (109, 'kelly', 'brown', '202', '4-feb-1993 00:00:00', '600', 'admin', 5, 'usa', 27000);
    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (110, 'yuki', 'ichida', '22', '4-feb-1993 00:00:00', '115', 'eng', 3, 'japan', 6000000);
    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (113, 'mary', 'page', '845', '12-apr-1993 00:00:00', '671', 'eng', 4, 'usa', 48000);
    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (114, 'bill', 'parker', '247', '1-jun-1993 00:00:00', '623', 'eng', 5, 'usa', 35000);
    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (118, 'takashi', 'yamamoto', '23', '1-jul-1993 00:00:00', '115', 'srep', 4, 'japan', 7480000);
    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (121, 'roberto', 'ferrari', '1', '12-jul-1993 00:00:00', '125', 'srep', 4, 'italy', 33000);
    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (127, 'michael', 'yanowski', '492', '9-aug-1993 00:00:00', '100', 'srep', 4, 'usa', 44000);
    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (134, 'jacques', 'glon', null, '23-aug-1993 00:00:00', '123', 'srep', 4, 'france', 38500);
    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (136, 'scott', 'johnson', '265', '13-sep-1993 00:00:00', '623', 'doc', 3, 'usa', 60000);
    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (138, 't.j.', 'green', '218', '1-nov-1993 00:00:00', '621', 'eng', 4, 'usa', 36000);
    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (141, 'pierre', 'osborne', null, '3-jan-1994 00:00:00', '121', 'srep', 4, 'switzerland', 110000);
    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (144, 'john', 'montgomery', '820', '30-mar-1994 00:00:00', '672', 'eng', 5, 'usa', 35000);
    insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade, job_country, salary) values (145, 'mark', 'guckenheimer', '221', '2-may-1994 00:00:00', '622', 'eng', 5, 'usa', 32000);
    commit;

    alter table country add primary key (country);
    alter table department add unique (department);
    alter table department add primary key (dept_no);
    alter table employee add primary key (emp_no);


    alter table employee add foreign key (dept_no) references department (dept_no);
    alter table department add foreign key (head_dept) references department (dept_no);
    alter table department add foreign key (mngr_no) references employee (emp_no);
    commit;

"""

db = db_factory(init=init_script)

test_script = """
    set list on;
    select distinct
        e.emp_no,
        e.first_name,
        e.last_name,
        e.phone_ext,
        e.hire_date,
        e.dept_no,
        e.job_code,
        e.job_grade,
        e.job_country,
        e.salary,
        e.full_name,
        d.department,
        d.head_dept,
        d.mngr_no,
        d.budget,
        d.location,
        d.phone_no,
        c.country,
        c.currency
    from employee e
    join department d on e.dept_no = d.dept_no
    left join country c on e.job_country = c.country
    ;
"""

act = isql_act('db', test_script)

expected_stdout = """
    EMP_NO                          2
    FIRST_NAME                      robert
    LAST_NAME                       nelson
    PHONE_EXT                       250
    HIRE_DATE                       1988-12-28 00:00:00.0000
    DEPT_NO                         600
    JOB_CODE                        vp
    JOB_GRADE                       2
    JOB_COUNTRY                     usa
    SALARY                          105900.00
    FULL_NAME                       nelson, robert
    DEPARTMENT                      engineering
    HEAD_DEPT                       000
    MNGR_NO                         2
    BUDGET                          1100000.00
    LOCATION                        monterey
    PHONE_NO                        (408) 555-1234
    COUNTRY                         usa
    CURRENCY                        dollar

    EMP_NO                          4
    FIRST_NAME                      bruce
    LAST_NAME                       young
    PHONE_EXT                       233
    HIRE_DATE                       1988-12-28 00:00:00.0000
    DEPT_NO                         621
    JOB_CODE                        eng
    JOB_GRADE                       2
    JOB_COUNTRY                     usa
    SALARY                          97500.00
    FULL_NAME                       young, bruce
    DEPARTMENT                      software development
    HEAD_DEPT                       620
    MNGR_NO                         <null>
    BUDGET                          400000.00
    LOCATION                        monterey
    PHONE_NO                        (408) 555-1234
    COUNTRY                         usa
    CURRENCY                        dollar

    EMP_NO                          5
    FIRST_NAME                      kim
    LAST_NAME                       lambert
    PHONE_EXT                       22
    HIRE_DATE                       1989-02-06 00:00:00.0000
    DEPT_NO                         130
    JOB_CODE                        eng
    JOB_GRADE                       2
    JOB_COUNTRY                     usa
    SALARY                          102750.00
    FULL_NAME                       lambert, kim
    DEPARTMENT                      field office: east coast
    HEAD_DEPT                       100
    MNGR_NO                         11
    BUDGET                          500000.00
    LOCATION                        boston
    PHONE_NO                        (617) 555-1234
    COUNTRY                         usa
    CURRENCY                        dollar

    EMP_NO                          8
    FIRST_NAME                      leslie
    LAST_NAME                       johnson
    PHONE_EXT                       410
    HIRE_DATE                       1989-04-05 00:00:00.0000
    DEPT_NO                         180
    JOB_CODE                        mktg
    JOB_GRADE                       3
    JOB_COUNTRY                     usa
    SALARY                          64635.00
    FULL_NAME                       johnson, leslie
    DEPARTMENT                      marketing
    HEAD_DEPT                       100
    MNGR_NO                         <null>
    BUDGET                          1500000.00
    LOCATION                        san francisco
    PHONE_NO                        (415) 555-1234
    COUNTRY                         usa
    CURRENCY                        dollar

    EMP_NO                          9
    FIRST_NAME                      phil
    LAST_NAME                       forest
    PHONE_EXT                       229
    HIRE_DATE                       1989-04-17 00:00:00.0000
    DEPT_NO                         622
    JOB_CODE                        mngr
    JOB_GRADE                       3
    JOB_COUNTRY                     usa
    SALARY                          75060.00
    FULL_NAME                       forest, phil
    DEPARTMENT                      quality assurance
    HEAD_DEPT                       620
    MNGR_NO                         9
    BUDGET                          300000.00
    LOCATION                        monterey
    PHONE_NO                        (408) 555-1234
    COUNTRY                         usa
    CURRENCY                        dollar

    EMP_NO                          11
    FIRST_NAME                      k. j.
    LAST_NAME                       weston
    PHONE_EXT                       34
    HIRE_DATE                       1990-01-17 00:00:00.0000
    DEPT_NO                         130
    JOB_CODE                        srep
    JOB_GRADE                       4
    JOB_COUNTRY                     usa
    SALARY                          86292.94
    FULL_NAME                       weston, k. j.
    DEPARTMENT                      field office: east coast
    HEAD_DEPT                       100
    MNGR_NO                         11
    BUDGET                          500000.00
    LOCATION                        boston
    PHONE_NO                        (617) 555-1234
    COUNTRY                         usa
    CURRENCY                        dollar

    EMP_NO                          12
    FIRST_NAME                      terri
    LAST_NAME                       lee
    PHONE_EXT                       256
    HIRE_DATE                       1990-05-01 00:00:00.0000
    DEPT_NO                         000
    JOB_CODE                        admin
    JOB_GRADE                       4
    JOB_COUNTRY                     usa
    SALARY                          53793.00
    FULL_NAME                       lee, terri
    DEPARTMENT                      corporate headquarters
    HEAD_DEPT                       <null>
    MNGR_NO                         105
    BUDGET                          1000000.00
    LOCATION                        monterey
    PHONE_NO                        (408) 555-1234
    COUNTRY                         usa
    CURRENCY                        dollar

    EMP_NO                          14
    FIRST_NAME                      stewart
    LAST_NAME                       hall
    PHONE_EXT                       227
    HIRE_DATE                       1990-06-04 00:00:00.0000
    DEPT_NO                         900
    JOB_CODE                        finan
    JOB_GRADE                       3
    JOB_COUNTRY                     usa
    SALARY                          69482.63
    FULL_NAME                       hall, stewart
    DEPARTMENT                      finance
    HEAD_DEPT                       000
    MNGR_NO                         46
    BUDGET                          400000.00
    LOCATION                        monterey
    PHONE_NO                        (408) 555-1234
    COUNTRY                         usa
    CURRENCY                        dollar

    EMP_NO                          15
    FIRST_NAME                      katherine
    LAST_NAME                       young
    PHONE_EXT                       231
    HIRE_DATE                       1990-06-14 00:00:00.0000
    DEPT_NO                         623
    JOB_CODE                        mngr
    JOB_GRADE                       3
    JOB_COUNTRY                     usa
    SALARY                          67241.25
    FULL_NAME                       young, katherine
    DEPARTMENT                      customer support
    HEAD_DEPT                       620
    MNGR_NO                         15
    BUDGET                          650000.00
    LOCATION                        monterey
    PHONE_NO                        (408) 555-1234
    COUNTRY                         usa
    CURRENCY                        dollar

    EMP_NO                          20
    FIRST_NAME                      chris
    LAST_NAME                       papadopoulos
    PHONE_EXT                       887
    HIRE_DATE                       1990-01-01 00:00:00.0000
    DEPT_NO                         671
    JOB_CODE                        mngr
    JOB_GRADE                       3
    JOB_COUNTRY                     usa
    SALARY                          89655.00
    FULL_NAME                       papadopoulos, chris
    DEPARTMENT                      research and development
    HEAD_DEPT                       670
    MNGR_NO                         20
    BUDGET                          460000.00
    LOCATION                        burlington, vt
    PHONE_NO                        (802) 555-1234
    COUNTRY                         usa
    CURRENCY                        dollar

    EMP_NO                          24
    FIRST_NAME                      pete
    LAST_NAME                       fisher
    PHONE_EXT                       888
    HIRE_DATE                       1990-09-12 00:00:00.0000
    DEPT_NO                         671
    JOB_CODE                        eng
    JOB_GRADE                       3
    JOB_COUNTRY                     usa
    SALARY                          81810.19
    FULL_NAME                       fisher, pete
    DEPARTMENT                      research and development
    HEAD_DEPT                       670
    MNGR_NO                         20
    BUDGET                          460000.00
    LOCATION                        burlington, vt
    PHONE_NO                        (802) 555-1234
    COUNTRY                         usa
    CURRENCY                        dollar

    EMP_NO                          28
    FIRST_NAME                      ann
    LAST_NAME                       bennet
    PHONE_EXT                       5
    HIRE_DATE                       1991-02-01 00:00:00.0000
    DEPT_NO                         120
    JOB_CODE                        admin
    JOB_GRADE                       5
    JOB_COUNTRY                     england
    SALARY                          22935.00
    FULL_NAME                       bennet, ann
    DEPARTMENT                      european headquarters
    HEAD_DEPT                       100
    MNGR_NO                         36
    BUDGET                          700000.00
    LOCATION                        london
    PHONE_NO                        71 235-4400
    COUNTRY                         england
    CURRENCY                        pound

    EMP_NO                          29
    FIRST_NAME                      roger
    LAST_NAME                       de souza
    PHONE_EXT                       288
    HIRE_DATE                       1991-02-18 00:00:00.0000
    DEPT_NO                         623
    JOB_CODE                        eng
    JOB_GRADE                       3
    JOB_COUNTRY                     usa
    SALARY                          69482.63
    FULL_NAME                       de souza, roger
    DEPARTMENT                      customer support
    HEAD_DEPT                       620
    MNGR_NO                         15
    BUDGET                          650000.00
    LOCATION                        monterey
    PHONE_NO                        (408) 555-1234
    COUNTRY                         usa
    CURRENCY                        dollar

    EMP_NO                          34
    FIRST_NAME                      janet
    LAST_NAME                       baldwin
    PHONE_EXT                       2
    HIRE_DATE                       1991-03-21 00:00:00.0000
    DEPT_NO                         110
    JOB_CODE                        sales
    JOB_GRADE                       3
    JOB_COUNTRY                     usa
    SALARY                          61637.81
    FULL_NAME                       baldwin, janet
    DEPARTMENT                      pacific rim headquarters
    HEAD_DEPT                       100
    MNGR_NO                         34
    BUDGET                          600000.00
    LOCATION                        kuaui
    PHONE_NO                        (808) 555-1234
    COUNTRY                         usa
    CURRENCY                        dollar

    EMP_NO                          36
    FIRST_NAME                      roger
    LAST_NAME                       reeves
    PHONE_EXT                       6
    HIRE_DATE                       1991-04-25 00:00:00.0000
    DEPT_NO                         120
    JOB_CODE                        sales
    JOB_GRADE                       3
    JOB_COUNTRY                     england
    SALARY                          33620.63
    FULL_NAME                       reeves, roger
    DEPARTMENT                      european headquarters
    HEAD_DEPT                       100
    MNGR_NO                         36
    BUDGET                          700000.00
    LOCATION                        london
    PHONE_NO                        71 235-4400
    COUNTRY                         england
    CURRENCY                        pound

    EMP_NO                          37
    FIRST_NAME                      willie
    LAST_NAME                       stansbury
    PHONE_EXT                       7
    HIRE_DATE                       1991-04-25 00:00:00.0000
    DEPT_NO                         120
    JOB_CODE                        eng
    JOB_GRADE                       4
    JOB_COUNTRY                     england
    SALARY                          39224.06
    FULL_NAME                       stansbury, willie
    DEPARTMENT                      european headquarters
    HEAD_DEPT                       100
    MNGR_NO                         36
    BUDGET                          700000.00
    LOCATION                        london
    PHONE_NO                        71 235-4400
    COUNTRY                         england
    CURRENCY                        pound

    EMP_NO                          44
    FIRST_NAME                      leslie
    LAST_NAME                       phong
    PHONE_EXT                       216
    HIRE_DATE                       1991-06-03 00:00:00.0000
    DEPT_NO                         623
    JOB_CODE                        eng
    JOB_GRADE                       4
    JOB_COUNTRY                     usa
    SALARY                          56034.38
    FULL_NAME                       phong, leslie
    DEPARTMENT                      customer support
    HEAD_DEPT                       620
    MNGR_NO                         15
    BUDGET                          650000.00
    LOCATION                        monterey
    PHONE_NO                        (408) 555-1234
    COUNTRY                         usa
    CURRENCY                        dollar

    EMP_NO                          45
    FIRST_NAME                      ashok
    LAST_NAME                       ramanathan
    PHONE_EXT                       209
    HIRE_DATE                       1991-08-01 00:00:00.0000
    DEPT_NO                         621
    JOB_CODE                        eng
    JOB_GRADE                       3
    JOB_COUNTRY                     usa
    SALARY                          80689.50
    FULL_NAME                       ramanathan, ashok
    DEPARTMENT                      software development
    HEAD_DEPT                       620
    MNGR_NO                         <null>
    BUDGET                          400000.00
    LOCATION                        monterey
    PHONE_NO                        (408) 555-1234
    COUNTRY                         usa
    CURRENCY                        dollar

    EMP_NO                          46
    FIRST_NAME                      walter
    LAST_NAME                       steadman
    PHONE_EXT                       210
    HIRE_DATE                       1991-08-09 00:00:00.0000
    DEPT_NO                         900
    JOB_CODE                        cfo
    JOB_GRADE                       1
    JOB_COUNTRY                     usa
    SALARY                          116100.00
    FULL_NAME                       steadman, walter
    DEPARTMENT                      finance
    HEAD_DEPT                       000
    MNGR_NO                         46
    BUDGET                          400000.00
    LOCATION                        monterey
    PHONE_NO                        (408) 555-1234
    COUNTRY                         usa
    CURRENCY                        dollar

    EMP_NO                          52
    FIRST_NAME                      carol
    LAST_NAME                       nordstrom
    PHONE_EXT                       420
    HIRE_DATE                       1991-10-02 00:00:00.0000
    DEPT_NO                         180
    JOB_CODE                        prel
    JOB_GRADE                       4
    JOB_COUNTRY                     usa
    SALARY                          42742.50
    FULL_NAME                       nordstrom, carol
    DEPARTMENT                      marketing
    HEAD_DEPT                       100
    MNGR_NO                         <null>
    BUDGET                          1500000.00
    LOCATION                        san francisco
    PHONE_NO                        (415) 555-1234
    COUNTRY                         usa
    CURRENCY                        dollar

    EMP_NO                          61
    FIRST_NAME                      luke
    LAST_NAME                       leung
    PHONE_EXT                       3
    HIRE_DATE                       1992-02-18 00:00:00.0000
    DEPT_NO                         110
    JOB_CODE                        srep
    JOB_GRADE                       4
    JOB_COUNTRY                     usa
    SALARY                          68805.00
    FULL_NAME                       leung, luke
    DEPARTMENT                      pacific rim headquarters
    HEAD_DEPT                       100
    MNGR_NO                         34
    BUDGET                          600000.00
    LOCATION                        kuaui
    PHONE_NO                        (808) 555-1234
    COUNTRY                         usa
    CURRENCY                        dollar

    EMP_NO                          65
    FIRST_NAME                      sue anne
    LAST_NAME                       o'brien
    PHONE_EXT                       877
    HIRE_DATE                       1992-03-23 00:00:00.0000
    DEPT_NO                         670
    JOB_CODE                        admin
    JOB_GRADE                       5
    JOB_COUNTRY                     usa
    SALARY                          31275.00
    FULL_NAME                       o'brien, sue anne
    DEPARTMENT                      consumer electronics div.
    HEAD_DEPT                       600
    MNGR_NO                         107
    BUDGET                          1150000.00
    LOCATION                        burlington, vt
    PHONE_NO                        (802) 555-1234
    COUNTRY                         usa
    CURRENCY                        dollar

    EMP_NO                          71
    FIRST_NAME                      jennifer m.
    LAST_NAME                       burbank
    PHONE_EXT                       289
    HIRE_DATE                       1992-04-15 00:00:00.0000
    DEPT_NO                         622
    JOB_CODE                        eng
    JOB_GRADE                       3
    JOB_COUNTRY                     usa
    SALARY                          53167.50
    FULL_NAME                       burbank, jennifer m.
    DEPARTMENT                      quality assurance
    HEAD_DEPT                       620
    MNGR_NO                         9
    BUDGET                          300000.00
    LOCATION                        monterey
    PHONE_NO                        (408) 555-1234
    COUNTRY                         usa
    CURRENCY                        dollar

    EMP_NO                          72
    FIRST_NAME                      claudia
    LAST_NAME                       sutherland
    PHONE_EXT                       <null>
    HIRE_DATE                       1992-04-20 00:00:00.0000
    DEPT_NO                         140
    JOB_CODE                        srep
    JOB_GRADE                       4
    JOB_COUNTRY                     canada
    SALARY                          100914.00
    FULL_NAME                       sutherland, claudia
    DEPARTMENT                      field office: canada
    HEAD_DEPT                       100
    MNGR_NO                         72
    BUDGET                          500000.00
    LOCATION                        toronto
    PHONE_NO                        (416) 677-1000
    COUNTRY                         canada
    CURRENCY                        cdndlr

    EMP_NO                          83
    FIRST_NAME                      dana
    LAST_NAME                       bishop
    PHONE_EXT                       290
    HIRE_DATE                       1992-06-01 00:00:00.0000
    DEPT_NO                         621
    JOB_CODE                        eng
    JOB_GRADE                       3
    JOB_COUNTRY                     usa
    SALARY                          62550.00
    FULL_NAME                       bishop, dana
    DEPARTMENT                      software development
    HEAD_DEPT                       620
    MNGR_NO                         <null>
    BUDGET                          400000.00
    LOCATION                        monterey
    PHONE_NO                        (408) 555-1234
    COUNTRY                         usa
    CURRENCY                        dollar

    EMP_NO                          85
    FIRST_NAME                      mary s.
    LAST_NAME                       macdonald
    PHONE_EXT                       477
    HIRE_DATE                       1992-06-01 00:00:00.0000
    DEPT_NO                         100
    JOB_CODE                        vp
    JOB_GRADE                       2
    JOB_COUNTRY                     usa
    SALARY                          111262.50
    FULL_NAME                       macdonald, mary s.
    DEPARTMENT                      sales and marketing
    HEAD_DEPT                       000
    MNGR_NO                         85
    BUDGET                          2000000.00
    LOCATION                        san francisco
    PHONE_NO                        (415) 555-1234
    COUNTRY                         usa
    CURRENCY                        dollar

    EMP_NO                          94
    FIRST_NAME                      randy
    LAST_NAME                       williams
    PHONE_EXT                       892
    HIRE_DATE                       1992-08-08 00:00:00.0000
    DEPT_NO                         672
    JOB_CODE                        mngr
    JOB_GRADE                       4
    JOB_COUNTRY                     usa
    SALARY                          56295.00
    FULL_NAME                       williams, randy
    DEPARTMENT                      customer services
    HEAD_DEPT                       670
    MNGR_NO                         94
    BUDGET                          850000.00
    LOCATION                        burlington, vt
    PHONE_NO                        (802) 555-1234
    COUNTRY                         usa
    CURRENCY                        dollar

    EMP_NO                          105
    FIRST_NAME                      oliver h.
    LAST_NAME                       bender
    PHONE_EXT                       255
    HIRE_DATE                       1992-10-08 00:00:00.0000
    DEPT_NO                         000
    JOB_CODE                        ceo
    JOB_GRADE                       1
    JOB_COUNTRY                     usa
    SALARY                          212850.00
    FULL_NAME                       bender, oliver h.
    DEPARTMENT                      corporate headquarters
    HEAD_DEPT                       <null>
    MNGR_NO                         105
    BUDGET                          1000000.00
    LOCATION                        monterey
    PHONE_NO                        (408) 555-1234
    COUNTRY                         usa
    CURRENCY                        dollar

    EMP_NO                          107
    FIRST_NAME                      kevin
    LAST_NAME                       cook
    PHONE_EXT                       894
    HIRE_DATE                       1993-02-01 00:00:00.0000
    DEPT_NO                         670
    JOB_CODE                        dir
    JOB_GRADE                       2
    JOB_COUNTRY                     usa
    SALARY                          111262.50
    FULL_NAME                       cook, kevin
    DEPARTMENT                      consumer electronics div.
    HEAD_DEPT                       600
    MNGR_NO                         107
    BUDGET                          1150000.00
    LOCATION                        burlington, vt
    PHONE_NO                        (802) 555-1234
    COUNTRY                         usa
    CURRENCY                        dollar

    EMP_NO                          109
    FIRST_NAME                      kelly
    LAST_NAME                       brown
    PHONE_EXT                       202
    HIRE_DATE                       1993-02-04 00:00:00.0000
    DEPT_NO                         600
    JOB_CODE                        admin
    JOB_GRADE                       5
    JOB_COUNTRY                     usa
    SALARY                          27000.00
    FULL_NAME                       brown, kelly
    DEPARTMENT                      engineering
    HEAD_DEPT                       000
    MNGR_NO                         2
    BUDGET                          1100000.00
    LOCATION                        monterey
    PHONE_NO                        (408) 555-1234
    COUNTRY                         usa
    CURRENCY                        dollar

    EMP_NO                          110
    FIRST_NAME                      yuki
    LAST_NAME                       ichida
    PHONE_EXT                       22
    HIRE_DATE                       1993-02-04 00:00:00.0000
    DEPT_NO                         115
    JOB_CODE                        eng
    JOB_GRADE                       3
    JOB_COUNTRY                     japan
    SALARY                          6000000.00
    FULL_NAME                       ichida, yuki
    DEPARTMENT                      field office: japan
    HEAD_DEPT                       110
    MNGR_NO                         118
    BUDGET                          500000.00
    LOCATION                        tokyo
    PHONE_NO                        3 5350 0901
    COUNTRY                         japan
    CURRENCY                        yen

    EMP_NO                          113
    FIRST_NAME                      mary
    LAST_NAME                       page
    PHONE_EXT                       845
    HIRE_DATE                       1993-04-12 00:00:00.0000
    DEPT_NO                         671
    JOB_CODE                        eng
    JOB_GRADE                       4
    JOB_COUNTRY                     usa
    SALARY                          48000.00
    FULL_NAME                       page, mary
    DEPARTMENT                      research and development
    HEAD_DEPT                       670
    MNGR_NO                         20
    BUDGET                          460000.00
    LOCATION                        burlington, vt
    PHONE_NO                        (802) 555-1234
    COUNTRY                         usa
    CURRENCY                        dollar

    EMP_NO                          114
    FIRST_NAME                      bill
    LAST_NAME                       parker
    PHONE_EXT                       247
    HIRE_DATE                       1993-06-01 00:00:00.0000
    DEPT_NO                         623
    JOB_CODE                        eng
    JOB_GRADE                       5
    JOB_COUNTRY                     usa
    SALARY                          35000.00
    FULL_NAME                       parker, bill
    DEPARTMENT                      customer support
    HEAD_DEPT                       620
    MNGR_NO                         15
    BUDGET                          650000.00
    LOCATION                        monterey
    PHONE_NO                        (408) 555-1234
    COUNTRY                         usa
    CURRENCY                        dollar

    EMP_NO                          118
    FIRST_NAME                      takashi
    LAST_NAME                       yamamoto
    PHONE_EXT                       23
    HIRE_DATE                       1993-07-01 00:00:00.0000
    DEPT_NO                         115
    JOB_CODE                        srep
    JOB_GRADE                       4
    JOB_COUNTRY                     japan
    SALARY                          7480000.00
    FULL_NAME                       yamamoto, takashi
    DEPARTMENT                      field office: japan
    HEAD_DEPT                       110
    MNGR_NO                         118
    BUDGET                          500000.00
    LOCATION                        tokyo
    PHONE_NO                        3 5350 0901
    COUNTRY                         japan
    CURRENCY                        yen

    EMP_NO                          121
    FIRST_NAME                      roberto
    LAST_NAME                       ferrari
    PHONE_EXT                       1
    HIRE_DATE                       1993-07-12 00:00:00.0000
    DEPT_NO                         125
    JOB_CODE                        srep
    JOB_GRADE                       4
    JOB_COUNTRY                     italy
    SALARY                          33000.00
    FULL_NAME                       ferrari, roberto
    DEPARTMENT                      field office: italy
    HEAD_DEPT                       120
    MNGR_NO                         121
    BUDGET                          400000.00
    LOCATION                        milan
    PHONE_NO                        2 430 39 39
    COUNTRY                         italy
    CURRENCY                        euro

    EMP_NO                          127
    FIRST_NAME                      michael
    LAST_NAME                       yanowski
    PHONE_EXT                       492
    HIRE_DATE                       1993-08-09 00:00:00.0000
    DEPT_NO                         100
    JOB_CODE                        srep
    JOB_GRADE                       4
    JOB_COUNTRY                     usa
    SALARY                          44000.00
    FULL_NAME                       yanowski, michael
    DEPARTMENT                      sales and marketing
    HEAD_DEPT                       000
    MNGR_NO                         85
    BUDGET                          2000000.00
    LOCATION                        san francisco
    PHONE_NO                        (415) 555-1234
    COUNTRY                         usa
    CURRENCY                        dollar

    EMP_NO                          134
    FIRST_NAME                      jacques
    LAST_NAME                       glon
    PHONE_EXT                       <null>
    HIRE_DATE                       1993-08-23 00:00:00.0000
    DEPT_NO                         123
    JOB_CODE                        srep
    JOB_GRADE                       4
    JOB_COUNTRY                     france
    SALARY                          38500.00
    FULL_NAME                       glon, jacques
    DEPARTMENT                      field office: france
    HEAD_DEPT                       120
    MNGR_NO                         134
    BUDGET                          400000.00
    LOCATION                        cannes
    PHONE_NO                        58 68 11 12
    COUNTRY                         france
    CURRENCY                        euro

    EMP_NO                          136
    FIRST_NAME                      scott
    LAST_NAME                       johnson
    PHONE_EXT                       265
    HIRE_DATE                       1993-09-13 00:00:00.0000
    DEPT_NO                         623
    JOB_CODE                        doc
    JOB_GRADE                       3
    JOB_COUNTRY                     usa
    SALARY                          60000.00
    FULL_NAME                       johnson, scott
    DEPARTMENT                      customer support
    HEAD_DEPT                       620
    MNGR_NO                         15
    BUDGET                          650000.00
    LOCATION                        monterey
    PHONE_NO                        (408) 555-1234
    COUNTRY                         usa
    CURRENCY                        dollar

    EMP_NO                          138
    FIRST_NAME                      t.j.
    LAST_NAME                       green
    PHONE_EXT                       218
    HIRE_DATE                       1993-11-01 00:00:00.0000
    DEPT_NO                         621
    JOB_CODE                        eng
    JOB_GRADE                       4
    JOB_COUNTRY                     usa
    SALARY                          36000.00
    FULL_NAME                       green, t.j.
    DEPARTMENT                      software development
    HEAD_DEPT                       620
    MNGR_NO                         <null>
    BUDGET                          400000.00
    LOCATION                        monterey
    PHONE_NO                        (408) 555-1234
    COUNTRY                         usa
    CURRENCY                        dollar

    EMP_NO                          141
    FIRST_NAME                      pierre
    LAST_NAME                       osborne
    PHONE_EXT                       <null>
    HIRE_DATE                       1994-01-03 00:00:00.0000
    DEPT_NO                         121
    JOB_CODE                        srep
    JOB_GRADE                       4
    JOB_COUNTRY                     switzerland
    SALARY                          110000.00
    FULL_NAME                       osborne, pierre
    DEPARTMENT                      field office: switzerland
    HEAD_DEPT                       120
    MNGR_NO                         141
    BUDGET                          500000.00
    LOCATION                        zurich
    PHONE_NO                        1 211 7767
    COUNTRY                         switzerland
    CURRENCY                        sfranc

    EMP_NO                          144
    FIRST_NAME                      john
    LAST_NAME                       montgomery
    PHONE_EXT                       820
    HIRE_DATE                       1994-03-30 00:00:00.0000
    DEPT_NO                         672
    JOB_CODE                        eng
    JOB_GRADE                       5
    JOB_COUNTRY                     usa
    SALARY                          35000.00
    FULL_NAME                       montgomery, john
    DEPARTMENT                      customer services
    HEAD_DEPT                       670
    MNGR_NO                         94
    BUDGET                          850000.00
    LOCATION                        burlington, vt
    PHONE_NO                        (802) 555-1234
    COUNTRY                         usa
    CURRENCY                        dollar

    EMP_NO                          145
    FIRST_NAME                      mark
    LAST_NAME                       guckenheimer
    PHONE_EXT                       221
    HIRE_DATE                       1994-05-02 00:00:00.0000
    DEPT_NO                         622
    JOB_CODE                        eng
    JOB_GRADE                       5
    JOB_COUNTRY                     usa
    SALARY                          32000.00
    FULL_NAME                       guckenheimer, mark
    DEPARTMENT                      quality assurance
    HEAD_DEPT                       620
    MNGR_NO                         9
    BUDGET                          300000.00
    LOCATION                        monterey
    PHONE_NO                        (408) 555-1234
    COUNTRY                         usa
    CURRENCY                        dollar
"""

@pytest.mark.version('>=3')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout

