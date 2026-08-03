from src.models.team import Team
from src.repositories.base_repository import BaseRepository


class TeamRepository(BaseRepository):

    def insert_teams(self, teams: list[Team]):

        sql = """

        INSERT IGNORE INTO teams(

            team_id,
            full_name,
            abbreviation,
            nickname,
            city,
            state,
            year_founded

        )

        VALUES(%s,%s,%s,%s,%s,%s,%s)

        """

        dados = [

            (

                t.team_id,
                t.full_name,
                t.abbreviation,
                t.nickname,
                t.city,
                t.state,
                t.year_founded

            )

            for t in teams

        ]

        self.cursor.executemany(sql, dados)