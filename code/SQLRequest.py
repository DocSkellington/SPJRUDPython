
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
        self.aliases = {}
        self.conditions = []
        self.from_clause = None

    def __str__(self):
        res = "SELECT "
        for i in range(len(self.columns)):
            if i != 0:
                res += ", "
            res += self.columns[i]
            if self.columns[i] in self.aliases:
                res += " AS " + self.aliases[self.columns[i]]
        res += " FROM "
        res += str(self.from_clause)
        if len(self.conditions) > 0:
            res += " WHERE "
            for i in range(len(self.conditions)):
                if i != 0:
                    res += " AND "
                res += self.conditions[i]
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
                if column in self.aliases:
                    del self.aliases[column]
            else:
                i += 1

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
