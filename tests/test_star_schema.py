import unittest
from unittest.mock import Mock

from src.database.initialize import SQL_DIRECTORY
from src.repositories.analytics_repository import AnalyticsRepository


class StarSchemaTests(unittest.TestCase):
    def test_creates_dimensions_and_facts(self):
        schema = (SQL_DIRECTORY / "star_schema.sql").read_text(encoding="utf-8")
        for table in ("dim_date", "dim_season", "dim_team", "dim_player", "fact_games", "fact_player_game_stats"):
            self.assertIn(f"CREATE TABLE IF NOT EXISTS {table}", schema)

    def test_season_end_year_is_one_year_after_start_year(self):
        cursor = Mock()
        repository = AnalyticsRepository(Mock(cursor=cursor))

        repository.refresh_star_schema()

        season_insert = cursor.execute.call_args_list[1].args[0]
        self.assertIn(
            "CAST(SUBSTRING(season, 1, 4) AS UNSIGNED) + 1",
            season_insert,
        )
        self.assertNotIn("SUBSTRING(season, 6, 2)", season_insert)
