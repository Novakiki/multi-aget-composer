import sqlite3
from typing import Dict, List
from datetime import datetime
from termcolor import colored

class EvolutionStore:
    """Stores and retrieves evolution history."""
    
    def __init__(self, db_path: str = "evolution_history.db"):
        """Initialize the evolution store."""
        self.db_path = db_path
        self._init_db()
        
    def _init_db(self):
        """Initialize the database schema."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Evolution states table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS evolution_states (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        stage TEXT NOT NULL,
                        connection_strength REAL,
                        emergence_strength REAL,
                        theme_coverage REAL,
                        depth REAL,
                        pattern_count INTEGER,
                        growth_rate REAL,
                        trend TEXT
                    )
                """)
                
                # Themes table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS evolution_themes (
                        state_id INTEGER,
                        theme TEXT,
                        FOREIGN KEY(state_id) REFERENCES evolution_states(id)
                    )
                """)
                
                print(colored("✅ Evolution store initialized", "green"))
                
        except Exception as e:
            print(colored(f"❌ Database initialization error: {str(e)}", "red"))
            
    def store_evolution_state(self, state: Dict) -> bool:
        """Store an evolution state."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Insert evolution state
                cursor.execute("""
                    INSERT INTO evolution_states (
                        timestamp, stage, connection_strength,
                        emergence_strength, theme_coverage, depth,
                        pattern_count, growth_rate, trend
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    state['timestamp'],
                    state['stage'],
                    state['metrics']['connection_strength'],
                    state['metrics']['emergence_strength'],
                    state['metrics']['theme_coverage'],
                    state['metrics']['depth'],
                    state['pattern_count'],
                    state.get('progression', {}).get('growth_rate', 0.0),
                    state.get('progression', {}).get('trend', 'initial')
                ))
                
                state_id = cursor.lastrowid
                
                # Store themes
                for theme in state.get('themes', []):
                    cursor.execute("""
                        INSERT INTO evolution_themes (state_id, theme)
                        VALUES (?, ?)
                    """, (state_id, theme))
                
                print(colored(f"✅ Stored evolution state: {state['stage']}", "green"))
                return True
                
        except Exception as e:
            print(colored(f"❌ Store error: {str(e)}", "red"))
            return False
            
    def get_evolution_history(self, limit: int = None) -> List[Dict]:
        """Retrieve evolution history."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get states with limit if specified
                query = """
                    SELECT * FROM evolution_states 
                    ORDER BY timestamp DESC
                """
                if limit:
                    query += f" LIMIT {limit}"
                    
                cursor.execute(query)
                states = cursor.fetchall()
                
                history = []
                for state in states:
                    # Get themes for this state
                    cursor.execute("""
                        SELECT theme FROM evolution_themes
                        WHERE state_id = ?
                    """, (state[0],))
                    themes = [row[0] for row in cursor.fetchall()]
                    
                    history.append({
                        'timestamp': state[1],
                        'stage': state[2],
                        'metrics': {
                            'connection_strength': state[3],
                            'emergence_strength': state[4],
                            'theme_coverage': state[5],
                            'depth': state[6]
                        },
                        'pattern_count': state[7],
                        'progression': {
                            'growth_rate': state[8],
                            'trend': state[9]
                        },
                        'themes': themes
                    })
                
                return history
                
        except Exception as e:
            print(colored(f"❌ Retrieval error: {str(e)}", "red"))
            return [] 