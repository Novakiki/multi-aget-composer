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
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        # Initialize only once
        base_path = Path(__file__).parent
        self.db_path = base_path / DB_SETTINGS['PATH'].split('/')[-1]
        self.schema_path = base_path / DB_SETTINGS['SCHEMA'].split('/')[-1]
        self.encoding = DB_SETTINGS['ENCODING']
        self.timeout = DB_SETTINGS['TIMEOUT']
        self.retries = DB_SETTINGS['RETRIES']
        self.retry_delay = 1
        
        self._init_db()
        self._initialized = True
    
    def _init_db(self):
        """Initialize database with retry logic."""
        for attempt in range(self.retries):
            try:
                with open(self.schema_path, 'r', encoding=self.encoding) as f:
                    schema = f.read()
                
                conn = sqlite3.connect(self.db_path, timeout=self.timeout)
                # Execute each statement separately
                for statement in schema.split(';'):
                    statement = statement.strip()
                    if statement:  # Skip empty statements
                        print(f"Executing:\n{statement}\n")  # Debug
                        conn.execute(statement)
                conn.commit()
                conn.close()
                return
                
            except Exception as e:
                print(colored(f"❌ DB init attempt {attempt + 1} failed: {str(e)}", "red"))
                if attempt == self.retries - 1:
                    raise
                time.sleep(self.retry_delay)
    
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
            # Drop all tables
            conn.executescript("""
                DROP TABLE IF EXISTS patterns;
                DROP TABLE IF EXISTS sequences;
                DROP TABLE IF EXISTS pattern_cache;
                DROP TABLE IF EXISTS cache_metrics;
                DROP TABLE IF EXISTS pattern_proposals;
                DROP TABLE IF EXISTS pattern_votes;
                DROP TABLE IF EXISTS pattern_status_history;
                DROP TABLE IF EXISTS validation_results;
                DROP TABLE IF EXISTS validation_phases;
            """)
        
        # Reinitialize clean database
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
        """Clean up sequences while preserving structure."""
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript("""
                DELETE FROM patterns;
                DELETE FROM sequences;
                DELETE FROM pattern_cache;
            """)
            conn.commit()
    
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