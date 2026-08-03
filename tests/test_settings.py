import unittest

from src.config.settings import ConfigurationError, get_settings


class SettingsTests(unittest.TestCase):
    def test_requires_database_credentials(self):
        with self.assertRaises(ConfigurationError):
            get_settings({"DB_HOST": "localhost"})

    def test_uses_safe_defaults_and_optional_api_configuration(self):
        settings = get_settings({
            "DB_HOST": "localhost",
            "DB_USER": "root",
            "DB_PASSWORD": "secret",
            "DB_NAME": "nba",
        })
        self.assertEqual(settings.db_port, 3306)
        self.assertEqual(settings.nba_api_max_retries, 3)
