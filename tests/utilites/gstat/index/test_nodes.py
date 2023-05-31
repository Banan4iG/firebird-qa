#coding:utf-8
"""
ID:          utilites.gstat.index.nodes
TITLE:       Check number of the index nodes. 
DESCRIPTION: 
NOTES:
"""

import pytest
from firebird.qa import *
from pathlib import Path
import string

METRIC = 'nodes'

PAGE_SIZE = 4096
FIELD_WIDTH = 100

db = db_factory(page_size=PAGE_SIZE)

act = python_act('db')

init_script = f"""
    create table TEST (id int, str char({FIELD_WIDTH}));
    commit;
"""

id = 0

for lower in string.ascii_lowercase:
    for upper in string.ascii_lowercase:
        for digit in string.digits: 
            temp_string = (lower + upper + digit)*30
            temp_script = f"""
                insert into TEST values({id}, '{temp_string}');
            """
            init_script += temp_script
            id += 1
init_script += """
    commit;
    create INDEX IDX_TEST on TEST(STR);
    commit;
"""   

conf = store_config('databases.conf')
new_config = temp_file('new_databases.conf')

@pytest.mark.version('>=3.0')
def test_no_records(act: Action, gstat_helpers):   
    with act.db.connect() as con:
        con.execute_immediate(f"create TABLE TEST(STR CHAR({FIELD_WIDTH}));")
        con.commit()
        con.execute_immediate(f"create INDEX IDX_TEST on TEST(STR);")
        con.commit()

    act.gstat(switches=['-i'])
    nodes = gstat_helpers.get_stat(act.stdout, 'TEST', METRIC)
    assert nodes == 0

@pytest.mark.version('>=3.0')
def test_without_deleted_records(act: Action, gstat_helpers):   
    
    act.isql(switches=[], input=init_script)
    act.reset()

    act.gstat(switches=['-i'])
    nodes = gstat_helpers.get_stat(act.stdout, 'TEST', METRIC)
    assert nodes == 6760

@pytest.mark.version('>=3.0')
def test_with_sweep(act: Action, gstat_helpers, conf: ConfigManager, new_config: Path):   
    databases_conf=f"""
    gstat_total_versions = {act.db.db_path}
    {{
        GCPolicy=cooperative
    }}
    """
    new_config.write_text(databases_conf)
    conf.replace(new_config)

    act.isql(switches=[], input=init_script)
    act.reset()

    with act.db.connect() as con:
        con.execute_immediate(f"DELETE FROM TEST WHERE ID < 760 ;")
        con.commit()

    # Before sweep
    act.gstat(switches=['-i'])
    nodes = gstat_helpers.get_stat(act.stdout, 'TEST', METRIC)
    assert nodes == 6760

    # After sweep
    act.gfix(switches=['-sweep', act.db.dsn])
    act.reset()
    
    act.gstat(switches=['-i'])
    nodes = gstat_helpers.get_stat(act.stdout, 'TEST', METRIC)
    assert nodes == 6000



