CREATE TABLE IF NOT EXISTS teams (
    team_id INT NOT NULL PRIMARY KEY,
    full_name VARCHAR(80) NOT NULL,
    abbreviation VARCHAR(5) NOT NULL,
    nickname VARCHAR(50) NULL,
    city VARCHAR(50) NULL,
    state VARCHAR(50) NULL,
    year_founded SMALLINT NULL
);

CREATE TABLE IF NOT EXISTS players (
    player_id INT NOT NULL PRIMARY KEY,
    first_name VARCHAR(50) NULL,
    last_name VARCHAR(50) NULL,
    full_name VARCHAR(200) NOT NULL,
    birth_date DATE NULL,
    school VARCHAR(255) NULL,
    country VARCHAR(100) NULL,
    height VARCHAR(20) NULL,
    weight INT NULL,
    season_exp INT NULL,
    jersey VARCHAR(20) NULL,
    position VARCHAR(100) NULL,
    is_active BOOLEAN NULL,
    team_id INT NULL,
    draft_year INT NULL,
    draft_round INT NULL,
    draft_number INT NULL
);

-- A API contém alguns jogadores de nome único, como Nene.
-- Também aplica a regra a bancos criados por versões anteriores do projeto.
ALTER TABLE players
    MODIFY first_name VARCHAR(50) NULL,
    MODIFY last_name VARCHAR(50) NULL,
    MODIFY full_name VARCHAR(200) NOT NULL,
    MODIFY school VARCHAR(255) NULL,
    MODIFY country VARCHAR(100) NULL,
    MODIFY height VARCHAR(20) NULL,
    MODIFY jersey VARCHAR(20) NULL,
    MODIFY position VARCHAR(100) NULL;

CREATE TABLE IF NOT EXISTS player_enrichment_checkpoint (
    player_id INT NOT NULL PRIMARY KEY,
    enriched_at DATETIME NOT NULL,
    CONSTRAINT fk_enrichment_player
        FOREIGN KEY (player_id) REFERENCES players(player_id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS games (
    game_id VARCHAR(20) NOT NULL PRIMARY KEY,
    season VARCHAR(10) NOT NULL,
    season_type VARCHAR(30) NOT NULL DEFAULT 'Regular Season',
    game_date DATE NOT NULL,
    home_team_id INT NOT NULL,
    away_team_id INT NOT NULL,
    home_score SMALLINT NULL,
    away_score SMALLINT NULL,
    status VARCHAR(30) NULL
);

CREATE TABLE IF NOT EXISTS player_game_stats (
    game_id VARCHAR(20) NOT NULL,
    player_id INT NOT NULL,
    team_id INT NOT NULL,
    player_name VARCHAR(200) NULL,
    minutes VARCHAR(20) NULL,
    points SMALLINT NULL,
    rebounds SMALLINT NULL,
    assists SMALLINT NULL,
    steals SMALLINT NULL,
    blocks SMALLINT NULL,
    turnovers SMALLINT NULL,
    personal_fouls SMALLINT NULL,
    field_goals_made SMALLINT NULL,
    field_goals_attempted SMALLINT NULL,
    three_pointers_made SMALLINT NULL,
    three_pointers_attempted SMALLINT NULL,
    free_throws_made SMALLINT NULL,
    free_throws_attempted SMALLINT NULL,
    plus_minus SMALLINT NULL,
    start_position VARCHAR(10) NULL,
    comment VARCHAR(255) NULL,
    PRIMARY KEY (game_id, player_id)
);

CREATE TABLE IF NOT EXISTS player_game_stats_checkpoint (
    game_id VARCHAR(20) NOT NULL PRIMARY KEY,
    total_players SMALLINT NOT NULL,
    loaded_at DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS game_ingestion_checkpoint (
    season VARCHAR(10) NOT NULL,
    season_type VARCHAR(30) NOT NULL,
    total_games INT NOT NULL,
    loaded_at DATETIME NOT NULL,
    PRIMARY KEY (season, season_type)
);
