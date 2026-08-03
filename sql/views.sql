CREATE OR REPLACE VIEW vw_players_with_teams AS
SELECT
    p.player_id,
    p.full_name AS player_name,
    p.is_active,
    p.position,
    p.season_exp,
    t.team_id,
    t.full_name AS team_name,
    t.abbreviation AS team_abbreviation
FROM players AS p
LEFT JOIN teams AS t ON t.team_id = p.team_id;
