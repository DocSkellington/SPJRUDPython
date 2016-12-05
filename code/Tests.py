import unittest
import Database
import Operations

class TestCheckOperations(unittest.TestCase):
    """ Unit tests on the check method of the operations """
    def setUp(self):
        """ Sets up the unit test class """
        self.db = Database.Database()
        self.db.connect_to_SQL("Test.db")

    def test_relation(self):
        """ Tests the Relation """
        rel = Operations.Relation("Cities", self.db)
        self.assertTrue(rel.check())
        rel = Operations.Relation("CitIes", self.db)
        self.assertFalse(rel.check())

    def test_selection(self):
        """ Tests the Selection """
        selection = Operations.Selection("Name", Operations.Equal(), 'Paris', True, Operations.Relation("Cities", self.db))
        self.assertTrue(selection.check())
        selection = Operations.Selection("Paris", Operations.Equal(), 'Name', True, Operations.Relation("Cities", self.db))
        self.assertFalse(selection.check())
        selection = Operations.Selection("Name", Operations.Equal(), "Paris", True, Operations.Relation("Citjie", self.db))

    def test_projection(self):
        """ Tests the projection """
        projection = Operations.Projection(["Name"], Operations.Relation("Cities", self.db))
        self.assertTrue(projection.check())
        projection = Operations.Projection(["Name", "Country"], Operations.Relation("Cities", self.db))
        self.assertTrue(projection.check())
        projection = Operations.Projection(['Couname'], Operations.Relation("Cities", self.db))
        self.assertFalse(projection.check())
        projection = Operations.Projection(['Name', 'Countrygzu'], Operations.Relation("Cities", self.db))
        self.assertFalse(projection.check())
        projection = Operations.Projection(["Name"], Operations.Relation("Citoiej", self.db))
        self.assertFalse(projection.check())

    def test_rename(self):
        """ Tests the Rename """
        rename = Operations.Rename("Name", "City", Operations.Relation("Cities", self.db))
        self.assertTrue(rename.check())
        rename = Operations.Rename("City", "Name", Operations.Relation("Cities", self.db))
        self.assertFalse(rename.check())
        rename = Operations.Relation("Name", "City", Operations.Relation("Citiejikq", self.db))
        self.assertFalse(rename.check())

if __name__ == '__main__':
    unittest.main()
