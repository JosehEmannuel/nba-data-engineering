import unittest

from src.models.player import Player
from src.repositories.player_repository import PlayerRepository


class CursorStub:
    def __init__(self):
        self.statement = ""
        self.values = []

    def executemany(self, statement, values):
        self.statement = statement
        self.values = values


class SessionStub:
    def __init__(self):
        self.cursor = CursorStub()


class PlayerRepositoryTests(unittest.TestCase):
    def test_insert_players_updates_existing_records(self):
        repository = PlayerRepository(SessionStub())
        repository.insert_players([Player(1, "Jane", "Doe", "Jane Doe", True)])
        self.assertIn("ON DUPLICATE KEY UPDATE", repository.cursor.statement)
        self.assertEqual(repository.cursor.values[0], (1, "Jane", "Doe", "Jane Doe", True))
