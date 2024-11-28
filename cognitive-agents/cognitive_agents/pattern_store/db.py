"""Database connection and basic operations."""
import sqlite3
from typing import Dict, List
from pathlib import Path
from datetime import datetime
import json

class PatternStore:
    def __init__(self):
        self.db_path = Path(__file__).parent / "patterns.db"
        self._init_db()
    
    def _init_db(self):
        """Initialize database with schema."""
        with sqlite3.connect(self.db_path) as conn:
            with open(Path(__file__).parent / "schema.sql") as f:
                conn.executescript(f.read())
    
    def create_sequence(self, sequence_type: str) -> str:
        """Create a new sequence and return its ID."""
        sequence_id = f"{sequence_type}_{datetime.now().isoformat()}"
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO sequences (id, type, created_at)
                VALUES (?, ?, ?)
            """, (sequence_id, sequence_type, datetime.now().isoformat()))
        return sequence_id
    
    def store_pattern(self, pattern: Dict, sequence_id: str) -> int:
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
                DROP TABLE IF EXISTS correlations;
                DROP TABLE IF EXISTS patterns;
                DROP TABLE IF EXISTS sequences;
                DROP TABLE IF EXISTS pattern_evolution;
                DROP TABLE IF EXISTS pattern_relationships;
            """)
            self._init_db()