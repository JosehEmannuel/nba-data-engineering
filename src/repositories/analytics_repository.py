from src.repositories.base_repository import BaseRepository


class AnalyticsRepository(BaseRepository):
    """Constrói a camada dimensional a partir das tabelas de ingestão."""

    def refresh_star_schema(self):
        statements = [
            """INSERT INTO dim_date (date_key, full_date, calendar_year, calendar_quarter, calendar_month, month_name, day_of_month, day_of_week, day_name)
            SELECT DISTINCT DATE_FORMAT(game_date, '%Y%m%d'), game_date, YEAR(game_date), QUARTER(game_date), MONTH(game_date), MONTHNAME(game_date), DAY(game_date), DAYOFWEEK(game_date), DAYNAME(game_date)
            FROM games ON DUPLICATE KEY UPDATE full_date=VALUES(full_date)""",
            """INSERT INTO dim_season (season, start_year, end_year)
            SELECT DISTINCT season, CAST(SUBSTRING(season, 1, 4) AS UNSIGNED), CAST(SUBSTRING(season, 1, 4) AS UNSIGNED) + 1
            FROM games ON DUPLICATE KEY UPDATE start_year=VALUES(start_year), end_year=VALUES(end_year)""",
            """INSERT INTO dim_team (team_id, team_name, abbreviation, city, state, year_founded)
            SELECT team_id, full_name, abbreviation, city, state, year_founded FROM teams
            ON DUPLICATE KEY UPDATE team_name=VALUES(team_name), abbreviation=VALUES(abbreviation), city=VALUES(city), state=VALUES(state), year_founded=VALUES(year_founded)""",
            """INSERT INTO dim_team (team_id, team_name)
            SELECT source.team_id, CONCAT('Historic team ', source.team_id)
            FROM (SELECT home_team_id AS team_id FROM games UNION SELECT away_team_id AS team_id FROM games) AS source
            LEFT JOIN dim_team AS dimension ON dimension.team_id = source.team_id
            WHERE dimension.team_id IS NULL""",
            """INSERT INTO dim_player (player_id, full_name, first_name, last_name, birth_date, country, position, is_active, draft_year)
            SELECT player_id, full_name, first_name, last_name, birth_date, country, position, is_active, draft_year FROM players
            ON DUPLICATE KEY UPDATE full_name=VALUES(full_name), first_name=VALUES(first_name), last_name=VALUES(last_name), birth_date=VALUES(birth_date), country=VALUES(country), position=VALUES(position), is_active=VALUES(is_active), draft_year=VALUES(draft_year)""",
            """INSERT INTO dim_player (player_id, full_name)
            SELECT stats.player_id, COALESCE(MAX(stats.player_name), CONCAT('Historic player ', stats.player_id))
            FROM player_game_stats AS stats LEFT JOIN dim_player AS dimension ON dimension.player_id = stats.player_id
            WHERE dimension.player_id IS NULL GROUP BY stats.player_id""",
            """INSERT INTO fact_games (game_id, date_key, season, season_type, home_team_id, away_team_id, home_score, away_score, winner_team_id, score_margin, status)
            SELECT game_id, DATE_FORMAT(game_date, '%Y%m%d'), season, season_type, home_team_id, away_team_id, home_score, away_score,
            CASE WHEN home_score > away_score THEN home_team_id WHEN away_score > home_score THEN away_team_id ELSE NULL END, ABS(home_score - away_score), status FROM games
            ON DUPLICATE KEY UPDATE date_key=VALUES(date_key), season=VALUES(season), season_type=VALUES(season_type), home_team_id=VALUES(home_team_id), away_team_id=VALUES(away_team_id), home_score=VALUES(home_score), away_score=VALUES(away_score), winner_team_id=VALUES(winner_team_id), score_margin=VALUES(score_margin), status=VALUES(status)""",
            """INSERT INTO fact_player_game_stats (game_id, player_id, team_id, date_key, season, season_type, minutes_played, points, rebounds, assists, steals, blocks, turnovers, personal_fouls, field_goals_made, field_goals_attempted, three_pointers_made, three_pointers_attempted, free_throws_made, free_throws_attempted, plus_minus)
            SELECT stats.game_id, stats.player_id, stats.team_id, DATE_FORMAT(games.game_date, '%Y%m%d'), games.season, games.season_type,
            CASE WHEN stats.minutes REGEXP '^[0-9]+:[0-9]{2}$' THEN CAST(SUBSTRING_INDEX(stats.minutes, ':', 1) AS DECIMAL(7,2)) + CAST(SUBSTRING_INDEX(stats.minutes, ':', -1) AS DECIMAL(7,2)) / 60 ELSE NULL END,
            stats.points, stats.rebounds, stats.assists, stats.steals, stats.blocks, stats.turnovers, stats.personal_fouls, stats.field_goals_made, stats.field_goals_attempted, stats.three_pointers_made, stats.three_pointers_attempted, stats.free_throws_made, stats.free_throws_attempted, stats.plus_minus
            FROM player_game_stats AS stats INNER JOIN games ON games.game_id = stats.game_id
            ON DUPLICATE KEY UPDATE team_id=VALUES(team_id), date_key=VALUES(date_key), season=VALUES(season), season_type=VALUES(season_type), minutes_played=VALUES(minutes_played), points=VALUES(points), rebounds=VALUES(rebounds), assists=VALUES(assists), steals=VALUES(steals), blocks=VALUES(blocks), turnovers=VALUES(turnovers), personal_fouls=VALUES(personal_fouls), field_goals_made=VALUES(field_goals_made), field_goals_attempted=VALUES(field_goals_attempted), three_pointers_made=VALUES(three_pointers_made), three_pointers_attempted=VALUES(three_pointers_attempted), free_throws_made=VALUES(free_throws_made), free_throws_attempted=VALUES(free_throws_attempted), plus_minus=VALUES(plus_minus)""",
        ]
        for statement in statements:
            self.cursor.execute(statement)
