import unittest

import pandas as pd

from src.services.nba_api_service import NBAApiService


class PlayerGameStatsTests(unittest.TestCase):
    def test_converts_box_score_row(self):
        dataframe = pd.DataFrame([{
            "PLAYER_ID": 1, "TEAM_ID": 2, "PLAYER_NAME": "Jane Doe", "MIN": "30:00",
            "PTS": 20, "REB": 5, "AST": 6, "STL": 2, "BLK": 1, "TO": 3, "PF": 2,
            "FGM": 7, "FGA": 12, "FG3M": 2, "FG3A": 4, "FTM": 4, "FTA": 5,
            "PLUS_MINUS": 8, "START_POSITION": "G", "COMMENT": "",
        }])
        stats = NBAApiService.player_stats_from_dataframe(dataframe, "0022400001")
        self.assertEqual(len(stats), 1)
        self.assertEqual(stats[0].points, 20)
        self.assertEqual(stats[0].game_id, "0022400001")

    def test_ignores_aggregate_rows_without_a_player_id(self):
        dataframe = pd.DataFrame([
            {"PLAYER_ID": None, "TEAM_ID": 2, "PLAYER_NAME": "Team Totals"},
            {"PLAYER_ID": 1, "TEAM_ID": 2, "PLAYER_NAME": "Jane Doe"},
        ])
        stats = NBAApiService.player_stats_from_dataframe(dataframe, "0022400001")
        self.assertEqual([stat.player_id for stat in stats], [1])

    def test_converts_v3_box_score_row(self):
        dataframe = pd.DataFrame([{
            "personId": 1, "teamId": 2, "firstName": "Jane", "familyName": "Doe",
            "minutes": "30:00", "points": 20, "reboundsTotal": 5, "assists": 6,
            "steals": 2, "blocks": 1, "turnovers": 3, "foulsPersonal": 2,
            "fieldGoalsMade": 7, "fieldGoalsAttempted": 12, "threePointersMade": 2,
            "threePointersAttempted": 4, "freeThrowsMade": 4, "freeThrowsAttempted": 5,
            "plusMinusPoints": 8, "position": "G", "comment": "",
        }])
        stats = NBAApiService.player_stats_from_dataframe(dataframe, "0022501195")
        self.assertEqual(stats[0].player_name, "Jane Doe")
        self.assertEqual(stats[0].points, 20)
