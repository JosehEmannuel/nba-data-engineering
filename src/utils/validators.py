from typing import Optional


class Validators:

    @staticmethod
    def validate_player_id(player_id: int):

        if player_id <= 0:

            raise ValueError(
                "player_id inválido."
            )

    @staticmethod
    def validate_team_id(team_id: int):

        if team_id <= 0:

            raise ValueError(
                "team_id inválido."
            )

    @staticmethod
    def validate_name(name: Optional[str]):

        if name is None:

            raise ValueError(
                "Nome não pode ser vazio."
            )

        if len(name.strip()) == 0:

            raise ValueError(
                "Nome não pode ser vazio."
            )