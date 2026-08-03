from pathlib import Path

from src.config.settings import get_settings
from src.database.connection import get_connection


SQL_DIRECTORY = Path(__file__).resolve().parents[2] / "sql"


def _execute_sql_file(cursor, filename: str):
    """Executa um arquivo SQL; índices já existentes são preservados."""
    script = (SQL_DIRECTORY / filename).read_text(encoding="utf-8")
    for statement in script.split(";"):
        if not statement.strip():
            continue
        try:
            cursor.execute(statement)
        except Exception as error:
            # MySQL retorna 1061 quando um CREATE INDEX é repetido.
            if filename != "indexes.sql" or getattr(error, "errno", None) != 1061:
                raise


def _remove_legacy_player_team_foreign_key(cursor):
    """Remove uma FK incompatível com IDs históricos da NBA API.

    A dimensão ``teams`` contém as franquias atuais, enquanto jogadores
    históricos podem apontar para IDs de franquias extintas. O ID de origem é
    preservado em ``players.team_id`` para permitir análises históricas.
    """
    cursor.execute("""
        SELECT CONSTRAINT_NAME
        FROM information_schema.KEY_COLUMN_USAGE
        WHERE TABLE_SCHEMA = DATABASE()
          AND TABLE_NAME = 'players'
          AND COLUMN_NAME = 'team_id'
          AND REFERENCED_TABLE_NAME = 'teams'
    """)
    for (constraint_name,) in cursor.fetchall():
        cursor.execute(f"ALTER TABLE players DROP FOREIGN KEY `{constraint_name}`")


def _ensure_column(cursor, table: str, column: str, definition: str):
    cursor.execute("""
        SELECT 1
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s AND COLUMN_NAME = %s
    """, (table, column))
    if cursor.fetchone() is None:
        cursor.execute(f"ALTER TABLE `{table}` ADD COLUMN `{column}` {definition}")


def initialize_database():
    """Cria o banco e as tabelas necessárias sem apagar dados existentes."""
    settings = get_settings()
    connection = get_connection(include_database=False)
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{settings.db_name}`")
        cursor.execute(f"USE `{settings.db_name}`")
        _execute_sql_file(cursor, "schema.sql")
        _ensure_column(cursor, "games", "season_type", "VARCHAR(30) NOT NULL DEFAULT 'Regular Season' AFTER season")
        _remove_legacy_player_team_foreign_key(cursor)
        for filename in ("indexes.sql", "views.sql"):
            _execute_sql_file(cursor, filename)
        connection.commit()
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    initialize_database()
    print("Banco de dados inicializado com sucesso.")
