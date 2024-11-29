from typing import Dict, List
from datetime import datetime
from termcolor import colored
from cognitive_agents.community.pattern_democracy import PatternDemocracy

class CommunityWisdom:
    """Enables collective wisdom emergence."""
    
    def __init__(self, democracy: PatternDemocracy):
        self.democracy = democracy
        self.emerging_patterns = {}
        
    async def observe_patterns(self, patterns: List[Dict]) -> Dict:
        """Notice emerging community patterns."""
        try:
            for pattern in patterns:
                # Submit for validation
                proposal = await self.democracy.propose_pattern(pattern)
                
                # Track emergence
                theme = pattern.get('theme', 'general')
                if theme not in self.emerging_patterns:
                    self.emerging_patterns[theme] = []
                self.emerging_patterns[theme].append({
                    'pattern': pattern,
                    'proposal_id': proposal['id'],
                    'timestamp': datetime.now().isoformat()
                })
            
            return {
                'proposals': len(patterns),
                'themes': list(self.emerging_patterns.keys()),
                'emergence_strength': self._calculate_emergence()
            }
            
        except Exception as e:
            print(colored(f"❌ Pattern observation error: {str(e)}", "red"))
            return {} 

    def _calculate_emergence(self) -> float:
        """Calculate the strength of emerging patterns."""
        try:
            if not self.emerging_patterns:
                return 0.0
                
            # Calculate per-theme strength
            theme_strengths = []
            for theme, patterns in self.emerging_patterns.items():
                # Pattern count factor
                count_factor = min(1.0, len(patterns) / 5.0)
                
                # Pattern strength average
                strengths = [p['pattern'].get('strength', 0) for p in patterns]
                avg_strength = sum(strengths) / len(strengths) if strengths else 0
                
                # Theme strength
                theme_strength = count_factor * avg_strength
                theme_strengths.append(theme_strength)
                
            # Overall emergence strength
            emergence = sum(theme_strengths) / len(theme_strengths)
            return min(1.0, emergence)
            
        except Exception as e:
            print(colored(f"❌ Emergence calculation error: {str(e)}", "red"))
            return 0.0 