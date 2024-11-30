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
        print(colored(f"\n🤔 Evolving Question: {question}", "cyan"))
        
        # 1. Extract themes
        themes = await self.theme_extractor.extract_themes(question)
        
        # 2. Store as pattern with themes
        pattern = {
            'type': 'question',
            'content': question,
            'themes': themes
        }
        pattern_id = await self.store.store_pattern(pattern)
        
        # 3. Find semantic connections
        similar = await self.semantics.find_similar(pattern_id)
        
        # 4. Generate insights
        insights = await self._generate_insights(question, similar)
        
        return {
            'pattern_id': pattern_id,
            'themes': themes,
            'insights': insights,
            'connections': similar
        }
        
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