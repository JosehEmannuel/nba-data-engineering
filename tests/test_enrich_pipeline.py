import unittest
from unittest.mock import patch

from src.ingestion.enrich_players import EnrichPlayersPipeline
from src.models.player import Player


class PlayersStub:
    def __init__(self):
        self.updated = []
        self.checkpoints = []

    def get_player_ids_to_enrich(self):
        return [1, 2]

    def update_players(self, players):
        self.updated.extend(players)

    def mark_enriched(self, players):
        self.checkpoints.extend(players)


class UowStub:
    def __init__(self):
        self.players = PlayersStub()
        self.commits = 0

    def commit(self):
        self.commits += 1


class ServiceStub:
    def fetch_player_details(self, player_id):
        if player_id == 2:
            raise ConnectionError("temporarily unavailable")
        return Player(player_id, "Jane", "Doe", "Jane Doe", True)


class EnrichPipelineTests(unittest.TestCase):
    @patch("src.ingestion.enrich_players.time.sleep")
    def test_saves_successes_and_leaves_failures_for_next_execution(self, _sleep):
        pipeline = EnrichPlayersPipeline()
        pipeline.service = ServiceStub()
        uow = UowStub()
        pipeline.execute(uow)
        self.assertEqual([player.player_id for player in uow.players.updated], [1])
        self.assertEqual([player.player_id for player in uow.players.checkpoints], [1])
        self.assertEqual(uow.commits, 1)
