from typing import Dict, List, Optional
from datetime import datetime
from termcolor import colored
import numpy as np
from .intentional_memory import IntentionalMemory
import hashlib

class RAGEnhancer:
    """Enhances memory with contextual retrieval and generation."""
    
    def __init__(self, memory: IntentionalMemory):
        self.memory = memory
        self.context_window = 5  # From ARCHITECTURE.md
        self.context_cache = {}  # Cache retrieved context
        
        # Define enhancement types from DIMENSIONS.md
        self.enhancement_types = {
            'historical': {
                'description': 'Previous related thoughts',
                'weight': 0.4
            },
            'conceptual': {
                'description': 'Related concepts and patterns',
                'weight': 0.3
            },
            'intentional': {
                'description': 'Intent-based connections',
                'weight': 0.3
            }
        }
        
        print(colored("🔍 RAG Enhancement System Initialized", "green"))
        
    async def enhance_thought(
        self,
        thought: str,
        intent: Optional[str] = None
    ) -> Dict:
        """Enhance thought with relevant context."""
        try:
            print(colored("\n🔄 Starting thought enhancement...", "cyan"))
            
            # 1. Get base embedding
            embedding = self.memory.encoder.encode(thought)
            
            # 2. Retrieve relevant context
            context = await self._retrieve_context(
                thought,
                embedding,
                intent
            )
            
            # 3. Generate enhanced understanding
            enhancement = await self._generate_enhancement(
                thought,
                context
            )
            
            # 4. Cache for future use
            self._cache_enhancement(thought, enhancement)
            
            return enhancement
            
        except Exception as e:
            print(colored(f"❌ Enhancement error: {str(e)}", "red"))
            return self._create_empty_enhancement()
            
    async def _retrieve_context(
        self,
        thought: str,
        embedding: np.ndarray,
        intent: Optional[str]
    ) -> Dict:
        """Retrieve relevant context for enhancement."""
        context = {
            'historical': [],
            'conceptual': [],
            'intentional': []
        }
        
        # Get historical context
        if intent:
            category = self.memory.categories.get(intent)
            if category:
                similar_thoughts = self._find_similar_in_category(
                    embedding,
                    category,
                    top_k=self.context_window
                )
                context['historical'].extend(similar_thoughts)
        
        # Get conceptual context
        # (Implementation based on DIMENSIONS.md)
        
        return context
        
    def _find_similar_in_category(
        self,
        query_embedding: np.ndarray,
        category: 'IntentionCategory',
        top_k: int = 5
    ) -> List[Dict]:
        """Find similar thoughts within a category."""
        if not category.memory['embeddings']:
            return []
            
        # Calculate similarities
        similarities = [
            np.dot(query_embedding, stored_vec)
            for stored_vec in category.memory['embeddings']
        ]
        
        # Get top matches
        indices = np.argsort(similarities)[-top_k:]
        
        return [{
            'thought': category.memory['thoughts'][i],
            'similarity': float(similarities[i]),
            'metadata': category.memory['metadata'][i]
        } for i in indices]
        
    def _create_empty_enhancement(self) -> Dict:
        """Create empty enhancement structure."""
        return {
            'context': {
                'historical': [],
                'conceptual': [],
                'intentional': []
            },
            'enhancement': '',
            'timestamp': datetime.now().isoformat()
        } 

    async def _generate_enhancement(self, thought: str, context: Dict) -> Dict:
        """Generate enhanced understanding using context."""
        try:
            # Basic enhancement for now
            return {
                'context': context,
                'enhancement': thought,  # Placeholder
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            print(colored(f"❌ Generation error: {str(e)}", "red"))
            return self._create_empty_enhancement()
        
    def _cache_enhancement(self, thought: str, enhancement: Dict) -> None:
        """Cache enhancement results with TTL."""
        try:
            # Create cache key
            cache_key = hashlib.sha256(thought.encode()).hexdigest()
            
            # Add cache metadata
            cache_entry = {
                'enhancement': enhancement,
                'timestamp': datetime.now().isoformat(),
                'ttl': 3600,  # 1 hour TTL
                'access_count': 0
            }
            
            # Store in cache
            self.context_cache[cache_key] = cache_entry
            
            # Cleanup old cache entries
            self._cleanup_cache()
            
            print(colored("📦 Enhancement cached", "green"))
            
        except Exception as e:
            print(colored(f"⚠️ Cache error: {str(e)}", "yellow"))
            
    def _cleanup_cache(self) -> None:
        """Remove expired cache entries."""
        try:
            current_time = datetime.now()
            expired_keys = []
            
            for key, entry in self.context_cache.items():
                cache_time = datetime.fromisoformat(entry['timestamp'])
                age = (current_time - cache_time).total_seconds()
                
                if age > entry['ttl']:
                    expired_keys.append(key)
                    
            # Remove expired entries
            for key in expired_keys:
                del self.context_cache[key]
                
            if expired_keys:
                print(colored(f"🧹 Removed {len(expired_keys)} expired cache entries", "yellow"))
                
        except Exception as e:
            print(colored(f"⚠️ Cache cleanup error: {str(e)}", "yellow"))
        