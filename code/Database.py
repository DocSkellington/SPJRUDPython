import sqlite3
import Description
import copy
from Exceptions import *

class Database(object):
    """ Defines a database and its operations """
    def __str__(self):
        return self.DB + " " + str(self.tables) + " " + str(self.descriptions)

    def __init__(self):
        """ The constructor """
        self.DB = ""
        self.conn = None
        self.c = None
        self.tables = []
        self.descriptions = {}

    def connect_to_SQL(self, DB):
        """ Connects to a SQL database, retrieves the name and the description of the tables from the database
        Args:
            DB (str): The name of the database file
        """
        if self.DB != DB:
            self.DB = DB
            self.conn = sqlite3.connect(DB)
            self.c = self.conn.cursor()
            self.c.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = self.c.fetchall()
            for table in tables:
                desc = self.describe(table[0])
                description = Description.Description()
                description.parse(desc)
                self.add_description(table[0], description)

    def add_description(self, table, description):
        """ Adds a description in the database schema.
            The table can only appear once. Otherwise, an DoubledTableException is thrown
        Args:
            table (str): The name of the table
            description (Description.Description): The description of the table
        """
        if table in self.descriptions:
            raise DoubledTableException(table + " is already in the schema of the database")
        self.descriptions[table] = description
        self.tables.append(table)

    def get_description(self, table):
        """ Returns the description corresponding to the given table name. If the table is not stored, an MissingTableException is thrown
        Args:
            table (str): The name of the table
        """
        if table not in self.descriptions:
            raise MissingTableException(table + " is not a known table")
        return copy.deepcopy(self.descriptions[table])

    def get_number_tables(self):
        """ Returns the number of tables in this database
        """
        return len(self.tables)

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
        return table in self.tables

