from src.models.player import Player
from src.repositories.base_repository import BaseRepository


class PlayerRepository(BaseRepository):

    def get_all_player_ids(self):

        self.cursor.execute("""

            SELECT player_id

            FROM players

            ORDER BY player_id

        """)

        return [row[0] for row in self.cursor.fetchall()]

    def insert_players(self, players: list[Player]):

        sql = """

        INSERT INTO players(

            player_id,
            first_name,
            last_name,
            full_name,
            is_active

        )

        VALUES(%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE
            first_name=VALUES(first_name),
            last_name=VALUES(last_name),
            full_name=VALUES(full_name),
            is_active=VALUES(is_active)

        """

        dados = [

            (

                p.player_id,
                p.first_name,
                p.last_name,
                p.full_name,
                p.is_active

            )

            for p in players

        ]

        self.cursor.executemany(sql, dados)

    def get_player_ids_to_enrich(self):
        """Retorna jogadores que ainda não têm checkpoint de enriquecimento."""
        self.cursor.execute("""
            SELECT p.player_id
            FROM players AS p
            LEFT JOIN player_enrichment_checkpoint AS c
                ON c.player_id = p.player_id
            WHERE c.player_id IS NULL
            ORDER BY p.player_id
        """)
        return [row[0] for row in self.cursor.fetchall()]

    def mark_enriched(self, players: list[Player]):
        """Registra em lote os jogadores enriquecidos com sucesso."""
        if not players:
            return
        self.cursor.executemany("""
            INSERT INTO player_enrichment_checkpoint (player_id, enriched_at)
            VALUES (%s, UTC_TIMESTAMP())
            ON DUPLICATE KEY UPDATE enriched_at=VALUES(enriched_at)
        """, [(player.player_id,) for player in players])

    def update_players(self, players: list[Player]):

        sql = """

        UPDATE players

        SET

            birth_date=%s,
            school=%s,
            country=%s,
            height=%s,
            weight=%s,
            season_exp=%s,
            jersey=%s,
            position=%s,
            is_active=%s,
            team_id=%s,
            draft_year=%s,
            draft_round=%s,
            draft_number=%s

        WHERE player_id=%s

        """

        dados = [

            (

                p.birth_date,
                p.school,
                p.country,
                p.height,
                p.weight,
                p.season_exp,
                p.jersey,
                p.position,
                p.is_active,
                p.team_id,
                p.draft_year,
                p.draft_round,
                p.draft_number,
                p.player_id

            )

            for p in players

        ]

        self.cursor.executemany(sql, dados)
