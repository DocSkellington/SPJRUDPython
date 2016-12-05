import sqlite3

class MissingDatabaseException(Exception):
    """ Handles the case where the user tries to use a command on a database when no database is loaded"""
    pass

class Database(object):
    """ Defines a database and its operations """
    def __str__(self):
        return self.DB + " " + str(self.tables)

    def __init__(self):
        """ The constructor """
        self.DB = ""
        self.conn = None
        self.c = None
        self.tables = []

    def connect_to_SQL(self, DB):
        """ Connects to a SQL database """
        if self.DB != DB:
            self.DB = DB
            self.conn = sqlite3.connect(DB)
            self.c = self.conn.cursor()
            self.c.execute("SELECT name FROM sqlite_master WHERE type='table'")
            self.tables = self.c.fetchall()

    def execute(self, command):
        """ Executes a command """
        if self.conn != None:
            self.c.execute(command)
        else:
            raise MissingDatabaseException()

    def commit(self):
        """ Saves changes """
        if self.conn != None:
            self.conn.commit()
        else:
            raise MissingDatabaseException()

    def close(self):
        """ Closes the connection to the database """
        if self.conn != None:
            self.conn.close()
            self.conn = None
            self.c = None
            self.tables = []
        else:
            raise MissingDatabaseException()

    def describe(self, table):
        """ Retrieves the information of the table """
        if self.conn != None:
            self.c.execute('PRAGMA TABLE_INFO({})'.format(table))
            info = self.c.fetchall()
            return info
        else:
            raise MissingDatabaseException()

    def belongs(self, table):
        """ Does the table belong to the database ? """
        if self.conn != None:
            return (table,) in self.tables
        else:
            raise MissingDatabaseException()
