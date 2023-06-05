#coding:utf-8
"""
ID:          utilites.gstat.index.nodes_deleted_records
TITLE:       Check number of the index nodes after deleting records
DESCRIPTION: 
NOTES:
"""

import pytest
from firebird.qa import *
from pathlib import Path
import string

PAGE_SIZE = 4096
FIELD_WIDTH = 100

METRIC = 'nodes'

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

db = db_factory(page_size=PAGE_SIZE, init=init_script)
act = python_act('db')

conf = store_config('databases.conf')
new_config = temp_file('new_databases.conf')

@pytest.mark.version('>=3.0')
def test_1(act: Action, gstat_helpers, conf: ConfigManager, new_config: Path):   
    databases_conf=f"""
    gstat_total_versions = {act.db.db_path}
    {{
        GCPolicy=cooperative
    }}
    """
    new_config.write_text(databases_conf)
    conf.replace(new_config)

    with act.db.connect() as con:
        con.execute_immediate(f"DELETE FROM TEST WHERE ID < 760 ;")
        con.commit()

    # Before sweep
    act.gstat(switches=['-i'])
    nodes = gstat_helpers.get_metric(act.stdout, 'TEST', METRIC)
    assert nodes == 6760

    # After sweep
    act.gfix(switches=['-sweep', act.db.dsn])
    act.reset()
    
    act.gstat(switches=['-i'])
    nodes = gstat_helpers.get_metric(act.stdout, 'TEST', METRIC)
    assert nodes == 6000



