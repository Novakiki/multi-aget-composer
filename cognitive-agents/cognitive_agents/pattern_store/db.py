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
        base_path = Path(DB_SETTINGS['path']).parent
        base_path.mkdir(parents=True, exist_ok=True)
        
        self.db_path = Path(DB_SETTINGS['path'])
        self._setup_database()
        PatternStore._initialized = True
    
    def _setup_database(self):
        """Initialize database schema."""
        try:
            with sqlite3.connect(
                self.db_path,
                timeout=DB_SETTINGS['timeout'],
                isolation_level=DB_SETTINGS['isolation_level']
            ) as conn:
                # Create patterns table
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS patterns (
                        id TEXT PRIMARY KEY,
                        type TEXT NOT NULL,
                        content TEXT NOT NULL,
                        confidence REAL NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create sequences table
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS sequences (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        type TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create pattern_cache table
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS pattern_cache (
                        hash TEXT PRIMARY KEY,
                        patterns TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        use_count INTEGER DEFAULT 1
                    )
                """)
                
                conn.commit()
                
        except Exception as e:
            print(colored(f"❌ Database setup error: {str(e)}", "red"))
            raise
    
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
        self._setup_database()
    
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
        try:
            thought_hash = hashlib.sha256(thought.encode()).hexdigest()
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT patterns 
                    FROM pattern_cache
                    WHERE hash = ?
                """, (thought_hash,))
                
                row = cursor.fetchone()
                if row:
                    # Update usage stats
                    conn.execute("""
                        UPDATE pattern_cache 
                        SET last_used = datetime('now'),
                            use_count = use_count + 1
                        WHERE hash = ?
                    """, (thought_hash,))
                    return json.loads(row[0])
                return []
                
        except Exception as e:
            print(colored(f"⚠️ Error retrieving patterns: {str(e)}", "yellow"))
            return []
    
    def cleanup_sequences(self):
        """Clean up sequences while preserving structure."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Check if tables exist first
                tables = conn.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name IN ('patterns', 'sequences', 'pattern_cache')
                """).fetchall()
                
                if tables:  # Only delete if tables exist
                    conn.executescript("""
                        DELETE FROM patterns;
                        DELETE FROM sequences;
                        DELETE FROM pattern_cache;
                    """)
                    conn.commit()
                
        except Exception as e:
            print(colored(f"❌ Cleanup error: {str(e)}", "red"))
    
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