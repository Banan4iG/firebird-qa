#coding:utf-8
#
# PROGRAM/MODULE: firebird-qa
# FILE:           firebird/qa/plugin.py
# DESCRIPTION:    pytest plugin for Firebird QA
# CREATED:        9.4.2021
#
# The contents of this file are subject to the MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Copyright (c) 2020 Firebird Project (www.firebirdsql.org)
# All Rights Reserved.
#
# Contributor(s): Pavel Císař (original code)
#                 ______________________________________

"""firebird-qa - pytest plugin for Firebird QA


"""

from __future__ import annotations
from typing import List, Dict, Union, Optional
import sys
import locale
import os
import re
import shutil
import platform
import pytest
from _pytest.fixtures import FixtureRequest
from _pytest.terminal import TerminalReporter, _get_raw_skip_reason, _format_trimmed
from _pytest.reports import TestReport
from subprocess import run, CompletedProcess, PIPE, STDOUT
from pathlib import Path
from configparser import ConfigParser, ExtendedInterpolation
from packaging.specifiers import SpecifierSet
from packaging.version import parse
import time
from threading import Thread, Barrier
from firebird.driver import connect, connect_server, create_database, driver_config, \
     NetProtocol, Server, CHARSET_MAP, Connection, Cursor, \
     DESCRIPTION_NAME, DESCRIPTION_DISPLAY_SIZE, DatabaseConfig, DBKeyScope, DbInfoCode, \
     DbWriteMode, get_api
from firebird.driver.core import _connect_helper

_vars_ = {'server': None,
          'bin-dir': None,
          'firebird-config': None,
          'runslow': False,
          }

_platform = platform.system()
_nodemap = {}

FIELD_ID = 'ID:'
FIELD_ISSUE = 'ISSUE:'
FIELD_TITLE = 'TITLE:'
FIELD_DECRIPTION = 'DESCRIPTION:'
FIELD_NOTES = 'NOTES:'
FIELD_JIRA = 'JIRA:'

class ExecutionError(Exception):
    pass

def pytest_addoption(parser, pluginmanager):
    """Adds plugin-specific pytest command-line options.

    .. seealso:: `pytest documentation <_pytest.hookspec.pytest_addoption>` for details.
    """
    grp = parser.getgroup('firebird', "Firebird server", 'general')
    grp.addoption('--server', help="Server configuration name", default='')
    grp.addoption('--bin-dir', metavar='PATH', help="Path to directory with Firebird utilities")
    grp.addoption('--protocol',
                  choices=[i.name.lower() for i in NetProtocol],
                  help="Network protocol used for database attachments")
    grp.addoption('--runslow', action='store_true', default=False, help="Run slow tests")
    grp.addoption('--save-output', action='store_true', default=False, help="Save test std[out|err] output to files")

def pytest_report_header(config):
    """Returns plugin-specific test session header.

    .. seealso:: `pytest documentation <_pytest.hookspec.pytest_report_header>` for details.
    """
    return ["System:",
            f"  encodings: sys:{sys.getdefaultencoding()} locale:{locale.getpreferredencoding()} filesystem:{sys.getfilesystemencoding()}",
            "Firebird:",
            f"  server: {_vars_['server']} [v{_vars_['version']}, {_vars_['server-arch']}, {_vars_['arch']}]",
            f"  home: {_vars_['home-dir']}",
            f"  bin: {_vars_['bin-dir']}",
            f"  client library: {_vars_['fbclient']}",
            ]

def set_tool(tool: str):
    "Helper function for `pytest_configure`."
    path: Path = _vars_['bin-dir'] / tool
    if not path.is_file():
        path = path.with_suffix('.exe')
        if not path.is_file():
            # If server is Red Database, try using rdb prefix to find tool
            if _vars_['is_rdb']:
                rdb_tool = tool.replace('fb', 'rdb')
                path: Path = _vars_['bin-dir'] / rdb_tool
                if not path.is_file():
                    path = path.with_suffix('.exe')
                    if not path.is_file():
                        pytest.exit(f"Can't find '{tool}' in {_vars_['bin-dir']}")
                _vars_[rdb_tool] = path
    _vars_[tool] = path

class QATerminalReporter(TerminalReporter):
    def _getfailureheadline(self, rep):
        head_line = rep.head_line
        if head_line:
            return rep.nodeid
        return "test session"  # XXX?
    def pytest_runtest_logstart(self, nodeid: str, location: Tuple[str, Optional[int], str]) -> None:
        # Ensure that the path is printed before the
        # 1st test of a module starts running.
        nodeid = _nodemap.get(nodeid, nodeid)
        if self.showlongtestinfo:
            line = nodeid + ' '
            self.write_ensure_prefix(line, "")
            self.flush()
        elif self.showfspath:
            self.write_fspath_result(nodeid, "")
            self.flush()
    def pytest_runtest_logreport(self, report: TestReport) -> None:
        self._tests_ran = True
        rep = report
        res: Tuple[
            str, str, Union[str, Tuple[str, Mapping[str, bool]]]
        ] = self.config.hook.pytest_report_teststatus(report=rep, config=self.config)
        category, letter, word = res
        if not isinstance(word, tuple):
            markup = None
        else:
            word, markup = word
        self._add_stats(category, [rep])
        if not letter and not word:
            # Probably passed setup/teardown.
            return
        running_xdist = hasattr(rep, "node")
        if markup is None:
            was_xfail = hasattr(report, "wasxfail")
            if rep.passed and not was_xfail:
                markup = {"green": True}
            elif rep.passed and was_xfail:
                markup = {"yellow": True}
            elif rep.failed:
                markup = {"red": True}
            elif rep.skipped:
                markup = {"yellow": True}
            else:
                markup = {}
        if self.verbosity <= 0:
            self._tw.write(letter, **markup)
        else:
            self._progress_nodeids_reported.add(rep.nodeid)
            line = rep._qa_id_ + ' '
            if not running_xdist:
                self.write_ensure_prefix(line, word, **markup)

                if self._show_progress_info == "count":
                    num_tests = self._session.testscollected
                    progress_length = len(" [{}/{}]".format(str(num_tests), str(num_tests)))
                else:
                    progress_length = len(" [100%]")

                if rep.skipped or hasattr(report, "wasxfail"):
                    available_width = (
                        (self._tw.fullwidth - self._tw.width_of_current_line)
                        - progress_length
                        - 1
                    )
                    reason = _get_raw_skip_reason(rep)
                    reason_ = _format_trimmed(" ({})", reason, available_width)
                    if reason and reason_ is not None:
                        self._tw.write(reason_)
                if self._show_progress_info:
                    self._write_progress_information_filling_space()
            else:
                self.ensure_newline()
                self._tw.write("[%s]" % rep.node.gateway.id)
                if self._show_progress_info:
                    self._tw.write(
                        self._get_progress_information_message() + " ", cyan=True
                    )
                else:
                    self._tw.write(" ")
                self._tw.write(word, **markup)
                self._tw.write(" " + line)
                self.currentfspath = -2
        self.flush()

@pytest.mark.tryfirst
def pytest_runtest_makereport(item, call):
    result = TestReport.from_item_and_call(item, call)
    for attr in dir(item):
        if attr.startswith('_qa_'):
            setattr(result, attr, getattr(item, attr))
    return result

@pytest.mark.trylast
def pytest_configure(config):
    """Plugin configuration.

    .. seealso:: `pytest documentation <_pytest.hookspec.pytest_configure>` for details.
    """
    # pytest.ini
    config.addinivalue_line("markers", "version(versions): Firebird version specifications")
    config.addinivalue_line("markers", "platform(platforms): Platform names")
    config.addinivalue_line("markers", "slow: Mark test as slow to run")
    if config.getoption('help'):
        return
    config_path: Path = Path.cwd() / 'firebird-driver.conf'
    if config_path.is_file():
        driver_config.read(str(config_path))
        _vars_['firebird-config'] = config_path
    driver_config.register_database('pytest')
    #
    _vars_['basetemp'] = config.getoption('basetemp')
    _vars_['runslow'] = config.getoption('runslow')
    _vars_['root'] = config.rootpath
    path = config.rootpath / 'databases'
    _vars_['databases'] = path if path.is_dir() else config.rootpath
    path = config.rootpath / 'backups'
    _vars_['backups'] = path if path.is_dir() else config.rootpath
    path = config.rootpath / 'files'
    _vars_['files'] = path if path.is_dir() else config.rootpath
    _vars_['server'] = config.getoption('server')
    _vars_['protocol'] = config.getoption('protocol')
    _vars_['save-output'] = config.getoption('save_output')
    srv_conf = driver_config.get_server(_vars_['server'])
    _vars_['host'] = srv_conf.host.value if srv_conf is not None else ''
    _vars_['port'] = srv_conf.port.value if srv_conf is not None else ''
    _vars_['password'] = srv_conf.password.value
    #
    db_conf = driver_config.register_database('employee')
    db_conf.server.value = _vars_['server']
    db_conf.database.value = 'employee.fdb'
    # Handle server-specific "fb_client_library" configuration option
    _vars_['fbclient'] = 'UNKNOWN'
    cfg = ConfigParser(interpolation=ExtendedInterpolation())
    cfg.read(str(config_path))
    if cfg.has_option(_vars_['server'], 'fb_client_library'):
        fbclient = Path(cfg.get(_vars_['server'], 'fb_client_library'))
        if not fbclient.is_file():
            pytest.exit(f"Client library '{fbclient}' not found!")
        driver_config.fb_client_library.value = str(fbclient)
    cfg.clear()
    _vars_['fbclient'] = get_api().client_library_name
    # THIS should load the driver API, do not connect db or server earlier!
    with connect_server(_vars_['server'], user='SYSDBA',
                        password=_vars_['password']) as srv:
        from firebird.driver import SrvInfoCode
        _vars_['version'] = parse(srv.info.version.replace('-dev', ''))
        _vars_['home-dir'] = Path(srv.info.home_directory)
        if bindir := config.getoption('bin_dir'):
            _vars_['bin-dir'] = Path(bindir)
        else:
            bindir = _vars_['home-dir'] / 'bin'
            if not bindir.exists():
                bindir = _vars_['home-dir']
            _vars_['bin-dir'] = bindir
        _vars_['lock-dir'] = Path(srv.info.lock_directory)
        _vars_['bin-dir'] = Path(bindir) if bindir else _vars_['home-dir']
        _vars_['security-db'] = Path(srv.info.security_database)
        _vars_['arch'] = srv.info.architecture
        srv_version = srv.info.get_info(SrvInfoCode.SERVER_VERSION)
        _vars_['is_rdb'] = any(srv_version.find(check) > -1 for check in ['RedDatabase', 'Red Database'])
    # tools
    for tool in ['isql', 'gbak', 'nbackup', 'gstat', 'gfix', 'gsec', 'fbsvcmgr']:
        set_tool(tool)
    # Driver encoding for NONE charset
    CHARSET_MAP['NONE'] = 'utf-8'
    CHARSET_MAP[None] = 'utf-8'
    # Server architecture [CS,SS,SC]
    with connect('employee') as con1, connect('employee') as con2:
        sql = f"""
        select count(distinct a.mon$server_pid), min(a.mon$remote_protocol),
        max(iif(a.mon$remote_protocol is null, 1, 0))
        from mon$attachments a
        where a.mon$attachment_id in ({con1.info.id}, {con2.info.id}) or upper(a.mon$user) = upper('cache writer')
    """
        cur1 = con1.cursor()
        cur1.execute(sql)
        server_cnt, server_pro, cache_wrtr = cur1.fetchone()
        if server_pro is None:
            result = 'Embedded'
        elif cache_wrtr == 1:
            result = 'SuperServer'
        elif server_cnt == 2:
            result = 'Classic'
        else:
            f1 = con1.info.get_info(DbInfoCode.FETCHES)
            cur2 = con2.cursor()
            cur2.execute('select 1 from rdb$database').fetchall()
            f2 = con1.info.get_info(DbInfoCode.FETCHES)
            result = 'SuperClassic' if f1 == f2 else 'SuperServer'
    _vars_['server-arch'] = result
    # Change terminal reporter
    standard_reporter = config.pluginmanager.getplugin('terminalreporter')
    pspec_reporter = QATerminalReporter(standard_reporter.config)
    config.pluginmanager.unregister(standard_reporter)
    config.pluginmanager.register(pspec_reporter, 'terminalreporter')

def pytest_collection_modifyitems(session, config, items):
    skip_slow = pytest.mark.skip(reason="need --runslow option to run")
    # Apply skip markers
    for item in items:
        if 'slow' in item.keywords and not _vars_['runslow']:
            item.add_marker(skip_slow)
    # Deselect tests not applicable to tested engine version and platform
    selected = []
    deselected = []
    for item in items:
        platform_ok = True
        for platforms in [mark.args for mark in item.iter_markers(name="platform")]:
            platform_ok = _platform in platforms
        versions = [mark.args for mark in item.iter_markers(name="version")]
        if versions:
            spec = SpecifierSet(','.join(list(versions[0])))
            if platform_ok and _vars_['version'] in spec:
                selected.append(item)
            else:
                deselected.append(item)
    items[:] = selected
    config.hook.pytest_deselected(items=deselected)
    # Add OUR OWN test metadata to Item
    for item in items:
        item._qa_id_ = item.nodeid
        item._qa_issue_ = None
        item._qa_jira_ = None
        item._qa_title_ = 'UNKNOWN'
        item._qa_description_ = ''
        item._qa_notes_ = ''
        module_doc = item.parent.obj.__doc__
        if module_doc is None:
            continue
        current_field = 'NONE'
        for line in module_doc.splitlines():
            uline = line.upper()
            if uline.startswith(FIELD_ID):
                current_field = FIELD_ID
                item._qa_id_ = line[len(FIELD_ID):].strip()
                _nodemap[item.nodeid] = item._qa_id_
            elif uline.startswith(FIELD_ISSUE):
                current_field = FIELD_ISSUE
                item._qa_issue_ = line[len(FIELD_ISSUE):].strip()
            elif uline.startswith(FIELD_JIRA):
                current_field = FIELD_JIRA
                item._qa_jira_ = line[len(FIELD_JIRA):].strip()
            elif uline.startswith(FIELD_TITLE):
                current_field = FIELD_TITLE
                item._qa_title_ = line[len(FIELD_TITLE):].strip()
            elif uline.startswith(FIELD_DECRIPTION):
                current_field = FIELD_DECRIPTION
                item._qa_description_ = line[len(FIELD_DECRIPTION):].strip()
            elif uline.startswith(FIELD_NOTES):
                current_field = FIELD_NOTES
                item._qa_notes_ = line[len(FIELD_NOTES):].strip()
            elif current_field == FIELD_DECRIPTION:
                if item._qa_description_:
                    item._qa_description_ += '\n'
                item._qa_description_ += line.strip()
            elif current_field == FIELD_NOTES:
                if item._qa_notes_:
                    item._qa_notes_ += '\n'
                item._qa_notes_ += line.strip()
            else:
                # Unknown field
                pass

def substitute_macros(text: str, macros: Dict[str, str]):
    """Helper function to substitute `$(name)` macros in text.

    .. important::

       Used only for backward compatibility with `fbtest`. The use of `$(name)` macros in
       tests is **deprecated**.
    """
    f_text = text
    for (pattern, replacement) in macros.items():
        replacement = replacement.replace(os.path.sep,'/')
        f_text = f_text.replace(f'$({pattern.upper()})', replacement)
    return f_text

class Database:
    """Object to access and manage single test database.

    Arguments:
        path: Path to directory where test database should be located.
        filename: Database filename.
        user: User name used to create/restore/connect the test database. Default is taken
            from server configuration.
        password: User password used to create/restore/connect the test database. Default
            is taken from server configuration.
        charset: Character set for test database.

    .. important::

        Do not create instances of this class directly! Use **only** fixtures created by `db_factory`.
    """
    def __init__(self, path: Path, filename: str, user: str=None, password: str=None,
                 charset: str=None, debug: str=''):
        self._debug: str = debug
        #: Full path to test database.
        self.db_path: Path = path / filename
        #: DSN to test database.
        self.dsn: str = None
        #: Firebird CHARACTER SET name for the database
        self.charset: str = 'NONE' if charset is None else charset.upper()
        if _vars_['host']:
            self.dsn = f"{_vars_['host']}:{str(self.db_path)}"
        else:
            self.dsn = str(self.db_path)
        #: Substitutions for `$(name)` macros. Do not use them directly, as use of
        #: `$(name)` macros in tests is **deprecated**, and supported only for backward
        #: compatibility with `fbtest`.
        self.subs = {'temp_directory': str(path / 'x')[:-1],
                     'database_location': str(path / 'x')[:-1],
                     'DATABASE_PATH': str(path / 'x')[:-1],
                     'DSN': self.dsn,
                     'files_location': str(_vars_['root'] / 'files'),
                     'backup_location': str(_vars_['root'] / 'backups'),
                     'suite_database_location': str(_vars_['root'] / 'databases'),
                     }
        srv_conf = driver_config.get_server(_vars_['server'])
        #: User name
        self.user: str = srv_conf.user.value if user is None else user
        #: User password
        self.password: str = srv_conf.password.value if password is None else password
    def _make_config(self, *, page_size: int=None, sql_dialect: int=None, charset: str=None,
                     user: str=None, password: str=None) -> None:
        """Helper method that sets `firebird-driver`_ configuration for `pytest` database
        to work with this particular test database instance. Used before methods that
        need to call `~firebird.driver.core.connect` or `~firebird.driver.core.create_database` methods.
        """
        db_conf = self.get_config()
        db_conf.clear()
        db_conf.server.value = _vars_['server']
        db_conf.database.value = str(self.db_path)
        db_conf.user.value = self.user if user is None else user
        db_conf.password.value = self.password if password is None else password
        if sql_dialect is not None:
            db_conf.db_sql_dialect.value = sql_dialect
            db_conf.sql_dialect.value = sql_dialect
        if page_size is not None:
            db_conf.page_size.value = page_size
        if charset is not None:
            db_conf.db_charset.value = charset
            db_conf.charset.value = charset
        if _vars_['protocol'] is not None:
            db_conf.protocol.value = NetProtocol._member_map_[_vars_['protocol'].upper()]
    def get_config(self) -> DatabaseConfig:
        """Returns `firebird-driver`_ configuration for test database (`pytest`).
        """
        return driver_config.get_database('pytest')
    def create(self, page_size: int=None, sql_dialect: int=None) -> None:
        """Create the test database.

        Arguments:
            page_size: Database page size.
            sql_dialect: Database SQL dialect.

        .. note::

           Typically, this method is used only by `db_factory` to create the test database
           (during fixture setup) unless `do_not_create` argument is set to True.

        """
        __tracebackhide__ = True
        self._make_config(page_size=page_size, sql_dialect=sql_dialect, charset=self.charset)
        charset = self.charset
        print(f"Creating db: {self.dsn} [{page_size=}, {sql_dialect=}, {charset=}, user={self.user}, password={self.password}]")
        with create_database('pytest'):
            pass
    def restore(self, backup: str) -> None:
        """Create the test database from backup.

        Arguments:
            backup: Backup filename.

        .. note::

           Typically, this method is used only by `db_factory` to create the test database
           (during fixture setup) unless `do_not_create` argument is set to True.

        """
        __tracebackhide__ = True
        fbk_file: Path = _vars_['backups'] / backup
        if not fbk_file.is_file():
            raise ValueError(f"Backup file '{fbk_file}' not found")
        print(f"Restoring db: {self.db_path} from {fbk_file}")
        result = run([_vars_['gbak'], '-r', '-v', '-user', self.user,
                      '-password', self.password,
                      str(fbk_file), str(self.dsn)], capture_output=True)
        if result.returncode:
            print(f"-- stdout {'-' * 20}")
            print(result.stdout)
            print(f"-- stderr {'-' * 20}")
            print(result.stderr)
            raise Exception("Database restore failed")
        return result
    def copy(self, filename: str) -> None:
        """Create the test database as copy of template database.

        Arguments:
            filename: Template database filename.

        .. note::

           Typically, this method is used only by `db_factory` to create the test database
           (during fixture setup) unless `do_not_create` argument is set to True.

        """
        __tracebackhide__ = True
        src_path = _vars_['databases'] / filename
        #print(f"Copying db: {self.db_path} from {src_path}")
        shutil.copyfile(src_path, self.db_path)
        # Fix permissions
        if platform.system != 'Windows':
            os.chmod(self.db_path, 16895)
    def init(self, script: str) -> CompletedProcess:
        """Initialize the test database by running ISQL script.

        Arguments:
            script: SQL script content to be executed by ISQL.

        .. note::

           Typically, this method is used only by `db_factory` to initialize the test database
           (during fixture setup) unless `do_not_create` argument is set to True.

        """
        __tracebackhide__ = True
        result = run([_vars_['isql'], '-ch', 'UTF8', '-user', self.user,
                      '-password', self.password, str(self.dsn)],
                     input=substitute_macros(script, self.subs),
                     encoding='utf8', capture_output=True)
        if result.returncode:
            print(f"-- stdout {'-' * 20}")
            print(result.stdout)
            print(f"-- stderr {'-' * 20}")
            print(result.stderr)
            raise Exception("Database init script execution failed")
        return result
    def drop(self) -> None:
        """Drop the test database.

        .. note::

           Typically, this method is used only by `db_factory` to drop the test database
           after test execution (during fixture teardown) unless `do_not_drop` argument is
           set to True.

        """
        __tracebackhide__ = True
        with connect_server(_vars_['server']) as srv:
            srv.database.no_linger(database=self.db_path)
        self._make_config()
        with connect('pytest') as db:
            db._att._name = self._debug
            try:
                db.execute_immediate('delete from mon$attachments where mon$attachment_id != current_connection')
                db.commit()
            except:
                pass
            #print(f"Removing db: {self.db_path}")
            try:
                db.drop_database()
            except:
                pass
        if self.db_path.is_file():
            self.db_path.unlink(missing_ok=True)
    def connect(self, *, user: str=None, password: str=None, role: str=None, no_gc: bool=None,
                no_db_triggers: bool=None, dbkey_scope: DBKeyScope=None,
                session_time_zone: str=None, charset: str=None, sql_dialect: int=None,
                auth_plugin_list: str=None) -> Connection:
        """Create new connection to test database.

        Arguments:
            user: User name for this connection.
            password: User password for this connection.
            role: Role name.
            no_gc: When `True`, the Garbage Collection is disabled for this connection.
            no_db_triggers: When `True`, the database triggers are disabled for this connection.
            dbkey_scope: Scope for `db_key's` for this connection.
            session_time_zone: Session time zone.
            charset: Character set for this connection.
            sql_dialect: SQL dialect used for connection.
            auth_plugin_list: List of authentication plugins override.

        .. tip::

           It's highly recommended to use the :ref:`with <with>` statement to ensure that
           the returned `~firebird.driver.core.Connection` is properly closed even if test
           fails or raises an error. Otherwise the teardown of test database fixture may
           fail as well, adding unnecessary clutter to test session report.
        """
        __tracebackhide__ = True
        self._make_config(user=user, password=password, charset=charset, sql_dialect=sql_dialect)
        result = connect('pytest', role=role, no_gc=no_gc, no_db_triggers=no_db_triggers,
                       dbkey_scope=dbkey_scope, session_time_zone=session_time_zone,
                       auth_plugin_list=auth_plugin_list)
        result._att._name = self._debug
        return result
    def set_async_write(self) -> None:
        "Set the database to `async write` mode."
        __tracebackhide__ = True
        with connect_server(_vars_['server']) as srv:
            srv.database.set_write_mode(database=self.db_path, mode=DbWriteMode.ASYNC)
    def set_sync_write(self) -> None:
        "Set the database to `sync write` mode."
        __tracebackhide__ = True
        with connect_server(_vars_['server']) as srv:
            srv.database.set_write_mode(database=self.db_path, mode=DbWriteMode.SYNC)

def db_factory(*, filename: str='test.fdb', init: str=None, from_backup: str=None,
               copy_of: str=None, page_size: int=None, sql_dialect: int=None,
               charset: str=None, user: str=None, password: str=None,
               do_not_create: bool=False, do_not_drop: bool=False, async_write: bool=True):
    """Factory function that returns :doc:`fixture <fixture>` providing the `Database` instance.

    Arguments:
        filename: Test database filename (without path).
        init:     Test database initialization script (isql format).
        from_backup: Backup filename (without path) from which the test database should be restored.
            File must be located in `backups` directory.
        copy_of:  Filename (without path) of the database that should be copied as test database.
            File must be located in `databases` directory.
        page_size: Test database page size.
        sql_dialect: SQL dialect for test database.
        charset: Character set for test database.
        user: User name used to create/restore/connect the test database. Default is taken
            from server configuration.
        password: User password used to create/restore/connect the test database. Default
            is taken from server configuration.
        do_not_create: When `True`, the preparation of test database is skipped. Use this
            option to define test databases created by test itself, so they are properly
            removed.
        do_not_drop: When `True`, the ficture will not drop the test database. Use this
           option when test database is removed by test itself (as part of test routine).
        async_write: When `True`, the database is set to async write before initialization.
    """

    @pytest.fixture
    def database_fixture(request: FixtureRequest, db_path) -> Database:
        db = Database(db_path, filename, user, password, charset, debug=str(request.module))
        if not do_not_create:
            if from_backup is None and copy_of is None:
                db.create(page_size, sql_dialect)
            elif from_backup is not None:
                db.restore(from_backup)
            elif copy_of is not None:
                db.copy(copy_of)
            if async_write:
                db.set_async_write()
            if init: # Do not check for None, we want to skip empty scripts as well
                db.init(init)
        yield db
        if not do_not_drop:
            db.drop()

    return database_fixture

@pytest.fixture
def db_path(tmp_path) -> Path:
    """:doc:`fixture <fixture>` function that returns path to temporary directory for database files.

    On non-Windows platforms makes sure that directory has permissions that user, group and
    other can write there.

    .. seealso:: `tmp_path <_pytest.tmpdir.tmp_path>` fixture.
    """
    if platform.system != 'Windows':
        base = _vars_['basetemp']
        if base is None:
            os.chmod(tmp_path.parent, 16895)
            os.chmod(tmp_path.parent.parent, 16895)
        else:
            os.chmod(Path(base), 16895)
        os.chmod(tmp_path, 16895)
    return tmp_path

class User:
    """Object to access and manage single Firebird test user.

    Arguments:
        db: Database used to manage test user.
        filename: Database filename.
        name: User name.
        password: User password.
        plugin: Secutiry plugin name used to manage this user.
        charset: Firebird CHARACTER SET used for connections that manage this user.
        active: Create user as active.
        tags: Tags for user.
        first_name: User's first name.
        middle_name: User's middle name.
        last_name: User's last name.
        admin: ADMIN flag.
        do_not_create: When `True`, the user is not created when `with` context is entered.

    .. note::

       Users are managed through SQL commands executed on connection to specified test
       database to ensure that security database configuration for this test database is
       respected.

    .. important::

       It's NOT RECOMMENDED to create instances of this class directly! The preffered way
       is to use fixtures created by `user_factory`.

       As test databases are managed by fixtures, it's necessary to ensure that users are
       created after database initialization, and removed before test database is removed.
       So, user `setup` and `teardown` is managed via context manager protocol and the
       :ref:`with <with>` statement that must be executed within scope of used database.
       Fixture created by `user_factory` does this automatically.
    """
    def __init__(self, db: Database, *, name: str, password: str, plugin: str, charset: str,
                 active: bool=True, tags: Dict[str]=None, first_name: str=None,
                 middle_name: str=None, last_name: str=None, admin: bool=False,
                 do_not_create: bool=False):
        #: Database used to manage test user.
        self.db: Database = db
        self.__name: str = name if name.startswith('"') else name.upper()
        self.__password: str = password
        self.__plugin: str = plugin
        self.__p = ''  if self.__plugin is None else f" USING PLUGIN {self.__plugin}"
        #: Firebird CHARACTER SET used for connections that manage this user.
        self.charset: str = charset
        self.__active: bool = active
        self.__first_name: str = first_name
        self.__middle_name: str = middle_name
        self.__last_name: str = last_name
        self.__tags: Dict[str] = tags
        self.__admin: bool = admin
        self.__create: bool = not do_not_create
    def __enter__(self) -> Role:
        if self.__create:
            self.create()
        return self
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if self.exists():
            self.drop()
    def exists(self) -> bool:
        "Returns `True` if user exists."
        __tracebackhide__ = True
        with self.db.connect(charset=self.charset) as con:
            c = con.cursor()
            name = self.name[1:-1] if self.name.startswith('"') else self.name
            cmd = f"SELECT COUNT(*) FROM SEC$USERS WHERE SEC$USER_NAME = '{name}'"
            if self.__plugin is not None:
                cmd += f" AND SEC$PLUGIN = '{self.__plugin}'"
            cnt = c.execute(cmd).fetchone()[0]
        return cnt > 0
    def create(self) -> None:
        """Creates user in security context of defined test database. Called automatically
        when `with` context is entered and `do_not_create` is `False`.

        .. note:: Sets all user attributes (names, tags etc.).

        .. important:: If user already exists, it's removed before it's re-created.
        """
        __tracebackhide__ = True
        if self.exists():
            self.drop()
        with self.db.connect(charset=self.charset) as con:
            con.execute_immediate(f"CREATE USER {self.name} PASSWORD '{self.__password}' {'ACTIVE' if self.__active else 'INACTIVE'}{self.__p}{' GRANT ADMIN ROLE' if self.__admin else ''}")
            if self.__first_name is not None:
                con.execute_immediate(f"ALTER USER {self.name} SET FIRSTNAME '{self.__first_name}'{self.__p}")
            if self.__middle_name is not None:
                con.execute_immediate(f"ALTER USER {self.name} SET MIDDLENAME '{self.__middle_name}'{self.__p}")
            if self.__last_name is not None:
                con.execute_immediate(f"ALTER USER {self.name} SET LASTNAME '{self.__last_name}'{self.__p}")
            if self.__tags is not None:
                tags = ', '.join([f"{name} = '{value}'" for name, value in self.__tags.items()])
                con.execute_immediate(f"ALTER USER {self.name} SET TAGS ({tags}){self.__p}")
            con.commit()
        print(f"CREATE user: {self.name} PLUGIN: {self.plugin}")
    def drop(self) -> None:
        """Drop user in security context of defined test database. Called automatically
        on `with` context exit.

        .. note:: If needed, also removes all grants for this user via REVOKE ALL ON ALL.
        """
        __tracebackhide__ = True
        with self.db.connect(charset=self.charset) as con:
            c = con.cursor()
            grants = c.execute('select count(*) from '\
                               '(select rdb$user as a from rdb$user_privileges '\
                               'union all select sec$user as a from sec$db_creators) '\
                               'where a = ?',
                               [self.name if self.name.startswith('"') else self.name.upper()]).fetchone()[0]
            if grants > 0:
                c.execute(f'revoke all on all from {self.name}')
                con.commit()
            #
            print(f"DROP user: {self.name} PLUGIN: {self.plugin}")
            con.execute_immediate(f"DROP USER {self.name}{self.__p}")
            con.commit()
    def set_tag(self, name: str, *, value: str) -> None:
        """Create/Set user tag value.

        Arguments:
           name: Tag name.
           value: Tag value.
        """
        __tracebackhide__ = True
        with self.db.connect(charset=self.charset) as con:
            con.execute_immediate(f"ALTER USER {self.name} TAGS ({name} = '{value}'){self.__p}")
            con.commit()
    def drop_tag(self, name: str) -> None:
        """Drop user tag.

        Arguments:
           name: Tag name.
        """
        __tracebackhide__ = True
        with self.db.connect(charset=self.charset) as con:
            con.execute_immediate(f"ALTER USER {self.name} TAGS (DROP {name}){self.__p}")
            con.commit()
    @property
    def name(self) -> str:
        "User name [R/O]"
        return self.__name
    @property
    def plugin(self) -> str:
        "Security plugin [R/O]"
        if self.__plugin is None:
            with self.db.connect() as con:
                c = con.cursor()
                self.__plugin = c.execute(f'SELECT SEC$PLUGIN FROM SEC$USERS').fetchone()[0].strip()
        return self.__plugin
    @property
    def password(self) -> str:
        "User password [R/W]"
        return self.__password
    @password.setter
    def password(self, value: str) -> None:
        with self.db.connect(charset=self.charset) as con:
            con.execute_immediate(f"ALTER USER {self.__name} SET PASSWORD '{value}'")
            con.commit()
        self.__password = value
    @property
    def first_name(self) -> str:
        "First name [R/W]"
        return self.__first_name
    @first_name.setter
    def first_name(self, value: str) -> None:
        with self.db.connect(charset=self.charset) as con:
            con.execute_immediate(f"ALTER USER {self.__name} SET FIRSTNAME '{value}'")
            con.commit()
        self.__first_name = value
    @property
    def middle_name(self) -> str:
        "Middle name [R/W]"
        return self.__middle_name
    @middle_name.setter
    def middle_name(self, value: str) -> None:
        with self.db.connect(charset=self.charset) as con:
            con.execute_immediate(f"ALTER USER {self.__name} SET MIDDLENAME '{value}'")
            con.commit()
        self.__middle_name = value
    @property
    def last_name(self) -> str:
        "Last name [R/W]"
        return self.__last_name
    @last_name.setter
    def last_name(self, value: str) -> None:
        with self.db.connect(charset=self.charset) as con:
            con.execute_immediate(f"ALTER USER {self.__name} SET LASTNAME '{value}'")
            con.commit()
        self.__last_name = value
    @property
    def tags(self) -> Dict[str]:
        "User tags [R/O]"
        return dict(self.__tags)

def user_factory(db_fixture_name: str, *, name: str, password: str='', plugin: str=None,
                 charset: str='utf8', active: bool=True, tags: Dict[str]=None,
                 first_name: str=None, middle_name: str=None, last_name: str=None,
                 admin: bool=False, do_not_create: bool=False):
    """Factory function that returns :doc:`fixture <fixture>` providing the `User` instance.

    Arguments:
        db_fixture_name: Name of database fixture.
        name: User name.
        password: User password.
        plugin: Secutiry plugin name used to manage this user.
        charset: Firebird CHARACTER SET used for connections that manage this user.
        active: Create user as active.
        tags: Tags for user.
        first_name: User's first name.
        middle_name: User's middle name.
        last_name: User's last name.
        admin: ADMIN flag.
        do_not_create: When `True`, the user is not created when `with` context is entered.

    .. important::

       The `db_fixture_name` must be name of variable that holds the fixture created by
       `db_factory` function.

       **Test must use both, user and database fixtures!**

    .. note::

       Database must exists before user is created by fixture, so you cannot use database
       fixtures created with `do_not_create` option!
    """

    @pytest.fixture
    def user_fixture(request: FixtureRequest) -> User:
        with User(request.getfixturevalue(db_fixture_name), name=name, password=password,
                  plugin=plugin, charset=charset, active=active, tags=tags,
                  first_name=first_name, middle_name=middle_name, last_name=last_name,
                  admin=admin, do_not_create=do_not_create) as user:
            yield user

    return user_fixture

def trace_thread(act: Action, b: Barrier, cfg: List[str], output: List[str], keep_log: bool,
                 encoding: str):
    """Function used by `TraceSession` for execution in separate thread to run trace session.

    Arguments:
        act: Action instance.
        b: Barrier instance used for synchronization.
        cfg: Trace configuration.
        output: List used to store trace session output.
        keep_log: When `True`, the trace session output is discarded.
        encoding: Encoding for trace session output.
    """
    with act.connect_server() as srv:
        srv.encoding = encoding
        srv.trace.start(config='\n'.join(cfg))
        b.wait()
        for line in srv:
            if keep_log:
                output.append(line)

class TraceSession:
    """Object to manage Firebird trace session.

    Arguments:
       act: Action instance.
       config: Trace session configuration.
       keep_log: When `True`, the trace session output is discarded.
       encoding: Encoding for trace session output.

    .. important::

       Do not create instances of this class directly! Always use `Action.trace` method and the
       :ref:`with <with>` statement.

       Example::

          with act.trace(db_events=trace_cfg):
              # your test here
          # Process trace output, for example by passing to stdout
          act_1.trace_to_stdout()

       The trace session is automatically stopped on exit from `with` context, and trace
       output is copied to `Action.trace_log` attribute.

       .. note::

          For simplicity, we stop **ALL** trace sessions and `Action` keeps only one session
          log, so you should not run multiple trace session simultaneously!
    """
    def __init__(self, act: Action, config: List[str], keep_log: bool=True, encoding: str='ascii'):
        #: Action instance.
        self.act: Action = act
        #: Trace session configuration.
        self.config: List[str] = config
        #: List used to store trace session output.
        self.output: List[str] = []
        #: When `True`, the trace session output is discarded.
        self.keep_log: bool = keep_log
        #: Thread used to execute trace session
        self.trace_thread: Thread = None
        #: Encoding for trace session output.
        self.encoding: str = encoding
    def __enter__(self) -> TraceSession:
        b = Barrier(2)
        self.trace_thread = Thread(target=trace_thread, args=[self.act, b, self.config,
                                                              self.output, self.keep_log,
                                                              self.encoding])
        self.trace_thread.start()
        b.wait()
        return self
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        time.sleep(2)
        with self.act.connect_server() as srv:
            for session in list(srv.trace.sessions.keys()):
                srv.trace.stop(session_id=session)
            self.trace_thread.join(5.0)
            if self.trace_thread.is_alive():
                pytest.fail('Trace thread still alive')
        self.act.trace_log = self.output

class ServerKeeper:
    """Helper context manager class to temporary change the server used by `Action`.

    Arguments:
        atc: Action instance.
        server: New server specification.

    Example::

       with ServerKeeper(act_1, None): # Use embedded server for trace
           with act_1.trace(config=trace_1):
               # Your test here
       # Process trace output, for example by passing to stdout
       act_1.trace_to_stdout()
    """
    def __init__(self, act: Action, server: str):
        self.act: Action = act
        self.server:str = server
        self.old_value = None
    def __enter__(self):
        self.old_value = self.act.vars['server']
        self.act.vars['server'] = self.server
        return self
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if self.old_value is not None:
            self.act.vars['server'] = self.old_value

class Envar:
    """Object to manage environment variables in tests.

    Arguments:
        name: Variable name.
        value: Variable value.

    .. important::

       It's NOT RECOMMENDED to create instances of this class directly! The preffered way
       is to use fixtures created by `envar_factory`.

       Environment variable `setup` and `teardown` is managed via context manager protocol
       and the :ref:`with <with>` statement. Fixture created by `envar_factory` does this
       automatically.

       .. note::

          If environment variable already exists when context is entered, its value is
          preserved and restored at context exit. If the variable does not exist before,
          it is deleted.
    """
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value
        self.old_value = None
    def __enter__(self) -> Envar:
        if self.name in os.environ:
            self.old_value = os.environ[self.name]
        os.environ[self.name] = self.value
        return self
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if self.old_value is not None:
            os.environ[self.name] = self.old_value
        else:
            del os.environ[self.name]

def envar_factory(*, name: str, value: str):
    """Factory function that returns :doc:`fixture <fixture>` providing the `Envar` instance.

    Arguments:
        name: Variable name.
        value: Variable value.

    .. note::

       If environment variable already exists before test execution, its value is preserved
       and restored when test execution is finished. If the variable does not exist before,
       it is deleted.
    """

    @pytest.fixture
    def envar_fixture() -> User:
        with Envar(name, value) as envar:
            yield envar

    return envar_fixture

class Role:
    """Object to access and manage single Firebird test role.

    Arguments:
        database: Database used to manage test role.
        name: Role name.
        charset: Firebird CHARACTER SET used for connections that manage this role.
        do_not_create: When `True`, the role is not created when `with` context is entered.

    .. note::

       Roles are managed through SQL commands executed on connection to specified test
       database.

    .. important::

       It's NOT RECOMMENDED to create instances of this class directly! The preffered way
       is to use fixtures created by `role_factory`.

       As test databases are managed by fixtures, it's necessary to ensure that roles are
       created after database initialization, and removed before test database is removed.
       So, role `setup` and `teardown` is managed via context manager protocol and the
       :ref:`with <with>` statement that must be executed within scope of used database.
       Fixture created by `role_factory` does this automatically.
    """
    def __init__(self, database: Database, name: str, charset: str, do_not_create: bool):
        #: Database used to manage test role.
        self.db: Database = database
        #: Role name.
        self.name: str = name if name.startswith('"') else name.upper()
        #: Firebird CHARACTER SET used for connections that manage this role.
        self.charset = charset
        #: When `True`, the role is not created when `with` context is entered.
        self.do_not_create: bool = do_not_create
    def __enter__(self) -> Role:
        if not self.do_not_create:
            self.create()
        return self
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if self.exists():
            self.drop()
    def create(self) -> None:
        """Creates role in test database. Called automatically when `with` context is
        entered and `do_not_create` is `False`.

        .. important:: If role already exists, it's removed before it's re-created.
        """
        __tracebackhide__ = True
        if self.exists():
            self.drop()
        with self.db.connect(charset=self.charset) as con:
            con.execute_immediate(f'CREATE ROLE {self.name}')
            con.commit()
            print(f"CREATE role: {self.name}")
    def drop(self) -> None:
        """Drop role in defined test database. Called automatically on `with` context exit.
        """
        __tracebackhide__ = True
        with self.db.connect(charset=self.charset) as con:
            con.execute_immediate(f'DROP ROLE {self.name}')
            con.commit()
            print(f"DROP role: {self.name}")
    def exists(self) -> bool:
        "Returns `True` if role exists."
        __tracebackhide__ = True
        with self.db.connect(charset=self.charset) as con:
            c = con.cursor()
            name = self.name[1:-1] if self.name.startswith('"') else self.name
            cmd = f"SELECT COUNT(*) FROM RDB$ROLES WHERE RDB$ROLE_NAME = '{name}'"
            cnt = c.execute(cmd).fetchone()[0]
        return cnt > 0

def role_factory(db_fixture_name: str, *, name: str, charset: str='utf8', do_not_create: bool=False):

    @pytest.fixture
    def role_fixture(request: FixtureRequest) -> User:
        with Role(request.getfixturevalue(db_fixture_name), name, charset, do_not_create) as role:
            yield role

    return role_fixture

class Action:
    """Class to manage and execute Firebird tests.

    Arguments:
      db: Primary test database.
      script: Test ISQL script.
      substitutions: REGEX substitutions to be applied on stdout/stderr on cleanup.
      outfile: Base path/filename for stdout/stderr protocols of external Firebird tool execution.

    .. important::

        Do not create instances of this class directly! Use **only** fixtures created by
        `isql_act` or `python_act`.
    """
    def __init__(self, db: Database, script: str, substitutions: List[str], outfile: Path, node: pytest.Item):
        self._node: pytest.Item = node
        #: Primary test database.
        self.db: Database = db
        #: Test script
        self.script: str = substitute_macros(script, self.db.subs)
        #: Return code from last external Firebird tool execution.
        self.return_code: int = 0
        #: Content of standard output from last external Firebird tool execution.
        self.stdout: str = ''
        self._clean_stdout: str = None
        #: Content of error output from last external Firebird tool execution.
        self.stderr: str = ''
        self._clean_stderr: str = None
        #: Expected standard output.
        self.expected_stdout: str = ''
        self._clean_expected_stdout: str = None
        #: Expected error output.
        self.expected_stderr: str = ''
        self._clean_expected_stderr: str = None
        #: REGEX substitutions applied on stdout/stderr on cleanup.
        self.substitutions: List[str] = [] if substitutions is None else [x for x in substitutions]
        #: Base path/filename for stdout/stderr protocols of external Firebird tool execution.
        self.outfile: Path = outfile
        #: Output from last executed trace session.
        self.trace_log: List[str] = []
    def space_strip(self, value: str) -> str:
        """Reduce spaces in value.
        """
        value= re.sub("(?m)^\\s+", "", value)
        return re.sub("(?m)\\s+$", "", value)
    def string_strip(self, value: str, substitutions: List[str]=[], isql: bool=True,
                     remove_space: bool=True) -> str:
        """Remove unwanted isql noise strings and apply substitutions defined
        in recipe to captured output value.
        """
        if not value:
            return value
        if isql:
            for regex in map(re.compile,['(?m)Database:.*\\n?', 'SQL>[ \\t]*\\n?',
                                       'CON>[ \\t]*\\n?', '-->[ \\t]*\\n?']):
                value = re.sub(regex, "", value)
        for pattern, replacement in substitutions:
            value= re.compile(pattern, re.M).sub(replacement, value)
        if remove_space:
            value = self.space_strip(value)
        return value
    def execute(self, *, do_not_connect: bool=False, charset: str=None, io_enc: str=None,
                combine_output: bool=False) -> None:
        """Execute test `script` using ISQL.

        Arguments:
           do_not_connect: Do not connect to primary test database on ISQL execution.
           charset: Charset to be used for connection instead charset of primary test database.
           io_enc: Python encoding to be used to decode text output instead encoding that
              corresponds to used character set.
           combine_output: Combine stdout/stderr into stdout.

        By default, script is executed on primary test database with NONE charset. ISQL
        output is captured into `stdout` and `stderr`, and exit code is stored into
        `return_code`. If pytest `--save-output` command-line option is used, the content
        of stdout/stderr is also stored into test protocol files with `.out`/`.err` suffix.

        .. important::

           If `return_code` is not zero, and script execution failure is not expected (either
           via defined `expected_stderr` value or using `combine_output` = True), it raises and
           `Exception` with "ISQL script execution failed" message and prints content of stdout
           and stderr.
        """
        __tracebackhide__ = True
        out_file: Path = self.outfile.with_suffix('.out')
        err_file: Path = self.outfile.with_suffix('.err')
        if out_file.is_file():
            out_file.unlink()
        if err_file.is_file():
            err_file.unlink()
        charset = charset.upper() if charset else self.db.charset
        if io_enc is None:
            io_enc = CHARSET_MAP[charset]
        params = [_vars_['isql'], '-ch', charset]
        if not do_not_connect:
            params.extend(['-user', self.db.user, '-password', self.db.password, str(self.db.dsn)])
        if combine_output:
            result: CompletedProcess = run(params, input=substitute_macros(self.script, self.db.subs),
                                           encoding=io_enc, stdout=PIPE, stderr=STDOUT)
        else:
            result: CompletedProcess = run(params, input=self.script,
                                           encoding=io_enc, capture_output=True)
        if result.returncode and not bool(self.expected_stderr) and not combine_output:
            self._node.add_report_section('call', 'ISQL stdout', result.stdout)
            self._node.add_report_section('call', 'ISQL stderr', result.stderr)
            raise ExecutionError("Test script execution failed")

        self.return_code: int = result.returncode
        self.stdout: str = result.stdout
        self.stderr: str = result.stderr
        # Store output
        if _vars_['save-output']:
            if self.stdout:
                out_file.write_text(self.stdout, encoding='utf8')
            if self.stderr:
                err_file.write_text(self.stderr, encoding='utf8')
    def extract_meta(self, *, from_db: Database=None, charset: str=None, io_enc: str=None) -> str:
        """Call ISQL to extract database metadata (using `-x` option).

        Arguments:
           from_db: Extract metadata from specified database instead primary test database.
           charset: Charset to be used for connection instead charset of primary test database.
           io_enc: Python encoding to be used to decode text output instead encoding that
              corresponds to used character set.

        By default, metadata are extracted from primary test database using NONE connection
        charset. ISQL output is captured into `stdout` and `stderr`, and exit code is stored
        into `return_code`. If pytest `--save-output` command-line option is used, the content
        of stdout/stderr is also stored into test protocol files with `.out`/`.err` suffix.

        .. important::

           If `return_code` is not zero, and isql execution failure is not expected (either
           via defined `expected_stderr` value or using `combine_output` = True), it raises
           and `Exception` with "ISQL execution failed" message and prints content
           of stdout and stderr.
        """
        __tracebackhide__ = True
        out_file: Path = self.outfile.with_suffix('.out')
        err_file: Path = self.outfile.with_suffix('.err')
        if out_file.is_file():
            out_file.unlink()
        if err_file.is_file():
            err_file.unlink()
        db = self.db if from_db is None else from_db
        charset = charset.upper() if charset else self.db.charset
        if io_enc is None:
            io_enc = CHARSET_MAP[charset]
        result = run([_vars_['isql'], '-x', '-ch', charset, '-user', db.user,
                      '-password', db.password, str(db.dsn)],
                     encoding=io_enc, capture_output=True)
        if result.returncode:
            self._node.add_report_section('call', 'ISQL stdout', result.stdout)
            self._node.add_report_section('call', 'ISQL stderr', result.stderr)
            raise ExecutionError("ISQL execution failed")
        self.return_code: int = result.returncode
        self.stdout: str = result.stdout
        self.stderr: str = result.stderr
        # Store output
        if _vars_['save-output']:
            if self.stdout:
                out_file.write_text(self.stdout, encoding=io_enc)
            if self.stderr:
                err_file.write_text(self.stderr, encoding=io_enc)
        return self.stdout
    def gstat(self, *, switches: List[str], charset: str=None, io_enc: str=None,
              connect_db: bool=True, credentials: bool=True) -> None:
        """Run `gstat` utility.

        Arguments:
           switches: List with command-line switches (passed to `subprocess.run`).
           charset: Decode output using encoding that corresponds to this charset instead
             charset of primary test database.
           connect_db: When `True` adds primary test database DSN to switches.
           credentials: When `True` adds switches to connect as primary test database user.

        By default, GSTAT is executed on primary test database, and output is captured into
        `stdout` and `stderr`, and exit code is stored to `return_code`. If pytest `--save-output`
        command-line option is used, the content of stdout/stderr is also stored into test
        protocol files with `.out`/`.err` suffix.

        Example::

           act_1.gstat(switches=['-h'])
           act_1.gstat(switches=['-h', str(test_db)], connect_db=False)

        .. important::

           If `return_code` is not zero, and script execution failure is not expected (either
           via defined `expected_stderr` value or using `combine_output` = True), it raises and
           `Exception` with "gstat execution failed" message and prints content of stdout
           and stderr.
        """
        __tracebackhide__ = True
        out_file: Path = self.outfile.with_suffix('.out')
        err_file: Path = self.outfile.with_suffix('.err')
        if out_file.is_file():
            out_file.unlink()
        if err_file.is_file():
            err_file.unlink()
        #
        charset = charset.upper() if charset else self.db.charset
        if io_enc is None:
            io_enc = CHARSET_MAP[charset]
        params = [_vars_['gstat']]
        if credentials:
            params.extend(['-user', self.db.user, '-password', self.db.password])
        params.extend(switches)
        if connect_db:
            params.append(str(self.db.dsn))
        result: CompletedProcess = run(params, encoding=io_enc, capture_output=True)
        if result.returncode and not bool(self.expected_stderr):
            self._node.add_report_section('call', 'gstat stdout', result.stdout)
            self._node.add_report_section('call', 'gstat stderr', result.stderr)
            raise ExecutionError("gstat execution failed")
        self.return_code: int = result.returncode
        self.stdout: str = result.stdout
        self.stderr: str = result.stderr
        # Store output
        if _vars_['save-output']:
            if self.stdout:
                out_file.write_text(self.stdout, encoding=io_enc)
            if self.stderr:
                err_file.write_text(self.stderr, encoding=io_enc)
    def gsec(self, *, switches: List[str]=None, charset: str=None, io_enc: str=None,
             input: str=None, credentials: bool=True) -> None:
        """Run `gstat` utility.

        Arguments:
           switches: List with command-line switches (passed to `subprocess.run`).
           charset: Decode output using encoding that corresponds to this charset instead
             charset of primary test database.
           connect_db: When `True` adds primary test database DSN to switches.
           credentials: When `True` adds switches to connect as primary test database user.

        By default, GSTAT is executed on primary test database, and output is captured into
        `stdout` and `stderr`, and exit code is stored to `return_code`. If pytest `--save-output`
        command-line option is used, the content of stdout/stderr is also stored into test
        protocol files with `.out`/`.err` suffix.

        Example::

           act_1.gstat(switches=['-h'])
           act_1.gstat(switches=['-h', str(test_db)], connect_db=False)

        .. important::

           If `return_code` is not zero, and script execution failure is not expected (either
           via defined `expected_stderr` value or using `combine_output` = True), it raises and
           `Exception` with "gstat execution failed" message and prints content of stdout
           and stderr.
        """
        __tracebackhide__ = True
        out_file: Path = self.outfile.with_suffix('.out')
        err_file: Path = self.outfile.with_suffix('.err')
        if out_file.is_file():
            out_file.unlink()
        if err_file.is_file():
            err_file.unlink()
        #
        charset = charset.upper() if charset else self.db.charset
        if io_enc is None:
            io_enc = CHARSET_MAP[charset]
        params = [_vars_['gsec']]
        if switches:
            params.extend(switches)
        if credentials:
            params.extend(['-user', self.db.user, '-password', self.db.password])
        result: CompletedProcess = run(params, input=input,
                                       encoding=io_enc, capture_output=True)
        if result.returncode and not bool(self.expected_stderr):
            self._node.add_report_section('call', 'gsec stdout', result.stdout)
            self._node.add_report_section('call', 'gsec stderr', result.stderr)
            raise ExecutionError("gsec execution failed")
        self.return_code: int = result.returncode
        self.stdout: str = result.stdout
        self.stderr: str = result.stderr
        # Store output
        if _vars_['save-output']:
            if self.stdout:
                out_file.write_text(self.stdout, encoding=io_enc)
            if self.stderr:
                err_file.write_text(self.stderr, encoding=io_enc)
    def gbak(self, *, switches: List[str]=None, charset: str=None, io_enc: str=None,
             input: str=None, credentials: bool=True, combine_output: bool=False) -> None:
        """Run `gbak` utility.

        Arguments:
           do_not_connect: Do not connect to primary test database on ISQL execution.
           charset: Firebird CHARACTER SET name.
           combine_output: Combine stdout/stderr into stdout.

        By default, script is executed on primary test database with NONE charset, and
        ISQL output is captured into `stdout` and `stderr`, and exit code is stored to
        `return_code`.

        If pytest `--save-output` command-line option is used, the content of stdout/stderr
        from ISQL is stored into protocol files with `.out`/`.err` suffix.

        .. important::

           If `return_code` is not zero, and script execution failure is not expected (either
           via defined `expected_stderr` value or using `combine_output` = True), it raises and
           `Exception` with "ISQL script execution failed" message and prints content of stdout
           and stderr.
        """
        __tracebackhide__ = True
        out_file: Path = self.outfile.with_suffix('.out')
        err_file: Path = self.outfile.with_suffix('.err')
        if out_file.is_file():
            out_file.unlink()
        if err_file.is_file():
            err_file.unlink()
        #
        charset = charset.upper() if charset else self.db.charset
        if io_enc is None:
            io_enc = CHARSET_MAP[charset]
        params = [_vars_['gbak']]
        if credentials:
            params.extend(['-user', self.db.user, '-password', self.db.password])
        if switches:
            params.extend(switches)
        if combine_output:
            result: CompletedProcess = run(params, input=input,
                                           encoding=io_enc, stdout=PIPE, stderr=STDOUT)
        else:
            result: CompletedProcess = run(params, input=input,
                                           encoding=io_enc, capture_output=True)
        if result.returncode and not (bool(self.expected_stderr) or combine_output):
            self._node.add_report_section('call', 'gbak stdout', result.stdout)
            self._node.add_report_section('call', 'gbak stderr', result.stderr)
            raise ExecutionError("gbak execution failed")
        self.return_code: int = result.returncode
        self.stdout: str = result.stdout
        self.stderr: str = result.stderr
        # Store output
        if _vars_['save-output']:
            if self.stdout:
                out_file.write_text(self.stdout, encoding=io_enc)
            if self.stderr:
                err_file.write_text(self.stderr, encoding=io_enc)
    def nbackup(self, *, switches: List[str], charset: str=None, io_enc: str=None,
                credentials: bool=True, combine_output: bool=False) -> None:
        """Run `nbackup` utility.

        Arguments:
           do_not_connect: Do not connect to primary test database on ISQL execution.
           charset: Firebird CHARACTER SET name.
           combine_output: Combine stdout/stderr into stdout.

        By default, script is executed on primary test database with NONE charset, and
        ISQL output is captured into `stdout` and `stderr`, and exit code is stored to
        `return_code`.

        If pytest `--save-output` command-line option is used, the content of stdout/stderr
        from ISQL is stored into protocol files with `.out`/`.err` suffix.

        .. important::

           If `return_code` is not zero, and script execution failure is not expected (either
           via defined `expected_stderr` value or using `combine_output` = True), it raises and
           `Exception` with "ISQL script execution failed" message and prints content of stdout
           and stderr.
        """
        __tracebackhide__ = True
        out_file: Path = self.outfile.with_suffix('.out')
        err_file: Path = self.outfile.with_suffix('.err')
        if out_file.is_file():
            out_file.unlink()
        if err_file.is_file():
            err_file.unlink()
        #
        charset = charset.upper() if charset else self.db.charset
        if io_enc is None:
            io_enc = CHARSET_MAP[charset]
        params = [_vars_['nbackup']]
        params.extend(switches)
        if credentials:
            params.extend(['-user', self.db.user, '-password', self.db.password])
        if combine_output:
            result: CompletedProcess = run(params, encoding=io_enc, stdout=PIPE, stderr=STDOUT)
        else:
            result: CompletedProcess = run(params, encoding=io_enc, capture_output=True)
        if result.returncode and not (bool(self.expected_stderr) or combine_output):
            self._node.add_report_section('call', 'nbackup stdout', result.stdout)
            self._node.add_report_section('call', 'nbackup stderr', result.stderr)
            raise ExecutionError("nbackup execution failed")
        self.return_code: int = result.returncode
        self.stdout: str = result.stdout
        self.stderr: str = result.stderr
        # Store output
        if _vars_['save-output']:
            if self.stdout:
                out_file.write_text(self.stdout, encoding=io_enc)
            if self.stderr:
                err_file.write_text(self.stderr, encoding=io_enc)
    def gfix(self, *, switches: List[str]=None, charset: str=None, io_enc: str=None,
             input: str=None, credentials: bool=True) -> None:
        """Run `gfix` utility.

        Arguments:
           do_not_connect: Do not connect to primary test database on ISQL execution.
           charset: Firebird CHARACTER SET name.
           combine_output: Combine stdout/stderr into stdout.

        By default, script is executed on primary test database with NONE charset, and
        ISQL output is captured into `stdout` and `stderr`, and exit code is stored to
        `return_code`.

        If pytest `--save-output` command-line option is used, the content of stdout/stderr
        from ISQL is stored into protocol files with `.out`/`.err` suffix.

        .. important::

           If `return_code` is not zero, and script execution failure is not expected (either
           via defined `expected_stderr` value or using `combine_output` = True), it raises and
           `Exception` with "ISQL script execution failed" message and prints content of stdout
           and stderr.
        """
        __tracebackhide__ = True
        out_file: Path = self.outfile.with_suffix('.out')
        err_file: Path = self.outfile.with_suffix('.err')
        if out_file.is_file():
            out_file.unlink()
        if err_file.is_file():
            err_file.unlink()
        #
        charset = charset.upper() if charset else self.db.charset
        if io_enc is None:
            io_enc = CHARSET_MAP[charset]
        params = [_vars_['gfix']]
        if switches:
            params.extend(switches)
        if credentials:
            params.extend(['-user', self.db.user, '-password', self.db.password])
        result: CompletedProcess = run(params, input=input,
                                       encoding=io_enc, capture_output=True)
        if result.returncode and not bool(self.expected_stderr):
            self._node.add_report_section('call', 'gfix stdout', result.stdout)
            self._node.add_report_section('call', 'gfix stderr', result.stderr)
            raise ExecutionError("gfix execution failed")
        self.return_code: int = result.returncode
        self.stdout: str = result.stdout
        self.stderr: str = result.stderr
        # Store output
        if _vars_['save-output']:
            if self.stdout:
                out_file.write_text(self.stdout, encoding=io_enc)
            if self.stderr:
                err_file.write_text(self.stderr, encoding=io_enc)
    def isql(self, *, switches: List[str], charset: str=None, io_enc: str=None,
             input: str=None, input_file: Path=None, connect_db: bool=True,
             credentials: bool=True, combine_output: bool=False, use_db: Database=None) -> None:
        """Run `isql` utility.

        Arguments:
           do_not_connect: Do not connect to primary test database on ISQL execution.
           charset: Firebird CHARACTER SET name.
           combine_output: Combine stdout/stderr into stdout.

        By default, script is executed on primary test database with NONE charset, and
        ISQL output is captured into `stdout` and `stderr`, and exit code is stored to
        `return_code`.

        If pytest `--save-output` command-line option is used, the content of stdout/stderr
        from ISQL is stored into protocol files with `.out`/`.err` suffix.

        .. important::

           If `return_code` is not zero, and script execution failure is not expected (either
           via defined `expected_stderr` value or using `combine_output` = True), it raises and
           `Exception` with "ISQL script execution failed" message and prints content of stdout
           and stderr.
        """
        __tracebackhide__ = True
        out_file: Path = self.outfile.with_suffix('.out')
        err_file: Path = self.outfile.with_suffix('.err')
        if out_file.is_file():
            out_file.unlink()
        if err_file.is_file():
            err_file.unlink()
        #
        db = self.db if use_db is None else use_db
        charset = charset.upper() if charset else db.charset
        params = [_vars_['isql'], '-ch', charset]
        if io_enc is None:
            io_enc = CHARSET_MAP[charset]
        if credentials:
            params.extend(['-user', db.user, '-password', db.password])
        params.extend(switches)
        if input_file is not None:
            params.extend(['-i', str(input_file)])
        if connect_db:
            params.append(str(db.dsn))
        if combine_output:
            result: CompletedProcess = run(params, input=input,
                                           encoding=io_enc, stdout=PIPE, stderr=STDOUT)
        else:
            result: CompletedProcess = run(params, input=input,
                                           encoding=io_enc, capture_output=True)
        if result.returncode and not (bool(self.expected_stderr) or combine_output):
            self._node.add_report_section('call', 'ISQL stdout', result.stdout)
            self._node.add_report_section('call', 'ISQL stderr', result.stderr)
            raise ExecutionError("ISQL execution failed")
        self.return_code: int = result.returncode
        self.stdout: str = result.stdout
        self.stderr: str = result.stderr
        # Store output
        if _vars_['save-output']:
            if self.stdout:
                out_file.write_text(self.stdout, encoding=io_enc)
            if self.stderr:
                err_file.write_text(self.stderr, encoding=io_enc)
    def svcmgr(self, *, switches: List[str]=None, charset: str=None, io_enc: str=None,
               connect_mngr: bool=True) -> None:
        """Run `fbsvcmgr` utility.

        Arguments:
           do_not_connect: Do not connect to primary test database on ISQL execution.
           charset: Charset for use by ISQL.
           combine_output: Combine stdout/stderr into stdout.

        By default, script is executed on primary test database with NONE charset, and
        ISQL output is captured into `stdout` and `stderr`, and exit code is stored to
        `return_code`.

        If pytest `--save-output` command-line option is used, the content of stdout/stderr
        from ISQL is stored into protocol files with `.out`/`.err` suffix.

        .. important::

           If `return_code` is not zero, and script execution failure is not expected (either
           via defined `expected_stderr` value or using `combine_output` = True), it raises and
           `Exception` with "ISQL script execution failed" message and prints content of stdout
           and stderr.
        """
        __tracebackhide__ = True
        out_file: Path = self.outfile.with_suffix('.out')
        err_file: Path = self.outfile.with_suffix('.err')
        if out_file.is_file():
            out_file.unlink()
        if err_file.is_file():
            err_file.unlink()
        #
        charset = charset.upper() if charset else self.db.charset
        if io_enc is None:
            io_enc = CHARSET_MAP[charset]
        params = [_vars_['fbsvcmgr']]
        if connect_mngr:
            params.extend([f"{_vars_['host']}:service_mgr" if _vars_['host'] else 'service_mgr',
                           'user', self.db.user, 'password', self.db.password])
        if switches:
            params.extend(switches)
        result: CompletedProcess = run(params, encoding=io_enc, capture_output=True)
        if result.returncode and not bool(self.expected_stderr):
            self._node.add_report_section('call', 'fbsvcmgr stdout', result.stdout)
            self._node.add_report_section('call', 'fbsvcmgr stderr', result.stderr)
            raise ExecutionError("fbsvcmgr execution failed")
        self.return_code: int = result.returncode
        self.stdout: str = result.stdout
        self.stderr: str = result.stderr
        # Store output
        if _vars_['save-output']:
            if self.stdout:
                out_file.write_text(self.stdout, encoding=io_enc)
            if self.stderr:
                err_file.write_text(self.stderr, encoding=io_enc)
    def connect_server(self, *, user: str='SYSDBA', password: str=None, role: str=None) -> Server:
        __tracebackhide__ = True
        return connect_server(_vars_['server'], user=user,
                              password=_vars_['password'] if password is None else password,
                              role=role)
    def get_firebird_log(self) -> List[str]:
        __tracebackhide__ = True
        with self.connect_server() as srv:
            srv.info.get_log()
            return srv.readlines()
    def is_version(self, version_spec: str) -> bool:
        spec = SpecifierSet(version_spec)
        return _vars_['version'] in spec
    def get_server_architecture(self) -> str:
        return _vars_['server-arch']
    def get_dsn(self, filename: Union[str, Path], protocol: str=None) -> str:
        return _connect_helper('', self.host, self.port, str(filename),
                               protocol if protocol else self.protocol)
    def reset(self) -> None:
        self.return_code: int = 0
        self._clean_stdout = None
        self._clean_stderr = None
        self._clean_expected_stdout = None
        self._clean_expected_stderr = None
        #
        self.expected_stdout = ''
        self.expected_stderr = ''
        self.stdout = ''
        self.stderr = ''
    def print_data(self, cursor: Cursor) -> None:
        # Print a header.
        for fieldDesc in cursor.description:
            print (fieldDesc[DESCRIPTION_NAME].ljust(fieldDesc[DESCRIPTION_DISPLAY_SIZE]),end=' ')
        print('')
        for fieldDesc in cursor.description:
            print ("-" * max((len(fieldDesc[DESCRIPTION_NAME]),fieldDesc[DESCRIPTION_DISPLAY_SIZE])),end=' ')
        print('')
        # For each row, print the value of each field left-justified within
        # the maximum possible width of that field.
        fieldIndices = range(len(cursor.description))
        for row in cursor:
            for fieldIndex in fieldIndices:
                fieldValue = row[fieldIndex]
                if not isinstance(fieldValue, str):
                    fieldValue = str(fieldValue)
                fieldMaxWidth = max((len(cursor.description[fieldIndex][DESCRIPTION_NAME]),cursor.description[fieldIndex][DESCRIPTION_DISPLAY_SIZE]))
                print (fieldValue.ljust(fieldMaxWidth), end=' ')
            print('')
    def print_data_list(self, cursor: Cursor, *, prefix: str='') -> None:
        for row in cursor:
            i = 0
            for fieldDesc in cursor.description:
                print(f'{prefix}{fieldDesc[DESCRIPTION_NAME].ljust(32)}{row[i]}')
                i += 1
            print()
    def trace(self, *, db_events: List[str]=None, svc_events: List[str]=None,
              config: List[str]=None, keep_log: bool=True, encoding: str='ascii',
              database: str=None) -> TraceSession:
        if config is not None:
            return TraceSession(self, config, keep_log=keep_log, encoding=encoding)
        else:
            config = []
            if db_events:
                database = self.db.db_path.name if database is None else database
                config.extend([f'database=%[\\\\/]{database}', '{', 'enabled = true'])
                config.extend(db_events)
                config.append('}')
            if svc_events:
                config.extend(['services', '{', 'enabled = true'])
                config.extend(svc_events)
                config.append('}')
            return TraceSession(self, config, keep_log=keep_log, encoding=encoding)
    def trace_to_stdout(self, *, upper: bool=False) -> None:
        log = ''.join(self.trace_log)
        self.stdout = log.upper() if upper else log
    def envar(self, name: str, value: str) -> Envar:
        return Envar(name, value)
    def match_any(self, line: str, patterns) -> bool:
        for pattern in patterns:
            if pattern.search(line):
                return True
        return False
    def print_callback(self, line: str) -> None:
        print(line, end='')
    def get_config(self, key: str) -> Optional[str]:
        with connect('employee') as con:
            c = con.cursor()
            row = c.execute('select RDB$CONFIG_VALUE from rdb$config where upper(RDB$CONFIG_NAME) = ?', [key.upper()]).fetchone()
        return row[0] if row else None
    @property
    def clean_stdout(self) -> str:
        """Content of `stdout` with unwanted isql noise removed and applied `substitutions` [R/O].
        """
        if self._clean_stdout is None:
            self._clean_stdout = self.string_strip(self.stdout, self.substitutions)
        return self._clean_stdout
    @property
    def clean_stderr(self) -> str:
        """Content of `stderr` with unwanted isql noise removed and applied `substitutions` [R/O].
        """
        if self._clean_stderr is None:
            self._clean_stderr = self.string_strip(self.stderr, self.substitutions)
        return self._clean_stderr
    @property
    def clean_expected_stdout(self) -> str:
        """Content of `expected_stdout` with unwanted isql noise removed and applied `substitutions` [R/O].
        """
        if self._clean_expected_stdout is None:
            self._clean_expected_stdout = self.string_strip(self.expected_stdout, self.substitutions)
        return self._clean_expected_stdout
    @property
    def clean_expected_stderr(self) -> str:
        """Content of `expected_stderr` with unwanted isql noise removed and applied `substitutions` [R/O].
        """
        if self._clean_expected_stderr is None:
            self._clean_expected_stderr = self.string_strip(self.expected_stderr, self.substitutions)
        return self._clean_expected_stderr
    @property
    def vars(self) -> Dict[str]:
        "Directory with plugin various configuration parameters and variables."
        return _vars_
    @property
    def host(self) -> str:
        "Host machine of tested Firebird server."
        return _vars_['host']
    @property
    def port(self) -> str:
        "Port of tested Firebird server."
        return _vars_['port']
    @property
    def protocol(self) -> str:
        "Default protocol for connections to databases."
        return _vars_['protocol']
    @property
    def security_db(self) -> str:
        "Path to Firebird security database."
        return _vars_['security-db']
    @property
    def home_dir(self) -> Path:
        "Path to Firebird home directory."
        return _vars_['home-dir']
    @property
    def bin_dir(self) -> Path:
        "Path to directory with Firebird utilities."
        return _vars_['bin-dir']
    @property
    def files_dir(self) -> Path:
        "Path to directory with test suite data files."
        return _vars_['files']
    @property
    def platform(self) -> str:
        "Current execution platform identifier."
        return _platform

def isql_act(db_fixture_name: str, script: str, *, substitutions: List[str]=None):

    @pytest.fixture
    def isql_act_fixture(request: FixtureRequest) -> Action:
        db: Database = request.getfixturevalue(db_fixture_name)
        f: Path = Path.cwd() / 'out' / request.module.__name__.replace('.', '/')
        if _vars_['save-output'] and not f.parent.exists():
            f.parent.mkdir(parents=True)
        f = f.with_name(f'{f.stem}-{request.function.__name__}.out')
        result: Action = Action(db, script, substitutions, f, request.node)
        return result

    return isql_act_fixture

def python_act(db_fixture_name: str, *, substitutions: List[str]=None):

    @pytest.fixture
    def python_act_fixture(request: FixtureRequest) -> Action:
        db: Database = request.getfixturevalue(db_fixture_name)
        f: Path = Path.cwd() / 'out' / request.module.__name__.replace('.', '/')
        if _vars_['save-output'] and not f.parent.exists():
            f.parent.mkdir(parents=True)
        f = f.with_name(f'{f.stem}-{request.function.__name__}.out')
        result: Action = Action(db, '', substitutions, f, request.node)
        return result

    return python_act_fixture

def temp_file(filename: Union[str, Path]):
    """Factory function that returns :doc:`fixture <fixture>` providing the `Path` to
    temporary file.

    Arguments:
        filename: File name.

    .. note::

       Created fixture has only one purpose: if specified temporary file exists at fixture
       `teardown`, it is removed.
    """

    @pytest.fixture
    def temp_file_fixture(tmp_path) -> Path:
        tmp_file = tmp_path / filename
        yield tmp_file
        if tmp_file.is_file():
            tmp_file.unlink()

    return temp_file_fixture

def temp_files(filenames: List[Union[str, Path]]):
    """Factory function that returns :doc:`fixture <fixture>` providing the list of `Path`
    instances to temporary files.

    Arguments:
        filenames: List of file names.

    .. note::

       Created fixture has only one purpose: if any from specified temporary file exists
       at fixture `teardown`, it is removed.
    """

    @pytest.fixture
    def temp_files_fixture(tmp_path) -> List[Path]:
        tmp_files = []
        for filename in filenames:
            tmp_files.append(tmp_path / filename)
        yield tmp_files
        for tmp_file in tmp_files:
            if tmp_file.is_file():
                tmp_file.unlink()

    return temp_files_fixture

