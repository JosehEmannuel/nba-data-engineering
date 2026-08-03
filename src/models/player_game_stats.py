from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class PlayerGameStats:
    """Estatísticas de um jogador em uma partida."""

    game_id: str
    player_id: int
    team_id: int
    player_name: Optional[str] = None
    minutes: Optional[str] = None
    points: Optional[int] = None
    rebounds: Optional[int] = None
    assists: Optional[int] = None
    steals: Optional[int] = None
    blocks: Optional[int] = None
    turnovers: Optional[int] = None
    personal_fouls: Optional[int] = None
    field_goals_made: Optional[int] = None
    field_goals_attempted: Optional[int] = None
    three_pointers_made: Optional[int] = None
    three_pointers_attempted: Optional[int] = None
    free_throws_made: Optional[int] = None
    free_throws_attempted: Optional[int] = None
    plus_minus: Optional[int] = None
    start_position: Optional[str] = None
    comment: Optional[str] = None
