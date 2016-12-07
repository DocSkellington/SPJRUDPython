import abc
import Database
import Description
import copy

class InvalidTypesComparaisonException(Exception):
    """ Handles the case where the user wants to compare two columns (or one column and a constant) of two different types """
    pass

class Operation(abc.ABC):
    """ Defines the common attributs of the operations
    """
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
    """ Defines a relation.
    """
    def __init__(self, nameRelation, database):
        super().__init__()
        self.nameRelation = nameRelation
        self.database = database

    def __repr__(self):
        return "Relation: " + self.nameRelation + " " + str(self.database) + " " + repr(self.elements)

    def check(self):
        if (self.database.belongs(self.nameRelation)):
            self.description = self.database.get_description(self.nameRelation)
            return True
        else:
            return False

    def translate(self):
        pass

class Rename(Operation):
    """ Defines a Rename operation
    """
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

        self.description.change_column_name(self.name, self.newName)
        return True

    def translate(self):
        pass

class Projection(Operation):
    """ Defines a Projection operation
    """
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
            if not self.description.is_column_name(column):
                return False

        self.description.keep_columns(self.columns)
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

class GreaterEqual(Comparator):
    def __str__(self):
        return ">="

    def translate(self):
        return str(self)

class Lesser(Comparator):
    def __str__(self):
        return "<"

    def translate(self):
        return str(self)

class LesserEqual(Comparator):
    def __str__(self):
        return "<="

    def translate(self):
        return str(self)

class Selection(Operation):
    """ Defines a Selection operation
    """
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

        if not self.description.is_column_name(self.attribut):
            raise Description.InvalidColumnNameException(self.attribut, self.description)

        if self.cst:
            if self.description.get_column_type(self.attribut) is type(self.other):
                return True
            else:
                raise InvalidTypesComparaisonException("Impossible to compare a " + str(self.description.get_column_type(self.attribut)) + " and a " + str(self.other))
        else:
            if self.description.is_column_name(self.other):
                if self.description.get_column_type(self.attribut) is self.description.get_column_type(self.other):
                    return True
                else:
                    raise InvalidTypesComparaisonException("Impossible to compare a " + str(self.description.get_column_type(self.attribut)) + " and a " + str(self.description.get_column_type(self.other)))
            else:
                raise Description.InvalidColumnNameException(self.other, self.description)

    def translate(self):
        pass
