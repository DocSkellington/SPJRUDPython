
class SQLRequest(object):
    """ Defines a SQL Request. This is used for the translation
    Attributs:
        columns (list of str): The columns to keep (SELECT columns)
        aliases (dictionary of str): The aliases to use
        conditions (list of str): The conditions to use in the WHERE
        from_clause (str or SQLRequest): The table we must retrieve the data from
    """

    def __init__(self):
        self.columns = []
        self.aliases_to_col = {}
        self.col_to_aliases = {}
        self.conditions = []
        self.from_clause = None

    def __str__(self):
        res = "SELECT "
        for i in range(len(self.columns)):
            if i != 0:
                res += ", "
            if self.columns[i] in self.aliases_to_col:
                res += self.aliases_to_col[self.columns[i]] + " AS " + self.columns[i]
            else:
                res += self.columns[i]
        res += " FROM "
        res += str(self.from_clause)
        if len(self.conditions) > 0:
            res += " WHERE "
            for i in range(len(self.conditions)):
                if i != 0:
                    res += " AND "
                if self.conditions[i].left in self.col_to_aliases:
                    self.conditions[i].left = self.col_to_aliases[self.conditions[i].left]
                res += str(self.conditions[i])
        return res

    def add_column(self, column):
        """ Adds a column in the columns list
        Args:
            column (str): The name of the column to add
        """
        if column not in self.columns:
            self.columns.append(column)

    def keep_columns(self, columns):
        """ Keeps only the given columns
        Args:
            columns (list of str): The names of the columns to keep
        """
        i = 0
        while i < len(self.columns):
            column = self.columns[i]
            if column not in columns:
                self.columns.remove(column)
                if column in self.aliases_to_col:
                    del self.aliases_to_col[column]
            else:
                i += 1

    def add_alias(self, column, alias):
        """ Adds an alias in the request
        Args:
            column (str): The name of the column to change
            alias (str): The new name of the column
        """
        print(column)
        print(self.aliases_to_col)
        print(self.col_to_aliases)
        if column in self.aliases_to_col:               # We change an alias
            if alias in self.col_to_aliases:            # We remove the alias
                del self.aliases_to_col[column]
                del self.col_to_aliases[alias]
                for i in range(len(self.columns)):
                    if self.columns[i] == column:
                        self.columns[i] = alias
                        break
            else:
                # We must change to col -> aliases to match the new value
                self.col_to_aliases[self.aliases_to_col[column]] = alias
                # We must create a new aliases -> col and delete the former one
                self.aliases_to_col[alias] = self.aliases_to_col[column]
                del self.aliases_to_col[column]
                for i in range(len(self.columns)):
                    if self.columns[i] == column:
                        self.columns[i] = alias
                        break
        else:
            self.aliases_to_col[alias] = column
            self.col_to_aliases[column] = alias
            for i in range(len(self.columns)):
                if self.columns[i] == column:
                    self.columns[i] = alias
                    break

    def add_condition(self, condition):
        """ Adds a condition in the list
        Args:
            condition (str): The condition to add (in format: column =/<=/<>/... cst/column)
        """
        self.conditions.append(condition)

    def set_from_clause(self, clause):
        """ Sets the clause FROM
        Args:
            clause (str or SQLRequest): The FROM clause
        """
        self.from_clause = clause

class SubrequestsHandler(object):
    def __init__(self, left, right, operator):
        self.left = left
        self.right =  right
        self.operator = operator
        
    def __str__(self):
        return str(self.left) + " " + self.operator + " " + str(self.right)