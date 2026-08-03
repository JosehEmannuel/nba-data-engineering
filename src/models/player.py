from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass(slots=True)
class Player:

    player_id: int

    first_name: Optional[str]

    last_name: Optional[str]

    full_name: str

    is_active: bool

    birth_date: Optional[date] = None

    school: Optional[str] = None

    country: Optional[str] = None

    height: Optional[str] = None

    weight: Optional[int] = None

    season_exp: Optional[int] = None

    jersey: Optional[str] = None

    position: Optional[str] = None

    team_id: Optional[int] = None

    draft_year: Optional[int] = None

    draft_round: Optional[int] = None

    draft_number: Optional[int] = None

    def __str__(self):

        return f"{self.full_name} ({self.player_id})"

    @property
    def is_rookie(self) -> bool:

        return self.season_exp == 0
