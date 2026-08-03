import unittest

from src.database.initialize import SQL_DIRECTORY


class SchemaTests(unittest.TestCase):
    def test_player_text_fields_allow_api_variations(self):
        schema = (SQL_DIRECTORY / "schema.sql").read_text(encoding="utf-8")
        self.assertIn("jersey VARCHAR(20) NULL", schema)
        self.assertIn("position VARCHAR(100) NULL", schema)
