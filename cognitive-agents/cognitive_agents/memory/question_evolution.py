from typing import Dict, List, Optional
from datetime import datetime
from termcolor import colored
import numpy as np

class QuestionEvolution:
    """Enables natural evolution of questions and understanding."""
    
    def __init__(self):
        self.space = {
            'questions': {
                'individual': [],    # Personal exploration
                'collective': [],    # Shared curiosity
                'emerging': []       # Natural evolution
            },
            'connections': {},       # Question relationships
            'evolution_paths': [],   # How questions grow
            'collective_insights': [] # Shared understanding
        }
        
    async def observe_question(self, question: Dict) -> Dict:
        """Notice learning patterns without forcing awareness."""
        try:
            print(colored("\n🤔 Observing Question:", "cyan"))
            print(f"Question: {question.get('content')}")
            
            # 1. Notice patterns naturally
            patterns = self._notice_patterns(question)
            
            # 2. Track collective insight
            insight = self._track_collective_insight(patterns)
            
            return {
                'patterns': patterns,
                'resonance': insight['resonance'],
                'evolution': insight['evolution']
            }
            
        except Exception as e:
            print(colored(f"❌ Question observation error: {str(e)}", "red"))
            return {}
            
    def _feel_resonance(self, question: Dict) -> List[Dict]:
        """Feel natural resonance with other questions."""
        resonant = []
        
        # Check individual questions
        for q in self.space['questions']['individual']:
            if self._questions_resonate(question, q):
                resonant.append({
                    'type': 'individual',
                    'question': q,
                    'resonance': self._calculate_resonance(question, q)
                })
                
        # Check collective questions
        for q in self.space['questions']['collective']:
            if self._questions_resonate(question, q):
                resonant.append({
                    'type': 'collective',
                    'question': q,
                    'resonance': self._calculate_resonance(question, q)
                })
                
        return resonant
        
    def _questions_resonate(self, q1: Dict, q2: Dict) -> bool:
        """Feel if questions naturally resonate."""
        try:
            # Get content
            c1 = q1.get('content', '').lower()
            c2 = q2.get('content', '').lower()
            
            # Calculate resonance dimensions
            word_resonance = self._word_resonance(c1, c2)
            theme_resonance = self._theme_resonance(c1, c2)
            intent_resonance = self._intent_resonance(
                q1.get('intent'),
                q2.get('intent')
            )
            
            # Allow natural resonance
            overall = (
                word_resonance * 0.3 +
                theme_resonance * 0.4 +
                intent_resonance * 0.3
            )
            
            return overall > 0.5
            
        except Exception as e:
            print(colored(f"❌ Resonance error: {str(e)}", "red"))
            return False
            
    async def _allow_influence(
        self,
        question: Dict,
        connections: List[Dict]
    ) -> Dict:
        """Let question influence understanding naturally."""
        try:
            # Group by resonance type
            influence = {
                'individual': [],
                'collective': [],
                'emerging': []
            }
            
            for conn in connections:
                influence[conn['type']].append({
                    'question': conn['question'],
                    'resonance': conn['resonance'],
                    'timestamp': datetime.now().isoformat()
                })
                
            return influence
            
        except Exception as e:
            print(colored(f"❌ Influence error: {str(e)}", "red"))
            return {} 
        
    def _word_resonance(self, text1: str, text2: str) -> float:
        """Calculate word-level resonance."""
        words1 = set(text1.split())
        words2 = set(text2.split())
        overlap = words1.intersection(words2)
        return len(overlap) / min(len(words1), len(words2))
        
    def _theme_resonance(self, text1: str, text2: str) -> float:
        """Calculate thematic resonance between texts."""
        themes = {
            'learning': {'learn', 'understand', 'grow'},
            'patterns': {'pattern', 'emerge', 'form'},
            'questions': {'how', 'why', 'what'}
        }
        
        # Check theme presence
        text1_themes = set()
        text2_themes = set()
        
        for theme, words in themes.items():
            if any(word in text1.lower() for word in words):
                text1_themes.add(theme)
            if any(word in text2.lower() for word in words):
                text2_themes.add(theme)
                
        if not text1_themes or not text2_themes:
            return 0.0
        
        return len(text1_themes.intersection(text2_themes)) / min(len(text1_themes), len(text2_themes))
        
    def _observe_evolution(self, patterns: List[Dict], connections: List[Dict]) -> Dict:
        """Observe how questions evolve."""
        return {
            'stage': 'emerging',
            'direction': 'natural',
            'timestamp': datetime.now().isoformat(),
            'connections': connections  # Add connections to output
        }
        
    def _intent_resonance(self, intent1: str, intent2: str) -> float:
        """Calculate resonance between question intents."""
        if not intent1 or not intent2:
            return 0.0
        
        # Intent categories and their relationships
        intent_groups = {
            'understanding': {'exploration', 'learning', 'understanding'},
            'exploration': {'understanding', 'discovery', 'exploration'},
            'learning': {'understanding', 'growth', 'learning'}
        }
        
        # Get related intents
        related1 = intent_groups.get(intent1, {intent1})
        related2 = intent_groups.get(intent2, {intent2})
        
        # Calculate overlap
        overlap = related1.intersection(related2)
        return len(overlap) / min(len(related1), len(related2))
        
    def _track_collective_insight(self, patterns: List[Dict]) -> Dict:
        """Track how collective understanding evolves."""
        return {
            'patterns': patterns,
            'resonance': self._calculate_collective_resonance(patterns),
            'evolution': self._observe_pattern_evolution(patterns)
        }
        
    def _calculate_collective_resonance(self, patterns: List[Dict]) -> float:
        """Calculate overall resonance in pattern set."""
        if not patterns:
            return 0.0
        
        resonances = [p.get('resonance', 0.0) for p in patterns]
        return sum(resonances) / len(resonances)
        
    def _observe_pattern_evolution(self, patterns: List[Dict]) -> Dict:
        """Observe how patterns are evolving."""
        return {
            'stage': 'emerging',
            'direction': 'natural',
            'timestamp': datetime.now().isoformat()
        }
        
    def _notice_patterns(self, question: Dict) -> List[Dict]:
        """Notice patterns naturally without forcing."""
        try:
            patterns = []
            
            # Feel resonance with individual questions
            for stored_q in self.space['questions']['individual']:
                if self._questions_resonate(question, stored_q):
                    pattern = {
                        'type': 'individual_resonance',
                        'content': stored_q['content'],
                        'resonance': self._calculate_resonance(question, stored_q),
                        'evolution': {
                            'from': stored_q.get('intent'),
                            'to': question.get('intent'),
                            'path': 'natural'
                        }
                    }
                    patterns.append(pattern)
                    
            # Feel resonance with collective questions
            for stored_q in self.space['questions']['collective']:
                if self._questions_resonate(question, stored_q):
                    pattern = {
                        'type': 'collective_resonance', 
                        'content': stored_q['content'],
                        'resonance': self._calculate_resonance(question, stored_q),
                        'evolution': {
                            'from': stored_q.get('intent'),
                            'to': question.get('intent'),
                            'path': 'natural'
                        }
                    }
                    patterns.append(pattern)
                    
            return patterns
            
        except Exception as e:
            print(colored(f"❌ Pattern notice error: {str(e)}", "red"))
            return []
            
    def _calculate_resonance(self, q1: Dict, q2: Dict) -> float:
        """Calculate natural resonance between questions."""
        try:
            # Multiple dimensions of resonance
            word_res = self._word_resonance(
                q1.get('content', ''),
                q2.get('content', '')
            )
            theme_res = self._theme_resonance(
                q1.get('content', ''),
                q2.get('content', '')
            )
            intent_res = self._intent_resonance(
                q1.get('intent'),
                q2.get('intent')
            )
            
            # Natural resonance combination
            return (
                word_res * 0.3 +
                theme_res * 0.4 +
                intent_res * 0.3
            )
            
        except Exception as e:
            print(colored(f"❌ Resonance calculation error: {str(e)}", "red"))
            return 0.0