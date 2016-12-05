import abc
import Database
import Description
import copy

class Operation(abc.ABC):
    def __init__(self):
        self.elements = []
        self.description = Description.Description()

    @abc.abstractmethod
    def check(self):
        """ Checks the syntax of the operation """
        pass

    @abc.abstractmethod
    def translate(self):
        """ Translates the operation in SPJRUD into a SQL request """
        pass

    def getDescription(self):
        """ Returns a deep copy of the description of this operation """
        return copy.deepcopy(self.description)

class Relation(Operation):
    def __init__(self, nameTable, database):
        super().__init__()
        self.nameTable = nameTable
        self.database = database

    def __repr__(self):
        return "Relation: " + self.nameTable + " " + str(self.database) + " " + repr(self.elements)

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
        #print(repr(self))

    def __repr__(self):
        return "Rename: " + self.name + " into " + self.newName + "; " + repr(self.elements)

    def check(self):
        if not self.elements[0].check():
            return False

        self.description = self.elements[0].getDescription()

        try:
            self.description.changeColumnName(self.name, self.newName)
            return True
        except Description.InvalidColumnName:
            return False

    def translate(self):
        pass

class Projection(Operation):
    def __init__(self, columns, operation):
        super().__init__()
        self.columns = columns
        self.elements = [operation]
        #print(repr(self))

    def __repr__(self):
        return "Projection: " + str(self.columns) + " " + repr(self.elements)

    def check(self):
        if not self.elements[0].check():
            return False
    
        self.description = self.elements[0].getDescription()

        for column in self.columns:
            if not self.description.isColumnName(column):
                return False

        self.description.keepColumns(self.columns)
        return True

    def translate(self):
        pass

class Comparator(abc.ABC):
    """ Defines a comparator used by the Selection/SELECT request """
    @abc.abstractmethod
    def translate(self):
        """ Translates the comparator in Select into a comparator used by a SELECT request """
        pass

class Equal(Comparator):
    def __str__(self):
        return "="

    def translate(self):
        return str(self)

class Different(Comparator):
    def __str__(self):
        return "<>"

    def translate(self):
        return str(self)

class Greater(Comparator):
    def __str__(self):
        return ">"

    def translate(self):
        return str(self)

class Lesser(Comparator):
    def __str__(self):
        return "<"

    def translate(self):
        return str(self)

class Selection(Operation):
    def __init__(self, attribut, comparator, other, cst, operation):
        """ cst est un boolena. other est l'autre partie de la comparaison """
        super().__init__()
        self.attribut = attribut
        self.comparator = comparator
        self.other = other
        self.cst = cst
        self.elements = [operation]
        #print(repr(self))

    def __repr__(self):
        return "Selection: " + self.attribut + " " + str(self.comparator) + " " + self.other + " (" + str(self.cst) + ") " + repr(self.elements)

    def check(self):
        if not self.elements[0].check():
            return False

        self.description = self.elements[0].getDescription()

        if not self.description.isColumnName(self.attribut):
            return False

        if self.cst:
            return self.description.getColumnType(self.attribut) is type(self.other)
        else:
            return self.description.isColumnName(self.other)

    def translate(self):
        pass
