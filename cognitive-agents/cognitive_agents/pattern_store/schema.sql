-- Pattern Storage Schema

-- Sequences table to track emotional sequences
CREATE TABLE IF NOT EXISTS sequences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,  -- confidence, frustration, excitement
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Patterns table for storing detected patterns
CREATE TABLE IF NOT EXISTS patterns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sequence_id INTEGER,
    category TEXT NOT NULL,  -- emotional, behavioral, surface, meta
    theme TEXT NOT NULL,
    confidence REAL NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    thought TEXT NOT NULL,
    FOREIGN KEY (sequence_id) REFERENCES sequences(id)
);

-- New tables for pattern caching and recovery
CREATE TABLE IF NOT EXISTS pattern_cache (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    thought_hash TEXT NOT NULL,        -- Hash of the thought text
    thought_text TEXT NOT NULL,        -- Original thought
    patterns_json TEXT NOT NULL,       -- Stored as JSON
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    last_used_at TEXT NOT NULL DEFAULT (datetime('now')),
    use_count INTEGER DEFAULT 0,
    UNIQUE(thought_hash)               -- For quick lookups
);

-- Add cache metrics table
CREATE TABLE IF NOT EXISTS cache_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL DEFAULT (datetime('now')),
    total_entries INTEGER NOT NULL,
    total_hits INTEGER NOT NULL,
    avg_hits REAL NOT NULL,
    avg_age_days REAL NOT NULL
);

-- Create indices for better performance
CREATE INDEX IF NOT EXISTS idx_patterns_sequence 
ON patterns(sequence_id);

CREATE INDEX IF NOT EXISTS idx_patterns_category 
ON patterns(category);

-- Index for pattern similarity searches
CREATE INDEX IF NOT EXISTS idx_patterns_theme 
ON patterns(theme);

CREATE INDEX IF NOT EXISTS idx_pattern_cache_thought 
ON pattern_cache(thought_text);
  