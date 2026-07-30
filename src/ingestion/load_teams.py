import pandas as pd

from src.database.team_repository import TeamRepository
from src.services.nba_api_service import NBAApiService

class TeamIngestion:

    def __init__(self):
        self.repository = TeamRepository()

    def extract(self):
        lista = NBAApiService.get_teams()
        return pd.DataFrame(lista)

    def transform(self, df):

        df = df.rename(columns={
            "id": "team_id"
        })

        df = df[
            [
                "team_id",
                "full_name",
                "abbreviation",
                "nickname",
                "city",
                "state",
                "year_founded"
            ]
        ]

        return df

    def load(self, df):

        dados = [
            (
                int(row.team_id),
                row.full_name,
                row.abbreviation,
                row.nickname,
                row.city,
                row.state,
                int(row.year_founded)
            )
            for row in df.itertuples(index=False)
        ]

        self.repository.insert_teams(dados)

    def run(self):

        df = self.extract()

        print(f"{len(df)} times extraídos.")

        df = self.transform(df)

        self.load(df)

        print("Pipeline concluído!")


if __name__ == "__main__":
    pipeline = TeamIngestion()
    pipeline.run()