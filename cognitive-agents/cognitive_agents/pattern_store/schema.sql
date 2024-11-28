-- Pattern evolution tracking
CREATE TABLE IF NOT EXISTS pattern_evolution (
    id INTEGER PRIMARY KEY,
    pattern_id INTEGER,
    from_version INTEGER,
    to_version INTEGER,
    change_type TEXT,  -- 'refinement', 'merge', 'split'
    change_description TEXT,
    timestamp TEXT,
    FOREIGN KEY (pattern_id) REFERENCES patterns(id)
);

-- Pattern relationships
CREATE TABLE IF NOT EXISTS pattern_relationships (
    id INTEGER PRIMARY KEY,
    pattern_id1 INTEGER,
    pattern_id2 INTEGER,
    relationship_type TEXT,  -- 'similar', 'opposite', 'causes', 'results_from'
    strength REAL,
    FOREIGN KEY (pattern_id1) REFERENCES patterns(id),
    FOREIGN KEY (pattern_id2) REFERENCES patterns(id)
);

-- Sequences and patterns
CREATE TABLE IF NOT EXISTS sequences (
    id TEXT PRIMARY KEY,
    type TEXT NOT NULL,  -- confidence, frustration, excitement
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS patterns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sequence_id TEXT NOT NULL,
    category TEXT NOT NULL,
    theme TEXT NOT NULL,
    confidence REAL NOT NULL,
    timestamp TEXT NOT NULL,
    thought TEXT NOT NULL,
    FOREIGN KEY (sequence_id) REFERENCES sequences(id)
);

CREATE TABLE IF NOT EXISTS correlations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sequence_id TEXT NOT NULL,
    from_pattern_id INTEGER,
    to_pattern_id INTEGER,
    confidence REAL NOT NULL,
    evidence TEXT NOT NULL,
    FOREIGN KEY (sequence_id) REFERENCES sequences(id),
    FOREIGN KEY (from_pattern_id) REFERENCES patterns(id),
    FOREIGN KEY (to_pattern_id) REFERENCES patterns(id)
); 