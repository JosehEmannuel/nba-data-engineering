from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass(slots=True)
class Game:

    game_id: str

    season: str

    game_date: date

    home_team_id: int

    away_team_id: int

    home_score: Optional[int] = None

    away_score: Optional[int] = None

    status: Optional[str] = None

    season_type: str = "Regular Season"
