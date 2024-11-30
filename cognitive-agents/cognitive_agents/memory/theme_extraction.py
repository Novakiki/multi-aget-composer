from typing import List, Dict
from termcolor import colored

class ThemeExtraction:
    """Natural extraction of themes from patterns."""
    
    def __init__(self, store, network):
        self.store = store
        self.network = network
        self.core_themes = {
            'patterns': ['pattern', 'form', 'structure', 'emerge'],
            'nature': ['nature', 'natural', 'organic', 'environment'],
            'evolution': ['evolution', 'develop', 'grow', 'change'],
            'learning': ['learn', 'understand', 'comprehend', 'grasp']
        }
        
    async def extract_themes(self, content: str) -> List[str]:
        """Extract themes using core concepts."""
        content = content.lower()
        themes = set()
        
        # Match core themes
        for theme, keywords in self.core_themes.items():
            if any(word in content for word in keywords):
                themes.add(theme)
                
        print(colored(f"Found Themes: {', '.join(themes)}", "cyan"))
        return list(themes) 