CREATE INDEX idx_players_team_id ON players (team_id);

CREATE INDEX idx_players_active_name ON players (is_active, full_name);

CREATE INDEX idx_enrichment_checkpoint_date
    ON player_enrichment_checkpoint (enriched_at);

CREATE INDEX idx_games_season_date ON games (season, game_date);

CREATE INDEX idx_games_home_team ON games (home_team_id);

CREATE INDEX idx_games_away_team ON games (away_team_id);

CREATE INDEX idx_games_season_type ON games (season_type, season);

CREATE INDEX idx_game_checkpoint_loaded_at
    ON game_ingestion_checkpoint (loaded_at);

CREATE INDEX idx_player_game_stats_player ON player_game_stats (player_id);

CREATE INDEX idx_player_game_stats_team ON player_game_stats (team_id);

CREATE INDEX idx_player_game_stats_checkpoint_date
    ON player_game_stats_checkpoint (loaded_at);
