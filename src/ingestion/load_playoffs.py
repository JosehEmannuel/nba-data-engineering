import os

from src.ingestion.load_games import LoadGamesPipeline


if __name__ == "__main__":
    LoadGamesPipeline(
        start_season=os.getenv("NBA_START_SEASON", "1946-47"),
        end_season=os.getenv("NBA_END_SEASON", "2025-26"),
        season_type="Playoffs",
    ).run()
