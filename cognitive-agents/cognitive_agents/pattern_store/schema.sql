CREATE TABLE sequences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE patterns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sequence_id INTEGER,
    category TEXT NOT NULL,
    theme TEXT NOT NULL,
    confidence REAL NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    thought TEXT NOT NULL,
    FOREIGN KEY (sequence_id) REFERENCES sequences(id)
);

CREATE TABLE pattern_cache (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    thought_hash TEXT NOT NULL UNIQUE,
    thought_text TEXT NOT NULL,
    patterns_json TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    last_used_at TEXT NOT NULL DEFAULT (datetime('now')),
    use_count INTEGER DEFAULT 0
);
