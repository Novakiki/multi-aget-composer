from typing import List, Dict
from termcolor import colored

class ThemeExtraction:
    """Natural extraction of themes from patterns."""
    
    def __init__(self, store, network):
        self.store = store
        self.network = network
        
    async def extract_themes(self, content: str) -> List[str]:
        """Extract themes naturally from content."""
        print(colored(f"\n🎯 Extracting Themes:", "cyan"))
        
        # Start with basic themes
        base_themes = ['learning', 'evolution']
        
        # Find related patterns
        patterns = await self.store.find_patterns_by_content(content)
        
        # Extract themes from related patterns
        for pattern in patterns:
            if 'themes' in pattern:
                base_themes.extend(pattern['themes'])
                
        # Remove duplicates while preserving order
        unique_themes = list(dict.fromkeys(base_themes))
        
        print(f"Found Themes: {', '.join(unique_themes)}")
        return unique_themes 