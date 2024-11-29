from typing import Dict, List, Optional
from datetime import datetime
from termcolor import colored
import numpy as np
from .intentional_memory import IntentionalMemory
import hashlib
from ..openai_client import AsyncOpenAI

class RAGEnhancer:
    """Enhances memory with contextual retrieval and generation."""
    
    # Configuration from DIMENSIONS.md
    THRESHOLDS = {
        'similarity': 0.6,    # Increase base threshold
        'high_relevance': 0.8,  # Make high relevance harder to achieve
        'minimal': 0.4       # Raise minimal threshold
    }
    
    WEIGHTS = {
        'similarity': 0.5,   # Increase base similarity importance
        'intent_match': 0.2,  # Reduce intent weight
        'recency': 0.3      # Keep recency as is
    }
    
    def __init__(self, memory: IntentionalMemory):
        self.memory = memory
        self.client = AsyncOpenAI()
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
        
        # Add conceptual context
        context['conceptual'] = await self._find_conceptual_patterns(
            thought,
            embedding
        )
        
        return context
        
    def _find_similar_in_category(
        self,
        query_embedding: np.ndarray,
        category: 'IntentionCategory',
        top_k: int = 5
    ) -> List[Dict]:
        """Find similar thoughts with enhanced scoring."""
        if not category.memory['embeddings']:
            return []
            
        # Calculate base similarities
        similarities = [
            np.dot(query_embedding, stored_vec)
            for stored_vec in category.memory['embeddings']
        ]
        
        # Calculate recency scores
        current_time = datetime.now()
        recency_scores = []
        for metadata in category.memory['metadata']:
            time_diff = (current_time - datetime.fromisoformat(metadata['timestamp'])).total_seconds()
            recency_score = 1.0 / (1.0 + time_diff / 3600)  # Decay over hours
            recency_scores.append(recency_score)
            
        # Add intent matching score
        intent_scores = []
        for metadata in category.memory['metadata']:
            intent_match = float(metadata['intent'] == category.name)
            intent_scores.append(intent_match)
        
        # Update final scores to include intent
        final_scores = [
            similarities[i] * self.WEIGHTS['similarity'] +
            recency_scores[i] * self.WEIGHTS['recency'] +
            intent_scores[i] * self.WEIGHTS['intent_match']
            for i in range(len(similarities))
        ]
        
        # Filter and sort
        scored_indices = [
            (i, score) for i, score in enumerate(final_scores)
            if score >= self.THRESHOLDS['similarity']
        ]
        scored_indices.sort(key=lambda x: x[1], reverse=True)
        
        # Get top matches
        matches = []
        for idx, score in scored_indices[:top_k]:
            if score >= self.THRESHOLDS['minimal']:
                matches.append({
                    'thought': category.memory['thoughts'][idx],
                    'similarity': float(similarities[idx]),
                    'recency_score': float(recency_scores[idx]),
                    'combined_score': float(score),
                    'metadata': category.memory['metadata'][idx],
                    'relevance_level': self._get_relevance_level(score)
                })
                
        return matches
        
    def _get_relevance_level(self, score: float) -> str:
        """Get human-readable relevance level."""
        if score >= self.THRESHOLDS['high_relevance']:
            return 'high'
        elif score >= self.THRESHOLDS['similarity']:
            return 'medium'
        return 'low'
        
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
        
    async def _find_conceptual_patterns(
        self,
        thought: str,
        embedding: np.ndarray
    ) -> List[Dict]:
        """Find conceptual patterns in thought."""
        try:
            # 1. Extract core concepts
            concepts = await self._extract_concepts(thought)
            print(colored("\n📊 Extracted Concepts:", "cyan"))
            for concept in concepts:
                print(f"  • {concept['name']} ({concept['type']})")
            
            # 2. Find semantic clusters
            clusters = self._find_semantic_clusters(embedding)
            print(colored(f"\n🔍 Found {len(clusters)} semantic clusters", "cyan"))
            
            # 3. Identify conceptual patterns
            patterns = []
            for concept in concepts:
                related_thoughts = self._find_concept_related_thoughts(
                    concept,
                    clusters
                )
                print(colored(f"\n🔄 Processing concept: {concept['name']}", "yellow"))
                print(f"  Found {len(related_thoughts)} related thoughts")
                
                if related_thoughts:
                    pattern = {
                        'concept': concept,
                        'related_thoughts': related_thoughts,
                        'confidence': self._calculate_concept_confidence(
                            concept,
                            related_thoughts
                        ),
                        'emergence_time': datetime.now().isoformat(),
                        'support_evidence': self._gather_concept_evidence(
                            concept,
                            related_thoughts
                        )
                    }
                    patterns.append(pattern)
                    
            print(colored(f"🧩 Found {len(patterns)} conceptual patterns", "green"))
            return patterns
            
        except Exception as e:
            print(colored(f"❌ Conceptual pattern error: {str(e)}", "red"))
            return []
        
    async def _extract_concepts(self, thought: str) -> List[Dict]:
        """Extract core concepts from thought using LLM."""
        try:
            result = await self.client.chat_with_retries(
                messages=[{
                    "role": "system",
                    "content": """Extract core concepts from this thought. Return JSON:
                    {
                        "concepts": [
                            {
                                "name": "concept_name",
                                "type": "technical/abstract/domain",
                                "confidence": 0.8,
                                "related_terms": ["term1", "term2"]
                            }
                        ]
                    }"""
                }, {
                    "role": "user",
                    "content": thought
                }]
            )
            
            concepts = result.get('concepts', [])
            print(colored(f"🔍 Extracted {len(concepts)} concepts", "cyan"))
            return concepts
            
        except Exception as e:
            print(colored(f"❌ Concept extraction error: {str(e)}", "red"))
            return []
        
    def _find_semantic_clusters(self, embedding: np.ndarray) -> List[Dict]:
        """Find semantic clusters in memory."""
        try:
            # Get all embeddings from memory
            all_embeddings = []
            all_thoughts = []
            
            for category in self.memory.categories.values():
                all_embeddings.extend(category.memory['embeddings'])
                all_thoughts.extend(category.memory['thoughts'])
                
            if not all_embeddings:
                return []
                
            # Calculate similarities
            similarities = [
                np.dot(embedding, stored_vec)
                for stored_vec in all_embeddings
            ]
            
            # Group into clusters
            clusters = []
            threshold = 0.5  # Lower threshold for more inclusive clustering
            
            for i, sim in enumerate(similarities):
                if sim >= threshold:
                    # Add debug output
                    print(colored(f"  • Cluster found: {all_thoughts[i]} (sim: {sim:.2f})", "cyan"))
                    clusters.append({
                        'centroid': all_embeddings[i],
                        'thoughts': [all_thoughts[i]],
                        'similarity': float(sim)
                    })
                    
            return clusters
            
        except Exception as e:
            print(colored(f"❌ Clustering error: {str(e)}", "red"))
            return []
        
    def _find_concept_related_thoughts(
        self,
        concept: Dict,
        clusters: List[Dict]
    ) -> List[Dict]:
        """Find thoughts related to a concept within clusters."""
        try:
            related = []
            # Add concept variations
            concept_terms = {concept['name']} | set(concept['related_terms'])
            concept_parts = set(word.lower() for term in concept_terms 
                              for word in term.split())
            
            for cluster in clusters:
                for thought in cluster['thoughts']:
                    thought_words = set(thought.lower().split())
                    # Check for any word overlap
                    if thought_words & concept_parts:
                        related.append({
                            'content': thought,
                            'similarity': cluster['similarity'],
                            'concept_match': concept['name']
                        })
                        
            return related
            
        except Exception as e:
            print(colored(f"❌ Related thoughts error: {str(e)}", "red"))
            return []
        
    def _calculate_concept_confidence(
        self,
        concept: Dict,
        related_thoughts: List[Dict]
    ) -> float:
        """Calculate confidence score for a conceptual pattern."""
        try:
            if not related_thoughts:
                return 0.0
            
            # Factors from DIMENSIONS.md
            factors = {
                'support': len(related_thoughts) / 5.0,  # Normalize by expected support
                'similarity': sum(t['similarity'] for t in related_thoughts) / len(related_thoughts),
                'base_confidence': concept.get('confidence', 0.5)
            }
            
            # Weighted combination
            confidence = (
                factors['support'] * 0.3 +
                factors['similarity'] * 0.4 +
                factors['base_confidence'] * 0.3
            )
            
            return min(1.0, confidence)  # Cap at 1.0
            
        except Exception as e:
            print(colored(f"❌ Confidence calculation error: {str(e)}", "red"))
            return 0.0
        
    def _gather_concept_evidence(
        self,
        concept: Dict,
        related_thoughts: List[Dict]
    ) -> List[Dict]:
        """Gather evidence supporting the conceptual pattern."""
        try:
            evidence = []
            
            # Direct matches
            for thought in related_thoughts:
                evidence.append({
                    'type': 'direct_match',
                    'content': thought['content'],
                    'strength': thought['similarity'],
                    'concept_term': thought['concept_match']
                })
                
            # Semantic relationships
            if len(related_thoughts) >= 2:
                evidence.append({
                    'type': 'semantic_cluster',
                    'content': f"Found {len(related_thoughts)} related thoughts",
                    'strength': sum(t['similarity'] for t in related_thoughts) / len(related_thoughts),
                    'cluster_size': len(related_thoughts)
                })
                
            # Concept type evidence
            evidence.append({
                'type': 'concept_classification',
                'content': f"Concept type: {concept['type']}",
                'strength': concept.get('confidence', 0.5),
                'concept_type': concept['type']
            })
            
            return evidence
            
        except Exception as e:
            print(colored(f"❌ Evidence gathering error: {str(e)}", "red"))
            return []
        