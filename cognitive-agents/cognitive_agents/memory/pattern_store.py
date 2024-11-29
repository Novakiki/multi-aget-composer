from typing import Dict, List
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from termcolor import colored

class PatternStore:
    """Basic pattern storage and evolution tracking."""
    
    def __init__(self, mongodb_uri: str = "mongodb://localhost:27017"):
        """Initialize with MongoDB."""
        self.client = AsyncIOMotorClient(mongodb_uri)
        self.db = self.client.evolution
        self.patterns = self.db.patterns
        
    async def store_pattern(self, pattern: Dict) -> str:
        """Store pattern and begin evolution."""
        try:
            pattern_id = f"pat_{datetime.now().isoformat()}"
            await self.patterns.insert_one({
                '_id': pattern_id,
                'content': pattern,
                'evolution': {
                    'stage': 'emerging',
                    'history': [],
                    'connections': []
                },
                'created_at': datetime.now()
            })
            print(colored(f"✨ Pattern {pattern_id} stored", "green"))
            return pattern_id
            
        except Exception as e:
            print(colored(f"❌ Storage error: {str(e)}", "red"))
            raise 