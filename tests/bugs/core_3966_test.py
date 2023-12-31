#coding:utf-8

"""
ID:          issue-4299
ISSUE:       4299
TITLE:       Creating a stored procedure with an "update or insert" statement with MATCHING fails
DESCRIPTION:
JIRA:        CORE-3966
FBTEST:      bugs.core_3966
"""

import pytest
from firebird.qa import *

db = db_factory(from_backup='employee-ods12.fbk')

test_script = """
    -- Table 'sales' for this SP is taken from standard samples database 'employee.fdb' which comes with every FB build.
    set term ^;
    create or alter procedure p_beteiligung_iu (
        gid char(36) character set iso8859_1 collate iso8859_1,
        gid_beteiligungs_verhaeltnis char(36) character set iso8859_1 collate iso8859_1,
        gid_vrinfo char(36) character set iso8859_1 collate iso8859_1,
        gid_agnr char(36) character set iso8859_1 collate iso8859_1,
        anteil numeric(18,3),
        ordernr integer,
        gueltig_ab date,
        gueltig_bis date,
        fuehrende_praemie char(1) character set iso8859_1 collate iso8859_1,
        fuehrende_courtage char(1) character set iso8859_1 collate iso8859_1,
        gid_zahlart char(36) character set iso8859_1 collate iso8859_1,
        gid_policen_beteiligte char(36) character set iso8859_1 collate iso8859_1,
        vsnrvr varchar(36) character set iso8859_1 collate iso8859_1,
        vsnr varchar(36) character set iso8859_1 collate iso8859_1
    )
    as
        declare variable von date;
        declare variable bis date;
        declare variable gid_policen char(36);
        declare variable gid_policen_or_detail char(36);
        declare variable alle_sollst_neumachen char(1);
        declare variable gid_beteiligung char(36);
        declare variable d char(1);
        declare variable po_number char(8);
        declare variable cust_no integer;
        declare variable sales_rep smallint;
        declare variable order_status varchar(7);
        declare variable order_date timestamp;
        declare variable ship_date timestamp;
        declare variable date_needed timestamp;
        declare variable paid char(1);
        declare variable qty_ordered integer;
        declare variable total_value decimal(9,2);
        declare variable discount float;
        declare variable item_type varchar(12);
        declare variable aged numeric(18,9);
    begin
      if (ordernr is null) then
      begin
        select max(b.qty_ordered) + 1
        from sales b
        where b.item_type = :gid_beteiligungs_verhaeltnis
        into :ordernr;
       end
      update or insert into sales (po_number, cust_no, sales_rep, order_status, order_date, ship_date, date_needed, paid,
                                   qty_ordered, total_value, discount, item_type)
      values (:po_number, :cust_no, :sales_rep, :order_status, :order_date, :ship_date, :date_needed, :paid, :qty_ordered,
              :total_value, :discount, :item_type)
      matching (po_number)
      returning (po_number)
      into :po_number;

    end
    ^
    -- from core-3968:
    create or alter procedure empiu (
        emp_no smallint,
        first_name varchar(15),
        last_name varchar(20),
        phone_ext varchar(4),
        hire_date timestamp,
        dept_no char(3),
        job_code varchar(5),
        job_grade smallint,
        job_country varchar(15),
        salary numeric(10,2),
        proj_id type of column project.proj_id)
    as
    begin
      select first 1 p.proj_id from project p where p.proj_id=:proj_id into :proj_id;
      update or insert into employee_project (emp_no, proj_id)
      values (:emp_no, :proj_id)
      matching (emp_no, proj_id);

      update or insert into employee (emp_no, first_name, last_name, phone_ext, hire_date, dept_no, job_code, job_grade,
                                      job_country, salary)
      values (:emp_no, :first_name, :last_name, :phone_ext, :hire_date, :dept_no, :job_code, :job_grade, :job_country,
              :salary)
      matching (emp_no);
    end
    ^
    set term ;^
    commit;

    drop procedure p_beteiligung_iu;
    drop procedure EMPIU;
    commit;
"""

act = isql_act('db', test_script)

@pytest.mark.version('>=3.0')
def test_1(act: Action):
    act.execute()
