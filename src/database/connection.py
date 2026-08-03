import mysql.connector

from src.config.settings import get_settings


def get_connection(include_database: bool = True):
    """Cria uma conexão transacional com o MySQL."""
    settings = get_settings()
    options = {
        "host": settings.db_host,
        "port": settings.db_port,
        "user": settings.db_user,
        "password": settings.db_password,
        "autocommit": False,
    }
    if include_database:
        options["database"] = settings.db_name
    return mysql.connector.connect(**options)
