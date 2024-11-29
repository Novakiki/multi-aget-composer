from typing import Dict, List, Optional
from datetime import datetime
from termcolor import colored

class MetaLearning:
    """Enables natural meta-cognitive development."""
    
    def __init__(self):
        self.patterns = {
            'cognitive': [],    # Thinking patterns
            'question': [],     # Question evolution
            'understanding': [] # Learning process
        }
        
    async def observe_learning(self, interaction: Dict) -> Dict:
        """Notice learning patterns without forcing awareness."""
        try:
            # 1. Notice patterns naturally
            patterns = self._notice_patterns(interaction)
            
            # 2. Enable reflection opportunities
            reflection = self._create_reflection_space(patterns)
            
            # 3. Allow natural insights
            insights = await self._allow_insights(reflection)
            
            return {
                'patterns': patterns,
                'reflection': reflection,
                'insights': insights,
                'meta_awareness': self._check_meta_awareness(insights)
            }
            
        except Exception as e:
            print(colored(f"❌ Learning observation error: {str(e)}", "red"))
            return {} 
        
    def _notice_patterns(self, interaction: Dict) -> List[Dict]:
        """Notice cognitive patterns naturally."""
        try:
            patterns = []
            
            # Notice question patterns
            if 'questions' in interaction:
                for q in interaction['questions']:
                    pattern = {
                        'type': 'question_pattern',
                        'content': q,
                        'strength': self._calculate_pattern_strength(q)
                    }
                    patterns.append(pattern)
                    
            # Notice understanding patterns
            if 'understanding' in interaction:
                pattern = {
                    'type': 'understanding_pattern',
                    'content': interaction['understanding'],
                    'strength': self._calculate_pattern_strength(
                        interaction['understanding']
                    )
                }
                patterns.append(pattern)
                
            return patterns
            
        except Exception as e:
            print(colored(f"❌ Pattern notice error: {str(e)}", "red"))
            return []
            
    def _create_reflection_space(self, patterns: List[Dict]) -> Dict:
        """Create natural space for reflection."""
        return {
            'patterns': patterns,
            'questions': self._generate_reflection_questions(patterns),
            'connections': self._find_pattern_connections(patterns)
        }
        
    async def _allow_insights(self, reflection: Dict) -> Dict:
        """Let insights emerge naturally."""
        try:
            # Calculate pattern strengths
            pattern_strengths = [p.get('strength', 0) for p in reflection['patterns']]
            avg_strength = sum(pattern_strengths) / len(pattern_strengths) if pattern_strengths else 0

            # Calculate connection strength
            connection_strength = len(reflection['connections']) / (len(reflection['patterns']) * 0.5) if reflection['patterns'] else 0
            connection_strength = min(1.0, connection_strength)

            # Calculate evolution quality based on reflection questions and connections
            evolution_quality = (
                len(reflection['questions']) / len(reflection['patterns']) if reflection['patterns'] else 0
            ) * avg_strength

            return {
                'meta_patterns': reflection['patterns'],
                'depth': len(reflection['patterns']) / 3.0,  # Natural scaling
                'evolution': 'emerging',
                'evolution_quality': min(1.0, evolution_quality),
                'connection_strength': connection_strength,
                'patterns': reflection['patterns']  # Include patterns for depth calculation
            }
            
        except Exception as e:
            print(colored(f"❌ Insight generation error: {str(e)}", "red"))
            return {
                'meta_patterns': [],
                'depth': 0,
                'evolution': 'emerging',
                'evolution_quality': 0,
                'connection_strength': 0,
                'patterns': []
            }
        
    def _check_meta_awareness(self, insights: Dict) -> float:
        """Calculate meta-awareness naturally."""
        try:
            if not insights:
                return 0.0
            
            # Multiple dimensions with clear logging
            pattern_depth = len(insights.get('patterns', [])) / 5.0  # Normalize
            evolution_quality = insights.get('evolution_quality', 0.0)
            connection_strength = insights.get('connection_strength', 0.0)
            
            # Log components
            print(colored("\n📊 Meta-Awareness Components:", "cyan"))
            print(f"  • Pattern Depth: {pattern_depth:.2f}")
            print(f"  • Evolution Quality: {evolution_quality:.2f}")
            print(f"  • Connection Strength: {connection_strength:.2f}")
            
            # Weighted combination
            awareness = (
                pattern_depth * 0.4 +
                evolution_quality * 0.3 + 
                connection_strength * 0.3
            )
            
            print(f"  • Final Meta-Awareness: {awareness:.2f}")
            
            return min(1.0, awareness)
            
        except Exception as e:
            print(colored(f"❌ Meta-awareness calculation error: {str(e)}", "red"))
            return 0.0
        
    def _calculate_pattern_strength(self, content: str) -> float:
        """Calculate natural pattern strength."""
        try:
            # Basic strength calculation
            words = content.split()
            base_strength = min(1.0, len(words) / 10.0)
            
            # Adjust for question depth
            if '?' in content:
                base_strength *= 1.2
                
            # Adjust for understanding markers
            understanding_words = {'because', 'therefore', 'thus', 'hence'}
            if any(word in content.lower() for word in understanding_words):
                base_strength *= 1.3
                
            return min(1.0, base_strength)
            
        except Exception as e:
            print(colored(f"❌ Strength calculation error: {str(e)}", "red"))
            return 0.0
        
    def _generate_reflection_questions(self, patterns: List[Dict]) -> List[str]:
        """Generate natural reflection questions."""
        questions = []
        
        for p in patterns:
            if p['type'] == 'question_pattern':
                questions.append(f"How does this question evolve: {p['content']}?")
            elif p['type'] == 'understanding_pattern':
                questions.append(f"What patterns emerge from: {p['content']}?")
                
        return questions
        
    def _find_pattern_connections(self, patterns: List[Dict]) -> List[Dict]:
        """Find natural connections between patterns."""
        connections = []
        
        for i, p1 in enumerate(patterns):
            for p2 in patterns[i+1:]:
                if self._patterns_connect(p1, p2):
                    connections.append({
                        'type': 'natural_connection',
                        'from': p1['content'],
                        'to': p2['content']
                    })
                    
        return connections
        
    def _patterns_connect(self, p1: Dict, p2: Dict) -> bool:
        """Check if patterns naturally connect."""
        words1 = set(p1['content'].lower().split())
        words2 = set(p2['content'].lower().split())
        return len(words1.intersection(words2)) > 0