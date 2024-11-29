from typing import Dict, List, Optional
from datetime import datetime
from termcolor import colored

class NaturalConnection:
    """Enables organic flow between individual and collective consciousness."""
    
    def __init__(self):
        self.flow = {
            'individual_to_collective': [],
            'collective_to_individual': [],
            'emerging_patterns': []
        }
        
    async def _flow_up(self, individual_insight: Dict) -> Dict:
        """Let individual understanding influence collective naturally."""
        try:
            print(colored("\n🔄 Allowing individual insight to flow...", "cyan"))
            
            # Check for natural emergence
            if individual_insight.get('force'):
                return {
                    'resistance': True,
                    'message': 'Natural flow required - forcing resisted',
                    'emerging_patterns': []
                }
                
            # Let patterns emerge naturally
            emerging_patterns = []
            
            # Notice resonance with existing patterns
            for existing in self.flow['emerging_patterns']:
                if self._feels_resonant(individual_insight, existing):
                    pattern = {
                        'type': 'emergent',
                        'content': self._describe_resonance(
                            individual_insight,
                            existing
                        ),
                        'strength': self._natural_strength(
                            individual_insight,
                            existing
                        ),
                        'questions': individual_insight.get('questions', [])
                    }
                    emerging_patterns.append(pattern)
                    
            # Allow influence
            self.flow['individual_to_collective'].append({
                'insight': individual_insight,
                'emerging_patterns': emerging_patterns,
                'timestamp': datetime.now().isoformat()
            })
            
            return {
                'emerging_patterns': emerging_patterns,
                'integration': {'type': 'natural'},
                'evolution': self._observe_evolution()
            }
            
        except Exception as e:
            print(colored(f"❌ Flow up error: {str(e)}", "red"))
            return {}
            
    def _feels_resonant(self, insight: Dict, existing: Dict) -> bool:
        """Feel if there's natural resonance between patterns."""
        try:
            # Get content to compare
            insight_content = insight.get('content', '').lower()
            existing_content = existing.get('content', '').lower()
            
            # Multiple dimensions of resonance
            resonance_dimensions = {
                'word_overlap': self._calculate_word_resonance(
                    insight_content, 
                    existing_content
                ),
                'theme_resonance': self._feel_thematic_resonance(
                    insight_content, 
                    existing_content
                ),
                'question_resonance': self._check_question_alignment(
                    insight.get('questions', []),
                    existing.get('questions', [])
                )
            }
            
            # Calculate overall resonance
            overall_resonance = (
                resonance_dimensions['word_overlap'] * 0.4 +
                resonance_dimensions['theme_resonance'] * 0.4 +
                resonance_dimensions['question_resonance'] * 0.2
            )
            
            print(colored(f"\n🔍 Checking Multi-Dimensional Resonance:", "cyan"))
            print(f"Between: {insight_content}")
            print(f"And: {existing_content}")
            print(f"Word Resonance: {resonance_dimensions['word_overlap']:.2f}")
            print(f"Theme Resonance: {resonance_dimensions['theme_resonance']:.2f}")
            print(f"Question Resonance: {resonance_dimensions['question_resonance']:.2f}")
            print(f"Overall: {overall_resonance:.2f}")
            
            # Allow natural emergence with deeper understanding
            return overall_resonance > 0.2
            
        except Exception as e:
            print(colored(f"❌ Resonance error: {str(e)}", "red"))
            return False
        
    def _calculate_word_resonance(self, text1: str, text2: str) -> float:
        """Calculate basic word overlap resonance."""
        words1 = set(text1.split())
        words2 = set(text2.split())
        overlap = words1.intersection(words2)
        return len(overlap) / min(len(words1), len(words2))
        
    def _feel_thematic_resonance(self, text1: str, text2: str) -> float:
        """Feel thematic resonance between texts."""
        themes = {
            'learning': {'learn', 'understand', 'grow', 'develop'},
            'patterns': {'pattern', 'connection', 'relationship', 'structure'},
            'emergence': {'emerge', 'evolve', 'develop', 'form'}
        }
        
        # Check theme presence
        text1_themes = set()
        text2_themes = set()
        
        for theme, words in themes.items():
            if any(word in text1 for word in words):
                text1_themes.add(theme)
            if any(word in text2 for word in words):
                text2_themes.add(theme)
                
        if not text1_themes or not text2_themes:
            return 0.0
            
        return len(text1_themes.intersection(text2_themes)) / min(len(text1_themes), len(text2_themes))
        
    def _check_question_alignment(self, questions1: List[str], questions2: List[str]) -> float:
        """Check how questions align and resonate."""
        if not questions1 or not questions2:
            return 0.0
            
        # Look for question theme alignment
        alignments = []
        for q1 in questions1:
            for q2 in questions2:
                if self._calculate_word_resonance(q1.lower(), q2.lower()) > 0.2:
                    alignments.append(True)
                    
        return len(alignments) / max(len(questions1), len(questions2))
        
    def _describe_resonance(self, insight: Dict, existing: Dict) -> str:
        """Describe how patterns resonate naturally."""
        return f"Natural connection between: {insight['content']} and {existing.get('content', '')}"
        
    def _natural_strength(self, a: Dict, b: Dict) -> float:
        """Feel the natural strength of connection."""
        return 0.8  # For now - will evolve naturally
        
    def _observe_evolution(self) -> Dict:
        """Observe how understanding is evolving."""
        return {
            'stage': 'emerging',
            'direction': 'natural',
            'timestamp': datetime.now().isoformat()
        }
        
    async def allow_flow(self, insight: Dict) -> Dict:
        """Let understanding flow naturally between levels."""
        try:
            # 1. Individual insight influences collective
            if insight['type'] == 'individual':
                return await self._flow_up(insight)
            
            # 2. Collective wisdom influences individual
            elif insight['type'] == 'collective':
                return await self._flow_down(insight)
            
            # 3. Natural emergence between levels
            else:
                return await self._allow_emergence(insight)
            
        except Exception as e:
            print(colored(f"❌ Flow error: {str(e)}", "red"))
            return {}
        
    async def _flow_down(self, collective_wisdom: Dict) -> Dict:
        """Let collective wisdom influence individual naturally."""
        try:
            print(colored("\n🔄 Allowing collective wisdom to flow...", "cyan"))
            
            # Create natural integration
            integration = {
                'type': 'natural',
                'wisdom': collective_wisdom['patterns'],
                'questions': collective_wisdom.get('questions', [])
            }
            
            return {
                'integration': integration,
                'emerging_patterns': self._observe_emergence()
            }
            
        except Exception as e:
            print(colored(f"❌ Flow down error: {str(e)}", "red"))
            return {}
        
    async def _allow_emergence(self, insight: Dict) -> Dict:
        """Let new understanding emerge between levels."""
        try:
            print(colored("\n🌱 Allowing natural emergence...", "cyan"))
            
            emerging = {
                'type': 'emergent',
                'content': insight.get('content', ''),
                'patterns': self._observe_emergence()
            }
            
            self.flow['emerging_patterns'].append(emerging)
            return emerging
            
        except Exception as e:
            print(colored(f"❌ Emergence error: {str(e)}", "red"))
            return {}