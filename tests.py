import unittest
from database import Database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database()

    def test_set_and_get(self):
        self.db.set("name", "Griffin")
        self.assertEqual(self.db.get("name"), "Griffin")
        self.assertEqual(self.db.get("cat"), "NULL")

    def test_delete(self):
        self.db.set("name", "Griffin")
        self.assertEqual(self.db.get("name"), "Griffin")
        self.db.delete("name")
        self.assertEqual(self.db.get("name"), "NULL")

    def test_count(self):
        self.db.set("name", "Griffin")
        self.db.set("nickname", "Griffin")
        self.assertEqual(self.db.count("Griffin"), 2)
        self.db.set("nickname", "Griffster")
        self.assertEqual(self.db.count("Griffin"), 1)

    def test_transactions_commit(self):
        self.db.begin()
        self.db.set("name", "Griffin")
        self.db.commit()
        self.assertEqual(self.db.get("name"), "Griffin")
        self.db.begin()
        self.db.set("name", "Daphne")
        self.db.commit()
        self.assertEqual(self.db.get("name"), "Daphne")

    def test_transactions_count(self):
        self.db.set("a", "Griffin")
        self.db.set("b", "Daphne")
        self.db.set("c", "Griffin")
        self.db.begin()
        self.db.set("c", "Clyde")
        self.assertEqual(self.db.count("Griffin"), 1)
        self.db.commit()
        self.assertEqual(self.db.count("Griffin"), 1)

    def test_transactions_rollback(self):
        self.db.set("name", "Griffin")
        self.db.begin()
        self.db.set("name", "Daphne")
        self.assertEqual(self.db.get("name"), "Daphne")
        self.db.rollback()
        self.assertEqual(self.db.get("name"), "Griffin")

    def test_transactions_rollback_count(self):
        self.db.set("a", "Griffin")
        self.db.set("b", "Daphne")
        self.db.set("c", "Griffin")
        self.db.begin()
        self.db.set("c", "Clyde")
        self.assertEqual(self.db.count("Griffin"), 1)
        self.db.rollback()
        self.assertEqual(self.db.count("Griffin"), 2)

    def test_transactions_rollback_not_found(self):
        self.assertEqual(self.db.rollback(), "TRANSACTION NOT FOUND")

if __name__ == '__main__':
    unittest.main()