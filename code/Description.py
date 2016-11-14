
class Description(object):
    """ Defines the description of a relation (columns, types,...) """
    def parse(self, describe):
        """ Reads the result of a describe request and puts the information into this structure """
        pass

    def getColumnNames(self):
        """ Returns a tuple with the names of the columns """
        pass

    def isColumnName(self, name):
        """ Returns true if the name is in the list of columns' names """
        pass

    def changeColumnName(self, name, newName):
        """ Changes the name of the corresponding column into the newName. If the column does not exist, an exception is raised """
        pass

    def canBeNull(self, name):
        """ Returns true if the values in the column with the name 'name' can be null, false otherwise """
        pass
