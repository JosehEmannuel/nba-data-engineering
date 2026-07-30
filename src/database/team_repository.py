from src.database.connection import get_connection


class TeamRepository:

    def insert_teams(self, dados):

        connection = get_connection()
        cursor = connection.cursor()

        sql = """
        INSERT IGNORE INTO teams (
            team_id,
            full_name,
            abbreviation,
            nickname,
            city,
            state,
            year_founded
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.executemany(sql, dados)

        connection.commit()

        print(f"{cursor.rowcount} times inseridos.")

        cursor.close()
        connection.close()