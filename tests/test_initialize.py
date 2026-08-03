import unittest

from src.database.initialize import SQL_DIRECTORY


class DatabaseInitializationTests(unittest.TestCase):
    def test_sql_artifacts_are_available(self):
        self.assertTrue((SQL_DIRECTORY / "schema.sql").is_file())
        self.assertTrue((SQL_DIRECTORY / "indexes.sql").is_file())
        self.assertTrue((SQL_DIRECTORY / "views.sql").is_file())
