import copy

class Description(object):
    """ Defines the description of a relation (columns, types,...) """
    def __str__(self):
        return self.columns + " " + self.canNull + " " + self.types

    def convert_type(self, SQLType):
        """ Converts a SQLType (VARCHAR, NULL, ...) into a Python type (str, None, ...). We consider DECIMAL, FLOAT and DOUBLE PRECISION as float """

        """ What do we do with DATE, TIME, TIMESTAMP, INTERVAL, ARRAY, MULTISET, XML?"""
        types = SQLType.split('(')
        if types[0] == 'VARCHAR' or types[0] == 'CHAR' or types[0] == 'CHARACTER' or types[0] == 'BINARY' or types[0] == 'VARBINARY':
            return 'str'
        elif types[0] == 'DECIMAL' or types[0] == 'NUMERIC' or types[0] == 'FLOAT' or types[0] == 'DOUBLE PRECISION':
            return 'float'
        elif types[0] == 'INTEGER' or types[0] == 'BIGINT':
            return 'int'
        print(types)

    def parse(self, describe):
        """ Reads the result of a describe request and puts the information into this structure """

        """ Describe looks like: (ID, 'Name', 'Type', is NotNull, DefaultValue, is PK)"""
        """ TODO """
        print(describe)
        self.columns = []
        self.canNull = []
        self.types = []
        for i in describe:
            self.columns.append(i[1])
            self.canNull.append(i[3] == 0)
            self.types.append(self.convert_type(i[2]))
        print(self.columns)

    def getColumnNames(self):
        """ Returns a tuple with the names of the columns """
        return copy.deepcopy(self.columns)

    def isColumnName(self, name):
        """ Returns true if the name is in the list of columns' names """
        return name in self.columns

    def changeColumnName(self, name, newName):
        """ Changes the name of the corresponding column into the newName. If the column does not exist or if the new name already exists, an exception is raised """
        if not self.isColumnName(name) or self.isColumnName(newName):
            raise Exception
        for i in range(0, len(self.columns)):
            if self.columns[i] == name:
                self.columns[i] = newName
                return

    def getColumnType(self, name):
        """ Return the type that the column 'name' supports (Integer, Text,...) """
        pass

    def keepColumns(self, names):
        """ Keeps only the columns that have a name in the given list """
        pass

    def canBeNull(self, name):
        """ Returns true if the values in the column with the name 'name' can be null, false otherwise """
        pass
