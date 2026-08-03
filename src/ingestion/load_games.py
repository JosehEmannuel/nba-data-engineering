import os
import re
from collections.abc import Generator

from src.ingestion.base_pipeline import BasePipeline
from src.services.nba_api_service import NBAApiService
from src.utils.batch import BatchProcessor


class LoadGamesPipeline(BasePipeline):
    """Carrega jogos de um intervalo de temporadas da NBA."""

    def __init__(
        self,
        start_season: str = "1946-47",
        end_season: str = "2025-26",
        season_type: str = "Regular Season",
    ):
        super().__init__()
        self.start_season = start_season
        self.end_season = end_season
        self.season_type = season_type
        self.service = NBAApiService()

    @staticmethod
    def seasons_between(start_season: str, end_season: str) -> Generator[str, None, None]:
        pattern = re.compile(r"^(\d{4})-(\d{2})$")
        start_match = pattern.fullmatch(start_season)
        end_match = pattern.fullmatch(end_season)
        if not start_match or not end_match:
            raise ValueError("Temporadas devem estar no formato AAAA-AA, por exemplo 2024-25.")

        start_year = int(start_match.group(1))
        end_year = int(end_match.group(1))
        if start_year > end_year:
            raise ValueError("A temporada inicial não pode ser posterior à final.")

        for year in range(start_year, end_year + 1):
            yield f"{year}-{str((year + 1) % 100).zfill(2)}"

    def execute(self, uow):
        completed_seasons = uow.games.get_completed_seasons(self.season_type)
        for season in self.seasons_between(self.start_season, self.end_season):
            if season in completed_seasons:
                self.logger.info("%s já foi carregada; ignorando.", season)
                continue

            total = 0
            games = self.service.fetch_games(season, self.season_type)
            for batch in BatchProcessor.chunk(games, batch_size=100):
                uow.games.insert_games(batch)
                uow.commit()
                total += len(batch)
                self.logger.info("%s jogos carregados para %s.", total, season)

            uow.games.mark_season_completed(season, self.season_type, total)
            uow.commit()
            self.logger.info("Temporada %s concluída: %s jogos.", season, total)


if __name__ == "__main__":
    LoadGamesPipeline(
        start_season=os.getenv("NBA_START_SEASON", "1946-47"),
        end_season=os.getenv("NBA_END_SEASON", "2025-26"),
        season_type=os.getenv("NBA_SEASON_TYPE", "Regular Season"),
    ).run()
