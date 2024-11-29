from typing import Dict, List, Optional
from datetime import datetime
from termcolor import colored
import numpy as np
from sentence_transformers import SentenceTransformer

class IntentionCategory:
    """Defines an intention category with its characteristics."""
    def __init__(self, name: str, description: str, keywords: List[str]):
        self.name = name
        self.description = description
        self.keywords = keywords
        self.memory = {
            'embeddings': [],    # Vector embeddings
            'thoughts': [],      # Original thoughts
            'metadata': [],      # Additional context
            'timestamps': [],    # When stored
            'connections': []    # Related thoughts
        }

class IntentionalMemory:
    """Core memory system with intentional storage and retrieval."""
    
    def __init__(self):
        # Initialize embedding model
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Define core intention categories
        self.categories = {
            'learning': IntentionCategory(
                name='learning',
                description='Knowledge acquisition and skill development',
                keywords=['learn', 'understand', 'study', 'practice']
            ),
            'growth': IntentionCategory(
                name='growth',
                description='Personal development and insights',
                keywords=['improve', 'develop', 'grow', 'change']
            ),
            'insight': IntentionCategory(
                name='insight',
                description='Pattern recognition and deep understanding',
                keywords=['realize', 'connect', 'pattern', 'understand']
            )
        }
        
        print(colored("🧠 Intentional Memory System Initialized", "green"))
        
    async def store_thought(
        self,
        thought: str,
        intent: Optional[str] = None
    ) -> Dict:
        """Store thought with intent classification."""
        try:
            # 1. Classify intent if not provided
            if not intent:
                intent = self._classify_intent(thought)
                
            # 2. Get category
            category = self.categories.get(intent)
            if not category:
                raise ValueError(f"Unknown intent category: {intent}")
                
            # 3. Create embedding
            embedding = self.encoder.encode(thought)
            
            # 4. Store with metadata
            timestamp = datetime.now().isoformat()
            metadata = {
                'timestamp': timestamp,
                'intent': intent,
                'embedding_version': '1.0'
            }
            
            # 5. Add to category memory
            category.memory['embeddings'].append(embedding)
            category.memory['thoughts'].append(thought)
            category.memory['metadata'].append(metadata)
            category.memory['timestamps'].append(timestamp)
            
            print(colored(f"💭 Thought stored with {intent} intent", "cyan"))
            return metadata
            
        except Exception as e:
            print(colored(f"❌ Error storing thought: {str(e)}", "red"))
            return {} 

    def _classify_intent(self, thought: str) -> str:
        """Classify the intention behind a thought."""
        try:
            # Convert to lower case for matching
            thought_lower = thought.lower()
            
            # Check each category's keywords
            scores = {}
            for name, category in self.categories.items():
                score = sum(
                    1 for keyword in category.keywords 
                    if keyword in thought_lower
                )
                scores[name] = score
                
            # Get highest scoring category
            if any(scores.values()):
                return max(scores.items(), key=lambda x: x[1])[0]
                
            # Default to 'insight' if no clear match
            return 'insight'
            
        except Exception as e:
            print(colored(f"❌ Error classifying intent: {str(e)}", "red"))
            return 'insight'  # Safe default

    async def integrate_understanding(self, thought: str):
        """Allow natural integration of individual and collective."""
        # Let understanding emerge
        individual_insight = await self.emergent_space.observe(thought)
        
        # Share with collective
        collective_response = await self.collective_wisdom.receive(individual_insight)
        
        # Allow natural evolution
        return await self.emergent_space.evolve(
            individual=individual_insight,
            collective=collective_response
        )