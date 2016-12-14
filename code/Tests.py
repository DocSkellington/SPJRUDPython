import unittest
import Database
import Operations
import Description
from Exceptions import *

class TestCheckOperations(unittest.TestCase):
    """ Unit tests on the check method of the operations """
    def setUp(self):
        """ Sets up the unit test class """
        self.db = Database.Database()
        self.db.connect_to_SQL("Test.db")

    def test_relation(self):
        """ Tests the Relation """
        rel = Operations.Relation("Cities", self.db)
        rel.check()
        rel = Operations.Relation("CitIes", self.db)
        with self.assertRaises(MissingTableException):
            rel.check()

    def test_selection(self):
        """ Tests the Selection """
        selection = Operations.Selection(Operations.Comparator("Name", "=", 'Paris', True), Operations.Relation("Cities", self.db))
        selection.check()
        selection = Operations.Selection(Operations.Comparator("Paris", '=', 'Name', True), Operations.Relation("Cities", self.db))
        with self.assertRaises(InvalidColumnNameException):
            selection.check()
        selection = Operations.Selection(Operations.Comparator("Name", '=', "Paris", True), Operations.Relation("Citjie", self.db))
        with self.assertRaises(MissingTableException):
            selection.check()
        selection = Operations.Selection(Operations.Comparator("Population", '=', 256461, True), Operations.Relation("Cities", self.db))
        selection.check()
        selection = Operations.Selection(Operations.Comparator("Population", '=', "256461", True), Operations.Relation("Cities", self.db))
        with self.assertRaises(Operations.InvalidTypesComparaisonException):
            selection.check()
        selection = Operations.Selection(Operations.Comparator("Name", '=', "Country", False), Operations.Relation("Cities", self.db))
        selection.check()
        selection = Operations.Selection(Operations.Comparator("Name", '=', "Population", False), Operations.Relation("Cities", self.db))
        with self.assertRaises(Operations.InvalidTypesComparaisonException):
            selection.check()
        selection = Operations.Selection(Operations.Comparator("Name", '=', "Cities", False), Operations.Relation("Cities", self.db))
        with self.assertRaises(InvalidColumnNameException):
            selection.check()

    def test_projection(self):
        """ Tests the projection """
        projection = Operations.Projection(["Name"], Operations.Relation("Cities", self.db))
        projection.check()
        projection = Operations.Projection(["Name", "Country"], Operations.Relation("Cities", self.db))
        projection.check()
        projection = Operations.Projection(['Couname'], Operations.Relation("Cities", self.db))
        with self.assertRaises(InvalidColumnNameException):
            projection.check()
        projection = Operations.Projection(['Name', 'Countrygzu'], Operations.Relation("Cities", self.db))
        with self.assertRaises(InvalidColumnNameException):
            projection.check()
        projection = Operations.Projection(["Name"], Operations.Relation("Citoiej", self.db))
        with self.assertRaises(MissingTableException):
            projection.check()

    def test_rename(self):
        """ Tests the Rename """
        rename = Operations.Rename("Name", "City", Operations.Relation("Cities", self.db))
        rename.check()
        rename = Operations.Rename("City", "Name", Operations.Relation("Cities", self.db))
        with self.assertRaises(InvalidColumnNameException):
            rename.check()
        rename = Operations.Rename("Name", "City", Operations.Relation("Citiejikq", self.db))
        with self.assertRaises(MissingTableException):
            rename.check()

    def test_union(self):
        """ Tests the union """
        union = Operations.Union(Operations.Relation("Cities", self.db), Operations.Relation("Cities", self.db))
        union.check()
        union = Operations.Union(Operations.Projection(["Name"], Operations.Relation("Cities", self.db)), Operations.Projection(["Name"], Operations.Relation("Cities", self.db)))
        union.check()
        union = Operations.Union(Operations.Projection(["Name"], Operations.Relation("Cities", self.db)), Operations.Projection(["Population"], Operations.Relation("Cities", self.db)))
        with self.assertRaises(SorteNotMatchingException):
            union.check()

if __name__ == '__main__':
    unittest.main()
