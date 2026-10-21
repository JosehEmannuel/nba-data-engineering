from src.database.session import DatabaseSession

from src.repositories.player_repository import PlayerRepository
from src.repositories.team_repository import TeamRepository
from src.repositories.game_repository import GameRepository
from src.repositories.player_game_stats_repository import PlayerGameStatsRepository
from src.repositories.analytics_repository import AnalyticsRepository


class UnitOfWork:

    def __init__(self):

        self.session = None

        self.players = None

        self.teams = None

        self.games = None

        self.player_game_stats = None

        self.analytics = None

    def __enter__(self):

        self.session = DatabaseSession()

        self.players = PlayerRepository(self.session)

        self.teams = TeamRepository(self.session)

        self.games = GameRepository(self.session)

        self.player_game_stats = PlayerGameStatsRepository(self.session)

        self.analytics = AnalyticsRepository(self.session)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        if exc_type is None:

            self.session.commit()

        else:

            self.session.rollback()

        self.session.close()

    def commit(self):
        """Confirma o lote atual e inicia uma nova transação no conector."""
        self.session.commit()
