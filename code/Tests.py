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
        """ Tests the RelationTable """
        rel = Operations.RelationTable("Cities", self.db)
        self.assertTrue(rel.check())
        rel = Operations.RelationTable("CitIes", self.db)
        self.assertFalse(rel.check())

    def test_selection(self):
        """ Tests the Selection """
        selection = Operations.Selection("Name", Operations.Equal(), 'Paris', True, Operations.RelationTable("Cities", self.db))
        self.assertTrue(selection.check())
        selection = Operations.Selection("Paris", Operations.Equal(), 'Name', True, Operations.RelationTable("Cities", self.db))
        self.assertFalse(selection.check())
        selection = Operations.Selection("Name", Operations.Equal(), "Paris", True, Operations.RelationTable("Citjie", self.db))

    def test_projection(self):
        """ Tests the projection """
        projection = Operations.Projection(["Name"], Operations.RelationTable("Cities", self.db))
        self.assertTrue(projection.check())
        projection = Operations.Projection(["Name", "Country"], Operations.RelationTable("Cities", self.db))
        self.assertTrue(projection.check())
        projection = Operations.Projection(['Couname'], Operations.RelationTable("Cities", self.db))
        self.assertFalse(projection.check())
        projection = Operations.Projection(['Name', 'Countrygzu'], Operations.RelationTable("Cities", self.db))
        self.assertFalse(projection.check())
        projection = Operations.Projection(["Name"], Operations.RelationTable("Citoiej", self.db))
        self.assertFalse(projection.check())

    def test_rename(self):
        """ Tests the Rename """
        rename = Operations.Rename("Name", "City", Operations.RelationTable("Cities", self.db))
        self.assertTrue(rename.check())
        rename = Operations.Rename("City", "Name", Operations.RelationTable("Cities", self.db))
        self.assertFalse(rename.check())
        rename = Operations.Rename("Name", "City", Operations.RelationTable("Citiejikq", self.db))
        self.assertFalse(rename.check())

if __name__ == '__main__':
    unittest.main()
