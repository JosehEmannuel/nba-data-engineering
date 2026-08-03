import unittest

import pandas as pd

from src.services.nba_api_service import NBAApiService
from src.ingestion.load_games import LoadGamesPipeline


class GamesTests(unittest.TestCase):
    def test_converts_two_team_rows_to_one_game(self):
        dataframe = pd.DataFrame([
            {"GAME_ID": "0022400001", "GAME_DATE": "2024-10-22", "TEAM_ID": 1,
             "MATCHUP": "AAA vs. BBB", "PTS": 100},
            {"GAME_ID": "0022400001", "GAME_DATE": "2024-10-22", "TEAM_ID": 2,
             "MATCHUP": "BBB @ AAA", "PTS": 95},
        ])
        games = list(NBAApiService.games_from_dataframe(dataframe, "2024-25"))
        self.assertEqual(len(games), 1)
        self.assertEqual(games[0].home_team_id, 1)
        self.assertEqual(games[0].away_score, 95)
        self.assertEqual(games[0].season_type, "Regular Season")

    def test_generates_every_season_in_an_interval(self):
        seasons = list(LoadGamesPipeline.seasons_between("2023-24", "2025-26"))
        self.assertEqual(seasons, ["2023-24", "2024-25", "2025-26"])
