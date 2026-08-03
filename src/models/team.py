from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class Team:

    team_id: int

    full_name: str

    abbreviation: str

    nickname: str

    city: str

    state: Optional[str] = None

    year_founded: Optional[int] = None

    def __str__(self):

        return self.full_name