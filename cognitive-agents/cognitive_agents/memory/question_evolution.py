from typing import Dict, List
from termcolor import colored

class QuestionEvolution:
    """Natural evolution of questions and insights."""
    
    def __init__(self, store, network, semantics, theme_extractor):
        self.store = store        # Pattern storage
        self.network = network    # Knowledge connections
        self.semantics = semantics # Understanding
        self.theme_extractor = theme_extractor
        
    async def evolve_question(self, question: str) -> Dict:
        """Let a question evolve naturally."""
        try:
            # Extract themes
            themes = await self.theme_extractor.extract_themes(question)
            
            # Store pattern with embedding
            pattern = {
                'content': question,
                'themes': themes
            }
            pattern_id = await self.store.store_pattern(pattern)
            
            # Find similar patterns with semantic search
            similar = await self.semantics.find_similar(pattern_id)
            
            # Create meaningful connections
            connections = []
            for match in similar:
                try:
                    connections.append({
                        'content': match['metadata']['content'],
                        'similarity': match['score'],
                        'themes': match['metadata'].get('themes', [])
                    })
                except KeyError as e:
                    print(colored(f"Warning: Malformed pattern data - {e}", "yellow"))
                    continue
            
            return {
                'pattern_id': pattern_id,
                'themes': themes,
                'connections': connections
            }
        except Exception as e:
            print(f"Error evolving question: {e}")
            return None
        
    async def _generate_insights(self, question: str, similar: List[Dict]) -> List[Dict]:
        """Generate insights from similar patterns."""
        insights = []
        
        for pattern in similar:
            insights.append({
                'type': 'connection',
                'content': pattern['metadata']['content'],
                'themes': pattern['metadata']['themes'],
                'score': pattern['score']
            })
        
        return insights