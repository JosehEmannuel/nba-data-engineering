from src.ingestion.base_pipeline import BasePipeline
from src.services.nba_api_service import NBAApiService
from src.utils.batch import BatchProcessor


class LoadTeamsPipeline(BasePipeline):
    """
    Responsável pela carga das franquias da NBA.
    """

    def __init__(self):
        super().__init__()
        self.service = NBAApiService()

    def execute(self, uow):

        generator = self.service.fetch_teams()

        total = 0

        for batch in BatchProcessor.chunk(generator, batch_size=30):

            uow.teams.insert_teams(batch)

            total += len(batch)

            self.logger.info(
                f"{total} times inseridos."
            )


if __name__ == "__main__":

    LoadTeamsPipeline().run()