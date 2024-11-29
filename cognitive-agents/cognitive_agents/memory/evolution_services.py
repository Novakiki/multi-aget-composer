from typing import Dict, Optional
from functools import lru_cache
import os
from pinecone import Pinecone
from neo4j import AsyncGraphDatabase
from motor.motor_asyncio import AsyncIOMotorClient

class EvolutionServices:
    """Service locator for evolution stack."""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {
            'pinecone': {
                'api_key': os.getenv('PINECONE_API_KEY'),
                'environment': os.getenv('PINECONE_ENV', 'gcp-starter')
            },
            'neo4j': {
                'uri': os.getenv('NEO4J_URI', 'neo4j://localhost:7687'),
                'user': os.getenv('NEO4J_USER', 'neo4j'),
                'password': os.getenv('NEO4J_PASSWORD')
            },
            'mongodb': {
                'uri': os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
            }
        }
        self._services = {}
        
    @lru_cache()
    def get_service(self, name: str):
        """Get or create service by name."""
        if name not in self._services:
            if name == 'pinecone':
                self._services[name] = Pinecone(
                    api_key=self.config['pinecone']['api_key']
                )
            elif name == 'neo4j':
                self._services[name] = AsyncGraphDatabase.driver(
                    self.config['neo4j']['uri'],
                    auth=(self.config['neo4j']['user'], 
                          self.config['neo4j']['password'])
                )
            elif name == 'mongodb':
                self._services[name] = AsyncIOMotorClient(
                    self.config['mongodb']['uri']
                )
        return self._services[name]
        
    def is_available(self, name: str) -> bool:
        """Check if service is configured and available."""
        try:
            service = self.get_service(name)
            if name == 'pinecone':
                service.list_indexes()
            elif name == 'neo4j':
                service.verify_connectivity()
            elif name == 'mongodb':
                service.admin.command('ping')
            return True
        except:
            return False 