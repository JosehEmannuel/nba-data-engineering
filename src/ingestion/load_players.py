from src.ingestion.base_pipeline import BasePipeline
from src.services.nba_api_service import NBAApiService
from src.utils.batch import BatchProcessor


class LoadPlayersPipeline(BasePipeline):
    """
    Responsável por realizar a carga inicial dos jogadores.
    """

    def __init__(self):
        super().__init__()
        self.service = NBAApiService()

    def execute(self, uow):

        generator = self.service.fetch_players()

        total = 0

        for batch in BatchProcessor.chunk(generator, batch_size=100):

            uow.players.insert_players(batch)

            total += len(batch)

            self.logger.info(
                f"{total} jogadores inseridos."
            )


if __name__ == "__main__":

    LoadPlayersPipeline().run()