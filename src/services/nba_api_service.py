import time
from collections.abc import Generator

from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.endpoints import boxscoretraditionalv2
from nba_api.stats.endpoints import boxscoretraditionalv3
from nba_api.stats.static import players as nba_players
from nba_api.stats.static import teams as nba_teams

from src.config.settings import get_settings
from src.models.player import Player
from src.models.team import Team
from src.utils.converters import Converters


class NBAApiService:
    """Único ponto de comunicação com a NBA API."""

    @staticmethod
    def fetch_players() -> Generator[Player, None, None]:
        for player in nba_players.get_players():
            yield Player(
                player_id=Converters.to_int(player["id"]),
                first_name=Converters.to_str(player["first_name"]),
                last_name=Converters.to_str(player["last_name"]),
                full_name=Converters.to_str(player["full_name"]),
                is_active=Converters.to_bool(player["is_active"]),
            )

    @staticmethod
    def fetch_teams() -> Generator[Team, None, None]:
        for team in nba_teams.get_teams():
            yield Team(
                team_id=Converters.to_int(team["id"]),
                full_name=Converters.to_str(team["full_name"]),
                abbreviation=Converters.to_str(team["abbreviation"]),
                nickname=Converters.to_str(team["nickname"]),
                city=Converters.to_str(team["city"]),
                state=Converters.to_str(team["state"]),
                year_founded=Converters.to_int(team["year_founded"]),
            )

    @staticmethod
    def fetch_games(season: str, season_type: str = "Regular Season") -> Generator["Game", None, None]:
        """Retorna os jogos de uma temporada, agrupando as duas linhas por partida."""
        from src.models.game import Game

        settings = get_settings()
        last_error = None
        for attempt in range(settings.nba_api_max_retries):
            try:
                dataframe = leaguegamefinder.LeagueGameFinder(
                    league_id_nullable="00",
                    season_nullable=season,
                    season_type_nullable=season_type,
                    timeout=settings.nba_api_timeout_seconds,
                ).get_data_frames()[0]
                yield from NBAApiService.games_from_dataframe(dataframe, season, season_type)
                return
            except Exception as error:
                last_error = error
                if attempt < settings.nba_api_max_retries - 1:
                    time.sleep(2 ** attempt)
        raise ConnectionError(
            f"Não foi possível obter os jogos de {season} após "
            f"{settings.nba_api_max_retries} tentativas."
        ) from last_error

    @staticmethod
    def games_from_dataframe(
        dataframe, season: str, season_type: str = "Regular Season"
    ) -> Generator["Game", None, None]:
        """Converte o retorno por time da API em uma partida por ``game_id``."""
        from src.models.game import Game

        for game_id, rows in dataframe.groupby("GAME_ID"):
            home_rows = rows[rows["MATCHUP"].str.contains("vs.", regex=False, na=False)]
            away_rows = rows[rows["MATCHUP"].str.contains("@", regex=False, na=False)]
            if home_rows.empty or away_rows.empty:
                continue
            home = home_rows.iloc[0]
            away = away_rows.iloc[0]
            yield Game(
                game_id=Converters.to_str(game_id),
                season=season,
                game_date=Converters.to_date(home["GAME_DATE"]),
                home_team_id=Converters.to_int(home["TEAM_ID"]),
                away_team_id=Converters.to_int(away["TEAM_ID"]),
                home_score=Converters.to_int(home.get("PTS")),
                away_score=Converters.to_int(away.get("PTS")),
                status="Final",
                season_type=season_type,
            )

    @staticmethod
    def fetch_player_game_stats(game_id: str) -> list["PlayerGameStats"]:
        """Busca o box score, priorizando o endpoint V3 atualmente suportado."""
        settings = get_settings()
        last_error = None
        for attempt in range(settings.nba_api_max_retries):
            try:
                dataframe = boxscoretraditionalv3.BoxScoreTraditionalV3(
                    game_id=game_id, timeout=settings.nba_api_timeout_seconds
                ).get_data_frames()[0]
                stats = NBAApiService.player_stats_from_dataframe(dataframe, game_id)
                if stats:
                    return stats

                # Mantém compatibilidade com jogos antigos ainda disponíveis apenas no V2.
                legacy_dataframe = boxscoretraditionalv2.BoxScoreTraditionalV2(
                    game_id=game_id, timeout=settings.nba_api_timeout_seconds
                ).get_data_frames()[0]
                legacy_stats = NBAApiService.player_stats_from_dataframe(legacy_dataframe, game_id)
                if legacy_stats:
                    return legacy_stats
                raise LookupError(f"A API não retornou estatísticas para o jogo {game_id}.")
            except Exception as error:
                last_error = error
                if attempt < settings.nba_api_max_retries - 1:
                    time.sleep(2 ** attempt)
        raise ConnectionError(f"Não foi possível obter estatísticas do jogo {game_id}.") from last_error

    @staticmethod
    def player_stats_from_dataframe(dataframe, game_id: str) -> list["PlayerGameStats"]:
        from src.models.player_game_stats import PlayerGameStats

        is_v3 = "personId" in dataframe.columns
        stats = []
        for _, row in dataframe.iterrows():
            player_id = Converters.to_int(row.get("personId" if is_v3 else "PLAYER_ID"))
            team_id = Converters.to_int(row.get("teamId" if is_v3 else "TEAM_ID"))
            # Algumas partidas históricas incluem uma linha agregada do time.
            if player_id is None or team_id is None:
                continue
            if is_v3:
                player_name = Converters.to_str(
                    f"{row.get('firstName', '')} {row.get('familyName', '')}"
                ) or Converters.to_str(row.get("nameI"))
            else:
                player_name = Converters.to_str(row.get("PLAYER_NAME"))
            stats.append(PlayerGameStats(
                game_id=game_id,
                player_id=player_id,
                team_id=team_id,
                player_name=player_name,
                minutes=Converters.to_str(row.get("minutes" if is_v3 else "MIN")),
                points=Converters.to_int(row.get("points" if is_v3 else "PTS")),
                rebounds=Converters.to_int(row.get("reboundsTotal" if is_v3 else "REB")),
                assists=Converters.to_int(row.get("assists" if is_v3 else "AST")),
                steals=Converters.to_int(row.get("steals" if is_v3 else "STL")),
                blocks=Converters.to_int(row.get("blocks" if is_v3 else "BLK")),
                turnovers=Converters.to_int(row.get("turnovers" if is_v3 else "TO")),
                personal_fouls=Converters.to_int(row.get("foulsPersonal" if is_v3 else "PF")),
                field_goals_made=Converters.to_int(row.get("fieldGoalsMade" if is_v3 else "FGM")),
                field_goals_attempted=Converters.to_int(row.get("fieldGoalsAttempted" if is_v3 else "FGA")),
                three_pointers_made=Converters.to_int(row.get("threePointersMade" if is_v3 else "FG3M")),
                three_pointers_attempted=Converters.to_int(row.get("threePointersAttempted" if is_v3 else "FG3A")),
                free_throws_made=Converters.to_int(row.get("freeThrowsMade" if is_v3 else "FTM")),
                free_throws_attempted=Converters.to_int(row.get("freeThrowsAttempted" if is_v3 else "FTA")),
                plus_minus=Converters.to_int(row.get("plusMinusPoints" if is_v3 else "PLUS_MINUS")),
                start_position=Converters.to_str(row.get("position" if is_v3 else "START_POSITION")),
                comment=Converters.to_str(row.get("comment" if is_v3 else "COMMENT")),
            ))
        return stats

    @staticmethod
    def fetch_player_details(player_id: int) -> Player:
        """Busca detalhes com timeout e novas tentativas exponenciais."""
        settings = get_settings()
        last_error = None
        for attempt in range(settings.nba_api_max_retries):
            try:
                frames = commonplayerinfo.CommonPlayerInfo(
                    player_id=player_id,
                    timeout=settings.nba_api_timeout_seconds,
                ).get_data_frames()
                if not frames or frames[0].empty:
                    raise LookupError(f"A API não retornou detalhes para o jogador {player_id}.")
                return NBAApiService._player_from_row(frames[0].iloc[0])
            except Exception as error:
                last_error = error
                if attempt < settings.nba_api_max_retries - 1:
                    time.sleep(2 ** attempt)
        raise ConnectionError(
            f"Não foi possível obter o jogador {player_id} após "
            f"{settings.nba_api_max_retries} tentativas."
        ) from last_error

    @staticmethod
    def _player_from_row(row) -> Player:
        return Player(
            player_id=Converters.to_int(row["PERSON_ID"]),
            first_name=Converters.to_str(row["FIRST_NAME"]),
            last_name=Converters.to_str(row["LAST_NAME"]),
            full_name=Converters.to_str(row["DISPLAY_FIRST_LAST"]),
            is_active=Converters.to_bool(row["ROSTERSTATUS"]),
            birth_date=Converters.to_date(row["BIRTHDATE"]),
            school=Converters.to_str(row["SCHOOL"]),
            country=Converters.to_str(row["COUNTRY"]),
            height=Converters.to_str(row["HEIGHT"]),
            weight=Converters.to_int(row["WEIGHT"]),
            season_exp=Converters.to_int(row["SEASON_EXP"]),
            jersey=Converters.to_str(row["JERSEY"]),
            position=Converters.to_str(row["POSITION"]),
            team_id=Converters.to_int(row["TEAM_ID"]),
            draft_year=Converters.to_int(row["DRAFT_YEAR"]),
            draft_round=Converters.to_int(row["DRAFT_ROUND"]),
            draft_number=Converters.to_int(row["DRAFT_NUMBER"]),
        )
