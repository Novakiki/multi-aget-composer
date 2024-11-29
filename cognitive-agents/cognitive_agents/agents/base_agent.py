from typing import List, Dict

class BaseAgent:
    def _create_result_structure(self, patterns: List[Dict], analysis: bool = True) -> Dict:
        """Create standardized result structure."""
        return {
            'patterns': patterns,
            'meta_synthesis': {
                'integration_quality': self._calculate_integration_quality(patterns),
                'analysis_complete': analysis
            },
            'evolution': {
                'stage': self._determine_evolution_stage(),
                'confidence': self._calculate_confidence()
            }
        } 