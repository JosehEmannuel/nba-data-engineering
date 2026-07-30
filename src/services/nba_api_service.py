from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import commonplayerinfo


class NBAApiService:

    @staticmethod
    def get_players():
        return players.get_players()

    @staticmethod
    def get_teams():
        return teams.get_teams()

    @staticmethod
    def get_player_details(player_id):
        return commonplayerinfo.CommonPlayerInfo(
            player_id=player_id
        ).get_data_frames()[0]