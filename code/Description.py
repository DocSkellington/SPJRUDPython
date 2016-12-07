import copy

class InvalidColumnNameException(Exception):
    """ Handles the case where the column name does not exist """
    pass

class DoubleColumnNameException(Exception):
    """ Handles the case where the column is already in the schema """
    pass

class InvalidTypeException(Exception):
    """ Handles the case where the type is not recognised """
    pass

def convert_type(SQLType):
    """ Converts a SQLType (VARCHAR, NULL, ...) into a Python type (str, None, ...). We consider DECIMAL, FLOAT and DOUBLE PRECISION as float
    Args:
        SQLType (str): a string that contains an SQL VARTYPE
    """

    #What do we do with DATE, TIME, TIMESTAMP, INTERVAL, ARRAY, MULTISET, XML?
    types = SQLType.split('(')
    if types[0] == 'VARCHAR' or types[0] == 'CHAR' or types[0] == 'CHARACTER' or types[0] == 'BINARY' or types[0] == 'VARBINARY':
        return str
    elif types[0] == 'DECIMAL' or types[0] == 'NUMERIC' or types[0] == 'FLOAT' or types[0] == 'DOUBLE PRECISION':
        return float
    elif types[0] == 'INTEGER' or types[0] == 'BIGINT':
        return int
    else:
        raise InvalidTypeException(type + "is an invalid type")

class Description(object):
    """ Defines the description of a relation (columns, types,...) """

    def __init__(self):
        self.columns = []
        self.canNull = {}
        self.types = {}

    def __str__(self):
        return str(self.columns) + " " + str(self.canNull) + " " + str(self.types)

    def __repr__(self):
        return str(self)

    def parse(self, describe):
        """ Reads the result of a describe request and puts the information into this structure
        Args:
            describe (str): the result of a describe request
        """

        """ A tuple in describe looks like: (ID, 'Name', 'Type', is NotNull, DefaultValue, is PK)"""
        self.columns = []
        self.canNull = {}
        self.types = {}
        for i in describe:
            self.columns.append(i[1])
            self.canNull[i[1]] = (i[3] == 0)
            self.types[i[1]] = convert_type(i[2])

    def get_column_names(self):
        """ Returns a list with the names of the columns """
        return copy.deepcopy(self.columns)

    def is_column_name(self, name):
        """ Returns true if the name is in the list of columns' names
        Args:
            name (str): The name we want to check
        """
        return name in self.columns

    def change_column_name(self, name, newName):
        """ Changes the name of the corresponding column into the newName. If the column does not exist or if the new name already exists, InvalidColumnNameException is raised
        Args:
            name (str): The name we want to change
            newName (str): The name we want to use
        """
        if not self.is_column_name(name) or self.is_column_name(newName):
            raise InvalidColumnNameException(name + " is not a column name")
        for i in range(0, len(self.columns)):
            if self.columns[i] == name:
                self.columns[i] = newName
                return

    def get_column_type(self, name):
        """ Return the type that the column 'name' supports (Integer, Text,...)
        Args:
            name (str): The name of the column
        """
        if not self.is_column_name(name):
            raise InvalidColumnNameException(name + " is not a column name")
        return self.types[name]

    def keep_columns(self, names):
        """ Keeps only the columns whose name is in the given list
        Args:
            names (list of str): The names of the columns we want to keep
        """
        columns = []
        canNull = {}
        types = {}

        for column in self.columns:
            if column in names:
                columns.append(column)
                canNull[column] = self.canNull[column]
                types[column] = self.types[column]

        self.column = columns
        self.canNull = canNull
        self.types = types


    def add_column(self, name, vartype, canNull):
        """ Adds a column into the description. The column is defined by a name, a vartype and if it can contain NULL
            The schema cannot contain multiple columns with the same name
        Args:
            name (str): The name of the column
            vartype (type): The type of the column (in Python type)
            canNull (boolean): Whether the column can contain NULL or not
        """
        if self.is_column_name(name):
            raise DoubleColumnNameException(name + " is already in the schema")
        self.columns.append(name)
        self.canNull[name] = canNull
        self.types[name] = vartype

    def can_be_null(self, name):
        """ Returns true if the values in the column with the name 'name' can be null, false otherwise
        Args:
            name (str): The name of a column
        """
        if not self.is_column_name(name):
            raise InvalidColumnNameException(name + " is not a column name")
        return self.canNull[name]
