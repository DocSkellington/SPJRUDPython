import copy

class Description(object):
    """ Defines the description of a relation (columns, types,...) """
    def parse(self, describe):
        """ Reads the result of a describe request and puts the information into this structure """
        pass

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
