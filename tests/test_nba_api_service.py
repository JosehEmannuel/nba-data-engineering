import unittest
from unittest.mock import patch

from src.services.nba_api_service import NBAApiService


class NBAApiServiceTests(unittest.TestCase):
    @patch("src.services.nba_api_service.nba_players.get_players")
    def test_keeps_player_with_missing_first_name(self, get_players):
        get_players.return_value = [{
            "id": 2403,
            "full_name": "Nene",
            "first_name": "",
            "last_name": "Nene",
            "is_active": False,
        }]

        player = next(NBAApiService.fetch_players())

        self.assertEqual(player.player_id, 2403)
        self.assertIsNone(player.first_name)
        self.assertEqual(player.full_name, "Nene")
