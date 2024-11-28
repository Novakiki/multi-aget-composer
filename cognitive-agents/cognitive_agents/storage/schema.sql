-- Add pattern evolution tracking
CREATE TABLE pattern_evolution (
    id INTEGER PRIMARY KEY,
    pattern_id INTEGER,
    from_version INTEGER,
    to_version INTEGER,
    change_type TEXT,  -- 'refinement', 'merge', 'split'
    change_description TEXT,
    timestamp TEXT,
    FOREIGN KEY (pattern_id) REFERENCES patterns(id)
);

-- Add pattern relationships
CREATE TABLE pattern_relationships (
    id INTEGER PRIMARY KEY,
    pattern_id1 INTEGER,
    pattern_id2 INTEGER,
    relationship_type TEXT,  -- 'similar', 'opposite', 'causes', 'results_from'
    strength REAL,
    FOREIGN KEY (pattern_id1) REFERENCES patterns(id),
    FOREIGN KEY (pattern_id2) REFERENCES patterns(id)
); 