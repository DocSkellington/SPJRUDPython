import abc
import Database

class Operation(abc.ABC):
    def __init__(self, database):
        self.elements = []
        self.description = []
        self.database = database

    @abc.abstractmethod
    def check(self):
        """ Checks the syntax of the operation """
        pass

    @abc.abstractmethod
    def translate(self):
        """ Translates the operation in SPJRUD into a SQL request """
        pass

    @abc.abstractmethod
    def getDescription(self):
        return description

class Relation(Operation):
    def __init__(self, nameTable):
        super().__init__()
        self.nameTable = nameTable

    def check(self):
        if (self.database.belongs(self.nameTable)):
            self.description = self.database.describe(self.nameTable)
            return true
        else:
            return False

    def translate(self):
        pass

