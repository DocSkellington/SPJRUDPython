import abc
import Database
import Description
import copy
from Exceptions import *
from SQLRequest import *

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
        """ Translates the operation in SPJRUD into a SQL request.
        Returns a SQLRequest object
        """
        pass

    def get_description(self):
        """ Returns a deep copy of the description of this operation """
        return copy.deepcopy(self.description)

class Relation(Operation):
    """ Defines a relation.
    """
    def __init__(self, nameRelation, database):
        super().__init__()
        self.nameRelation = nameRelation
        self.database = database

    def __str__(self):
        return "Relation: " + self.nameRelation

    def __repr__(self):
        return "Relation: " + self.nameRelation + " " + str(self.database) + " " + repr(self.elements)

    def check(self):
        if (self.database.belongs(self.nameRelation)):
            self.description = self.database.get_description(self.nameRelation)
        else:
            raise MissingTableException(self.nameRelation, self.database)

    def translate(self):
        request = SQLRequest()
        request.set_from_clause(self.nameRelation)
        columns = self.description.get_column_names()
        for column in columns:
            request.add_column(column)
        return request

class Rename(Operation):
    """ Defines a Rename operation
    """
    def __init__(self, name, newName, operation):
        super().__init__()
        self.name = name
        self.newName = newName
        self.elements = [operation]

    def __str__(self):
        return "Rename: " + self.name + " into " + self.newName + " of " + str(self.elements[0])

    def __repr__(self):
        return "Rename: " + self.name + " into " + self.newName + "; " + repr(self.elements)

    def check(self):
        self.elements[0].check()

        self.description = self.elements[0].get_description()

        try:
            self.description.change_column_name(self.name, self.newName)
        except Description.DoubleColumnNameException as err:
            raise Description.DoubleColumnNameException(err.columnName, err.description, "Rename: " + self.name + " to " + self.newName)
        except Description.InvalidColumnNameException as err:
            raise Description.InvalidColumnNameException(err.columnName, err.description, "Rename: " + self.name + " to " + self.newName)

    def translate(self):
        request = self.elements[0].translate()
        request.add_alias(self.name, self.newName)
        return request

class Projection(Operation):
    """ Defines a Projection operation
    """
    def __init__(self, columns, operation):
        super().__init__()
        self.columns = columns
        self.elements = [operation]

    def __str__(self):
        return "Projection: " + str(self.columns) + " of " + str(self.elements[0])

    def __repr__(self):
        return "Projection: " + str(self.columns) + " " + repr(self.elements)

    def check(self):
        self.elements[0].check()
        self.description = self.elements[0].get_description()

        for i in range(0, len(self.columns)):
            for j in range(i+1, len(self.columns)):
                if self.columns[i] == self.columns[j]:
                    raise DoubleColumnNameProjectionException(self.columns[i], self.columns, str(self))

        for column in self.columns:
            if not self.description.is_column_name(column):
                message = "Projection: ["
                for col in self.columns:
                    message += "'" + col + "'"
                message += ']'
                raise InvalidColumnNameException(column, self.description, message)

        self.description.keep_columns(self.columns)

    def translate(self):
        request = self.elements[0].translate()
        request.keep_columns(self.columns)
        return request

class Comparator(object):
    """ Defines a comparator used by the Selection/SELECT request """
    def __init__(self, left, comp, right, const):
        self.left = left
        self.comp = comp
        self.right = right
        self.const = const

    def __str__(self):
        res = self.left + self.comp
        if self.const:
            res += "'" + str(self.right) + "'"
        else:
            res += self.right
        return res

    def __repr__(self):
        return self.let + " " + self.comp + " " + str(self.right) + " (" + self.const + ")"

    def check(self, description):
        """ Checks if the comparator is correct
        Args:
            description (Description.Description): The schema to use
        """
        if not description.is_column_name(self.left):
            raise Description.InvalidColumnNameException(self.left, description, "Selection: " + str(self))

        if self.const:
            if not description.get_column_type(self.left) is type(self.right):
                raise InvalidTypesComparaisonException(str(description.get_column_type(self.left)), str(self.right), "Select: " + str(self))
        else:
            if description.is_column_name(self.right):
                if not description.get_column_type(self.left) is description.get_column_type(self.right):
                    raise InvalidTypesComparaisonException(str(description.get_column_type(self.left)), str(description.get_column_type(self.right)), "Select: " + str(self))
            else:
                raise Description.InvalidColumnNameException(self.right, description, "Selection: " + str(self))

class Selection(Operation):
    """ Defines a Selection operation
    """
    def __init__(self, comparator, operation):
        """ Args:
                comparator (Comparator): The comparator
                operation (Operation): The operation
        """
        super().__init__()
        self.comparator = comparator
        self.elements = [operation]

    def __str__(self):
        return "Selection: " + str(self.comparator)

    def __repr__(self):
        return "Selection: " + repr(self.comparator) + " " + repr(self.elements)

    def check(self):
        self.elements[0].check()

        self.description = self.elements[0].get_description()

        self.comparator.check(self.description)

    def translate(self):
        request = self.elements[0].translate()
        request.add_condition(copy.deepcopy(self.comparator))
        return request

class Union(Operation):
    """Defines a Union operation"""
    def __init__(self, left, right):
        super().__init__()
        self.elements.append(left)
        self.elements.append(right)

    def __str__(self):
        return "Union: " + str(self.elements[0]) + " and " + str(self.elements[1])

    def check(self):
        self.elements[0].check()
        self.elements[1].check()

        left = self.elements[0].get_description()
        right = self.elements[1].get_description()

        if not left.has_same_sorte(right):
            raise SorteNotMatchingException(left, right, str(self))

        self.description = left

    def translate(self):
        requestLeft = self.elements[0].translate()
        requestRight = self.elements[1].translate()
        return SubrequestsHandler(requestLeft, requestRight, "UNION")

class Difference(Operation):
    """Defines a Difference operation"""
    def __init__(self, left, right):
        super().__init__()
        self.elements.append(left)
        self.elements.append(right)
	
    def __str__(self):
        return "Difference: " + str(self.elements[0]) + " and " + str(self.elements[1])
		
    def check(self):
        self.elements[0].check()
        self.elements[1].check()
		
        left = self.elements[0].get_description()
        right = self.elements[1].get_description()
		
        if not left.has_same_sorte(right):
            raise SorteNotMatchingException(left, right, str(self))
			
        self.description = left
		
    def translate(self):
        requestLeft = self.elements[0].translate()
        requestRight = self.elements[1].translate()
        return SubrequestsHandler(requestLeft, requestRight, "EXCEPT")
		
class Join(Operation):
    """Defines a Join operation"""
    def __init__(self, left, right):
        super().__init__()
        self.elements.append(left)
        self.elements.append(right)
	
    def __str__(self):
        return "Join: " + str(self.elements[0]) + " and " + str(self.elements[1])
		
    def check(self):
        self.elements[0].check()
        self.elements[1].check()
		
        left = self.elements[0].get_description()
        right = self.elements[1].get_description()
		
        self.description = left
		
    def translate(self):
        requestLeft = self.elements[0].translate()
        requestRight = self.elements[1].translate()
        return SubrequestsHandler(requestLeft, requestRight, "INNER JOIN")