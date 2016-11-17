import abc
import Database
import Description

class Operation(abc.ABC):
    def __init__(self, database):
        self.elements = []
        self.description = Description()
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
        """ Returns a deep copy of the description of this operation """
        return copy.deepcopy(description)

class Relation(Operation):
    def __init__(self, nameTable):
        super().__init__()
        self.nameTable = nameTable

    def check(self):
        if (self.database.belongs(self.nameTable)):
            self.description.parse(self.database.describe(self.nameTable))
            return True
        else:
            return False

    def translate(self):
        pass

class Rename(Operation):
    def __init__(self, name, newName, operation):
        super().__init__()
        self.name = name
        self.newName = newName
        self.elements = [operation]

    def check(self):
        if not self.elements[0].check():
            return False

        self.description = self.elements[0].getDescription()

        try:
            description.changeColumnName(name, newName)
            return True
        except:
            return False

    def translate(self):
        pass

class Projection(Operation):
    def __init__(self, columns, operation):
        super().__init__()
        self.columns = columns
        self.elements = [operation]

    def check(self):
        if not self.elements[0].check():
            return False
    
        self.description = self.elements[0].getDescription()

        for column in self.columns:
            if not description.isColumnName(columns):
                return False

        description.keepColumns(self.columns)
        return True

    def translate(self):
        pass

class Selection(Operation):
    def __init__(self, attribut, comparator, other, cst, operation):
        """ cst est un boolena. other est l'autre partie de la comparaison """
        super().__init__()
        self.attribut = attribut
        self.comparator = comparator
        self.other = other
        self.cst = cst
        self.elements = [operation]

    def check(self):
        if not self.elements[0].check:
            return False

        self.description = self.elements[0].getDescription()

        if not self.description.isColumnName(attribut):
            return False

        if self.cst:
            return self.description.getColumnType(attribut) is type(other)
        else:
            return self.description.isColumnName(other)

    def translate(self):
        pass
