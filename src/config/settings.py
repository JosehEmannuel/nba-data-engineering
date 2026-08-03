import os
from dataclasses import dataclass

from dotenv import load_dotenv


class ConfigurationError(ValueError):
    """Indica que uma configuração obrigatória está ausente ou inválida."""


@dataclass(frozen=True, slots=True)
class Settings:
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str
    nba_api_timeout_seconds: float = 30.0
    nba_api_max_retries: int = 3


def _required(name: str, environment: dict[str, str]) -> str:
    value = environment.get(name, "").strip()
    if not value or value.startswith("<"):
        raise ConfigurationError(f"Defina a variável de ambiente {name}.")
    return value


def _positive_number(name: str, value: str, converter, default):
    raw_value = value or str(default)
    try:
        result = converter(raw_value)
    except ValueError as error:
        raise ConfigurationError(f"{name} deve ser um número válido.") from error
    if result <= 0:
        raise ConfigurationError(f"{name} deve ser maior que zero.")
    return result


def get_settings(environment: dict[str, str] | None = None) -> Settings:
    """Lê e valida as variáveis de ambiente somente quando necessárias."""
    load_dotenv()
    env = os.environ if environment is None else environment
    return Settings(
        db_host=_required("DB_HOST", env),
        db_port=_positive_number("DB_PORT", env.get("DB_PORT", ""), int, 3306),
        db_user=_required("DB_USER", env),
        db_password=_required("DB_PASSWORD", env),
        db_name=_required("DB_NAME", env),
        nba_api_timeout_seconds=_positive_number(
            "NBA_API_TIMEOUT_SECONDS", env.get("NBA_API_TIMEOUT_SECONDS", ""), float, 30
        ),
        nba_api_max_retries=_positive_number(
            "NBA_API_MAX_RETRIES", env.get("NBA_API_MAX_RETRIES", ""), int, 3
        ),
    )
