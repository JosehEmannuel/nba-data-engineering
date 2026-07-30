from nba_api.stats.static import players
import pandas as pd

from src.database.player_repository import PlayerRepository
from src.services.nba_api_service import NBAApiService

class PlayerIngestion:

    def __init__(self):
        self.repository = PlayerRepository()

    def extract(self):
        """Extrai os dados da API"""
        lista = NBAApiService.get_players()
        return pd.DataFrame(lista)

    def transform(self, df):
        """Transforma os dados"""

        df = df.rename(columns={
            "id": "player_id"
        })

        df = df[df["is_active"] == True]

        df = df[
            [
                "player_id",
                "first_name",
                "last_name",
                "full_name",
                "is_active"
            ]
        ]

        return df

    def load(self, df):
        """Carrega os dados no banco"""

        dados = [
            (
                int(row.player_id),
                row.first_name,
                row.last_name,
                row.full_name,
                bool(row.is_active)
            )
            for row in df.itertuples(index=False)
        ]

        self.repository.insert_players(dados)

    def run(self):
        """Executa todo o pipeline"""

        df = self.extract()

        print(f"Extraídos {len(df)} jogadores.")

        df = self.transform(df)

        print(f"Após transformação: {len(df)} jogadores ativos.")

        self.load(df)

        print("Pipeline finalizado com sucesso!")


if __name__ == "__main__":
    pipeline = PlayerIngestion()
    pipeline.run()