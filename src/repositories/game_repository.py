from src.models.game import Game
from src.repositories.base_repository import BaseRepository


class GameRepository(BaseRepository):
    """Persistência idempotente de jogos da NBA."""

    def insert_games(self, games: list[Game]):
        if not games:
            return
        self.cursor.executemany("""
            INSERT INTO games (
                game_id, season, season_type, game_date, home_team_id, away_team_id,
                home_score, away_score, status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                season=VALUES(season),
                season_type=VALUES(season_type),
                game_date=VALUES(game_date),
                home_team_id=VALUES(home_team_id),
                away_team_id=VALUES(away_team_id),
                home_score=VALUES(home_score),
                away_score=VALUES(away_score),
                status=VALUES(status)
        """, [
            (
                game.game_id, game.season, game.season_type, game.game_date, game.home_team_id,
                game.away_team_id, game.home_score, game.away_score, game.status,
            )
            for game in games
        ])

    def get_completed_seasons(self, season_type: str) -> set[str]:
        self.cursor.execute("""
            SELECT season
            FROM game_ingestion_checkpoint
            WHERE season_type = %s
        """, (season_type,))
        return {row[0] for row in self.cursor.fetchall()}

    def mark_season_completed(self, season: str, season_type: str, total_games: int):
        self.cursor.execute("""
            INSERT INTO game_ingestion_checkpoint (
                season, season_type, total_games, loaded_at
            ) VALUES (%s, %s, %s, UTC_TIMESTAMP())
            ON DUPLICATE KEY UPDATE
                total_games=VALUES(total_games),
                loaded_at=VALUES(loaded_at)
        """, (season, season_type, total_games))
