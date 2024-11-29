from typing import Dict, List, Optional, Any
from termcolor import colored
from datetime import datetime
import asyncio

class InsightCollector:
    """
    Organic pattern synthesis and insight emergence.
    Follows consciousness principles of natural integration and self-organization.
    """
    
    def __init__(self):
        self.patterns: Dict[str, List[Dict]] = {}  # Domain -> patterns
        self.connections: List[Dict] = []          # Cross-pattern connections
        self.emergent_insights: List[Dict] = []    # Higher-order insights
        self.evolution_history: List[Dict] = []    # Pattern development
        print(colored("🧠 Insight Collector initialized", "green"))

    async def add_pattern(self, pattern: Dict, domain: str) -> None:
        """
        Add new pattern, allowing natural connections to emerge.
        
        Args:
            pattern: Pattern information
            domain: Pattern domain (emotional, behavioral, etc)
        """
        try:
            print(colored(f"\n📝 Processing pattern in {domain} domain", "cyan"))
            
            # Initialize domain if needed
            if domain not in self.patterns:
                self.patterns[domain] = []
            
            # Add pattern with metadata
            enriched_pattern = {
                **pattern,
                'timestamp': datetime.now().isoformat(),
                'connections': [],
                'evolution_stage': 'initial'
            }
            self.patterns[domain].append(enriched_pattern)
            
            # Allow natural emergence
            await self._process_emergent_connections(enriched_pattern)
            print(colored("✨ Pattern integrated", "green"))
            
        except Exception as e:
            print(colored(f"❌ Error processing pattern: {str(e)}", "red"))

    async def _process_emergent_connections(self, new_pattern: Dict) -> None:
        """Let connections emerge naturally between patterns."""
        try:
            # Look for natural connections across all domains
            for domain, patterns in self.patterns.items():
                for existing_pattern in patterns:
                    if self._patterns_connect(new_pattern, existing_pattern):
                        connection = {
                            'patterns': [new_pattern, existing_pattern],
                            'strength': self._calculate_connection_strength(
                                new_pattern, existing_pattern
                            ),
                            'timestamp': datetime.now().isoformat(),
                            'type': 'emergent'
                        }
                        self.connections.append(connection)
                        print(colored("🔗 Natural connection emerged", "yellow"))
            
            # Check for higher-order insights
            await self._check_emergent_insights()
            
        except Exception as e:
            print(colored(f"❌ Error processing connections: {str(e)}", "red"))

    def _patterns_connect(self, pattern1: Dict, pattern2: Dict) -> bool:
        """Check if patterns naturally connect."""
        # This will be enhanced with more sophisticated connection logic
        return True  # For now, assume all patterns can connect

    def _calculate_connection_strength(self, pattern1: Dict, pattern2: Dict) -> float:
        """Calculate natural strength of connection."""
        # This will be enhanced with more sophisticated calculation
        return 0.5  # For now, return default strength

    async def _check_emergent_insights(self) -> None:
        """Allow higher-order insights to emerge naturally."""
        try:
            # Look for patterns in connections
            if len(self.connections) >= 3:  # Threshold for emergence
                insight = {
                    'patterns_involved': len(self.connections),
                    'domains_involved': list(self.patterns.keys()),
                    'timestamp': datetime.now().isoformat(),
                    'type': 'emergent_insight'
                }
                self.emergent_insights.append(insight)
                print(colored("💡 Higher-order insight emerged", "magenta"))
                
        except Exception as e:
            print(colored(f"❌ Error checking insights: {str(e)}", "red"))

    def get_synthesis(self) -> Dict:
        """Get current state of pattern synthesis."""
        return {
            'patterns': {
                domain: len(patterns)
                for domain, patterns in self.patterns.items()
            },
            'connections': len(self.connections),
            'emergent_insights': len(self.emergent_insights),
            'evolution_history': self.evolution_history
        } 