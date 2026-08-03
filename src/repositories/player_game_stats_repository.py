from src.models.player_game_stats import PlayerGameStats
from src.repositories.base_repository import BaseRepository


class PlayerGameStatsRepository(BaseRepository):
    """Persistência das estatísticas individuais por partida."""

    def get_game_ids_to_load(self) -> list[str]:
        self.cursor.execute("""
            SELECT g.game_id
            FROM games AS g
            LEFT JOIN player_game_stats_checkpoint AS c ON c.game_id = g.game_id
            WHERE c.game_id IS NULL
            ORDER BY g.game_date, g.game_id
        """)
        return [row[0] for row in self.cursor.fetchall()]

    def insert_stats(self, stats: list[PlayerGameStats]):
        if not stats:
            return
        self.cursor.executemany("""
            INSERT INTO player_game_stats (
                game_id, player_id, team_id, player_name, minutes, points, rebounds,
                assists, steals, blocks, turnovers, personal_fouls, field_goals_made,
                field_goals_attempted, three_pointers_made, three_pointers_attempted,
                free_throws_made, free_throws_attempted, plus_minus, start_position, comment
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s
            ) ON DUPLICATE KEY UPDATE
                team_id=VALUES(team_id), player_name=VALUES(player_name), minutes=VALUES(minutes),
                points=VALUES(points), rebounds=VALUES(rebounds), assists=VALUES(assists),
                steals=VALUES(steals), blocks=VALUES(blocks), turnovers=VALUES(turnovers),
                personal_fouls=VALUES(personal_fouls), field_goals_made=VALUES(field_goals_made),
                field_goals_attempted=VALUES(field_goals_attempted),
                three_pointers_made=VALUES(three_pointers_made),
                three_pointers_attempted=VALUES(three_pointers_attempted),
                free_throws_made=VALUES(free_throws_made), free_throws_attempted=VALUES(free_throws_attempted),
                plus_minus=VALUES(plus_minus), start_position=VALUES(start_position), comment=VALUES(comment)
        """, [
            (
                stat.game_id, stat.player_id, stat.team_id, stat.player_name, stat.minutes,
                stat.points, stat.rebounds, stat.assists, stat.steals, stat.blocks,
                stat.turnovers, stat.personal_fouls, stat.field_goals_made,
                stat.field_goals_attempted, stat.three_pointers_made,
                stat.three_pointers_attempted, stat.free_throws_made,
                stat.free_throws_attempted, stat.plus_minus, stat.start_position, stat.comment,
            )
            for stat in stats
        ])

    def mark_games_completed(self, game_ids: list[str], totals: dict[str, int]):
        if not game_ids:
            return
        self.cursor.executemany("""
            INSERT INTO player_game_stats_checkpoint (game_id, total_players, loaded_at)
            VALUES (%s, %s, UTC_TIMESTAMP())
            ON DUPLICATE KEY UPDATE
                total_players=VALUES(total_players), loaded_at=VALUES(loaded_at)
        """, [(game_id, totals[game_id]) for game_id in game_ids])
