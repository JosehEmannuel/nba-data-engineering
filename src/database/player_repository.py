from src.database.connection import get_connection


class PlayerRepository:

    def insert_players(self, dados):

        connection = get_connection()

        cursor = connection.cursor()

        sql = """
        INSERT IGNORE INTO players (
            player_id,
            first_name,
            last_name,
            full_name,
            is_active
        )
        VALUES (%s,%s,%s,%s,%s)
        """

        cursor.executemany(sql, dados)

        connection.commit()

        print(f"{cursor.rowcount} jogadores inseridos.")

        cursor.close()
        connection.close()