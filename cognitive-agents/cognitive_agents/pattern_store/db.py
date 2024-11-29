"""Database connection and basic operations."""
import sqlite3
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime
import json
import time
import hashlib
from termcolor import colored
from ..config import DB_SETTINGS, CACHE_SETTINGS

class PatternStore:
    def __init__(self):
        # Convert relative paths to absolute using package location
        base_path = Path(__file__).parent
        self.db_path = base_path / DB_SETTINGS['PATH'].split('/')[-1]
        self.schema_path = base_path / DB_SETTINGS['SCHEMA'].split('/')[-1]
        self.encoding = DB_SETTINGS['ENCODING']
        self.timeout = DB_SETTINGS['TIMEOUT']
        self.retries = DB_SETTINGS['RETRIES']
        
        self._init_db()
    
    def _init_db(self):
        """Initialize database with retry logic."""
        for attempt in range(self.retries):
            try:
                with open(self.schema_path, 'r', encoding=self.encoding) as f:
                    schema = f.read()
                
                conn = sqlite3.connect(self.db_path, timeout=self.timeout)
                conn.executescript(schema)
                conn.close()
                return
                
            except Exception as e:
                if attempt == self.retries - 1:
                    raise
                time.sleep(1)  # Wait before retry
    
    def create_sequence(self, sequence_type: str) -> int:
        """Create a new sequence and return its ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                INSERT INTO sequences (type, created_at)
                VALUES (?, datetime('now'))
                RETURNING id
            """, (sequence_type,))
            return cursor.fetchone()[0]
    
    def store_pattern(self, pattern: Dict, sequence_id: int) -> int:
        """Store a pattern and return its ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                INSERT INTO patterns 
                (sequence_id, category, theme, confidence, timestamp, thought)
                VALUES (?, ?, ?, ?, ?, ?)
                RETURNING id
            """, (
                sequence_id,
                pattern['category'],
                pattern['theme'],
                pattern['confidence'],
                pattern['timestamp'],
                pattern['thought']
            ))
            return cursor.fetchone()[0]
    
    def store_correlation(self, correlation: Dict, sequence_id: str):
        """Store a correlation between patterns."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO correlations 
                (sequence_id, from_pattern_id, to_pattern_id, confidence, evidence)
                VALUES (?, ?, ?, ?, ?)
            """, (
                sequence_id,
                correlation['from_pattern_id'],
                correlation['to_pattern_id'],
                correlation['confidence'],
                json.dumps(correlation['evidence'])
            ))
    
    def get_sequence_patterns(self, sequence_id: str) -> List[Dict]:
        """Get all patterns for a sequence."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT * FROM patterns 
                WHERE sequence_id = ?
                ORDER BY timestamp
            """, (sequence_id,))
            return cursor.fetchall()
    
    def cleanup(self):
        """Clean up database for testing."""
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript("""
                DROP TABLE IF EXISTS patterns;
                DROP TABLE IF EXISTS sequences;
            """)
            self._init_db()
    
    def cache_pattern(self, thought: str, patterns: List[Dict]) -> None:
        """Cache patterns for a thought."""
        thought_hash = hashlib.sha256(thought.encode()).hexdigest()
        
        with sqlite3.connect(self.db_path) as conn:
            try:
                conn.execute("""
                    INSERT INTO pattern_cache 
                    (thought_hash, thought_text, patterns_json)
                    VALUES (?, ?, ?)
                    ON CONFLICT(thought_hash) DO UPDATE SET
                        patterns_json = ?,
                        last_used_at = datetime('now'),
                        use_count = use_count + 1
                """, (
                    thought_hash,
                    thought,
                    json.dumps(patterns),
                    json.dumps(patterns)
                ))
            except Exception as e:
                print(colored(f"Cache error: {str(e)}", "yellow"))

    def get_cached_patterns(self, thought: str) -> List[Dict]:
        """Get cached patterns."""
        thought_hash = hashlib.sha256(thought.encode()).hexdigest()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT patterns_json
                FROM pattern_cache
                WHERE thought_hash = ?
            """, (thought_hash,))
            
            row = cursor.fetchone()
            if row:
                # Update usage stats
                conn.execute("""
                    UPDATE pattern_cache 
                    SET last_used_at = datetime('now'),
                        use_count = use_count + 1
                    WHERE thought_hash = ?
                """, (thought_hash,))
                return json.loads(row[0])
            return []
    
    def cleanup_sequences(self):
        """Clean up sequences while preserving pattern cache."""
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript("""
                DROP TABLE IF EXISTS patterns;
                DROP TABLE IF EXISTS sequences;
            """)
            # Reinitialize sequence tables only
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS sequences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT (datetime('now'))
                );
                
                CREATE TABLE IF NOT EXISTS patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sequence_id INTEGER,
                    category TEXT NOT NULL,
                    theme TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    timestamp TIMESTAMP NOT NULL,
                    thought TEXT NOT NULL,
                    FOREIGN KEY (sequence_id) REFERENCES sequences(id)
                );
                
                CREATE INDEX IF NOT EXISTS idx_patterns_sequence 
                ON patterns(sequence_id);
                
                CREATE INDEX IF NOT EXISTS idx_patterns_category 
                ON patterns(category);
            """)
    
    def cleanup_old_cache(self):
        """Remove expired cache entries."""
        with sqlite3.connect(self.db_path) as conn:
            # Remove old entries
            conn.execute("""
                DELETE FROM pattern_cache 
                WHERE (
                    julianday('now') - julianday(created_at) > ? 
                    AND use_count < ?
                )
                OR rowid NOT IN (
                    SELECT rowid FROM pattern_cache 
                    ORDER BY use_count DESC, last_used_at DESC 
                    LIMIT ?
                )
            """, (
                CACHE_SETTINGS['MAX_AGE_DAYS'],
                CACHE_SETTINGS['MIN_USE_COUNT'],
                CACHE_SETTINGS['MAX_CACHE_SIZE']
            ))
    
    def get_cache_metrics(self) -> Dict:
        """Get cache hit/miss metrics."""
        with sqlite3.connect(self.db_path) as conn:
            # Make SQLite return dictionaries
            conn.row_factory = sqlite3.Row
            
            cursor = conn.execute("""
                SELECT 
                    COUNT(*) as total_entries,
                    SUM(use_count) as total_hits,
                    AVG(use_count) as avg_hits,
                    AVG(julianday('now') - julianday(created_at)) as avg_age_days
                FROM pattern_cache
            """)
            row = cursor.fetchone()
            return {
                'total_entries': row['total_entries'],
                'total_hits': row['total_hits'] or 0,  # Handle NULL
                'avg_hits': float(row['avg_hits'] or 0),
                'avg_age_days': float(row['avg_age_days'] or 0)
            }