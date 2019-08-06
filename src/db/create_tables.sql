-- club table
CREATE TABLE IF NOT EXISTS club (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    url TEXT NOT NULL
)

-- tournament table
CREATE TABLE IF NOT EXISTS tournament (
    id INTEGER PRIMARY KEY,
    club_id INTEGER,
    url TEXT NOT NULL,
    date TEXT,
    rounds INTEGER,
    boards INTEGER,
    pairs INTEGER,
    tournament_type TEXT,
    FOREIGN KEY(club_id) REFERENCES club(id),
)

-- pair_score table
CREATE TABLE IF NOT EXISTS pair_score (
    id INTEGER PRIMARY KEY,
    player_name1 TEXT,
    player_name2 TEXT,
    club_name1 TEXT,
    club_name2 TEXT,
    points REAL,
    score REAL,
    tournament_id INTEGER NOT NULL,
    FOREIGN KEY(tournament_id) REFERENCES tournament(id)
)

-- pair_board table
CREATE TABLE IF NOT EXISTS pair_board (
    id INTEGER PRIMARY KEY,
    board_number INTEGER,
    opponent_name1 TEXT,
    opponent_name2 TEXT,
    contract_level INTEGER,
    contract_suit TEXT,
    doubled INTEGER,
    redoubled INTEGER,
    declearer TEXT,
    tricks INTEGER,
    lead_level INTEGER,
    lead_suit TEXT,
    score REAL,
    egge_enum TEXT,
    pair_score_id INTEGER,
    FOREIGN KEY(pair_score_id) REFERENCES pair_score(id)
)
