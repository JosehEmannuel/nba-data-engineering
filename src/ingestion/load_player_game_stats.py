import time

from src.ingestion.base_pipeline import BasePipeline
from src.services.nba_api_service import NBAApiService
from src.utils.batch import BatchProcessor


class LoadPlayerGameStatsPipeline(BasePipeline):
    """Carrega estatísticas individuais para todos os jogos persistidos."""

    def __init__(self):
        super().__init__()
        self.service = NBAApiService()

    def execute(self, uow):
        game_ids = uow.player_game_stats.get_game_ids_to_load()
        total = len(game_ids)
        loaded = 0
        self.logger.info("%s jogos aguardando estatísticas individuais.", total)

        for game_batch in BatchProcessor.chunk(game_ids, batch_size=10):
            batch_stats = []
            completed_games = []
            totals = {}
            for game_id in game_batch:
                try:
                    stats = self.service.fetch_player_game_stats(game_id)
                    batch_stats.extend(stats)
                    completed_games.append(game_id)
                    totals[game_id] = len(stats)
                    time.sleep(0.6)
                except Exception as error:
                    self.logger.exception("Erro ao buscar estatísticas do jogo %s: %s", game_id, error)

            uow.player_game_stats.insert_stats(batch_stats)
            uow.player_game_stats.mark_games_completed(completed_games, totals)
            uow.commit()
            loaded += len(completed_games)
            self.logger.info("%s/%s jogos com estatísticas confirmados.", loaded, total)


if __name__ == "__main__":
    LoadPlayerGameStatsPipeline().run()
