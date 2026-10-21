CREATE TABLE IF NOT EXISTS dim_date (
    date_key INT NOT NULL PRIMARY KEY,
    full_date DATE NOT NULL UNIQUE,
    calendar_year SMALLINT NOT NULL,
    calendar_quarter TINYINT NOT NULL,
    calendar_month TINYINT NOT NULL,
    month_name VARCHAR(12) NOT NULL,
    day_of_month TINYINT NOT NULL,
    day_of_week TINYINT NOT NULL,
    day_name VARCHAR(12) NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_season (
    season VARCHAR(10) NOT NULL PRIMARY KEY,
    start_year SMALLINT NOT NULL,
    end_year SMALLINT NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_team (
    team_id INT NOT NULL PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL,
    abbreviation VARCHAR(10) NULL,
    city VARCHAR(100) NULL,
    state VARCHAR(100) NULL,
    year_founded SMALLINT NULL
);

CREATE TABLE IF NOT EXISTS dim_player (
    player_id INT NOT NULL PRIMARY KEY,
    full_name VARCHAR(200) NOT NULL,
    first_name VARCHAR(100) NULL,
    last_name VARCHAR(100) NULL,
    birth_date DATE NULL,
    country VARCHAR(100) NULL,
    position VARCHAR(100) NULL,
    is_active BOOLEAN NULL,
    draft_year INT NULL
);

CREATE TABLE IF NOT EXISTS fact_games (
    game_id VARCHAR(20) NOT NULL PRIMARY KEY,
    date_key INT NOT NULL,
    season VARCHAR(10) NOT NULL,
    season_type VARCHAR(30) NOT NULL,
    home_team_id INT NOT NULL,
    away_team_id INT NOT NULL,
    home_score SMALLINT NULL,
    away_score SMALLINT NULL,
    winner_team_id INT NULL,
    score_margin SMALLINT NULL,
    status VARCHAR(30) NULL
);

CREATE TABLE IF NOT EXISTS fact_player_game_stats (
    game_id VARCHAR(20) NOT NULL,
    player_id INT NOT NULL,
    team_id INT NOT NULL,
    date_key INT NOT NULL,
    season VARCHAR(10) NOT NULL,
    season_type VARCHAR(30) NOT NULL,
    minutes_played DECIMAL(7, 2) NULL,
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
    PRIMARY KEY (game_id, player_id)
);
