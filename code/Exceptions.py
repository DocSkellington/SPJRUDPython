
class Error(Exception):
    """ Defines the exceptions used in this project """
    pass

class OperationException(Error):
    """ Defines the exceptions used for the operations """
    pass

class InvalidTypesComparaisonException(OperationException):
    """ Handles the case where the user wants to compare two columns (or one column and a constant) of two different types """
    def __init__(self, first, second, message):
        self.first = first
        self.second = second
        self.message = message

    def __str__(self):
        return "Impossible to compare a " + self.first + " and a " + self.second + " in " + self.message

class InvalidColumnNameException(OperationException):
    """ Handles the case where the column name does not exist """
    def __init__(self, columnName, description, message):
        self.columnName = columnName
        self.description = description
        self.message = message

    def __str__(self):
        return "'" + self.message + "' is invalid because '" + self.columnName + "' is not a column in the schema.\nThe schema is the following:\n" + str(self.description)

class DoubleColumnNameException(OperationException):
    """ Handles the case where the column is already in the schema """
    def __init__(self, columnName, description, message):
        self.columnName = columnName
        self.description = description
        self.message = message

    def __str__(self):
        return "'" + self.message + "' is invalid because '" + self.columnName + "' is already defined in the schema.\nThe schema is the following:\n" + str(self.description)

class DoubleColumnNameProjectionException(DoubleColumnNameException):
    def __str__(self):
        return "'" + self.message + "' is invalid because '" + self.columnName + "' is already defined in the list of columns to keep.\nThe columns are:\n" + str(self.description)

class SorteNotMatchingException(OperationException):
    """ Defines the exception where the descriptions have different sortes when they shouldn't"""
    def __init__(self, columnsLeft, columnsRight, message):
        self.columnsLeft = columnsLeft
        self.columnsRight = columnsRight
        self.message = message

    def __str__(self):
        return "'" + self.message + "' is invalid because '" + str(self.columnsLeft) + "' and '" + str(self.columnsRight) + "' don't have the same sorte."

class DatabaseException(Error):
    """ Defines the exception used for the database error """
    pass

class MissingDatabaseException(DatabaseException):
    """ Handles the case where the user tries to use a command on a database when no database is loaded"""
    pass

class DoubledTableException(DatabaseException):
    """ Handles the case where the user wants to add the description of a table already in the database """
    pass

class MissingTableException(DatabaseException):
    """ Handles the case where we try to access a table missing in the database """
    def __init__(self, name, database):
        self.name = name
        self.database = database

    def __str__(self):
        res = "You tried to access the table of name '" + self.name + "' but it does not belong to the database you want to use.\nThe database has the following tables:\n"
        for table in self.database.tables:
            res += "\t" + table + "\n"
        return res

class DatabaseNotFoundException(DatabaseException):
    """ Handles the case where the user wants to use a database but the filepath does not lead to a database """
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "The database you want to use (" + self.name + ") does not exist. Please check the spelling."

class EmptyDatabaseException(DatabaseException):
    """ Handles the case where the user wants to use an empty database """
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "The database you want to use (" + self.name + ") is empty or is not a database."

class ParserException(Error):
    """ Defines the exceptions for the parsers """
    pass

class InvalidTypeException(ParserException):
    """ Handles the case where the type is not recognised """
    def __init__(self, SQLType):
        self.SQLType = SQLType

    def __str__(self):
        return self.SQLType + " is not a recognised SQL type"

class InvalidKeywordException(ParserException):
    """ Defines the exception for a unknown keyword """
    def __init__(self, word, what):
        self.word = word
        self.what = what

    def __str__(self):
        return "'" + self.word + "' is an invalid " + self.what

class InvalidRequestException(ParserException):
    pass

class InvalidParenthesisException(ParserException):
    """ Defines the exception for wrong parenthesises/bracket """
    def __init__(self, char, prev, needed, pos):
        self.char = char
        self.prev = prev
        self.needed = needed
        self.pos = pos

    def __str__(self):
        return self.prev + " requires a " + self.needed + " but you wrote a " + self.char + " at position " + str(self.pos)

class MissingParenthesisException(ParserException):
    """ Defines the exception for a missing parenthesis/bracket """
    def __init__(self, char):
        self.char = char

    def __str__(self):
        return "you opened a " + self.char + " but did not close it"

class MissingOpeningParenthesisException(MissingParenthesisException):
    """ Defines the exception for a bracket/parenthesis closed but not opened """
    def __init__(self, char, should):
        super().__init__(char)
        self.should = should

    def __str__(self):
        return "you closed a " + self.char + " but you did not open with a " + self.should + " before"

class InvalidParameterException(ParserException):
    """ Defines the exception for an invalid parameter """
    def __init__(self, what, who):
        self.what = what
        self.who = who

    def __str__(self):
        return "you must provide " + self.what + " to " + self.who

class InvalidSchemaException(ParserException):
    """ Defines the exception for an invalid schema """
    pass
