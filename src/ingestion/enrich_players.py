import time

from src.ingestion.base_pipeline import BasePipeline
from src.services.nba_api_service import NBAApiService
from src.models.player import Player
from src.utils.batch import BatchProcessor


class EnrichPlayersPipeline(BasePipeline):
    """
    Busca informações detalhadas de todos os jogadores
    e atualiza o banco de dados.
    """

    def __init__(self):

        super().__init__()

        self.service = NBAApiService()

    def execute(self, uow):

        ids = uow.players.get_player_ids_to_enrich()

        total = len(ids)

        self.logger.info(
            f"{total} jogadores encontrados."
        )

        enriched = 0
        for id_batch in BatchProcessor.chunk(ids, batch_size=25):
            players: list[Player] = []
            for player_id in id_batch:
                try:
                    player = self.service.fetch_player_details(player_id)
                    players.append(player)
                    self.logger.info("[%s/%s] %s", enriched + len(players), total, player.full_name)
                    # Evita bloqueios da API sem impedir a retomada posterior.
                    time.sleep(0.6)
                except Exception as error:
                    self.logger.exception("Erro ao buscar jogador %s: %s", player_id, error)

            uow.players.update_players(players)
            uow.players.mark_enriched(players)
            uow.commit()
            enriched += len(players)
            self.logger.info("Lote confirmado: %s/%s jogadores enriquecidos.", enriched, total)


if __name__ == "__main__":

    EnrichPlayersPipeline().run()
