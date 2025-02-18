import unittest
from lib.db import get_db_connection

class TestDatabaseConnection(unittest.TestCase):
    def test_connection(self):
        try:
            with get_db_connection() as conn:
                self.assertIsNotNone(conn)
                print("Database connection test passed.")
        except Exception as e:
            self.fail(f"Database connection test failed: {e}")

if __name__ == "__main__":
    unittest.main() 