#-*- coding: utf-8 -*-
#
# Fork of Tornado Database using Postgres and Mysql


# Python Imports
import logging
import os
import threading
import time

# Extern Imports
import tornado.options
from tornado.options import options

# Project Imports
import aegis.stdlib


# Import drivers as needed and set up error classes
pgsql_available = False
PgsqlIntegrityError = None
PgsqlOperationalError = None
PgsqlDatabaseError = None
PgsqlProgrammingError = None
PgsqlUniqueViolation = None
PgsqlAdminShutdown = None
try:
    import psycopg2
    pgsql_available = True
    # These are here for mapping errors from psycopg2 into application namespace
    PgsqlIntegrityError = psycopg2.IntegrityError
    PgsqlOperationalError = psycopg2.OperationalError
    PgsqlDatabaseError = psycopg2.Error
    PgsqlProgrammingError = psycopg2.ProgrammingError
    PgsqlUniqueViolation = psycopg2.errors.UniqueViolation
    PgsqlAdminShutdown = psycopg2.errors.AdminShutdown
except Exception as ex:
    #logging.error("Couldn't import psycopg2 - maybe that's ok for now - but shim the exception types.")
    #logging.exception(ex)
    class PgsqlIntegrityError(BaseException):
        pass
    class PgsqlOperationalError(BaseException):
        pass
    class PgsqlDatabaseError(BaseException):
        pass
    class PgsqlProgrammingError(BaseException):
        pass
    class PgsqlUniqueViolation(BaseException):
        pass
    class PgsqlAdminShutdown(BaseException):
        pass

mysql_available = False
MysqlIntegrityError = None
MysqlOperationalError = None
MysqlInterfaceError = None
MysqlDataError = None
try:
    import MySQLdb
    mysql_available = True
    # These are here for mapping errors from MySQLdb into application namespace
    MysqlIntegrityError = MySQLdb._exceptions.IntegrityError
    MysqlOperationalError = MySQLdb._exceptions.OperationalError
    MysqlInterfaceError = MySQLdb._exceptions.InterfaceError
    MysqlDataError = MySQLdb._exceptions.DataError
except Exception as ex:
    #logging.error("Couldn't import MySQLdb - maybe that's ok for now - but shim the exception types.")
    #logging.exception(ex)
    class MysqlIntegrityError(BaseException):
        pass
    class MysqlOperationalError(BaseException):
        pass
    class MysqlInterfaceError(BaseException):
        pass
    class MysqlDataErrorError(BaseException):
        pass


# Thread-safe persistent database connection
dbconns = threading.local()


def db(use_schema=None, autocommit=True, **kwargs):
    if not hasattr(dbconns, 'databases'):
        dbconns.databases = {}
    # psycopg and probably mysqldb are thread-safe but not multiprocess-safe. If it's a separate process, create a new connection.
    # You'll want to do a db().close() after the multiprocessing function returns since the SSL breaks down anyways
    pid = os.getpid()
    dbconns.databases.setdefault(pid, {})
    if pgsql_available:
        # Autocommit==False will be its own short-lived connection, not cached or pooled, so we don't end up with transactions open from other cursors.
        if not autocommit:
            return PostgresConnection.connect(autocommit=False)
        # Autocommit==True we can cache the database connection and let autocommit handle cursor-transaction-safety
        pg_database = kwargs.get('pg_database') or options.pg_database
        if pg_database not in dbconns.databases[pid]:
            dbconns.databases[pid][pg_database] = PostgresConnection.connect(**kwargs)
        if not use_schema:
            use_schema = pg_database
    if mysql_available:
        mysql_database = kwargs.get('mysql_database') or options.mysql_database
        if mysql_database not in dbconns.databases[pid]:
            dbconns.databases[pid][mysql_database] = MysqlConnection.connect(**kwargs)
        if not use_schema:
            use_schema = mysql_database
    # Default situation - much better to be explicit which database we're connecting to!
    if not use_schema and len(dbconns.databases[pid]) == 1:
        use_schema = [dbconn for dbconn in dbconns.databases[pid].keys()][0]
    return dbconns.databases[pid][use_schema]


def dbnow(use_schema=None, dbconn=None):
    dbconn = dbconn if dbconn else db()
    return dbconn.get("SELECT NOW() AS now")

def sql_in_format(lst, cast):
    lst = [cast(lst_item) for lst_item in lst]
    format_strings = ','.join(['%s'] * len(lst))
    return lst, format_strings


class PostgresConnection(object):
    threads = {}

    def __init__(self, hostname, port, database, username=None, password=None, autocommit=True):
        """ Called by connect() class method using cls() notation """
        self.hostname = hostname
        self.port = port
        self.database = database
        args = "port={0} dbname={1}".format(self.port, self.database)
        if hostname is not None:
            args += " host={0}".format(hostname)
        if username is not None:
            args += " user={0}".format(username)
        if password is not None:
            args += " password={0}".format(password)
        self._db = None
        self._db_args = args
        self._autocommit = autocommit
        self._txn = None
        try:
            self._connect(autocommit=autocommit)
            if not autocommit:
                self._cursor()
        except Exception:
            logging.error("Cannot connect to PostgreSQL: %s", self.hostname, exc_info=True)

    @classmethod
    def connect(cls, autocommit=True, **kwargs):
        if 'pg_database' in kwargs:
            database = kwargs['pg_database']
            hostname = kwargs['pg_hostname']
            username = kwargs['pg_username']
            password = kwargs['pg_password']
            port = kwargs.get('pg_port', 5432)
        else:
            database = options.pg_database
            hostname = options.pg_hostname
            username = options.pg_username
            password = options.pg_password
            port = options.pg_port
        # force a new connection with a flag, or implicitly when using autocommit False
        if kwargs.get('force', False) or autocommit == False:
            return cls(hostname, port, database, username, password, autocommit=autocommit)
        # check existing connections
        ident = threading.current_thread().ident
        connections = cls.threads.setdefault(ident, {})
        if not database in connections:
            conn = cls(hostname, port, database, username, password)
            conn.database = database
            conn._connect(autocommit)
            cls.threads[ident][database] = conn
        return connections[database]

    def _connect(self, autocommit):
        self._db = psycopg2.connect(self._db_args)
        self._db.autocommit = autocommit

    def _cursor(self):
        # Connect if not connected.
        if self._db is None:
            self._connect(self._autocommit)
        # If auto-commit then return a new cursor immediately.
        if self._autocommit:
            return self._db.cursor()
        # The connection is single-use when doing a transaction via autocommit=False. That's the cursor to use until we commit the transaction.
        if not self._txn:
            self._txn = self._db.cursor()
        return self._txn

    def __del__(self):
        self.close()

    def close(self):
        if getattr(self, "_db", None) is not None:
            self._db.close()
            self._db = None

    def commit(self):
        if getattr(self, "_db", None) is not None:
            self._db.commit()
            self._txn = None

    def rollback(self):
        if getattr(self, "_db", None) is not None:
            self._db.rollback()
            self._txn = None

    def _execute(self, cursor, query, parameters, **kwargs):
        max_tries = 1
        try_cnt = 0
        while try_cnt < max_tries:
            try_cnt += 1
            try:
                aegis.stdlib.incr_start(aegis.stdlib.get_timer(), 'database')
                result = cursor.execute(query, parameters)
                aegis.stdlib.incr_stop(aegis.stdlib.get_timer(), 'database')
                return result
            except PgsqlUniqueViolation as ex:
                # UniqueViolation doesn't need to close connection, it needs to be handled in application
                raise
            except (psycopg2.Error, PgsqlAdminShutdown, PgsqlOperationalError) as ex:
                retry_errors = ['SSL SYSCALL error: EOF detected']
                if hasattr(ex, 'args') and ex.args[0] and max_tries < 3:
                    logging.warning("Got EOF or similar error. Retrying up to twice.")
                    max_tries += 1
                    continue
                logging.error("General Error at PostgreSQL - close connection/rollback")
                logging.error("Query Was: %s", query)
                logging.exception(ex)
                self.close()
                raise

    def iter(self, query, *parameters, **kwargs):
        """Returns an iterator for the given query and parameters."""
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters)
            column_names = [d[0] for d in cursor.description]
            if kwargs.get('cls'):
                for row in cursor:
                    yield kwargs['cls'](zip(column_names, row))
            else:
                for row in cursor:
                    yield Row(zip(column_names, row))
        finally:
            cursor.close()

    def query(self, query, *parameters, **kwargs):
        """ Returns a row list for the given query and parameters."""
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters, **kwargs)
            column_names = [d[0] for d in cursor.description]
            cls = kwargs.get('cls')
            if cls:
                rows = [cls(list(zip(column_names, row))) for row in cursor]
            else:
                rows = [Row(zip(column_names, row)) for row in cursor]
            if kwargs.get('return_column_names'):
                return (rows, column_names)
            return rows
        finally:
            if not self._txn:
                cursor.close()

    def get(self, query, *parameters, **kwargs):
        """ Returns the first row returned for the given query."""
        rows = self.query(query, *parameters, **kwargs)
        if not rows:
            return None
        elif len(rows) > 1:
            raise Exception("Multiple rows returned for Database.get() query")
        else:
            return rows[0]

    def execute(self, query, *parameters, **kwargs):
        # If it's an INSERT, return the lastrowid. Otherwise return the rowcount.
        if query.startswith('INSERT'):
            return self.execute_lastrowid(query, *parameters, **kwargs)
        else:
            return self.execute_rowcount(query, *parameters, **kwargs)

    def execute_lastrowid(self, query, *parameters, **kwargs):
        # Executes the given query, returning the lastrowid from the query.
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters)
            if cursor.rowcount > 0:
                try:
                    return cursor.fetchone()[0]
                except PgsqlProgrammingError as ex:
                    logging.error("No Results even though cursor says rowcount > 0. Probably left out '... RETURNING row_id'")
                    return None
        finally:
            if not self._txn:
                cursor.close()

    def execute_rowcount(self, query, *parameters, **kwargs):
        # Executes the given query, returning the rowcount from the query.
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters)
            return cursor.rowcount
        finally:
            if not self._txn:
                cursor.close()


class MysqlConnection(object):
    """ From torndb originally """
    def __init__(self, hostname, port, database, username=None, password=None, max_idle_time=7 * 3600):
        self.hostname = hostname
        self.database = database
        self.max_idle_time = max_idle_time
        args = dict(use_unicode=True, charset="utf8mb4", db=database, sql_mode="TRADITIONAL")
        if username is not None:
            args["user"] = username   # MysqlDB Interface param is 'user'
        if password is not None:
            args["passwd"] = password
        if not hostname:
            logging.error("ALERT TO DEVELOPER: No hostname specified for MysqlConnection. Check it's specified. Check environment variable being set.")
        args["host"] = hostname
        args["port"] = port
        self._db_init_command = 'SET time_zone = "+0:00"'
        self._db = None
        self._db_args = args
        self._last_use_time = time.time()
        try:
            self.reconnect()
        except Exception:
            logging.error("Cannot connect to MySQL on %s", self.hostname, exc_info=True)

    threads = {}

    @classmethod
    def connect(cls, **kwargs):
        if 'mysql_database' in kwargs:
            hostname = kwargs['mysql_hostname']
            port = kwargs['mysql_port']
            database = kwargs['mysql_database']
            username = kwargs['mysql_username']
            passwd = kwargs['mysql_password']
        else:
            hostname = options.mysql_hostname
            port = options.mysql_port
            database = options.mysql_database
            username = options.mysql_username
            passwd = options.mysql_password
        # force a new connection
        if kwargs.get('force', False):
            return cls(hostname, port, database, username, passwd)
        # check existing connections
        ident = threading.current_thread().ident
        target = '%s@%s' % (database, hostname)
        connections = cls.threads.setdefault(ident, {})
        if not target in connections:
            conn = cls(hostname, port, database, username, passwd)
            conn.execute("SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci", disable_audit_sql=True)
            conn.database = database
            cls.threads[ident][target] = conn
        #conn_debug = "%s %s %s" % (ident, target, connections)
        #aegis.stdlib.logw(conn_debug, "CONN DEBUG")
        return connections[target]

    def __del__(self):
        self.close()

    def close(self):
        """Closes this database connection."""
        if getattr(self, "_db", None) is not None:
            self._db.close()
            self._db = None

    def reconnect(self):
        """Closes the existing database connection and re-opens it."""
        self.close()
        self._db = MySQLdb.connect(autocommit=True, connect_timeout=3, **self._db_args)
        self.execute(self._db_init_command, disable_audit_sql=True)

    def iter(self, query, *parameters, **kwargs):
        """Returns an iterator for the given query and parameters."""
        self._ensure_connected()
        cursor = self._db.cursor(MySQLdb.cursors.SSCursor)
        try:
            self._execute(cursor, query, parameters)
            column_names = [d[0] for d in cursor.description]
            if kwargs.get('cls'):
                for row in cursor:
                    yield kwargs['cls'](zip(column_names, row))
            else:
                for row in cursor:
                    yield Row(zip(column_names, row))
        finally:
            cursor.close()

    def query(self, query, *parameters, **kwargs):
        """Returns a row list for the given query and parameters."""
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters)
            column_names = [d[0] for d in cursor.description]
            if kwargs.get('cls'):
                rows = [kwargs['cls'](zip(column_names, row)) for row in cursor]
            else:
                rows = [Row(zip(column_names, row)) for row in cursor]
            if kwargs.get('return_column_names'):
                return (rows, column_names)
            return rows
        finally:
            cursor.close()

    def get(self, query, *parameters, **kwargs):
        """Returns the first row returned for the given query."""
        rows = self.query(query, *parameters)
        if not rows:
            return None
        elif len(rows) > 1:
            raise Exception("Multiple rows returned for Database.get() query")
        else:
            row = rows[0]
            if row and kwargs.get('cls'):
                row = kwargs['cls'](row)
            return row

    # rowcount is a more reasonable default return value than lastrowid,
    # but for historical compatibility execute() must return lastrowid.
    def execute(self, query, *parameters, **kwargs):
        """Executes the given query, returning the lastrowid from the query."""
        if query.startswith('INSERT'):
            return self.execute_lastrowid(query, *parameters, **kwargs)
        else:
            return self.execute_rowcount(query, *parameters, **kwargs)

    def execute_lastrowid(self, query, *parameters, **kwargs):
        """Executes the given query, returning the lastrowid from the query."""
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters)
            return cursor.lastrowid
        finally:
            cursor.close()

    def execute_rowcount(self, query, *parameters, **kwargs):
        """Executes the given query, returning the rowcount from the query."""
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters)
            return cursor.rowcount
        finally:
            cursor.close()

    def executemany(self, query, parameters):
        """Executes the given query against all the given param sequences.
        We return the lastrowid from the query.
        """
        return self.executemany_lastrowid(query, parameters)

    def executemany_lastrowid(self, query, parameters):
        """Executes the given query against all the given param sequences.
        We return the lastrowid from the query.
        """
        cursor = self._cursor()
        try:
            cursor.executemany(query, parameters)
            return cursor.lastrowid
        finally:
            cursor.close()

    def executemany_rowcount(self, query, parameters):
        """Executes the given query against all the given param sequences.
        We return the rowcount from the query.
        """
        cursor = self._cursor()
        try:
            cursor.executemany(query, parameters)
            return cursor.rowcount
        finally:
            cursor.close()

    def _ensure_connected(self):
        # Mysql by default closes client connections that are idle for
        # 8 hours, but the client library does not report this fact until
        # you try to perform a query and it fails.  Protect against this
        # case by preemptively closing and reopening the connection
        # if it has been idle for too long (7 hours by default).
        if (self._db is None or (time.time() - self._last_use_time > self.max_idle_time)):
            self._last_use_time = time.time()
            self.reconnect()

    def _cursor(self):
        self._ensure_connected()
        return self._db.cursor()

    def _execute(self, cursor, query, parameters):
        max_tries = 1
        try_cnt = 0
        while try_cnt < max_tries:
            try_cnt += 1
            try:
                aegis.stdlib.incr_start(aegis.stdlib.get_timer(), 'database')
                result = cursor.execute(query, parameters)
                aegis.stdlib.incr_stop(aegis.stdlib.get_timer(), 'database')
                return result
            except MysqlInterfaceError as ex:
                logging.error("InterfaceError with MySQL on %s. Close connection and raise.", self.hostname)
                logging.exception(ex)
                self.close()
                raise
            except MysqlOperationalError as ex:
                # 1205: 'Lock wait timeout exceeded; try restarting transaction'
                # 1213: 'Deadlock found when trying to get lock; try restarting transaction'
                retry_errors = (1205, 1213)
                if hasattr(ex, 'args') and ex.args[0] in retry_errors:
                    logging.warning("Deadlock found or Lock wait timeout exceeded. Restarting transaction")
                    max_tries += 1
                    continue
                logging.error("OperationalError with MySQL on %s. Close connection and raise.", self.hostname)
                logging.error("Query Was: %s", query)
                logging.exception(ex)
                self.close()
                raise


# To support inserting something literally, like NOW(), into mini-ORM below
class Literal(str):
    pass


class Row(dict):
    """ A dict that allows for object-like property access syntax."""
    def __getattr__(self, name):
        if name not in self:
            raise AttributeError(name)
        return self[name]

    @classmethod
    def _table_name(cls):
        # Choose table name based on model table_names attribute
        #aegis.stdlib.logw(cls.table_name, "TABLE NAME")
        if hasattr(cls, 'table_names'):
            if aegis.config.get('pg_database'):
                cls.table_name = cls.table_names['pgsql']
            elif aegis.config.get('mysql_database'):
                cls.table_name = cls.table_names['mysql']
        return cls.table_name

    @classmethod
    def logw(cls, msg, value, row_id=''):
        logging.warning("%s: %s %s", msg, value, row_id)

    @classmethod
    def scan_id(cls, column, row_id):
        sql = 'SELECT * FROM %s WHERE %s=%%s' % (cls._table_name(), column)
        return db().query(sql, row_id, cls=cls)

    @classmethod
    def map_items(cls, items, key):
        return cls([(item[key], item) for item in items])

    @classmethod
    def map_id(cls, row_id, where_col, key_col, debug=False):
        items = cls.map_items(cls.scan_id(where_col, row_id), key_col)
        if debug:
            cls.logw("WHERE", where_col, row_id)
            logging.warning("")
            cls.logw("SCAN", cls.scan_id(where_col, row_id), row_id)
            logging.warning("")
            cls.logw("ITEMS", items, row_id)
        return items

    @classmethod
    def get_id(cls, column_id_val, member_id=None, dbconn=None):
        if not aegis.stdlib.validate_int(column_id_val):
            return None
        sql = 'SELECT * FROM %s WHERE %s=%%s'
        args = [int(column_id_val)]
        if member_id:
            sql = sql + ' AND member_id=%%s'
            args.append(int(member_id))
        sql = sql % (cls._table_name(), cls.id_column)
        dbconn = dbconn if dbconn else db()
        val = dbconn.get(sql, *args, cls=cls)
        return val

    @classmethod
    def scan(cls, dbconn=None):
        dbconn = dbconn if dbconn else db()
        sql = 'SELECT * FROM %s' % cls.table_name
        return dbconn.query(sql, cls=cls)

    @classmethod
    def scan_ids(cls, row_ids, dbconn=None):
        if not row_ids:
            return []
        dbconn = dbconn if dbconn else db()
        # Fail fast if any of the data are bad, to not return confusing results
        try:
            args, fmt = aegis.database.sql_in_format(row_ids, int)
        except ValueError as ex:
            logging.exception(ex)
            logging.error("Bad arguments passed from %s to aegis.database.Row.scan_ids(): %s", aegis.stdlib.get_caller(), row_ids)
            return []
        sql = "SELECT * FROM "+cls._table_name()+" WHERE "+cls.id_column+" IN ("+fmt+")"
        return dbconn.query(sql, *args, cls=cls)

    # kva_split(), insert(), update() together are a mini-ORM in processing arbitrary column-value combinations on a row.
    # define table_name and data_columns to know which are allowed to be set along with user action
    # columns and where are simple dictionaries: {'full_name': "FULL NAME", 'email': 'email@example.com'}
    @staticmethod
    def kva_split(columns):
        keys = []
        values = []
        args = []
        for key, value in columns.items():
            keys.append('%s' % key)
            if isinstance(value, Literal):
                values.append(value)
            else:
                values.append('%s')
                args.append(value)
        return keys, values, args

    @classmethod
    def insert_columns(cls, sql_txt='INSERT INTO %(db_table)s (%(keys)s) VALUES (%(values)s)', dbconn=None, **columns):
        dbconn = dbconn if dbconn else db()
        db_table = cls._table_name()
        # Filter out anything that's not in optional, pre-specified list of data columns
        data_columns = hasattr(cls, 'data_columns') and cls.data_columns
        if data_columns:
            columns = dict( [ (key, val) for key, val in columns.items() if key in data_columns] )
        keys, values, args = cls.kva_split(columns)
        if type(dbconn) is PostgresConnection:
            sql_txt += " RETURNING " + cls.id_column
        sql = sql_txt % {'db_table': db_table, 'keys': ', '.join(keys), 'values': ', '.join(values)}
        #aegis.stdlib.logw(sql, "SQL")
        #aegis.stdlib.logw(args, "ARGS")
        return dbconn.execute(sql, *args)

    @classmethod
    def update_columns(cls, columns, where, dbconn=None):
        dbconn = dbconn if dbconn else db()
        if not columns:
            logging.debug('Nothing to update. Skipping query')
            return 0
        db_table = cls._table_name()
        # Filter out anything that's not in optional, pre-specified list of data columns
        data_columns = hasattr(cls, 'data_columns') and cls.data_columns
        if data_columns:
            columns = dict( [ (key,val) for key, val in columns.items() if key in data_columns] )
        if not columns:
            return 0
        # SET clause
        keys, values, args = cls.kva_split(columns)
        set_clause = ', '.join(['%s=%s' % (key, value) for key, value in zip(keys, values)])
        # WHERE clause
        keys, values, args2 = cls.kva_split(where)
        args += args2
        where_clause = ' AND '.join(['%s=%s' % (key, value) for key, value in zip(keys, values)])
        # SQL statement
        sql = 'UPDATE %s SET %s WHERE %s' % (db_table, set_clause, where_clause)
        #aegis.stdlib.logw(sql, "SQL")
        #aegis.stdlib.logw(args, "ARGS")
        return dbconn.execute_rowcount(sql, *args)

    @classmethod
    def set_row(cls, data, dbconn):
        # INSERT or UPDATE
        data_row = cls.get_id(data[cls.id_column])
        if data_row:
            # compare everything in **data to data_row and don't update if there's no update
            cols = {}
            where = {cls.id_column: data_row[cls.id_column]}
            for key, value in data.items():
                if key in data_row and data_row[key] != value:
                    cols[key] = value
            if cols:
                return cls.update_columns(cols, where, dbconn=dbconn)
            else:
                # 0 rows updated when no columns to update
                return 0
        else:
            row_id = cls.insert_columns(**data, dbconn=dbconn)
            return 1
